using MalmoControl.DTO;
using MalmoControl.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MalmoControl.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HelpController : ControllerBase
    {
        IConfiguration _config;
        private IMQTTClient _client;

        public HelpController(IConfiguration config, IMQTTClient client){
            _client = client;
            _config = config;
        }

        [HttpGet("[action]")]
        public IActionResult getConfig(){

            List<string> asi_list = new List<string>();

            IConfigurationSection a = _config.GetSection("AgentShellScripts");            

            foreach (var child in a.GetChildren())
            {
                asi_list.Add(child.Key);
                Console.WriteLine(child.Key);

            }

            JObject configObject = new JObject() {

                ["mod"] = _config.GetSection("Mod")["name"],
                ["metadata_Url"] = _config.GetSection("MetadataServer")["url"],
                ["mqtthost"] = _config.GetSection("Mqtt")["host"],
                ["mqttport"] = _config.GetSection("Mqtt")["port"],
                ["mqttclient"] = _config.GetSection("Mqtt")["clientID"],
                ["testbed_version"] = _config.GetSection("About")["system_version"],
                ["mission_list"] = getMissionListFromConfig(),
                ["callsign_list"] = new JArray(_config.GetSection("CallSignList").Get<List<string>>()),
                ["asi_list"] = new JArray(asi_list)
               
            };

            // Request that agents rollcall
            Task.Delay(5000).ContinueWith(t =>
            {
                RollcallDTO dto = new RollcallDTO();
                dto.header.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
                dto.header.message_type = "agent";
                dto.header.version = "0.1";
                dto.msg.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
                dto.msg.source = "agent";
                dto.msg.sub_type = "rollcall:request";
                dto.msg.version = "0.1";
                dto.data.rollcall_id = Guid.NewGuid().ToString();
                _client.publish(dto.convertToJObject().ToString(), "agent/control/rollcall/request");
            });

            return Ok(configObject);
        }

        [HttpGet("[action]")]
        public IActionResult getAbout(){

            //"system_name": "ASIST Testbed",
            //"system_description": "The ASIST testbed provides an environment for research into human/AI teams.",
            //"darpa_acknolwedgement": "The ASIST project is sponsored by DARPA",
            //"system_version": "0.2",
            //"system_build_date": "2020-02-21 09:00:00",
            //"aptima_legal_notice": "Copyright 2020, Aptima Inc.",
            //"other_notices": [ "Minecraft", "Malmo", "Elastic", "PMEngine", "MQTT" ]
            
            JObject helpObject = new JObject(){
                
                ["system_name"] = _config.GetSection("About")["system_name"],
                ["system_description"] = _config.GetSection("About")["system_description"],
                ["darpa_acknolwedgement"] = _config.GetSection("About")["darpa_acknolwedgement"], 
                ["system_version"] = _config.GetSection("About")["system_version"],
                ["system_build_date"] = _config.GetSection("About")["system_build_date"],
                ["aptima_legal_notice"] = _config.GetSection("About")["aptima_legal_notice"],
                ["other_notices"] = new JArray(_config.GetSection("About").GetSection("other_notices").Get<List<string>>() )
            
            };

            //return with api
            return Ok(helpObject);
            
        }

        private JArray getMissionListFromConfig(){ 
            JArray array = new JArray();

            IConfigurationSection section = _config.GetSection("MissionList");
            IEnumerable<IConfigurationSection> children  = section.GetChildren();
            foreach (var child in children)
            {
                JObject missionObject = new JObject {
                    
                    ["MissionName"] =  child["MissionName"],
                    ["MapName"] = child["MapName"],
                    ["MapBlockFilename"] = child["MapBlockFilename"],
                    ["MapInfoFilename"] = child["MapInfoFilename"]                    
                };

                //Console.WriteLine( missionObject.ToString() );
                
                array.Add(missionObject);
                    
            }

            return array;

        }

        private JArray getRoleTextFromConfig(){ 
            JArray array = new JArray();

            IConfigurationSection section = _config.GetSection("RoleSpecificText");
            IEnumerable<IConfigurationSection> children  = section.GetChildren();
            foreach (var child in children)
            {
                JObject roletextObject = new JObject {
                    
                    ["mission_name"] =  child["mission_name"],
                    ["medic_text"] = child["medic_text"],
                    ["transport_text"] = child["transport_text"],
                    ["engineer_text"] = child["engineer_text"]                    
                };
                
                array.Add(roletextObject);
                    
            }

            return array;

        }

    }
}