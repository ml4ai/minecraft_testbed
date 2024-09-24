using System;
using System.Collections.Generic;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace MalmoControl.Controllers
{
    [Produces("Application/json")]
    [Consumes("Application/json")]
    [Route("api/[controller]")]
    [ApiController]

    public class AgentController : ControllerBase
    {
        
        private IMQTTClient _client;
        private IConfiguration _config;
        private IExperiment _experiment;
        private Dictionary<string, UpDown> agentScripts;
        private ILogger<AgentController> _logger;


        public AgentController(IMQTTClient client, IConfiguration config, IExperiment experiment, ILogger<AgentController> logger)
        {

            _logger = logger;
            _client = client;
            _config = config;
            _experiment = experiment;          

            IConfigurationSection a = config.GetSection("AgentShellScripts");

            agentScripts = new Dictionary<string, UpDown>();

            foreach (var child in a.GetChildren())
            {
                agentScripts.Add(child.Key, new UpDown(child.GetValue<string>("up"), child.GetValue<string>("down")));

            }
        }        

        [HttpPut("[action]")]
        public IActionResult control( AgentControlDTO dto ){

             dto.header.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff")+'Z';
             dto.header.message_type = "control";        

           try {                
                _client.publish(dto.convertToJObject().ToString(),"control");
            }

            catch(Exception e){ 
                _logger.LogInformation(e.StackTrace);                
            }

            try
            {
                string agent_identifier = dto.data.agent_identifier;
                string command = dto.data.command;

                UpDown upDown = null;

                agentScripts.TryGetValue(agent_identifier, out upDown);

                if( upDown != null)
                {
                    if (command.Equals("up"))
                    {
                        _logger.LogInformation("Running : " + upDown.up);
                        BashHelper.Bash(upDown.up);
                    }
                    else if (command.Equals("down"))
                    {
                        _logger.LogInformation("Running : " + upDown.down);
                        BashHelper.Bash(upDown.down);
                    }
                }
                else
                {
                    _logger.LogInformation("ERROR: UpDown object was null for : " + agent_identifier);
                }
            }

            catch (Exception e)
            {
                _logger.LogInformation(e.StackTrace);
            }
            return Ok(dto);
            
        }     

        internal class UpDown
        {
            public string up;
            public string down;
            internal UpDown(string up, string down)
            {
                this.up = up;
                this.down = down;
            }
        }
    }
}