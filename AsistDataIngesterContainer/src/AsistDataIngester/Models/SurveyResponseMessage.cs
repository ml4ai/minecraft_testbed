using Newtonsoft.Json.Linq;
using System.Linq;
using System.Threading.Tasks;

namespace AsistDataIngester.Models
{
    public class SurveyResponseMessage
    {
        public CommonHeader header { get; set; }
        public CommonMsg msg { get; set; }
        public JObject data { get; set; }

        public SurveyResponseMessage()
        {
            header = new CommonHeader();
            msg = new CommonMsg();
        }
    }
}
