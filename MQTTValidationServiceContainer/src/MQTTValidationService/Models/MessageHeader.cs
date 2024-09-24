using System;

namespace MQTTValidationService.Models
{
    public class MessageHeader
    {
        public string timestamp { get; set; }
        public string message_type { get; set; }
        public string version { get; set; }

        public MessageHeader()
        {
            // YYYY-MM-DDThh:mm:ss.ssssZ
            timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffffZ");

            message_type = "status";
            version = "0.1";
        }
    }
}
