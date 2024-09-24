

var nugetVersion = Argument<string>("nuget-version", null);
var semVer = Argument<string>("sem-version", null);
var assemblyVer = Argument<string>("assembly-version", null);
var branchName = Argument<string>("branchName", null);
var entryPoint = Argument<string>("entry-point", null);
GitVersion gitVersionResult = null;

var isRunningOnTeamCity = TeamCity.IsRunningOnTeamCity;

Action<Exception, string> reportError = (exception, taskName) => {
	Error("{0}", exception);
	if(isRunningOnTeamCity){
		TeamCity.BuildProblem(exception.ToString(), taskName);
	}
};

Action<string> mergeDll = (mainDll) => 
	{
		if(!FileExists(@"tools\LibZ.Tool\tools\libz.exe"))
			return;
			
		var path = System.IO.Path.GetDirectoryName(mainDll);
		var fileName = System.IO.Path.GetFileName(mainDll);
		StartProcess(@".\tools\LibZ.Tool\tools\libz.exe", new ProcessSettings
			{ 
				Arguments = "inject-dll --assembly "+fileName+" --include *.dll --exclude "+fileName+" --move",
				WorkingDirectory = path
			});
	};
	

Task("LocalFeedDirectory")
	.Does(() => {
		if(!DirectoryExists("./localFeed"))
				CreateDirectory("./localFeed");
			
		if(!DirectoryExists("./localFeed/interfaces"))
			CreateDirectory("./localFeed/interfaces");
		
		if(!DirectoryExists("./localFeed/plugins"))
				CreateDirectory("./localFeed/plugins");
			
		if(!DirectoryExists("./localFeed/core"))
				CreateDirectory("./localFeed/core");
	});

Task("Update-And-Get-Version")
	.Does(() => {
		GitVersion result;
		
		result = GitVersion(new GitVersionSettings {
					UpdateAssemblyInfo = true,
					OutputType = GitVersionOutput.Json
				});
			
		nugetVersion = result.NuGetVersion;
		semVer = result.SemVer;
		assemblyVer = result.AssemblySemVer;
		branchName = result.BranchName;
		
		if(isRunningOnTeamCity){
			TeamCity.SetBuildNumber(result.FullSemVer);
		}
		
		gitVersionResult = result;

		Information("Nuget Version: {0}", nugetVersion);
		Information("Semantic Version: {0}", semVer);
		Information("Assembly Semantic Version: {0}", assemblyVer);
		Information("Full Semantic Version: {0}", gitVersionResult.FullSemVer);		
		Information("Branch Name: {0}", branchName);
		Information("Complete");
	})
	.OnError(exception => reportError(exception, "Update-And-Get-Version"));
	
Task("Nuget-Restore-All")
	.Does(() => {
		var solutions = GetFiles("./**/*.sln");
		// Restore all NuGet packages.
		foreach(var solution in solutions)
		{
			Information("Restoring {0}", solution);
			NuGetRestore(solution);
		}
	})
	.OnError(exception => reportError(exception, "Nuget-Restore-All"));
	