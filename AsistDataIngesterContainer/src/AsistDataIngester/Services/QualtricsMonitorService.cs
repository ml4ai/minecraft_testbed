using AsistDataIngester.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AsistDataIngester.Services
{
    public class QualtricsMonitorService : IQualtricsMonitorService
    {
        private ILogger Log { get; set; }
        private IMQTTService MQTTService { get; set; }
        private Timer Timer { get; set; }
        private int RefreshTime { get; set; }
        private bool CheckingQualtrics { get; set; }
        private IConfiguration Configuration { get; }
        private AppSettings AppSettings { get; }
        private Dictionary<string, SurveyInfo> SurveyDict { get; set; }
        private static Dictionary<string, DateTime> ResponseLastUpdateDict { get; set; }
        private Dictionary<string, JArray> QuestionTextMappingDict { get; set; }

        public QualtricsMonitorService(ILoggerFactory loggerFactory, IConfiguration configuration, IMQTTService mqttService)
        {
            Log = loggerFactory.CreateLogger("QualtricsMonitorService");
            MQTTService = mqttService;
            AppSettings = new AppSettings();
            Configuration = configuration;
         
            Configuration.GetSection("App").Bind(AppSettings);
            RefreshTime = 10;
            SurveyDict = new Dictionary<string, SurveyInfo>();
            ResponseLastUpdateDict = new Dictionary<string, DateTime>();
            QuestionTextMappingDict = new Dictionary<string, JArray>();
        }

        public Task StartAsync()
        {
            Log.LogInformation("QualtricsMonitorService: Timed Background Service is starting: Refresh = " + RefreshTime + " seconds.");

            Timer = new Timer(DoWork, null, TimeSpan.Zero,
                TimeSpan.FromSeconds(RefreshTime));

            return Task.CompletedTask;
        }

        private void DoWork(object state)
        {
            if (CheckingQualtrics || MQTTService.ClientInfo == null)
            {
                return;
            }

            // Log.LogInformation("QualtricsMonitorService: Timed Background Service is working.");
            CheckingQualtrics = true;

            try
            {
                // Get the available survey ids
                HttpClient httpClient = new HttpClient();
                httpClient.DefaultRequestHeaders.Add("Accept", "application/json");
                httpClient.DefaultRequestHeaders.Add("X-API-TOKEN", AppSettings.QualtricsAPIToken);

                string url = $"https://iad1.qualtrics.com/API/v3/surveys";

                HttpResponseMessage response = httpClient.GetAsync(url).Result;

                if (response.StatusCode != HttpStatusCode.OK)
                {
                    Log.LogInformation("QualtricsMonitorService: Error code received from Qualtrics API");
                    CheckingQualtrics = false;
                    return;
                }

                string jsonString = response.Content.ReadAsStringAsync().Result;
                JObject jObject = JObject.Parse(jsonString);

                if (jObject["result"] != null && jObject["result"]["elements"] != null && jObject["result"]["elements"].Type == JTokenType.Array)
                {
                    JArray surveyArray = (JArray) jObject["result"]["elements"];

                    foreach (JObject surveyObj in surveyArray)
                    {
                        SurveyInfo survey = surveyObj.ToObject<SurveyInfo>();

                        SurveyDict[survey.Id] = survey;
                    }
                }

                // Check for new survey responses
                httpClient = new HttpClient();
                httpClient.DefaultRequestHeaders.Add("Conten-Type", "application/json");
                httpClient.DefaultRequestHeaders.Add("X-API-TOKEN", AppSettings.QualtricsAPIToken);
                HttpContent content = new StringContent("{ \"format\": \"json\"}",
                                Encoding.UTF8,
                                "application/json"); 

                foreach (string surveyId in SurveyDict.Keys)
                {
                    // Get Survey Definition
                    JArray questionTextMappingJArray = null;

                    if (QuestionTextMappingDict.Keys.Contains(surveyId))
                    {
                        questionTextMappingJArray = QuestionTextMappingDict[surveyId];
                    }
                    else
                    {
                        string surveyDefinitionUrl = $"https://iad1.qualtrics.com/API/v3/survey-definitions/{surveyId}";
                        List<QuestionSemanticText> questionTextMapping = new List<QuestionSemanticText>();

                        HttpResponseMessage surveyDefinitionResponse = httpClient.GetAsync(surveyDefinitionUrl).Result;

                        if (surveyDefinitionResponse.StatusCode != HttpStatusCode.OK)
                        {
                            Log.LogInformation("QualtricsMonitorService: Error code received fetching server definitions from Qualtrics API");
                            CheckingQualtrics = false;
                            return;
                        }

                        string surveyDefinitionJsonString = surveyDefinitionResponse.Content.ReadAsStringAsync().Result;
                        JObject surveyDefinitionJObject = JObject.Parse(surveyDefinitionJsonString);

                        if (surveyDefinitionJObject["result"] != null && surveyDefinitionJObject["result"]["Questions"] != null)
                        {
                            var q = surveyDefinitionJObject["result"]["Questions"];
                            foreach (var question in q)
                            {
                                string qId = ((JProperty)question).Name;
                                JObject value = (JObject)(((JProperty)question).Value);

                                var questionSemanticText = new QuestionSemanticText();

                                questionSemanticText.QID = ((JProperty)question).Name;
                                questionSemanticText.QuestionText = value["QuestionText"].ToString();
                                questionSemanticText.DataExportTag = value["DataExportTag"].ToString();

                                questionTextMapping.Add(questionSemanticText);
                            }
                        }

                        questionTextMappingJArray = JArray.FromObject(questionTextMapping);
                        QuestionTextMappingDict[surveyId] = questionTextMappingJArray;
                    }

                    // Get Survey Responses
                    url = $"https://iad1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses";
                    response = httpClient.PostAsync(url, content).Result;

                    if (response.StatusCode != HttpStatusCode.OK)
                    {
                        continue;
                    }

                    jsonString = response.Content.ReadAsStringAsync().Result;
                    jObject = JObject.Parse(jsonString);

                    if (jObject["result"] != null)
                    {
                        ExportInfo exportInfo = jObject["result"].ToObject<ExportInfo>();

                        // Check progress
                        httpClient = new HttpClient();
                        httpClient.DefaultRequestHeaders.Add("Accept", "application/json");
                        httpClient.DefaultRequestHeaders.Add("X-API-TOKEN", AppSettings.QualtricsAPIToken);

                        url = $"https://iad1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses/{exportInfo.ProgressId}";

                        response = httpClient.GetAsync(url).Result;

                        if (response.StatusCode != HttpStatusCode.OK)
                        {
                            continue;
                        }

                        jsonString = response.Content.ReadAsStringAsync().Result;
                        jObject = JObject.Parse(jsonString);

                        if (jObject["result"] != null)
                        {
                            ExportFileInfo exportFileInfo = jObject["result"].ToObject<ExportFileInfo>();

                            while (exportFileInfo.Status == "inProgress")
                            {
                                Thread.Sleep(2000);

                                response = httpClient.GetAsync(url).Result;

                                if (response.StatusCode != HttpStatusCode.OK)
                                {
                                    break;
                                }

                                jsonString = response.Content.ReadAsStringAsync().Result;
                                jObject = JObject.Parse(jsonString);

                                if (jObject["result"] != null)
                                {
                                    exportFileInfo = jObject["result"].ToObject<ExportFileInfo>();
                                }
                                else
                                {
                                    break;
                                }
                            }

                            if (exportFileInfo.Status != "complete")
                            {
                                continue;
                            }

                            // Download the results file
                            httpClient = new HttpClient();
                            httpClient.DefaultRequestHeaders.Add("Accept", "application/json");
                            httpClient.DefaultRequestHeaders.Add("X-API-TOKEN", AppSettings.QualtricsAPIToken);

                            url = $"https://iad1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses/{exportFileInfo.FileId}/file";

                            response = httpClient.GetAsync(url).Result;

                            if (response.StatusCode != HttpStatusCode.OK)
                            {
                                continue;
                            }

                            Stream fileStream = response.Content.ReadAsStreamAsync().Result;

                            using (var archive = new ZipArchive(fileStream))
                            {
                                var entry = archive.Entries.FirstOrDefault();

                                if (entry != null)
                                {
                                    using (var unzippedEntryStream = entry.Open())
                                    {
                                        using (var ms = new MemoryStream())
                                        {
                                            unzippedEntryStream.CopyTo(ms);
                                            var unzippedArray = ms.ToArray();
                                            jsonString = Encoding.Default.GetString(unzippedArray);

                                            // Have JSON result data
                                            jObject = JObject.Parse(jsonString);

                                            if (jObject["responses"] != null && jObject["responses"].Type == JTokenType.Array)
                                            {
                                                JArray responseArray = (JArray)jObject["responses"];

                                                foreach (JObject responseObj in responseArray)
                                                {
                                                    ResponseInfo responseInfo = responseObj["values"].ToObject<ResponseInfo>();

                                                    if (ResponseLastUpdateDict.ContainsKey(responseObj["responseId"].ToString()))
                                                    {
                                                        DateTime lastUpdate = ResponseLastUpdateDict[responseObj["responseId"].ToString()];

                                                        if (responseInfo.RecordedDate > lastUpdate)
                                                        {
                                                            ResponseLastUpdateDict[responseObj["responseId"].ToString()] = responseInfo.RecordedDate;
                                                        }
                                                        else
                                                        {
                                                            continue;
                                                        }
                                                    }
                                                    else
                                                    {
                                                        ResponseLastUpdateDict[responseObj["responseId"].ToString()] = responseInfo.RecordedDate;
                                                    }

                                                    if (responseObj["values"]["uniqueid"] != null)
                                                    {
                                                        // Add Question ID Mappings
                                                        responseObj["mappings"] = questionTextMappingJArray;

                                                        ClientInfoDTO matchingUser = MQTTService.ClientInfo.Where(ci => ci.unique_id == responseObj["values"]["uniqueid"].ToString()).FirstOrDefault();

                                                        if (matchingUser != null)
                                                        {

                                                            // Send MQTT Message
                                                            MQTTService.SendSurveyResponseMessage(responseObj, responseInfo);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Log.LogError(ex, "");
            }

            CheckingQualtrics = false;
            // Log.LogInformation("QualtricsMonitorService: Timed Background Service is finished working.");
        }

        public Task StopAsync()
        {
            Log.LogInformation("QualtricsMonitorService: Timed Background Service is stopping.");

            Timer?.Change(Timeout.Infinite, 0);

            return Task.CompletedTask;
        }

        public void Dispose()
        {
            Timer?.Dispose();
        }

        public static void ClearResponseDict()
        {
            ResponseLastUpdateDict.Clear();
        }
    }
}
