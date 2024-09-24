using NJsonSchema;
using System.Collections.Generic;

namespace ValidationServices.Services
{
    public interface IValidator
    {
        List<string> ValidateMessage(string topic, string message);
        JsonSchema LookupSchemaByMessageType(string message, out string messageType, out string subType);
    }
}