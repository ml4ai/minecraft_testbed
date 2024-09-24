using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AsistDataIngester.Models
{
    public class ControlMessage
    {
        public CommonHeader header { get; set; }
        public ControlMessageData msg { get; set; }

        public ControlMessage()
        {
            header = new CommonHeader();
            msg = new ControlMessageData();
        }
    }
}
