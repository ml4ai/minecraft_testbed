using MalmoControl.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.Interfaces
{
    public class ActivePorts : IActivePorts
    {

        public ActivePorts()
        {
            Ports.Data.Add("SomePort1");
            Ports.Data.Add("SomePort2");
            Ports.Data.Add("SomePort3");
        }
                  
        public ListDTO Ports {get;set;} = new ListDTO();

        public string malmoUp{get;set;} = "False";

    }
}
