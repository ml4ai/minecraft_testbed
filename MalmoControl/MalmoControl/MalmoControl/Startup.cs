using MalmoControl.Interfaces;
using MalmoControl.Websocket;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SpaServices.AngularCli;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace MalmoControl
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }      
        
        public IConfiguration Configuration { get; }       

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {

            services.AddSingleton<IActivePorts,ActivePorts>();          
            services.AddSingleton<IMQTTClient,MQTTClient>();
            services.AddSingleton<IExperiment,Experiment>();
            
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_1);
            
            // In production, the Angular files will be served from this directory
            services.AddSpaStaticFiles(configuration => {
                configuration.RootPath = "ClientApp/dist";
            });

            // CORS
            services.AddCors(options =>
            {
                options.AddPolicy("CorsPolicy",
                    builder => builder
                    .AllowAnyOrigin()
                    .AllowAnyHeader()
                    .AllowAnyMethod());
            });

            // SWAGGER
            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new OpenApiInfo { Title = "MalmoControl Api", Version = "v1" });
                //c.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, $"{Assembly.GetExecutingAssembly().GetName().Name}.xml"));
            });

            // SignalR
            services.AddSignalR();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env, ILoggerFactory loggerFactory, IApplicationLifetime lifetime)
        {
            lifetime.ApplicationStarted.Register(OnAppStarted);

            lifetime.ApplicationStopping.Register(OnAppStopping);

            lifetime.ApplicationStopped.Register(OnAppStopped);

            string swaggerEndpoint = "v1/swagger.json";
            
            string basePath = "https://localhost:9000/MalmoControl";

            if (env.IsDevelopment() ){ 
                basePath = "http://localhost:5002";
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
                app.UseHttpsRedirection();
            }

            // Enable middleware to serve generated Swagger as a JSON endpoint.
            app.UseSwagger(c=>
                { 
                    c.PreSerializeFilters.Add((swaggerDoc, httpReq) =>
		        {
			        swaggerDoc.Servers = new List<OpenApiServer> { new OpenApiServer { Url = basePath } };
		        });
                }
            );

            // Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.),
            // specifying the Swagger JSON endpoint.
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint(swaggerEndpoint, "MalmoControl API v1");
                
            });

            // CORS middleware
            app.UseCors(builder => builder
              .AllowAnyHeader()
              .AllowAnyMethod()
              .SetIsOriginAllowed((host) => true)
              .AllowCredentials()
            );

            // signalR middleware
            app.UseSignalR(builder => 
                {
                    builder.MapHub<SocketHub>("/ws");
                }
            );
            
            app.UseStaticFiles();
            app.UseSpaStaticFiles();  

            // MVC Controller routing
            app.UseMvc(routes => {
                routes.MapRoute(
                    name: "default",
                    template: "{controller}/{action=Index}/{id?}");
            });

            // SPA
            app.UseSpa(spa => {
                // To learn more about options for serving an Angular SPA from ASP.NET Core,
                // see https://go.microsoft.com/fwlink/?linkid=864501

                spa.Options.SourcePath = "ClientApp";
                spa.Options.StartupTimeout = new System.TimeSpan(0, 2, 0);
                

                if (env.IsDevelopment()) {
                    spa.UseAngularCliServer(npmScript: "start");
                    
                }
            });


        }

        private void OnAppStopped()
        {
            throw new NotImplementedException();
        }

        private void OnAppStopping()
        {
            throw new NotImplementedException();
        }

        private void OnAppStarted()
        {
            var creds = Configuration.GetSection("RegistryCredentials");
            string u = creds.GetValue<string>("username");
            string p = creds.GetValue<string>("password");
            try
            {
                Console.WriteLine("Attempting to log into docker registry ...");
                BashHelper.Bash("docker login -u " + u + " -p " + p + " https://gitlab.asist.aptima.com:5050");
            }
            catch (Exception e) {
                Console.WriteLine(e.StackTrace);
            }
            
        }
    }
}
