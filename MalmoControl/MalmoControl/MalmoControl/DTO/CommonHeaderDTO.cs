using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class CommonHeaderDTO
    {
        public string timestamp {get;set;} =  DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff")+'Z';
        public string message_type {get;set;} = "Not Set";
        public string version {get;set;} = "0.6";
    }
}
