using System;

namespace MQTTValidationService.Models
{
    public class HeartbeatMsg
    {
        public string timestamp { get; set; }
        public string source { get; set; }
        public string sub_type { get; set; }
        public string version { get; set; }

        public HeartbeatMsg()
        {
            // YYYY-MM-DDThh:mm:ss.ssssZ
            timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffffZ");
            sub_type = "heartbeat";
            source = "mqttvalidationservice";
            version = "0.1";
        }
    }
}