using AsistDataIngester.Models;
using AsistDataIngester.Services;
using Google.Cloud.Speech.V1;
using Grpc.Core;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AsistDataIngester.Hubs
{
    public class AudioHub : Hub
    {
        static private ILogger _logger;
        static private Dictionary<string, AudioHubClientInfo> AudioHubClientInfoDict = new Dictionary<string, AudioHubClientInfo>();
        static private IConfiguration Configuration { get; set; }
        static private AppSettings AppSettings { get; set; }

        private IMQTTService MQTTService { get; set; }
        private int StreamCycleTime = 4;    // Stream recycle time in minutes to avoid google timeout
        private string language_code = "en_US";

        public AudioHub(ILogger<AudioHub> logger, IConfiguration configuration, IMQTTService mqttService)
        {
            _logger = logger;
            MQTTService = mqttService;
            Configuration = configuration;
            AppSettings = new AppSettings();

            Configuration.GetSection("App").Bind(AppSettings);
        }

        public override async Task OnConnectedAsync()
        {
            string connectionId = Context.ConnectionId;

            var httpContext = Context.GetHttpContext();
            if (httpContext == null)
                throw new Exception("OnConnectedAsync: Unable to read HttpContext");

            var query = httpContext.Request.Query;
            string name = query["name"].ToString();
            int sampleRate = int.Parse(query["sampleRate"].ToString());

            // Lookup the client info or create a new record
            AudioHubClientInfo audioHubClientInfo = LookupdAudioHubClientInfo(connectionId);

            audioHubClientInfo.Name = name;
            audioHubClientInfo.SampleRate = sampleRate;

            _logger.LogInformation($"{connectionId}: {name} has connected to the Audio Hub");

            if (!AppSettings.DisableSpeechToText)
            {
                // Start Google speech detection
                Environment.SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", $"Google/google_application_credentials.json");

                SpeechClient client = SpeechClient.Create();
                RecognitionConfig config = new RecognitionConfig()
                {
                    AudioChannelCount = 1,
                    Encoding = RecognitionConfig.Types.AudioEncoding.Linear16,
                    SampleRateHertz = sampleRate,
                    LanguageCode = language_code,
                    EnableAutomaticPunctuation = true
                };

                var streamingRecognitionConfig = new StreamingRecognitionConfig()
                {
                    Config = config,
                    InterimResults = true
                };

                audioHubClientInfo.StreamingCall = client.StreamingRecognize();

                await audioHubClientInfo.StreamingCall.WriteAsync(new StreamingRecognizeRequest()
                {
                    StreamingConfig = streamingRecognitionConfig
                });

                // Print responses as they arrive.
                audioHubClientInfo.PrintResponses = Task.Run(async () => PrintResponsesCallback(audioHubClientInfo));
            }

            if (AppSettings.SaveAudioFiles)
            {
                // Write test wave file
                audioHubClientInfo.Writer = null;
                DateTime startTime = DateTime.Now;
                string playerIdentifier = name;

                if (MQTTService.ClientInfo != null)
                {
                    ClientInfoDTO matchingUser = MQTTService.ClientInfo.Where(ci => ci.playername == name).FirstOrDefault();

                    if (matchingUser != null && !String.IsNullOrEmpty(matchingUser.participantid))
                    {
                        // Use the Participant Id in the Wav filename if it is available
                        playerIdentifier = matchingUser.participantid;
                    }
                }

                audioHubClientInfo.AudioFilename = $"{playerIdentifier}_{MQTTService.TrialId.Split("-")[0]}_{startTime.ToString("MMddyyyy_HHmmss")}.wav";

                _logger.LogInformation($"AudioHub: Writing audio to {audioHubClientInfo.AudioFilename}");

                try
                {
                    audioHubClientInfo.Writer = new BinaryWriter(File.OpenWrite($"/app/RecordedAudio/{audioHubClientInfo.AudioFilename}"));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"AudioHub: Unable to open output file");
                }

                if (audioHubClientInfo.Writer != null)
                {
                    var header = new WaveHeader();
                    var format = new WaveFormatChunk((uint)audioHubClientInfo.SampleRate);
                    var data = new WaveDataChunk();

                    // Write the header
                    audioHubClientInfo.Writer.Write(header.sGroupID.ToCharArray());
                    audioHubClientInfo.Writer.Write(header.dwFileLength);
                    audioHubClientInfo.Writer.Write(header.sRiffType.ToCharArray());

                    // Write the format chunk
                    audioHubClientInfo.Writer.Write(format.sChunkID.ToCharArray());
                    audioHubClientInfo.Writer.Write(format.dwChunkSize);
                    audioHubClientInfo.Writer.Write(format.wFormatTag);
                    audioHubClientInfo.Writer.Write(format.wChannels);
                    audioHubClientInfo.Writer.Write(format.dwSamplesPerSec);
                    audioHubClientInfo.Writer.Write(format.dwAvgBytesPerSec);
                    audioHubClientInfo.Writer.Write(format.wBlockAlign);
                    audioHubClientInfo.Writer.Write(format.wBitsPerSample);

                    // Write the data chunk
                    audioHubClientInfo.Writer.Write(data.sChunkID.ToCharArray());
                    audioHubClientInfo.Writer.Write(data.dwChunkSize);
                }
            }

            await base.OnConnectedAsync();
        }

        private async void PrintResponsesCallback(AudioHubClientInfo audioHubClientInfo)
        {
            var responseStream = audioHubClientInfo.StreamingCall.GetResponseStream();
            try
            {
                while (await responseStream.MoveNextAsync())
                {
                    StreamingRecognizeResponse response = responseStream.Current;
                    foreach (StreamingRecognitionResult result in response.Results)
                    {
                        if (result.IsFinal && result.Alternatives.Count > 0)
                        {
                            _logger.LogInformation($"Audio Processor: {audioHubClientInfo.Name} - {result.Alternatives[0].Transcript}");

                            string playerIdentifier = audioHubClientInfo.Name;

                            if (MQTTService.ClientInfo != null)
                            {
                                ClientInfoDTO matchingUser = MQTTService.ClientInfo.Where(ci => ci.playername == audioHubClientInfo.Name).FirstOrDefault();

                                if (matchingUser != null && !String.IsNullOrEmpty(matchingUser.participantid))
                                {
                                    // Use the Participant Id in the Wav filename if it is available
                                    playerIdentifier = matchingUser.participantid;
                                }
                            }

                            // Send message on Message Bus
                            MQTTService.SendUserSpeechMessage(playerIdentifier, result.Alternatives[0].Transcript);

                            if (audioHubClientInfo.NeedRecycle)
                            {
                                RestartStream(audioHubClientInfo);
                            }
                        }
                    }
                }

            }
            catch (RpcException ex)
            {
                if (ex.StatusCode == StatusCode.OutOfRange)
                {
                    RestartStream(audioHubClientInfo);
                    return;
                }
                else {
                    throw;
                }
            }
        }

        private async void RestartStream(AudioHubClientInfo audioHubClientInfo)
        {
            // Shutdown current stream
            await audioHubClientInfo.StreamingCall.WriteCompleteAsync();
            await audioHubClientInfo.PrintResponses;

            // Recreate stream
            SpeechClient client = SpeechClient.Create();

            RecognitionConfig config = new RecognitionConfig()
            {
                AudioChannelCount = 1,
                Encoding = RecognitionConfig.Types.AudioEncoding.Linear16,
                SampleRateHertz = audioHubClientInfo.SampleRate,
                LanguageCode = language_code,
                EnableAutomaticPunctuation = true
            };

            var streamingRecognitionConfig = new StreamingRecognitionConfig()
            {
                Config = config,
                InterimResults = true
            };

            audioHubClientInfo.StreamingCall = client.StreamingRecognize();

            await audioHubClientInfo.StreamingCall.WriteAsync(new StreamingRecognizeRequest()
            {
                StreamingConfig = streamingRecognitionConfig
            });

            // Print responses as they arrive.
            audioHubClientInfo.PrintResponses = Task.Run(async () => PrintResponsesCallback(audioHubClientInfo));

            audioHubClientInfo.SpeechStreamStartTime = DateTime.Now;
            audioHubClientInfo.NeedRecycle = false;

            _logger.LogInformation($"Audio Processor: {audioHubClientInfo.Name} stream recycled");
        }

        public override async Task OnDisconnectedAsync(Exception exception)
        {
            _logger.LogInformation(Context.ConnectionId + "has disconnected from the Audio Hub");

            // Lookup the client info or create a new record
            AudioHubClientInfo audioHubClientInfo = LookupdAudioHubClientInfo(Context.ConnectionId);

            if (!AppSettings.DisableSpeechToText)
            {
                await audioHubClientInfo.StreamingCall.WriteCompleteAsync();
                await audioHubClientInfo.PrintResponses;
            }

            // Cleanup
            if (audioHubClientInfo.ExternalSocket != null)
            {
                audioHubClientInfo.ExternalSocket.Dispose();
                audioHubClientInfo.ExternalSocket = null;
            }
            AudioHubClientInfoDict.Remove(Context.ConnectionId);

            if (AppSettings.SaveAudioFiles && audioHubClientInfo.Writer != null)
            {
                audioHubClientInfo.Writer.Flush();
                audioHubClientInfo.Writer.Seek(4, SeekOrigin.Begin);
                uint filesize = (uint)audioHubClientInfo.Writer.BaseStream.Length;
                audioHubClientInfo.Writer.Write(filesize - 8);
                audioHubClientInfo.Writer.Close();

                _logger.LogInformation($"AudioHub: Finished writing audio to {audioHubClientInfo.AudioFilename}");
            }

            await base.OnDisconnectedAsync(exception);
        }

        public async Task SendAudioData(string data)
        {
            Int16[] intArray = Array.ConvertAll(data.Split(','), Int16.Parse);
            byte[] buf = new byte[intArray.Length * sizeof(Int16)];
            Buffer.BlockCopy(intArray, 0, buf, 0, buf.Length);

            // Lookup the client info or create a new record
            AudioHubClientInfo audioHubClientInfo = LookupdAudioHubClientInfo(Context.ConnectionId);

            if (!AppSettings.DisableSpeechToText && audioHubClientInfo.StreamingCall != null)
            {
                // Stream to Google Speech API
                audioHubClientInfo.StreamingCall.WriteAsync(
                new StreamingRecognizeRequest()
                {
                    AudioContent = Google.Protobuf.ByteString
                        .CopyFrom(buf)
                }).Wait();
            }

            // Determine if Stream Recycle is needed
            if (!audioHubClientInfo.NeedRecycle && (DateTime.Now - audioHubClientInfo.SpeechStreamStartTime).TotalMinutes > StreamCycleTime)
            {
                _logger.LogInformation($"Audio Processor: {audioHubClientInfo.Name} needs a recycle of the google speech detection stream");

                audioHubClientInfo.NeedRecycle = true;
            }

            // Send to external speech processors if needed
            if (!String.IsNullOrEmpty(AppSettings.ExternalSpeechProcessor))
            {
                SendAudioDataToWebSocket(audioHubClientInfo, buf);
            }

            if (AppSettings.SaveAudioFiles && audioHubClientInfo.Writer != null)
            {
                audioHubClientInfo.Writer.Write(buf);
            }
        }

        private AudioHubClientInfo LookupdAudioHubClientInfo(string connectionId)
        {
            AudioHubClientInfo audioHubClientInfo = null;
            if (AudioHubClientInfoDict.Keys.Contains(connectionId))
            {
                audioHubClientInfo = AudioHubClientInfoDict[connectionId];
            }
            else
            {
                audioHubClientInfo = new AudioHubClientInfo();
                AudioHubClientInfoDict.Add(connectionId, audioHubClientInfo);
            }

            return audioHubClientInfo;
        }

        //?id=adarsh&sampleRate=44100
        async private void SendAudioDataToWebSocket(AudioHubClientInfo audioHubClientInfo, byte[] buf)
        {
            if (audioHubClientInfo.ExternalSocket == null)
            {
                string playerIdentifier = audioHubClientInfo.Name;

                if (MQTTService.ClientInfo != null)
                {
                    ClientInfoDTO matchingUser = MQTTService.ClientInfo.Where(ci => ci.playername == audioHubClientInfo.Name).FirstOrDefault();

                    if (matchingUser != null && !String.IsNullOrEmpty(matchingUser.participantid))
                    {
                        // Use the Participant Id in the Wav filename if it is available
                        playerIdentifier = matchingUser.participantid;
                    }
                }

                string url = $"{AppSettings.ExternalSpeechProcessor}?id={playerIdentifier}&sampleRate={audioHubClientInfo.SampleRate}";

                audioHubClientInfo.ExternalSocket = new ClientWebSocket();
                audioHubClientInfo.ExternalSocket.Options.KeepAliveInterval = TimeSpan.FromSeconds(10);

                try
                {
                    _logger.LogInformation($"SendAudioDataToWebSocket: Opening Websocket connection");
                    await audioHubClientInfo.ExternalSocket.ConnectAsync(new Uri(url), CancellationToken.None);
                }
                catch (Exception)
                {
                    _logger.LogInformation($"SendAudioDataToWebSocket: Unable to open connect to: {url}");
                    return;
                } 
            }

            try
            {
                if (audioHubClientInfo.ExternalSocket != null && audioHubClientInfo.ExternalSocket.State == WebSocketState.Open)
                {
                    await Send(audioHubClientInfo.ExternalSocket, buf);
                }
            }
            catch (Exception ex)
            {
                _logger.LogInformation($"SendAudioDataToWebSocket: Unable to send audio data");
                audioHubClientInfo.ExternalSocket = null;
                return;
            }
        }

        static async Task Send(ClientWebSocket socket, byte[] data) =>
            await socket.SendAsync(data, WebSocketMessageType.Binary, true, CancellationToken.None);
    }
}
