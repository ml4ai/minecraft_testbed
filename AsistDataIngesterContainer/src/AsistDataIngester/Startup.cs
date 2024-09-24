using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using AsistDataIngester.Services;
using System;
using AsistDataIngester.Hubs;

namespace AsistDataIngester
{
    public class Startup
    {
        private IConfiguration Configuration { get; }
        static private IServiceProvider ServiceProvider { get; set; }
        static private ILogger Log { get; set; }

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(
                options => options.AddPolicy("AllowCors",
                    builder =>
                    {
                        builder
                            .AllowAnyOrigin()
                            .AllowCredentials()
                            .AllowAnyHeader()
                            .AllowAnyMethod();
                    })
            );

            // Register services
            services.AddSingleton<IMQTTService, MQTTService>();
            services.AddSingleton<IQualtricsMonitorService, QualtricsMonitorService>();

            services.AddSignalR();

            // Disable ssl check
            AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            ILoggerFactory loggerFactory = app.ApplicationServices
                .GetRequiredService<ILoggerFactory>();
            ServiceProvider = app.ApplicationServices;

            Log = loggerFactory.CreateLogger<Startup>();
            Log.LogInformation("AsistDataIngester starting up");

            // Create MQTT Service
            var mqttService = ServiceProvider.GetService<IMQTTService>();

            // Start Qualtrics MonitorService
            IQualtricsMonitorService QualtricsMonitorService = ServiceProvider.GetService<IQualtricsMonitorService>();
            QualtricsMonitorService.StartAsync();

            IApplicationLifetime applicationLifetime = app.ApplicationServices.GetRequiredService<IApplicationLifetime>();

            // CORS
            app.UseCors("AllowCors");

            // Register SignalR Hub
            app.UseSignalR(builder =>
            {
                builder.MapHub<AudioHub>(Configuration.GetValue<string>("SignalR:AudioEndPoint"), (options) =>
                {
                    options.ApplicationMaxBufferSize = 200 * 1024;
                });
            });

            // Register application lifetime methods
            applicationLifetime.ApplicationStopping.Register(OnShutdown);

            Log.LogInformation("AsistDataIngester is started");
        }

        static private void OnShutdown()
        {
            IQualtricsMonitorService QualtricsMonitorService = ServiceProvider.GetService<IQualtricsMonitorService>();
            QualtricsMonitorService.StopAsync();

            Log.LogInformation("AsistDataIngester is Shutdown");
        }
    }
}
