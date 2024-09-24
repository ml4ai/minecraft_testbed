using System.ComponentModel;

namespace MQTTValidationService.Models
{
    public class HeartbeatMessageData
    {
        public string state { get; set; }
        public bool active { get; set; }

        public HeartbeatMessageData()
        {
            state = "ok";
        }
    }
}
