using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.Interfaces
{
    public interface IMQTTClient
    {
        Task connect();

        void publish(string messageText, string topic);

        void Setup();

        JObject lastAgentMessage {get;set;}
        
        JObject lastExperimentMessage {get;set;}

        JObject lastTrialMessage {get;set;}
    }
}
