using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class MissionDTO
    {
        public string MissionName {get;set;} 
        
        public string MapName {get;set;}

        public string MapBlockFilename {get;set;}

        public string MapInfoFilename {get;set;}

        public List<ObserverInfoDTO> ObserverInfo { get; set; }        

    }

    public class ObserverInfoDTO
    {
        public string playername { get; set; }
   
    }
}