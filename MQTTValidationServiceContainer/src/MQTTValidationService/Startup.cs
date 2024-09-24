using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using MQTTValidationService.Services;
using System;
using ValidationServices.Services;

namespace MQTTValidationService
{
    public class Startup
    {
        private IConfiguration Configuration { get; }
        private IServiceProvider ServiceProvider {get;set;}
        private ILogger Log { get; set; }

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
            
        }
        
        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            // Register services
            services.AddSingleton<IMQTTService, MQTTService>();
            services.AddSingleton<IValidator, Validator>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            ILoggerFactory loggerFactory = app.ApplicationServices
                .GetRequiredService<ILoggerFactory>();
            ServiceProvider = app.ApplicationServices;

            Log = loggerFactory.CreateLogger<Startup>();
            Log.LogInformation("MQTTValidationService starting up");

            // Create MQTT Service
            var mqttService = ServiceProvider.GetService<IMQTTService>();

            Log.LogInformation("MQTTValidationService is started");
        }
    }
}
