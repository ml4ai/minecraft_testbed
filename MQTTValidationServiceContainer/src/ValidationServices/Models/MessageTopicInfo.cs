using System.Collections.Generic;

namespace ValidationServices.Models
{
    public class MessageTopicInfo
    {
        public string Topic { get; set; }
        public string Schema { get; set; }
        public string Description { get; set; }
        public string MessageType { get; set; }
        public List<string> SubTypes { get; set; }
    }
}
