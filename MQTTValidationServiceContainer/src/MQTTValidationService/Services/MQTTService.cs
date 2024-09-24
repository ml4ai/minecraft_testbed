using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using MQTTnet;
using MQTTnet.Client.Options;
using MQTTnet.Extensions.ManagedClient;
using MQTTValidationService.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using ValidationServices.Services;

namespace MQTTValidationService.Services
{
    public class MQTTService : IMQTTService
    {
        private ILogger Log { get; set; }
        private IValidator MQTTValidator { get; set; }
        private IManagedMqttClient Client { get; set; }
        private int MasterPort { get; set; }
        private string MasterIP { get; set; }

        public Boolean Connected = false;

        private string ClientID { get; set; }
        private string MessagesTopic { get; set; }
        private string HeartbeatTopic { get; set; }
        private string ControlTopic { get; set; }
        private Timer Timer { get; set; }
        private int HeartbeatInterval { get; set; }
        private bool ServiceActive { get; set; }

        public MQTTService(ILoggerFactory loggerFactory, IConfiguration config, IValidator mqttValidator)
        {
            Log = loggerFactory.CreateLogger<MQTTService>();
            MQTTValidator = mqttValidator;
            ServiceActive = false;

            var factory = new MqttFactory();
            Client = factory.CreateManagedMqttClient();
            MasterIP = config.GetSection("Mqtt")["host"];
            MasterPort = Int32.Parse(config.GetSection("Mqtt")["port"]);
            ClientID = config.GetSection("Mqtt")["clientID"];

            MessagesTopic = config.GetSection("Mqtt")["messagesTopic"];
            HeartbeatTopic = config.GetSection("Mqtt")["heartBeatTopic"];
            ControlTopic = config.GetSection("Mqtt")["ControlTopic"];

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

            await Client.SubscribeAsync(new TopicFilterBuilder().WithTopic("#").Build());

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

                // Handle Validator Control Messages
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

                // Don't talk to yourself
                if (e.ApplicationMessage.Topic == MessagesTopic)
                {
                    return;
                }
                // If service is not active, skip validation
                if (!ServiceActive)
                {
                    return;
                }

                // Validate Other Messages
                List<string> errors = MQTTValidator.ValidateMessage(e.ApplicationMessage.Topic, Encoding.UTF8.GetString(e.ApplicationMessage.Payload));
                if (errors != null && errors.Count > 0)
                {
                    // Send validation error
                    string message = CreateValidationErrorMessage(e.ApplicationMessage.Topic, Encoding.UTF8.GetString(e.ApplicationMessage.Payload), errors);
                    Log.LogWarning(e.ApplicationMessage.Topic + ": " + message);
                    SendMessage(message);
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
                .WithTopic(MessagesTopic)
                .WithPayload(message)
                .WithExactlyOnceQoS()
                .WithRetainFlag()
                .Build();

            Client.PublishAsync(msg);
        }

        private string CreateValidationErrorMessage(string topic, string message, List<string> errors)
        {
            ErrorMessage errorMessage = new ErrorMessage();

            // Add errors
            foreach (string error in errors)
            {
                errorMessage.msg.errors.Add(error);
            }

            // Add original message information
            try
            {
                JsonReader reader = new JsonTextReader(new StringReader(message));
                reader.DateParseHandling = DateParseHandling.None;
                JObject json = JObject.Load(reader);

                errorMessage.msg.messageheader = json["header"].ToString();

                // Copy the message_type if available
                if (json["header"] != null && json["header"]["message_type"] != null)
                {
                    errorMessage.msg.message_type = json["header"]["message_type"].ToString();
                }

                // Copy the sub_type if available
                if (json["msg"] != null && json["msg"]["sub_type"] != null)
                {
                    errorMessage.msg.sub_type = json["msg"]["sub_type"].ToString();
                }

                // Copy the source if available
                if (json["msg"] != null && json["msg"]["source"] != null)
                {
                    errorMessage.msg.source = json["msg"]["source"].ToString();
                }
            }
            catch (Exception)
            {

            }

            errorMessage.msg.messagetopic = topic;

            string result = JsonConvert.SerializeObject(errorMessage);

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
