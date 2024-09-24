using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AsistDataIngester.Models
{
    public class TrialMessage
    {
        public CommonHeader header { get; set; }
        public CommonMsg msg { get; set; }
        public StartTrialDataDTO data { get; set; }

        public TrialMessage()
        {
            header = new CommonHeader();
            msg = new CommonMsg();
        }
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
        public List<ClientInfoDTO> client_info { get; set; }

    }

    public class ClientInfoDTO
    {

        public string playername { get; set; }
        public string callsign { get; set; }
        public string participantid { get; set; }
        public string staticmapversion { get; set; }
        public string markerblocklegend { get; set; }
        public string unique_id { get; set; }

    }

}
