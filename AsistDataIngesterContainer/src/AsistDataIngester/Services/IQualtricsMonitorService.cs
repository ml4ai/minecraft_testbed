using System.Threading.Tasks;

namespace AsistDataIngester.Services
{
    public interface IQualtricsMonitorService
    {
        Task StartAsync();
        Task StopAsync();
    }
}