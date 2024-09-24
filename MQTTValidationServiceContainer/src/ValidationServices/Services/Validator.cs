using CsvHelper;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using NJsonSchema;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;
using ValidationServices.Models;
using ValidationServices.Util;

namespace ValidationServices.Services
{
    public class Validator : IValidator
    {
        private ILogger Log { get; set; }
        private IConfiguration Config { get; set; }
        private Dictionary<string, JsonSchema> TopicToSchemaMap { get; set; }
        private Dictionary<string, JsonSchema> MessageTypeToSchemaMap { get; set; }

        public Validator(ILoggerFactory loggerFactory, IConfiguration config)
        {
            Log = loggerFactory.CreateLogger<Validator>();
            Config = config;
            TopicToSchemaMap = new Dictionary<string, JsonSchema>();
            MessageTypeToSchemaMap = new Dictionary<string, JsonSchema>();

            try
            {
                // parse the message_topics csv file
                string rootDirectory = Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);
                using (var streamReader = System.IO.File.OpenText(Path.Combine(rootDirectory, "MessageSpecs", "message_topics.csv")))
                {
                    try
                    {
                        using (var csv = new CsvReader(streamReader))
                        {
                            csv.Configuration.RegisterClassMap<MessageTopicInfoMap>();
                            csv.Configuration.BadDataFound = null;
                            var records = csv.GetRecords<MessageTopicInfo>();
                            foreach (var messageTopicInfo in records)
                            {
                                Log.LogWarning($"Loading Topic: {messageTopicInfo.Topic}");

                                string partialPath = messageTopicInfo.Schema.Replace('/', Path.DirectorySeparatorChar);
                                string schemaPath = Path.Combine(rootDirectory, "MessageSpecs", partialPath);
                                JsonSchema parsedSchema = JsonSchema.FromFileAsync(schemaPath).Result;

                                DetermineMessageType(messageTopicInfo, parsedSchema);
                                TopicToSchemaMap.Add(messageTopicInfo.Topic, parsedSchema);

                                if (!String.IsNullOrEmpty(messageTopicInfo.MessageType) && messageTopicInfo.SubTypes != null && messageTopicInfo.SubTypes.Count > 0)
                                {
                                    foreach (var subType in messageTopicInfo.SubTypes)
                                    {
                                        string keyName = messageTopicInfo.MessageType + "_" + subType;

                                        if (!MessageTypeToSchemaMap.ContainsKey(keyName))
                                        {
                                            MessageTypeToSchemaMap.Add(keyName, parsedSchema);
                                        }
                                        else
                                        {
                                            Log.LogWarning($"Duplicate Message Type: Key = {keyName}    MessageType = {messageTopicInfo.MessageType}    SubType = {subType}    SchemaFile = {partialPath}");
                                        }
                                    }
                                }
                            }
                        }

                        Log.LogWarning($"Validator Schemas for all topics loaded successfully");
                    }
                    catch (Exception ex)
                    {
                        Log.LogError(ex.Message);
                        return;
                    }
                }
            }
            catch (System.Exception ex)
            {
                Log.LogError(ex, null);
            }
        }

        public List<string> ValidateMessage(string topic, string message)
        {
            List<string> errors = new List<string>();
            string messageType = null;
            string subType = null;

            try
            {
                JsonReader reader = new JsonTextReader(new StringReader(message));
                reader.DateParseHandling = DateParseHandling.None;
                JObject json = JObject.Load(reader);
                JsonSchema validationSchema = null;

                if (!String.IsNullOrEmpty(topic))
                {
                    if (TopicToSchemaMap.ContainsKey(topic))
                    {
                        // Simple match
                        validationSchema = TopicToSchemaMap[topic];
                    }
                    else
                    {
                        // Need to do a regex match
                        foreach (string topicToMatch in TopicToSchemaMap.Keys)
                        {
                            if (topicToMatch.Contains("+"))
                            {
                                string regexStr = topicToMatch.Replace("+", "[^/]+");
                                Regex regex = new Regex(regexStr);
                                Match match = regex.Match(topic);

                                if (match.Success)
                                {
                                    validationSchema = TopicToSchemaMap[topicToMatch];
                                    break;
                                }
                            }
                        }
                    }
                }

                // Try matching message type and sub-type
                if (validationSchema == null)
                {
                    validationSchema = LookupSchemaByMessageType(message, out messageType, out subType);
                }

                if (validationSchema == null)
                {
                    if (!String.IsNullOrEmpty(topic))
                    {
                        errors.Add($"Unknown Topic: {topic}");
                        return errors;
                    }
                    else if (!String.IsNullOrEmpty(messageType) && !String.IsNullOrEmpty(subType))
                    {
                        errors.Add($"Unknown messageType: {messageType}    subType: {subType}");
                        return errors;
                    }
                    else
                    {
                        errors.Add($"Malformed Message Header");
                        return errors;
                    }
                }

                errors = validationSchema.Validate(json).Select(r => r.ToString()).ToList();                   
                
            }
            catch (System.Exception ex)
            {

                errors.Add("Error parsing JSON input: " + ex.Message);
            }

            return errors;
        }

        public JsonSchema LookupSchemaByMessageType(string message, out string messageType, out string subType)
        {
            messageType = null;
            subType = null;

            try
            {
                JsonReader reader = new JsonTextReader(new StringReader(message));
                reader.DateParseHandling = DateParseHandling.None;
                JObject json = JObject.Load(reader);

                messageType = json["header"]["message_type"].Value<string>();
                subType = json["msg"]["sub_type"].Value<string>();

                return MessageTypeToSchemaMap[messageType + "_" + subType];
            }
            catch (Exception)
            {
                return null;
            }
        }

        private void DetermineMessageType(MessageTopicInfo messageTopicInfo, JsonSchema parsedSchema)
        {
            try
            {
                JsonSchemaProperty property = parsedSchema.Properties["header"].Properties["message_type"];
                messageTopicInfo.MessageType = property.ExtensionData["const"].ToString();

                property = parsedSchema.Properties["msg"].Properties["sub_type"];

                messageTopicInfo.SubTypes = new List<string>();
                if (property.IsEnumeration)
                {
                    foreach (var value in property.Enumeration)
                    {
                        messageTopicInfo.SubTypes.Add(value.ToString());
                    }
                }
                else {
                    messageTopicInfo.SubTypes.Add(property.ExtensionData["const"].ToString());
                }
            }
            catch (Exception ex)
            {
                return;
            }
        }
    }
}
