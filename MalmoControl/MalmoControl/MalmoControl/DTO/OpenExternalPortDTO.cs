using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class OpenExternalPortDTO
    {
        public string InternalPort {get;set;}
        public string ExternalPort {get;set;}

        public string InstanceNumber {get;set;}
        public string DockerNetwork {get;set;}

    }
}
