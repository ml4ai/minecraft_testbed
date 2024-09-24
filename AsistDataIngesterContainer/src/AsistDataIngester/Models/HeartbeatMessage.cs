namespace AsistDataIngester.Models
{
    public class HeartbeatMessage
    {
        public CommonHeader header { get; set; }
        public HeartbeatMsg msg { get; set; }
        public HeartbeatMessageData data { get; set; }

        public HeartbeatMessage()
        {
            header = new CommonHeader();
            msg = new HeartbeatMsg();
            data = new HeartbeatMessageData();
        }
    }
}
