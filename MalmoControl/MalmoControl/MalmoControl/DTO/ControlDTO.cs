using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class ControlDTO
    {
        public CommonHeaderDTO header = new CommonHeaderDTO();
        public AgentMessageDTO msg = new AgentMessageDTO();

         public JObject convertToJObject(){ 
        
            JObject obj = new JObject(){ 

                ["header"] = new JObject(){ 
                    
                    ["timestamp"] = header.timestamp,
                    ["message_type"] = header.message_type,
                    ["version"] = header.version
                },
                ["msg"] = new JObject(){
                    
                    ["command"] = msg.command,
                    ["experiment_name"] = msg.experiment_name,
                    ["trial_id"] = msg.trial_id
                }            
            };

            return obj;
        }
    }

    public class AgentMessageDTO
    { 
        public string trial_id = "NOT SET";
        public string command = "NOT SET";
        public string experiment_name = "NOT SET";        
    }
}
