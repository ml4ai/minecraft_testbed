using MalmoControl;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using MalmoControl.Websocket;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using System;

namespace MinecraftControl.Controllers
{
    [Produces("Application/json")]
    [Consumes("Application/json")]
    [Route("api/[controller]")]
    [ApiController]
    public class MinecraftController : ControllerBase
    {
        
        private readonly IMQTTClient _mqttclient;
        private readonly IHubContext<SocketHub> _socketHub;
        private IExperiment _experiment;       

        public MinecraftController(IExperiment experiment, IMQTTClient mqttclient, IHubContext<SocketHub> sockethub){
            
            _experiment = experiment;            
            _mqttclient = mqttclient;
            _socketHub = sockethub;           
        }

        [HttpPut("[action]")]

        public IActionResult startMission(MissionDTO dto)
        {
            string mapname = dto.MapName;
            // set mission name so minecraft-server can grab it on starting
            _experiment.mission_name = dto.MissionName; // this will say Falcon_Easy or whatever
            _experiment.missionDTO = dto;

            
            // STOP Current Minecraft server instance
            string stopCommand = "docker stop minecraft-server0";
            //Console.WriteLine( "Executing Bash Command : " + stopCommand);
            BashHelper.Bash(stopCommand + " && sleep 1 ");

            // UPDATE SERVER.PROPERTIES
            string server_properties_text = System.IO.File.ReadAllText("minecraft_data/server.properties");
            Console.Write(server_properties_text);
            string[] lines = server_properties_text.Split('\n');
            string current_map = null;
            
            foreach(string line in lines){ 
                
                // if the string starts with levelname, return the altered string with the last "newline" character removed
                if(line.StartsWith( "level-name=")){ 
                    current_map=line; 
                    break;
                } 
            }
            
            string match_string = current_map;
            string replace_string = "level-name="+mapname;

            Console.WriteLine("Match String : " + match_string + " --- Replace With : " + replace_string );      
            
            string replaceMissionCommand = "sed -i 's/"+match_string+"/"+replace_string+"/g' minecraft_data/server.properties";
            Console.WriteLine("Running Bash command : " + replaceMissionCommand);
            // BashHelper.Bash(replaceMissionCommand);
            // END UPDATE SERVER.PROPERTIES
             

            // REMOVE OLD WORLD SAVE AND REPLACE WITH CLEAN MAP

            //string deleteMapCommand = "rm -r minecraft_data/" + current_map.Substring(11) + "/";
            //BashHelper.Bash(deleteMapCommand);            

            //string copyMapCommand = "(cd CLEAN_MAPS && find " + current_map.Substring(11) + "/ -type f -exec install -Dm 777 \"{}\" \"../minecraft_data/{}\" \\;)";
            //string copyMapCommand = "cp -r CLEAN_MAPS/" + current_map.Substring(11) + "/ minecraft_data/" + current_map.Substring(11) + "/";

            //BashHelper.Bash(copyMapCommand);
            // END REMOVE OLD WORLD SAVE AND REPLACE WITH CLEAN MAP           

            // Start Minecraft Server instance with new server properties.
            string startCommand = "docker start minecraft-server0";
            //BashHelper.Bash(startCommand);  

            // '&&' MEANS DO NOT PROCESS FOLLOWING COMMAND UNTIL PREVIOUS RETURNS SUCCESSFUL
            // FULL COMMAND BUILT FROM COMMANDS ABOVE
            // Console.WriteLine("Running Bash command : " + deleteMapCommand);
            BashHelper.Bash( replaceMissionCommand );
            Console.WriteLine("Running Bash command : " + replaceMissionCommand);
            BashHelper.Bash(startCommand);
            Console.WriteLine("Executing Bash Command : " + startCommand);

            // CLEAR THE RESTART COUNTER WHEN STARTED FROM API
            MQTTProcessor.restartCount = 0;

            return Ok(dto.MissionName + "started.");
        }

    }
}