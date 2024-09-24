using CsvHelper.Configuration;
using ValidationServices.Models;

namespace ValidationServices.Util
{
    public class MessageTopicInfoMap : ClassMap<MessageTopicInfo>
    {
        public MessageTopicInfoMap()
        {
            Map(m => m.Topic).Name("Topic", "topic");
            Map(m => m.Schema).Name("Schema", "schema");
            Map(m => m.Description).Name("Description", "description");
        }
    }
}
