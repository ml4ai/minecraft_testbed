using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.CommandLine;
using System.CommandLine.Invocation;
using System.IO;
using ValidationServices.Services;

namespace LogFileValidator
{
    class Program
    {
        static public IServiceProvider ServiceProvider { get; set; }

        static int Main(string[] args)
        {
            // Config
            var config = new ConfigurationBuilder()
                .AddEnvironmentVariables()
                .Build();

            // Setup DI
            ServiceProvider = new ServiceCollection()
               .AddLogging()
               .AddSingleton<IConfiguration>(config)
               .AddSingleton<IValidator, Validator>()
               .BuildServiceProvider();

            //configure console logging
            //serviceProvider
            //    .GetService<ILoggingBuilder>()
            //    .AddConsole();

            var logger = ServiceProvider.GetService<ILoggerFactory>()
                .CreateLogger<Program>();
            logger.LogDebug("Starting application");

            var filenameOption = new Option<string>(
                    "--filename",
                    
                    description: "The filename to validate"
                );
            filenameOption.IsRequired = true;

            var rootCommand = new RootCommand
            {
                filenameOption
            };

            rootCommand.Description = "Validates messages contained in a log file";

            rootCommand.Handler = CommandHandler.Create<string>((filename) =>
            {
                Console.WriteLine($"The filename is: {filename}");

                ProcessLogFile(filename);
            });

            return rootCommand.Invoke(args);
        }

        private static void ProcessLogFile(string filename)
        {
            string line;
            int i = 1;
            IValidator validatorService = ServiceProvider.GetService<IValidator>();

            if (!File.Exists(filename))
            {
                Console.WriteLine($"The specified file does not exist");
                return;
            }

            StreamReader file = new StreamReader(filename);

            while ((line = file.ReadLine()) != null)
            {
                string messageType = null;
                string subType = null;

                try
                {
                    JsonReader reader = new JsonTextReader(new StringReader(line));
                    reader.DateParseHandling = DateParseHandling.None;
                    JObject json = JObject.Load(reader);


                    string topic = null;

                    if (json["topic"] != null)
                    {
                        json["topic"].Value<string>();
                    }

                    validatorService.LookupSchemaByMessageType(line, out messageType, out subType);
                    List<string> result = validatorService.ValidateMessage(topic, line);
                    if (result != null && result.Count > 0)
                    {
                        Console.WriteLine($"Source Line {i} - Topic = {topic}    MessageType = {messageType}    SubType = {subType}");
                        Console.WriteLine($"---------------------------------------------------");

                        foreach (var item in result)
                        {
                            Console.WriteLine(item);
                        }

                        Console.WriteLine();
                    }                
                }
                catch (Exception)
                {

                }

                i++;
            }
        }
    }
}
