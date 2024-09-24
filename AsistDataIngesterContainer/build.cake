#l "base.cake"

#tool "nuget:?package=GitVersion.CommandLine&version=4.0.0"

#addin "Cake.WebDeploy&version=0.3.3"

var target = Argument<string>("target", "Default");
var configuration = Argument<string>("configuration", "Release");
var runtime = Argument<string>("runtime", "win7-x64");
 
double unixTimestamp = 0;

public static class Directories
{
	public const string Bin = "./bin";
	public const string Dist = "./dist";
	public const string Local = "./packages.local";
	public const string Source = "./src";
}

FilePath        msdeploy    = "C:\\Program Files (x86)\\IIS\\Microsoft Web Deploy V3\\msdeploy.exe";

Action<FilePath, ProcessArgumentBuilder> Cmd => (path, args) => {
    var result = StartProcess(
        path,
        new ProcessSettings {
            Arguments = args
        });

    if(0 != result)
    {
        throw new Exception($"Failed to execute tool {path.GetFilename()} ({result})");
    }
};

// =============================================================================
// Helper Functions
// =============================================================================

// Visual Studio 15 is for 2017 (i.e. .NET Core)
public static bool IsSolutionPreVs15(ICakeContext context, string solution) {
	foreach(var line in System.IO.File.ReadLines(solution)) {
		// VisualStudioVersion = 14.0.25420.1
		if (line.StartsWith("VisualStudioVersion")) {
			var tokens = line.Split(new[] { '=', '.' }, StringSplitOptions.RemoveEmptyEntries);
			var i = int.Parse(tokens[1]);
			return (i < 15);
		}
	}

	throw new Exception(String.Format("VisualStudioVersion is missing for {0}.", solution));
}

// Visual Studio 15 is for 2017 (i.e. .NET Core)
public static bool IsCsprojPreVs15(ICakeContext context, string prj) {
	try {
		var el = System.Xml.Linq.XDocument.Load(prj).Root.Attribute("ToolsVersion");
		var i = double.Parse(el.Value);
		return (i < 15);
	} catch (Exception) {
		// Null exception expected
	}

	return false;
}

Setup(context =>
{
    // Executed BEFORE the first task.
    Information("Running tasks...");
	if(isRunningOnTeamCity)
		Information("Running on Teamcity");
	else
		Information("Running Locally");
	
	unixTimestamp = Math.Floor((DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds);
	Information("Unix Time : {0}", unixTimestamp);
});

Teardown(context =>
{
    // Executed AFTER the last task.
    Information("Finished running tasks.");
});

Task("Clean")
    .Does(() =>
{
    if(DirectoryExists(Directories.Dist))
		CleanDirectories(Directories.Dist);
    if(DirectoryExists(Directories.Local))
		CleanDirectories(Directories.Local);
	if(!DirectoryExists(Directories.Local))
		CreateDirectory(Directories.Local);
})
.OnError(exception => {
		Error("{0}", exception);
		if(isRunningOnTeamCity){
			TeamCity.BuildProblem(exception.ToString(), "Build");
		}
	});

Task("Build")
	.IsDependentOn("Update-And-Get-Version")
	.IsDependentOn("Nuget-Restore-All")
    .IsDependentOn("Clean")
    .Does(() =>
	{
		MSBuild("./src/AsistDataIngester.sln", (settings) => {
				settings.SetConfiguration(configuration);
				settings.EnvironmentVariables = new Dictionary<string, string>{
					{ "BUILD_BUILDNUMBER", gitVersionResult.FullSemVer }
				};
			});		
	})
	.OnError(exception => reportError(exception, "Build"));

Task("NetCoreBuild")
    .IsDependentOn("Clean")
	.IsDependentOn("Update-And-Get-Version")
    .Does(() =>
{
	// Build solutions in dependency order so local package dependencies are build
	var solutionFiles = GetFiles(Directories.Source + "/**/*.csproj");
	foreach(var solution in solutionFiles) {
		if (IsCsprojPreVs15(Context, solution.FullPath)) {
			continue;
		}

		// Get the extension from the "src" directory
		var ext = MakeAbsolute(new DirectoryPath(Directories.Source)).GetRelativePath(solution.GetDirectory());

		// Get the extension from the root project directory
		string root = null;
		var subPath = new DirectoryPath(Directories.Bin);

		foreach(var segment in ext.Segments) {
			if (root != null) {
				subPath = subPath.Combine(segment);
			} else {
				root = ext.Segments[0];
			}
		}

		var settings = new DotNetCorePublishSettings
		{
			Configuration = configuration,
			Runtime = runtime,
			OutputDirectory = new DirectoryPath(Directories.Dist).Combine(root).Combine(subPath),
			EnvironmentVariables = new Dictionary<string, string>{
				{ "BUILD_BUILDNUMBER", gitVersionResult.FullSemVer }
			}
		};

		Information("Publishing {0} to {1}", solution, settings.OutputDirectory);
		DotNetCorePublish(solution.FullPath, settings);
	}
})
.OnError(exception => {
		Error("{0}", exception);
		if(isRunningOnTeamCity){
			TeamCity.BuildProblem(exception.ToString(), "Build");
		}
	});

Task("WebDeployPackage")
	.IsDependentOn("Update-And-Get-Version")
	.IsDependentOn("Nuget-Restore-All")
    .IsDependentOn("Clean")
    .Does(() =>
	{
		MSBuild("./src/AsistDataIngester.sln", (settings) => {
			settings.SetConfiguration(configuration);
			settings.WithProperty("DeployOnBuild", "true");
  			settings.WithProperty("PublishProfile", "AsistDataIngester");
			settings.EnvironmentVariables = new Dictionary<string, string>{
				{ "BUILD_BUILDNUMBER", gitVersionResult.FullSemVer }
			};
		});
		
		DeleteFiles(Directories.Dist + "/WebDeploy/*.xml");
		DeleteFiles(Directories.Dist + "/WebDeploy/*.cmd");
		DeleteFiles(Directories.Dist + "/WebDeploy/*.txt");

		if(isRunningOnTeamCity){
        	TeamCity.PublishArtifacts("./dist/WebDeploy");
    	}		
	})
	.OnError(exception => reportError(exception, "WebDeployPackage"));

Task("DevWebDeploy")
	.IsDependentOn("WebDeployPackage")
    .Does(() =>
	{
		var SERVERPW = EnvironmentVariable("SERVERPW");

		// Cmd(msdeploy,
		// 	new ProcessArgumentBuilder()
		// 		.Append("-source:recycleApp")
		// 		.Append("-dest:recycleApp=\"Default Web SIte/Test101st/101STService\",ComputerName=\"spotlite.aptima.com\",UserName=\"adziki\",Password=\"" + SERVERPW + "\"")
		// 		.Append("-verb:sync")
		// );

		// Cmd(msdeploy,
		// 	new ProcessArgumentBuilder()
		// 		.Append("-source:package=\"" + System.IO.Path.Combine(System.IO.Directory.GetCurrentDirectory(), "dist\\WebDeploy") + "\\101STService.zip\"")
		// 		.Append("-dest:auto,ComputerName=\"spotlite.aptima.com\",UserName=\"adziki\",Password=\"" + SERVERPW + "\"")
		// 		.Append("-setParam:name=\"IIS Web Application Name\",value=\"Default Web SIte/Test101st/101STService\"")
		// 		.Append("-verb:sync")
		// 		.Append("-enableRule:DoNotDeleteRule")
		// );

	})
	.OnError(exception => {
		Error("{0}", exception);
		if(isRunningOnTeamCity){
			TeamCity.BuildProblem(exception.ToString(), "DevWebDepoy");
		}
	});	

// =============================================================================
// NuGet
// =============================================================================

Task("Nuget-Package")
	.IsDependentOn("NetCoreBuild")
	.Does(()=>{
		if (!DirectoryExists(Directories.Local)) {
			CreateDirectory(Directories.Local);
		}

		var nuspecFiles = GetFiles(Directories.Source + "/*.nuspec");
		foreach(var nuspec in nuspecFiles) {
			Information("Packaging {0}", nuspec);

			NuGetPack(nuspec, new NuGetPackSettings{
				Version = nugetVersion,
				OutputDirectory = Directories.Local
			});
		}

		if(isRunningOnTeamCity){
			TeamCity.PublishArtifacts(Directories.Local);
		}
	})
	.OnError(exception => {
		Error("{0}", exception);
		if(isRunningOnTeamCity){
			TeamCity.BuildProblem(exception.ToString(), "Build");
		}
	});

Task("Nuget-Publish")
	.IsDependentOn("Nuget-Package")
	.Does(() =>{
		if (DirectoryExists(Directories.Local)) {
			// var APIKey = EnvironmentVariable("GITLABAPIKEY");
			// var packages = GetFiles(Directories.Local + "/*.nupkg");
			// NuGetPush(packages, new NuGetPushSettings {
			// 	Source = "https://artifact.production.aptima.com/repository/pe-nuget/",
			// 	ApiKey = APIKey
			// });
		}
	});

Task("PackageAndDeploy")
	.IsDependentOn("DevWebDeploy")
	.IsDependentOn("Nuget-Publish")
	.Does(() =>{		
	});

Task("Default")
    .IsDependentOn("Build");

RunTarget(target);
