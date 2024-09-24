using System.Linq;
using System.Threading.Tasks;

namespace MQTTValidationService.Models
{
    public class ErrorMessage
    {
        public MessageHeader header { get; set; }
        public ErrorMessageData msg { get; set; }

        public ErrorMessage()
        {
            header = new MessageHeader();
            msg = new ErrorMessageData();
        }
    }
}
