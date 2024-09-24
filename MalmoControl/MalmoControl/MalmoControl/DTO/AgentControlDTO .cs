using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class AgentControlDTO
    {

        public class AgentControlDataDTO
        {
            public string agent_identifier = null;
            public string command = null;
        }

        public CommonHeaderDTO header = new CommonHeaderDTO();
        public CommonMessageDTO msg = new CommonMessageDTO();
        public AgentControlDataDTO data = new AgentControlDataDTO();

         public JObject convertToJObject(){ 
        
            JObject obj = new JObject(){ 

                ["header"] = new JObject(){ 
                    
                    ["timestamp"] = header.timestamp,
                    ["message_type"] = header.message_type,
                    ["version"] = header.version

                },
                ["msg"] = new JObject(){
                    
                    ["source"] = msg.source,
                    ["experiment_id"] = msg.experiment_id,
                    ["trial_id"] = msg.trial_id,
                    ["sub_type"] = msg.sub_type,
                    ["timestamp"] = msg.timestamp,
                    ["version"] = msg.version,
                    ["replay_parent_type"] = msg.replay_parent_type,
                    ["replay_parent_id"] = msg.replay_parent_id,
                    ["replay_id"]=msg.replay_id

                } 
                
                ["data"] = new JObject() {

                    ["agent_identifier"] = data.agent_identifier,
                    ["command"] = data.command  

                }
            };

            return obj;
        }
    }

}
