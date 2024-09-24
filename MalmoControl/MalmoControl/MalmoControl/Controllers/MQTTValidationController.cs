using System;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;

namespace MalmoControl.Controllers
{
    [Produces("Application/json")]
    [Consumes("Application/json")]
    [Route("api/[controller]")]
    [ApiController]

    public class MQTTValidationController : ControllerBase
    {
        
        private IMQTTClient _client;
        private IConfiguration _config;

        private IExperiment _experiment;
        
        public MQTTValidationController(IMQTTClient client, IConfiguration config, IExperiment experiment){
           
            _client = client;
            _config = config;
            _experiment = experiment;

        }        

        [HttpPut("[action]")]
        public IActionResult startValidation( ControlDTO dto ){

             dto.header.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddThh:mm:ss.ffff")+'Z';
             dto.header.message_type = "control";            

           try {                
                _client.publish(dto.convertToJObject().ToString(), "control/mqttvalidationservice");
            }

            catch(Exception e){ 
                Console.WriteLine(e);                
            }
            return Ok(dto);
            
        }

        [HttpPut("[action]")]
        public IActionResult stopValidation( ControlDTO dto ){

             dto.header.timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddThh:mm:ss.ffff")+'Z';
             dto.header.message_type = "control";            

           try {                
                _client.publish(dto.convertToJObject().ToString(), "control/mqttvalidationservice");
            }

            catch(Exception e){ 
                Console.WriteLine(e);                
            }
            return Ok(dto);
        }
    }
}