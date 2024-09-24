using System;

namespace MQTTValidationService.Models
{
    public class ControlMessageData
    {
        public string command { get; set; }
        public string experiment_name { get; set; }
        public string start_time { get; set; }
        public Guid? trial_id { get; set; }
        public Guid? replay_id { get; set; }

        public ControlMessageData()
        {

        }
    }
}