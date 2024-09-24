using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using MQTTnet;
using MQTTnet.Client.Options;
using MQTTnet.Extensions.ManagedClient;
using AsistDataIngester.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AsistDataIngester.Services
{
    public class MQTTService : IMQTTService
    {
        private ILogger Log { get; set; }
        private IManagedMqttClient Client { get; set; }
        private int MasterPort { get; set; }
        private string MasterIP { get; set; }

        public Boolean Connected = false;

        private string ClientID { get; set; }
        private string SurveyResponseTopic { get; set; }
        private string UserSpeechTopic { get; set; }
        private string HeartbeatTopic { get; set; }
        private string ControlTopic { get; set; }
        private string GetTrialInfoTopic { get; set; }
        private string TrialTopic { get; set; }
        private Timer Timer { get; set; }
        private int HeartbeatInterval { get; set; }
        static public bool ServiceActive { get; set; }

        public string ExperimentId { get; set; } = System.Guid.Empty.ToString();
        public string TrialId { get; set; } = System.Guid.Empty.ToString();

        public List<ClientInfoDTO> ClientInfo { get; set; }

        public MQTTService(ILoggerFactory loggerFactory, IConfiguration config)
        {
            Log = loggerFactory.CreateLogger<MQTTService>();
            ServiceActive = true;

            var factory = new MqttFactory();
            Client = factory.CreateManagedMqttClient();
            MasterIP = config.GetSection("Mqtt")["host"];
            MasterPort = Int32.Parse(config.GetSection("Mqtt")["port"]);
            ClientID = config.GetSection("Mqtt")["clientID"];

            SurveyResponseTopic = config.GetSection("Mqtt")["surveyResponseTopic"];
            UserSpeechTopic = config.GetSection("Mqtt")["userSpeechTopic"];
            HeartbeatTopic = config.GetSection("Mqtt")["heartBeatTopic"];
            ControlTopic = config.GetSection("Mqtt")["ControlTopic"];
            GetTrialInfoTopic = config.GetSection("Mqtt")["getTrialInfoTopic"];
            TrialTopic = config.GetSection("Mqtt")["trialTopic"];

            Log.LogInformation("MQTTService: MQTT Client Initializing");
            Console.WriteLine( "MQTT STARTING UP" );
            Setup();

            try
            {
                this.Connect().Wait();

            }
            catch (Exception e)
            {
                Log.LogError("MQTTService: There was an error establishing the MQTT connection on the Client Side");
                Log.LogError(null, e);
            }

            try
            {
                HeartbeatInterval = config.GetValue<int>("HeatbeatInterval");
            }
            catch (Exception)
            {
            }

            if (HeartbeatInterval <= 0)
            {
                HeartbeatInterval = 10;   // Default to 10 seconds
            }

            // Start Heart Beat Task
            Timer = new Timer(HeartbeatTask, null, TimeSpan.Zero,
                TimeSpan.FromSeconds(HeartbeatInterval));
        }

        public async Task Connect()
        {

            ManagedMqttClientOptions options = new ManagedMqttClientOptionsBuilder()
                .WithAutoReconnectDelay(TimeSpan.FromSeconds(5))
                .WithClientOptions(new MqttClientOptionsBuilder()
                    .WithClientId(ClientID)
                    .WithTcpServer(MasterIP, MasterPort)
                    .WithCleanSession()
                    .Build())
                .Build();

            await Client.StartAsync(options);

            await Client.SubscribeAsync(new TopicFilterBuilder()
                .WithTopic(ControlTopic)
                .WithTopic(GetTrialInfoTopic)
                .WithTopic(TrialTopic)
                .Build());

            Log.LogInformation("MQTTService: MQTT Client Running");
        }

        public async void Publish(string messageText, string topic)
        {

            var message = new MqttApplicationMessageBuilder()
                .WithTopic(topic)
                .WithPayload(messageText)
                .WithExactlyOnceQoS()
                .WithRetainFlag()
                .Build();

            await Client.PublishAsync(message);
        }

        public void Setup()
        {

            Client.UseApplicationMessageReceivedHandler(e =>
            {
                //Log.LogInformation("");
                //Log.LogInformation("### RECEIVED APPLICATION MESSAGE ###");
                //Log.LogInformation($"+ Topic = {e.ApplicationMessage.Topic}");
                //Log.LogInformation($"+ Payload = {Encoding.UTF8.GetString(e.ApplicationMessage.Payload)}");
                //Log.LogInformation($"+ QoS = {e.ApplicationMessage.QualityOfServiceLevel}");
                //Log.LogInformation($"+ Retain = {e.ApplicationMessage.Retain}");

                // Handle Asist Data Ingester Control Messages
                if (e.ApplicationMessage.Topic == ControlTopic)
                {
                    try
                    {
                        JsonSerializer jsonSerializer = new JsonSerializer();
                        JsonReader reader = new JsonTextReader(new StringReader(Encoding.UTF8.GetString(e.ApplicationMessage.Payload)));
                        reader.DateParseHandling = DateParseHandling.None;
                        ControlMessage controlMessage = jsonSerializer.Deserialize<ControlMessage>(reader);

                        if (controlMessage != null && controlMessage.msg != null && String.Compare(controlMessage.msg.command, "start", true) == 0)
                        {
                            // Received Start Message
                            Log.LogInformation("Received control message: start");
                            ServiceActive = true;
                            HeartbeatTask(null);
                        }
                        else if (controlMessage != null && controlMessage.msg != null && String.Compare(controlMessage.msg.command, "stop", true) == 0)
                        {
                            // Received Stop Message
                            Log.LogInformation("Received control message: stop");
                            ServiceActive = false;
                            HeartbeatTask(null);
                        }
                        else
                        {
                            Log.LogInformation("Received control message: Unknown - ignoring");
                        }

                        return;
                    }
                    catch (Exception ex)
                    {
                        Log.LogError("Error parsing control json message");
                        return;
                    }
                }
                else if (e.ApplicationMessage.Topic == GetTrialInfoTopic)
                {
                    try
                    {
                        JsonSerializer jsonSerializer = new JsonSerializer();
                        JsonReader reader = new JsonTextReader(new StringReader(Encoding.UTF8.GetString(e.ApplicationMessage.Payload)));
                        reader.DateParseHandling = DateParseHandling.None;
                        GetTrialInfoMessage trialInfoMessage = jsonSerializer.Deserialize<GetTrialInfoMessage>(reader);

                        if (trialInfoMessage != null)
                        {
                            ExperimentId = trialInfoMessage.experiment_id;
                            TrialId = trialInfoMessage.trial_id;

                            Log.LogInformation($"AsistDataIngestor: Recorded experiment_id = {ExperimentId}");
                            Log.LogInformation($"AsistDataIngestor: Recorded trial_id = {TrialId}");
                        }

                        return;
                    }
                    catch (Exception ex)
                    {
                        Log.LogError("Error parsing trial info json message");
                        return;
                    }
                }
                else if (e.ApplicationMessage.Topic == TrialTopic)
                {
                    try
                    {
                        JsonSerializer jsonSerializer = new JsonSerializer();
                        JsonReader reader = new JsonTextReader(new StringReader(Encoding.UTF8.GetString(e.ApplicationMessage.Payload)));
                        reader.DateParseHandling = DateParseHandling.None;
                        TrialMessage trialMessage = jsonSerializer.Deserialize<TrialMessage>(reader);

                        if (trialMessage != null)
                        {
                            ExperimentId = trialMessage.msg.experiment_id;
                            TrialId = trialMessage.msg.trial_id;

                            if(trialMessage.msg != null && trialMessage.msg.sub_type != null && trialMessage.msg.sub_type == "start")
                            {
                                QualtricsMonitorService.ClearResponseDict();
                            }

                            if (trialMessage.data != null && trialMessage.data.client_info != null)
                            {
                                ClientInfo = trialMessage.data.client_info;
                            }
                        }

                        return;
                    }
                    catch (Exception ex)
                    {
                        Log.LogError("Error parsing trial json message");
                        return;
                    }
                }

                // Don't talk to yourself
                if (e.ApplicationMessage.Topic == SurveyResponseTopic)
                {
                    return;
                }

            });

            Client.UseDisconnectedHandler(e =>
            {
                Log.LogInformation("MQTTService: Attempting to Connect to " + MasterIP);
                Log.LogInformation("MQTTService: Disconnected from MQTT Broker!");
                Connected = false;
            });

            Client.UseConnectedHandler(c =>
            {
                Log.LogInformation("MQTTService: Connected to MQTT Broker @ " + MasterIP + ":" + MasterPort + "!");
                Connected = true;
            });

        }

        public void SendMessage(string message)
        {
            var msg = new MqttApplicationMessageBuilder()
                .WithTopic(SurveyResponseTopic)
                .WithPayload(message)
                .WithExactlyOnceQoS()
                .WithRetainFlag()
                .Build();

            Client.PublishAsync(msg);
        }

        public void SendSurveyResponseMessage(JObject responseObj, ResponseInfo responseIno)
        {
            if (responseObj == null)
            {
                return;
            }

            string message = CreateSurveyResponseMessage(responseObj);
            Log.LogInformation($"MQTTService: Sending MQTT Response Message - Id = {responseObj["responseId"]}    RecordedDate = {responseIno.RecordedDate}");
            SendMessage(message);
        }

        public void SendUserSpeechMessage(string name, string text)
        {
            if (String.IsNullOrEmpty(name) || String.IsNullOrEmpty(text))
            {
                return;
            }

            UserSpeechMessage userSpeechMessage = new UserSpeechMessage();

            // Add original message information
            try
            {
                userSpeechMessage.msg.sub_type = "Status:UserSpeech";
                userSpeechMessage.msg.trial_id = TrialId;
                userSpeechMessage.msg.experiment_id = ExperimentId;

                JObject jObject = new JObject();
                jObject.Add("playername", name);
                jObject.Add("text", text);

                userSpeechMessage.data = jObject;
            }
            catch (Exception)
            {
                return;
            }

            string message = JsonConvert.SerializeObject(userSpeechMessage);

            Log.LogInformation($"MQTTService: Sending MQTT User Speech Message for {name}");

            var msg = new MqttApplicationMessageBuilder()
                .WithTopic(UserSpeechTopic)
                .WithPayload(message)
                .WithExactlyOnceQoS()
                .WithRetainFlag()
                .Build();

            Client.PublishAsync(msg);
        }

        private string CreateSurveyResponseMessage(JObject responseObj)
        {
            SurveyResponseMessage surveyResponseMessage = new SurveyResponseMessage();

            // Add original message information
            try
            {
                surveyResponseMessage.data = responseObj;
                surveyResponseMessage.msg.sub_type = "Status:SurveyResponse";
                surveyResponseMessage.msg.trial_id = TrialId;
                surveyResponseMessage.msg.experiment_id = ExperimentId;
            }
            catch (Exception)
            {

            }

            string result = JsonConvert.SerializeObject(surveyResponseMessage);

            return result;
        }

        private void HeartbeatTask(object state)
        {
            HeartbeatMessage heartbeatMessage = new HeartbeatMessage();
            heartbeatMessage.data.active = ServiceActive;
            string msg = JsonConvert.SerializeObject(heartbeatMessage);

            Publish(msg, HeartbeatTopic);
        }
    }
}
