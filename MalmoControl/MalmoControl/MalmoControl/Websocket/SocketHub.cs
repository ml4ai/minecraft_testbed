using System;
using System.Threading.Tasks;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json.Linq;

namespace MalmoControl.Websocket
{
    public class SocketHub: Hub
    {
        private IMQTTClient _client;
        IConfiguration config;
        private IExperiment _experiment;
        
        public SocketHub( IConfiguration config, IMQTTClient client, IExperiment experiment)
        { 

            Console.WriteLine( "Socket MiddleWare handling socket request.");            
            this.config = config;
            _client = client;
            _experiment = experiment;
        }
        
        public async Task SendMessage(JObject message) {
            
            Console.WriteLine( "SocketHub SendMessage Hit!");
            await Clients.All.SendAsync ("newMessage" , message );
        } 

         public async Task KeepAlive() {            
            
            Console.WriteLine("Front End Ping received.");
           
            RollcallDTO dto = new RollcallDTO();
            dto.header.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
            dto.header.message_type = "agent";
            dto.header.version = "0.1";
            dto.msg.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
            dto.msg.source = "agent";
            dto.msg.sub_type = "rollcall:request";
            dto.msg.version = "0.1";
            dto.msg.experiment_id = _experiment.experiment_id;
            dto.msg.trial_id = _experiment.trial_id;
            
            dto.data.rollcall_id = Guid.NewGuid().ToString();
             _client.publish( dto.convertToJObject().ToString(), "agent/control/rollcall/request" );             
            
        }       
       
        
        public async Task GetModConfig()
        {
            string mod = config.GetSection("Mod")["name"];
            string metadataServerUrl = config.GetSection("MetadataServer")["url"];

            Console.WriteLine("Modname on backend : " + mod );

            JObject configObject = new JObject(){
                ["name"] = mod,
                ["url"] = metadataServerUrl
            };

            try {
                await Clients.All.SendAsync("modConfig", configObject );
            }
            catch(Exception e) {
                Console.WriteLine(e);
            }            
        }
    }
}
