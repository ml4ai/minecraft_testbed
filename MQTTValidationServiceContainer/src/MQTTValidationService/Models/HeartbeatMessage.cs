namespace MQTTValidationService.Models
{
    public class HeartbeatMessage
    {
        public MessageHeader header { get; set; }
        public HeartbeatMsg msg { get; set; }
        public HeartbeatMessageData data { get; set; }

        public HeartbeatMessage()
        {
            header = new MessageHeader();
            msg = new HeartbeatMsg();
            data = new HeartbeatMessageData();
        }
    }
}
