using AsistDataIngester.Models;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;

namespace AsistDataIngester.Services
{
    public interface IMQTTService
    {
        string ExperimentId { get; set; }
        string TrialId { get; set; }
        List<ClientInfoDTO> ClientInfo { get; set; }

        void SendMessage(string message);
        void SendSurveyResponseMessage(JObject responseObj, ResponseInfo responseIno);
        void SendUserSpeechMessage(string name, string text);
    }
}