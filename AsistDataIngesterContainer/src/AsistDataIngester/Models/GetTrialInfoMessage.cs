namespace AsistDataIngester.Models
{
    public class GetTrialInfoMessage
    {
        public string experiment_id { get; set; }
        public string trial_id { get; set; }
        public string mission_name { get; set; }
    }
}