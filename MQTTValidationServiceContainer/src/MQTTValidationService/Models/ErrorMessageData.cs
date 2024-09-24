using System.Collections.Generic;

namespace MQTTValidationService.Models
{
    public class ErrorMessageData
    {
        public string state { get; set; }
        public string status { get; set; }
        public List<string> errors { get; set; }
        public string messagetopic { get; set; }
        public string messageheader { get; set; }
        public string message_type { get; set; }
        public string sub_type { get; set; }
        public string source { get; set; }

        public ErrorMessageData()
        {
            state = "error";
            status = "Illegal format message received";
            errors = new List<string>();
        }
    }
}
