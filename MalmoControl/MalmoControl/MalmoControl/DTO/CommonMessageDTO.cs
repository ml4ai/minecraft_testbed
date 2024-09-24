using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class CommonMessageDTO
    {
        public string experiment_id { get; set; } = null;
        public string trial_id { get; set; } = null;
        public string timestamp { get; set; } = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
        public string source { get; set; } = "simulator";
        public string sub_type { get; set; } = null;
        public string version { get; set; } = null;
        public string replay_parent_type { get; set; } = null;
        public string replay_parent_id { get; set; } = null;
        public string replay_id { get; set; } = null; 
    }
}
