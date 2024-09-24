using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class ExperimentDTO
    {
        public CommonHeaderDTO header {get;set;} = new CommonHeaderDTO();
        public StartExperimentMessageDTO msg {get;set;} = new StartExperimentMessageDTO();
        
        public StartExperimentDataDTO data {get;set;} = new StartExperimentDataDTO();

        public JObject convertToJObject(){ 
        
            JObject obj = new JObject(){ 

                ["header"] = new JObject(){ 
                    
                    ["timestamp"] = header.timestamp,
                    ["message_type"] = header.message_type,
                    ["version"] = header.version
                },
                ["msg"] = new JObject(){
                    
                    ["sub_type"] = msg.sub_type,
                    ["source"] = msg.source,
                    ["experiment_id"] = msg.experiment_id,                    
                    ["timestamp"]= msg.timestamp,
                    ["version"]= msg.version,
                    ["replay_parent_type"] = msg.replay_parent_type,
                    ["replay_parent_id"] = msg.replay_parent_id,
                    ["replay_id"] = msg.replay_id
                }, 
                ["data"] = new JObject(){
                    
                    ["date"] = data.date,
                    ["name"] = data.name,
                    ["author"] = data.author,                    
                    ["mission"]= data.mission
                }            
            };

            return obj;
        }
    }
   
    public class StartExperimentMessageDTO {
       
        public string sub_type {get;set;} = "create";
        public string source {get;set;} = "gui";
        public string timestamp {get;set;} = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff")+'Z';        
        public string experiment_id {get;set;} = "Not Set";
        public string version {get;set;} = "1.1";
        public string replay_parent_type {get;set;}
        public string replay_parent_id {get;set;}
        public string replay_id {get;set;}
    
    }

    public class StartExperimentDataDTO { 
        
        public string date {get;set;} =  DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff")+'Z';
        public string name {get;set;} = "Not Set";
        public string author {get;set;} = "Not Set";        
        public string mission {get;set;} = "Not Set";
    
    }
   

}
