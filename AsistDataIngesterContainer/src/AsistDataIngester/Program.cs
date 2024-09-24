using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;

namespace AsistDataIngester
{
    public class Program
    {
        static private ILogger Logger { get; set; }

        public static void Main(string[] args)
        {
            var config = new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", optional: false)
                .AddJsonFile($"appsettings.{Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT")}.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()
                .Build();

            string serverURL = config.GetValue<string>("ServerURL");

            var host = new WebHostBuilder()
                .ConfigureAppConfiguration((hostingContext, c) =>
                {
                    var env = hostingContext.HostingEnvironment;
                    c.AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
                            .AddJsonFile($"appsettings.{env.EnvironmentName}.json", optional: true, reloadOnChange: true);
                    c.AddEnvironmentVariables();
                })
                .UseKestrel(
                    (context, options) =>
                    {
                        options.Configure(context.Configuration.GetSection("Kestrel"));
                        options.AddServerHeader = false;
                    }
                )
                .UseIISIntegration()
                .UseStartup<Startup>()
                .UseUrls(serverURL)
                .ConfigureLogging((context, builder) =>
                {
                    builder.AddConfiguration(context.Configuration.GetSection("Logging"));
                    builder.AddConsole();
                    builder.AddFile(context.Configuration.GetSection("Logging").GetSection("File"));
                })
                .Build();

            host.Run();
        }
  
        static private void OnShutdown()
        {
            //Logger.LogInformation("AsistDataIngester is Shutting Down");

            Logger.LogInformation("AsistDataIngester is Shutdown");
        }
    }
}

