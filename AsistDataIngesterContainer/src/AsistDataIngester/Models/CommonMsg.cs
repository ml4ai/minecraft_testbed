using System;

namespace AsistDataIngester.Models
{
    public class CommonMsg
    {
        public string experiment_id { get; set; } = System.Guid.Empty.ToString();
        public string trial_id { get; set; } = System.Guid.Empty.ToString();
        public string timestamp { get; set; }
        public string source { get; set; }
        public string sub_type { get; set; }
        public string version { get; set; }

        public CommonMsg()
        {
            // YYYY-MM-DDThh:mm:ss.ssssZ
            timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffffZ");
            source = "asistdataingester";
            version = "0.4";
        }
    }
}

