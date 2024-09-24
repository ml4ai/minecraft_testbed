using Newtonsoft.Json.Linq;
using System.Linq;
using System.Threading.Tasks;

namespace AsistDataIngester.Models
{
    public class UserSpeechMessage
    {
        public CommonHeader header { get; set; }
        public CommonMsg msg { get; set; }
        public JObject data { get; set; }

        public UserSpeechMessage()
        {
            header = new CommonHeader();
            msg = new CommonMsg();
        }
    }
}
