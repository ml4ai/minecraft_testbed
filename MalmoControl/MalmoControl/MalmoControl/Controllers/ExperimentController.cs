using System;
using System.Net.Http;
using System.Threading.Tasks;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using MalmoControl.Websocket;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;

namespace MalmoControl.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ExperimentController : ControllerBase
    {
        private IMQTTClient _client;
        private IConfiguration _config;
        private IExperiment _experiment;
        private IHubContext<SocketHub> _sockethub;

        public ExperimentController(IMQTTClient client, IConfiguration config, IExperiment experiment, IHubContext<SocketHub> sockethub){
            
            _client = client;
            _sockethub = sockethub;
            _config = config;
            _experiment= experiment;
        }

        [HttpGet("[action]")]
        public IActionResult getTrialId(){

            StringDTO stringDTO = new StringDTO();
            stringDTO.Data = _experiment.trial_id.ToString();

            return Ok(stringDTO);
            
        }

        [HttpGet("[action]")]
        public IActionResult getExperimentId(){

            StringDTO stringDTO = new StringDTO();
            stringDTO.Data = _experiment.experiment_id.ToString();

            return Ok(stringDTO);
            
        }

        [HttpGet("[action]")]
        public IActionResult getIds(){

            IdDTO idDTO = new IdDTO();
            idDTO.trial_id = _experiment.trial_id;
            idDTO.experiment_id = _experiment.experiment_id;


            return Ok(idDTO);
            
        }

        
        [HttpGet("[action]")]
        public async Task<IActionResult> fetchExperiments(  ){            
            
           string url = _config.GetSection("MetadataServer")["url"];
           Console.WriteLine ( "Attempting to contact : " + url );
            JObject responseObject = new JObject(){ 
                ["experiments"] = null
            };
            using (var handler = new HttpClientHandler())
            {
                handler.ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => true;
                using ( var response = await new HttpClient(handler).GetAsync(url) )
                {
                    try{                 
                         
                        responseObject["experiments"] = await response.Content.ReadAsStringAsync();
                        //Console.WriteLine(responseObject["experiments"]);
                    }  
                    catch(HttpRequestException e)
                    {
                        Console.WriteLine("\nException Caught!");	
                        Console.WriteLine("Message :{0} ",e.Message);
                    }
                }
            }            

            return Ok(responseObject);
        
        }
       

        [HttpPost("[action]")]
        public IActionResult createExperiment(ExperimentDTO dto){

            Console.WriteLine("Starting Experiment with :  " + dto);
            
            dto.header.message_type = "experiment";                       
            
            dto.msg.experiment_id = Guid.NewGuid().ToString();
            
            // keep last Experiment message client
            _client.lastExperimentMessage = dto.convertToJObject();

            //publish to message bus
            try {                
                _client.publish(_client.lastExperimentMessage.ToString(),"experiment");
            }
            catch(Exception e){ 
                Console.WriteLine(e);                
            }

            return Ok(dto);
            
        }

        
        [HttpPost("[action]")]
        public IActionResult StartTrial( TrialDTO dto){

            Console.WriteLine("Starting Trial with :  " + dto.convertToJObject().ToString());
                 
            dto.header.message_type = "trial";
            
            dto.msg.trial_id = Guid.NewGuid().ToString();
            dto.data.experiment_date = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';
            dto.data.testbed_version = _config.GetSection("About")["system_version"];           
            
            _experiment.experiment_id = dto.msg.experiment_id;
            _experiment.trial_id = dto.msg.trial_id;            

            // store dto in experiment singleton
            _experiment.trialDTO = dto;            

            //publish to message bus
            try {
                _client.publish(dto.convertToJObject().ToString(), "trial");
            } catch (Exception e) {
                Console.WriteLine(e);
            }

            return Ok(dto);
        }

        
        [HttpGet("[action]")]
        public IActionResult StopTrial(){

            TrialDTO dto = _experiment.trialDTO;  
            string timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.ffff") + 'Z';

            dto.header.timestamp = timestamp;
            dto.msg.timestamp = timestamp;
            dto.msg.sub_type = "stop";

            _experiment.trialDTO = dto;           

            Console.WriteLine("Stopping Trial with id :  " + _experiment.trial_id);
           
            //publish to message bus
            try {
                _client.publish(_experiment.trialDTO.convertToJObject().ToString(), "trial");
            } catch (Exception e) {
                Console.WriteLine(e);
            }


            Console.WriteLine(" Stop Trial received ... PRE container kill async task");
            // Task.Run() i async so the method wil return before it finishes and prevent the error where Trial Stop message is not
            // published
           
            Console.WriteLine(" Stop Trial received ... POST container async task");

            return Ok(_experiment.trialDTO);
        }

        [HttpGet("[action]")]
        public IActionResult KillContainer()  {
            
            Console.WriteLine(" Kill Trial received ... PRE container stop async task");
            // Task.Run() i async so the method wil return before it finishes and prevent the error where Trial Stop message is not
            // published
            Task.Run(() =>
            {

                // Bring down Minecraft Server

                // STOP Current Minecraft server instance
                string stopCommand = "docker kill minecraft-server0";
                Console.WriteLine("Executing Bash Command : " + stopCommand);
                //BashHelper.Bash(stopCommand);

                // UPDATE SERVER.PROPERTIES
                string server_properties_text = System.IO.File.ReadAllText("minecraft_data/server.properties");
                Console.Write(server_properties_text);
                string[] lines = server_properties_text.Split('\n');
                string current_map = null;

                foreach (string line in lines)
                {

                    // if the string starts with levelname, return the altered string with the last "newline" character removed
                    if (line.StartsWith("level-name="))
                    {
                        current_map = line;
                        break;
                    }
                }

                string deleteMapCommand = "rm -r minecraft_data/" + current_map.Substring(11) + "/";
                //BashHelper.Bash(deleteMapCommand);            

                string copyMapCommand = "(cd CLEAN_MAPS && find " + current_map.Substring(11) + "/ -type f -exec install -Dm 777 \"{}\" \"../minecraft_data/{}\" \\;)";
                //string copyMapCommand = "cp -r CLEAN_MAPS/" + current_map.Substring(11) + "/ minecraft_data/" + current_map.Substring(11) + "/";

                //BashHelper.Bash(copyMapCommand);

                BashHelper.Bash(stopCommand + " && sleep 3 &&" + deleteMapCommand + " && sleep 1 && " + copyMapCommand);

                _client.publish("", "status/minecraft/stopped");
            });

            Console.WriteLine(" Kill Trial received ... POST container async task");

            JObject responseObject = new JObject()
            {
                ["container_stopped"] = true
            };

            return Ok(responseObject);
        }
    }
}