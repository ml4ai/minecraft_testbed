using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl
{
    public class PortsParser
    {

        public static string isPortListening( List<string> activePorts, string portNumber)
        {
            string value = "False";

            List<string> justPorts = new List<string>();
            string justPort = "-1";
            activePorts.ForEach( (port) => {
                           
                string[] splitString = port.Split(":");
                
                if(splitString.Length>1){
                    
                    string removedMost = splitString[1];
                    string[] removeSuffix = removedMost.Split(' ');
                    justPort = removeSuffix[0];                                    
                }

                justPorts.Add(justPort);                
            });

            value = justPorts.Contains(portNumber)?"True":"False";            

            return value; 
        }
    }
}
