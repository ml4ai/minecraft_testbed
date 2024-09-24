using MalmoControl.Controllers;
using MalmoControl.DTO;
using MalmoControl.Interfaces;
using MalmoControl.Websocket;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Configuration;
using MQTTnet;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Text;

namespace MalmoControl
{
    public static class MQTTProcessor
    {   
        public static int restartCount = 0;

        public static void process(IConfiguration config, MQTTClient mqtt , IHubContext<SocketHub> socketHub, MqttApplicationMessageReceivedEventArgs e, IExperiment experiment){

            NonAPIExperimentControl nonAPIExperimentControl = new NonAPIExperimentControl(config, mqtt, experiment,socketHub);

            JObject message = null;

            JObject alive_message = new JObject() {
                        ["data"] = "True"
            };

            if(e.ApplicationMessage.Topic.EndsWith("versioninfo")) 
            {
                    JObject versionmessage = null;
                    versionmessage = new JObject()
                        {
                            ["data"] = Encoding.UTF8.GetString(e.ApplicationMessage.Payload)
                        };
                    
                    socketHub.Clients.All.SendAsync("allContainers" , versionmessage);
            }


            switch(e.ApplicationMessage.Topic){

                case "status/agent/heartbeats":                    

                    socketHub.Clients.All.SendAsync("agentContainerInitialized" , alive_message);
                    
                    break;

                case "status/asistdataingester/heartbeats":
                    Console.WriteLine(e.ApplicationMessage.Topic);
                    break;
                case "status/mqttvalidationservice/heartbeats":

                    socketHub.Clients.All.SendAsync("messageValidatorInitialized" , alive_message);

                    try
                    {
                        JsonReader reader = new JsonTextReader(new StringReader(Encoding.UTF8.GetString(e.ApplicationMessage.Payload)));
                        reader.DateParseHandling = DateParseHandling.None;
                        JObject json = JObject.Load(reader);

                        if (json != null && json["data"] != null && json["data"]["active"] != null)
                        {
                            message = new JObject()
                            {
                                ["data"] = json["data"]["active"].ToString()
                            };
                            
                            socketHub.Clients.All.SendAsync("messageValidatorActive", message);
                        }
                    }
                    catch (Exception)
                    {

                    }

                    break;

                case "status/mqttvalidationservice/messages":                
                    
                    string validationMessage = Encoding.UTF8.GetString(e.ApplicationMessage.Payload, 0, e.ApplicationMessage.Payload.Length);
                    socketHub.Clients.All.SendAsync("messageValidatorMessage", validationMessage);

                    break;

                case "control/request/getTrialInfo":
                    
                    JObject trialInfoObject = new JObject(){                        
                        ["experiment_id"] = experiment.experiment_id,
                        ["trial_id"] = experiment.trial_id,
                        ["mission_name"] = experiment.missionDTO.MissionName,
                        ["map_name"] = experiment.missionDTO.MapName,
                        ["map_block_filename"] = experiment.missionDTO.MapBlockFilename,
                        ["map_info_filename"] = experiment.missionDTO.MapInfoFilename,
                    };                        
                    
                    if (experiment.missionDTO.ObserverInfo != null)
                    {
                        JArray observers = new JArray();
                        foreach (ObserverInfoDTO info in experiment.missionDTO.ObserverInfo) {

                            observers.Add(info.playername);
                        }

                        trialInfoObject["observer_info"] = observers;
                    }
                     if (experiment.trialDTO.data.client_info != null)
                    {
                        JObject callSigns = new JObject();
                        JObject participant_ids = new JObject();
                        
                        foreach(ClientInfoDTO info in experiment.trialDTO.data.client_info){
                    
                            callSigns.Add( info.playername,info.callsign);
                            participant_ids.Add(info.playername,info.participant_id);
                        }                        
                        
                        trialInfoObject["callsigns"] = callSigns;   
                        trialInfoObject["participant_ids"] = participant_ids;
                    }
                    if (experiment.trialDTO.data.intervention_agents != null) {
                        JArray agents = new JArray();
                        
                        foreach (String name in experiment.trialDTO.data.intervention_agents)
                        {
                            agents.Add(name);
                        }
                        trialInfoObject["active_agents"] = agents;

                    }

                    mqtt.publish(trialInfoObject.ToString(), "control/response/getTrialInfo");                    
                    
                    break;

                case "status/clientmapsystem/playername":

                    string playernameMessage = Encoding.UTF8.GetString(e.ApplicationMessage.Payload, 0, e.ApplicationMessage.Payload.Length);

                    JObject playernameObject = JObject.Parse(playernameMessage);
                
                    socketHub.Clients.All.SendAsync("clientmapsystemPlayername", playernameObject);

                    break;

                case "status/minecraft/loading":

                    JObject minecraftContainerMessage = new JObject()
                    {
                        ["data"] = "True"
                    };

                    socketHub.Clients.All.SendAsync("minecraftContainerUp", minecraftContainerMessage);

                    // parse the progress field to see what percentage to set the progress bar

                    string loadingProgress = Encoding.UTF8.GetString(e.ApplicationMessage.Payload, 0, e.ApplicationMessage.Payload.Length);

                    JObject progressObject = JObject.Parse(loadingProgress);

                    socketHub.Clients.All.SendAsync("minecraftLoadingProgress", progressObject);

                    // BELOW IS HANDLED WITH FRONT END LOGIC WHEN PROGRESS BAR REACHES 100
                    // socketHub.Clients.All.SendAsync("minecraftIsReady", minecraftReadyMessage);

                    break;

                case "status/server/stopped":

                    // parse the progress field to see what percentage to set the progress bar

                    string serverStopped = Encoding.UTF8.GetString(e.ApplicationMessage.Payload, 0, e.ApplicationMessage.Payload.Length);

                    JObject serverStoppedObject = JObject.Parse(serverStopped);

                    socketHub.Clients.All.SendAsync("minecraftServerStopped", serverStoppedObject);

                    bool error = (bool)serverStoppedObject.GetValue("error");

                    if (error  )
                    {
                        if (restartCount <= 5)
                        {
                            restartCount++;

                            JObject minecraftReadyMessage = new JObject()
                            {
                                ["data"] = "Restart"
                            };

                            socketHub.Clients.All.SendAsync("minecraftIsReady", minecraftReadyMessage);

                            JObject minecraftStoppedContainerMessage = new JObject()
                            {
                                ["data"] = "Restart"
                            };

                            socketHub.Clients.All.SendAsync("minecraftContainerUp", minecraftStoppedContainerMessage);

                            Console.WriteLine("There was a loading error in the Minecraft Server");

                            JObject stoppedProgressObject = new JObject()
                            {
                                ["loaded "] = 0
                            };

                            socketHub.Clients.All.SendAsync("minecraftLoadingProgress", stoppedProgressObject);


                            Console.WriteLine(" MINECRAFT SERVER HAS STOPPED WITH AN ERROR, ATTEMPTNG TO RESTART. RESTART COUNT : " + restartCount.ToString() + "/5 ");
                            
                            // Stop the Server and throw out the map                            
                            
                            nonAPIExperimentControl.StopServer();

                            // Start Server with saved DTO
                            
                            nonAPIExperimentControl.RestartServer(experiment.trialDTO);

                            // Start Mission with saved DTO
                            nonAPIExperimentControl.startMission(experiment.missionDTO);
                        }
                        else
                        {

                            JObject minecraftReadyMessage = new JObject()
                            {
                                ["data"] = "Fail"
                            };

                            socketHub.Clients.All.SendAsync("minecraftIsReady", minecraftReadyMessage);

                            JObject minecraftStoppedContainerMessage = new JObject()
                            {
                                ["data"] = "Fail"
                            };

                            socketHub.Clients.All.SendAsync("minecraftContainerUp", minecraftStoppedContainerMessage);

                            Console.WriteLine("There was a loading error in the Minecraft Server");

                            JObject stoppedProgressObject = new JObject()
                            {
                                ["loaded "] = 0
                            };

                            socketHub.Clients.All.SendAsync("minecraftLoadingProgress", stoppedProgressObject);


                            Console.WriteLine(" MINECRAFT SERVER HAS FAILED TO LOAD 5 TIMES ... SOMETHING IS WRONG. ");                            

                            // Stop the Server and throw out the map
                            nonAPIExperimentControl.StopServer();

                        }
                    }

                    break;

                case "agent/control/rollcall/response":

                    // parse the progress field to see what percentage to set the progress bar

                    string rollcallResponse = Encoding.UTF8.GetString(e.ApplicationMessage.Payload, 0, e.ApplicationMessage.Payload.Length);

                    JObject rollcallResponseObject = JObject.Parse(rollcallResponse);

                    socketHub.Clients.All.SendAsync("rollcallResponse", rollcallResponseObject);
                    break;

                case var a when e.ApplicationMessage.Topic.EndsWith("heartbeats"):
            
                JObject hbmessage = null;
                hbmessage = new JObject()
                {
                    ["data"] = Encoding.UTF8.GetString(e.ApplicationMessage.Payload)
                };
                socketHub.Clients.All.SendAsync("agentHeartbeats" , hbmessage);

                break;
            

            default: Console.WriteLine(e.ApplicationMessage.Topic);

                break;
            
            } 
        
        }        
    }
}
