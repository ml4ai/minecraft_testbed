using MalmoControl.Interfaces;
using MalmoControl.Websocket;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Configuration;
using MQTTnet;
using MQTTnet.Client.Options;
using MQTTnet.Extensions.ManagedClient;
using Newtonsoft.Json.Linq;
using System;
using System.Threading.Tasks;
using System.Text;

namespace MalmoControl
{
    public class MQTTClient : IMQTTClient 
    {
        private IManagedMqttClient client;
        private int MasterPort;
        private string MasterIP;
        private string ClientID;
        private IHubContext<SocketHub> _socketHub;
        private readonly IConfiguration _config;
        public IExperiment _experiment;
        public bool connected = false;

        public MQTTClient(IConfiguration config, IHubContext<SocketHub> socketHub, IExperiment experiment){            
            
            _config = config;
            
            var factory = new MqttFactory();            
            client = factory.CreateManagedMqttClient();
            
            MasterIP = _config.GetSection("Mqtt")["host"];
            MasterPort = Int32.Parse(config.GetSection("Mqtt")["port"]);            
            ClientID = _config.GetSection("Mqtt")["clientID"];           

            _socketHub = socketHub;
            _experiment = experiment;
            Console.WriteLine("MQTT Client Initializing");
            Setup();

            try {
                connect().Wait();

            } catch (Exception e) {

                Console.WriteLine("There was an error establishing the MQTT connection on the Client Side");
                Console.WriteLine(e.StackTrace);
            }
        }

         public async Task connect(){

            ManagedMqttClientOptions options = new ManagedMqttClientOptionsBuilder()
                .WithAutoReconnectDelay(TimeSpan.FromSeconds(5))
                .WithClientOptions(new MqttClientOptionsBuilder()
                    .WithClientId("MalmoControl")
                    .WithTcpServer(MasterIP,MasterPort)                   
                    .WithCleanSession()                    
                    .Build())
                .Build();
            
            await client.StartAsync(options);

            Console.WriteLine("MQTT Client Running");           

            await client.SubscribeAsync(new TopicFilterBuilder().WithTopic("status/#").Build());                        
            await client.SubscribeAsync(new TopicFilterBuilder().WithTopic("control/#").Build());
            await client.SubscribeAsync(new TopicFilterBuilder().WithTopic("agent/+/versioninfo").Build());
            await client.SubscribeAsync(new TopicFilterBuilder().WithTopic("agent/control/rollcall/response").Build());
            // await client.SubscribeAsync(new TopicFilterBuilder().WithTopic("malmo/Initialized").Build());
        }

        public async void publish(string messageText, string topic){ 
            
            var message = new MqttApplicationMessageBuilder()
                .WithTopic(topic)
                .WithPayload(messageText)
                .WithExactlyOnceQoS()
                //.WithRetainFlag()
                .Build();

            await client.PublishAsync(message);
        }

         public void Setup(){ 

            client.UseApplicationMessageReceivedHandler( e => 
            {
                // COMMENT BELOW WHEN NOT DEBUGGING
                Console.WriteLine("");
                // Console.WriteLine("### RECEIVED APPLICATION MESSAGE ###");
                // Console.WriteLine($"+ Topic = {e.ApplicationMessage.Topic}");
                // Console.WriteLine($"+ Payload = {Encoding.UTF8.GetString(e.ApplicationMessage.Payload)}");
                // Console.WriteLine($"+ QoS = {e.ApplicationMessage.QualityOfServiceLevel}");
                // Console.WriteLine($"+ Retain = {e.ApplicationMessage.Retain}");
                // Console.WriteLine();

                MQTTProcessor.process(_config, this,_socketHub,e,_experiment);
                
            });
            
            client.UseDisconnectedHandler(e=>{
                Console.WriteLine("\nDisconnected from MQTT Broker!");
                Console.WriteLine("Attempting to Connect to " + MasterIP);                
                connected = false;
            });

            client.UseConnectedHandler(c=>{
                Console.WriteLine("\nConnected to MQTT Broker @ "+MasterIP+":"+MasterPort+"!");
                connected = true;
            });
        }
        
        public JObject lastAgentMessage {get;set;} 

        public JObject lastExperimentMessage {get;set;} 

        public JObject lastTrialMessage {get;set;}
    }
}
