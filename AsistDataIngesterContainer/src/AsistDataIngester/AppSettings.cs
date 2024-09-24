using System;
using System.Collections.Generic;

namespace AsistDataIngester
{
    public class AppSettings
    {
        public String QualtricsAPIToken { get; set; }
        public bool DisableSpeechToText { get; set; }
        public String ExternalSpeechProcessor { get; set; }
        public bool SaveAudioFiles { get; set; }
    }
}
