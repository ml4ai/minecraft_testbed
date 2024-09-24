using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class TrialDTO
    {
        public CommonHeaderDTO header {get;set;} = new CommonHeaderDTO();
        public StartTrialMessageDTO msg {get;set;} = new StartTrialMessageDTO();
        
        public StartTrialDataDTO data {get;set;} = new StartTrialDataDTO();

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
                    ["trial_id"] = msg.trial_id,
                    ["timestamp"]= msg.timestamp,
                    ["version"]= msg.version,
                    ["replay_parent_type"] = msg.replay_parent_type,
                    ["replay_parent_id"] = msg.replay_parent_id,
                    ["replay_id"] = msg.replay_id
                }, 
                ["data"] = new JObject(){
                    
                    ["date"] = data.date,
                    ["name"] = data.name,
                    ["experimenter"] = data.experimenter,                    
                    ["subjects"]= new JArray(data.subjects),
                    ["notes"]= new JArray(data.notes),
                    ["testbed_version"] = data.testbed_version,
                    ["trial_number"] = data.trial_number,
                    ["group_number"] = data.group_number,
                    ["study_number"] = data.study_number,
                    ["condition"] = data.condition,
                    ["experiment_name"] = data.experiment_name,
                    ["experiment_author"] = data.experiment_author,
                    ["experiment_date"] = data.experiment_date,
                    ["experiment_mission"] = data.experiment_mission,
                    ["map_name"] = data.map_name,
                    ["map_block_filename"] = data.map_block_filename,
                    ["intervention_agents"] = new JArray(data.intervention_agents)
                    
                }
            };

            // Add Client_Info
            if (data.client_info != null)
            {
                obj["data"]["client_info"] = JArray.FromObject(data.client_info);
            }

            return obj;
        }
    }

    public class StartTrialMessageDTO
    {

        public string experiment_id { get; set; } = "Not Set";
        public string trial_id { get; set; } = "Not Set";
        public string sub_type { get; set; } = "start";
        public string source { get; set; } = "gui";
        public string timestamp { get; set; } = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
        public string version { get; set; } = "0.1";
        public string replay_parent_type {get;set;}
        public string replay_parent_id {get;set;}
        public string replay_id { get; set; }

    }

    public class StartTrialDataDTO
    {

        public string date { get; set; } = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
        public string name { get; set; }
        public string experimenter { get; set; }
        public List<string> subjects { get; set; } = new List<string>();
        public List<string> notes { get; set; } = new List<string>();
        public string testbed_version { get; set; } = "1.1.0"; // should make this pull automatically from appsettings
        public string trial_number { get; set; }
        public string group_number { get; set; }
        public string study_number { get; set; }
        public string condition { get; set; }
        public string experiment_name { get; set; }
        public string experiment_date { get; set; }
        public string experiment_author { get; set; }
        public string experiment_mission { get; set; }
        public string map_name { get; set; }
        public string map_block_filename { get; set; }
        public List<ClientInfoDTO> client_info { get; set; }
        public List<string> intervention_agents { get; set; } = new List<string>();
        //public RoleTextDTO role_text { get; set; }
    }

    public class ClientInfoDTO
    {

        public string playername { get; set; }
        public string callsign { get; set; }       
        public string participant_id { get; set; }
        public string staticmapversion { get; set; }
        public string markerblocklegend { get; set; }
        public string unique_id { get; set; }

    }

    public class RoleTextDTO
    {
      public string mission_name { get; set; }
      public string medic_text { get; set; }
      public string transport_text { get; set; }
      public string engineer_text { get; set; }
    }

}

