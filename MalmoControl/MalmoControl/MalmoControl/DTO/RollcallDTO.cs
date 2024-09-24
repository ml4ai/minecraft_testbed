using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MalmoControl.DTO
{
    public class RollcallDTO
    {
        public CommonHeaderDTO header = new CommonHeaderDTO();
        public RollcallMessageDTO msg = new RollcallMessageDTO();
        public RollcallDataDTO data = new RollcallDataDTO();

        public JObject convertToJObject()
        {

            JObject obj = new JObject()
            {

                ["header"] = new JObject()
                {

                    ["timestamp"] = header.timestamp,
                    ["message_type"] = header.message_type,
                    ["version"] = header.version
                },
                ["msg"] = new JObject()
                {
                    ["experiment_id"] = msg.experiment_id,
                    ["trial_id"] = msg.trial_id,
                    ["timestamp"] = msg.timestamp,
                    ["source"] = msg.source,
                    ["sub_type"] = msg.sub_type,
                    ["version"] = msg.version,
                },
                ["data"] = new JObject()
                {

                    ["rollcall_id"] = data.rollcall_id
                }
            };

            return obj;
        }
    }

    public class RollcallMessageDTO
    {
        public string experiment_id = Guid.Empty.ToString();
        public string trial_id = Guid.Empty.ToString();
        public string timestamp = "NOT SET";
        public string source = "NOT SET";
        public string sub_type = "NOT SET";
        public string version = "NOT SET";
    }

    public class RollcallDataDTO
    {
        public string rollcall_id = "NOT SET";
    }
}
