using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MQTTValidationService.Models
{
    public class ControlMessage
    {
        public MessageHeader header { get; set; }
        public ControlMessageData msg { get; set; }

        public ControlMessage()
        {
            header = new MessageHeader();
            msg = new ControlMessageData();
        }
    }
}
