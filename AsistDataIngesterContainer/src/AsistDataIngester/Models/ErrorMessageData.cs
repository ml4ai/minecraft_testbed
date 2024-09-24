using System.Collections.Generic;

namespace AsistDataIngester.Models
{
    public class ErrorMessageData
    {
        public string state { get; set; }
        public string status { get; set; }
        public List<string> errors { get; set; }
        public string messagetopic { get; set; }
        public string messageheader { get; set; }

        public ErrorMessageData()
        {
            state = "error";
            status = "Illegal format message received";
            errors = new List<string>();
        }
    }
}
