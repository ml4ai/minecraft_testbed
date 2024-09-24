namespace MQTTValidationService.Services
{
    public interface IMQTTService
    {
        void SendMessage(string message);
    }
}