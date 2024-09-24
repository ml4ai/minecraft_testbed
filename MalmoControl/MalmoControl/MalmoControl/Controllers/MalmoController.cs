using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using Microsoft.AspNetCore.SignalR;
using MalmoControl.Websocket;
using Newtonsoft.Json.Linq;

namespace MalmoControl.Controllers
{
    [Produces("Application/json")]
    [Consumes("Application/json")]
    [Route("api/[controller]")]
    [ApiController]
    public class MalmoController : ControllerBase
    {
        
        private readonly IActivePorts _activeports;
        private readonly IMQTTClient _mqttclient;
        private readonly IHubContext<SocketHub> _socketHub;
        private IExperiment _experiment;
        private int hitCount=0;

        public MalmoController(IActivePorts activeports, IMQTTClient mqttclient, IHubContext<SocketHub> sockethub, IExperiment experiment){
            
            _activeports = activeports;
            _mqttclient = mqttclient;
            _socketHub = sockethub;      
            _experiment = experiment;
        }

        /// <summary>
        /// Get Configuration
        /// </summary>
        /// <returns>Configuration</returns>
        [HttpGet("[action]")]
        public IActionResult malmoUp(){
            
            Console.WriteLine("Received MalmoUp? query.");
            StringDTO dto = new StringDTO();
            dto.Data = this._activeports.malmoUp.ToString();
           
            return Ok( dto );
            
        }

        [HttpGet("[action]")]

        public IActionResult getPorts(){            
            
            return Ok(this._activeports.Ports);
            
        }        

        [ApiExplorerSettings(IgnoreApi = true)]
        [HttpPut("[action]")]

        public IActionResult sendPorts(StringDTO dto){ 
            
            // change below to use logging instead of console
            
            // Console.WriteLine( "Received : " + dto.Data);
            
            string[] splitPorts = dto.Data.Split('\n');

            List<string> listPorts = new List<string>(splitPorts);

            this._activeports.Ports.Data = listPorts;

            // push to websocket          

            JObject portsMessage = new JObject(){                 
                ["data"]= new JArray(listPorts) 
            };
            
            _socketHub.Clients.All.SendAsync ("portsUpdate" , portsMessage );

            _activeports.malmoUp = PortsParser.isPortListening(this._activeports.Ports.Data,"10000");
            
            JObject malmoReadyMessage = new JObject(){                 
                ["data"]= _activeports.malmoUp 
            };

             _socketHub.Clients.All.SendAsync ("malmoIsReady" , malmoReadyMessage );
           
            
            // DO SOME LOGIC WITH THE PORTS

            
            hitCount++;
            return Ok(dto.Data);
            
        }

        [HttpPut("[action]")]

        public IActionResult startMission(MissionDTO dto)
        {
            _experiment.mission_name = dto.MissionName;
            // run bash command shell
            Console.WriteLine( "Received Mission : " + dto.MissionName);
            string cmdPrefix = "docker exec malmo-server0 /bin/bash -c \"python3 /home/malmo/MalmoPlatform/build/install/Python_Examples/";
            Console.WriteLine( "Executing : " + cmdPrefix + dto.MissionName + "\"");
            BashHelper.Bash(cmdPrefix + dto.MissionName+ "\"");
            return Ok(dto.MissionName + "started.");
        }

        [HttpPut("[action]")]

        public IActionResult openExternalPort(OpenExternalPortDTO dto)
        {
            // run bash command shell
            Console.WriteLine( "Received open port command.");
            string cmd= "docker run -d -p "+dto.ExternalPort+":1234 --network="+ dto.DockerNetwork +" verb/socat TCP-LISTEN:1234,fork TCP-CONNECT:malmo-server"+dto.InstanceNumber+":"+dto.InternalPort;
            Console.WriteLine( "Executing : " + cmd);
            BashHelper.Bash(cmd);
            return Ok(dto.InternalPort+" mapped to "+dto.ExternalPort + "on" + dto.DockerNetwork + " for Instance: "+ dto.InstanceNumber);
        }


    }
}