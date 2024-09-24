using Google.Cloud.Speech.V1;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.WebSockets;
using System.Threading.Tasks;
using static Google.Cloud.Speech.V1.SpeechClient;

namespace AsistDataIngester.Models
{
    public class AudioHubClientInfo
    {
        public StreamingRecognizeStream StreamingCall { get; set; }
        public Task PrintResponses { get; set; }
        public string Name { get; set; }
        public int SampleRate { get; set; }
        public DateTime SpeechStreamStartTime { get; set; }
        public bool NeedRecycle { get; set; }
        public ClientWebSocket ExternalSocket { get; set; }
        public BinaryWriter Writer { get; set; }
        public string AudioFilename { get; set; }

        public AudioHubClientInfo()
        {
            SpeechStreamStartTime = DateTime.Now;
            NeedRecycle = false;
        }
    }
}
