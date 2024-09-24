using MalmoControl.DTO;
using MalmoControl.Interfaces;



namespace MalmoControl
{
    public class Experiment:IExperiment
    {
       
        public string experiment_id{ get;set; } = System.Guid.Empty.ToString();

        public string trial_id{ get;set; } =  System.Guid.Empty.ToString();

        public string mission_name{ get;set; } = "Not Set";

        public MissionDTO missionDTO{ get;set; } = new MissionDTO();

        public ExperimentDTO experimentDTO{get;set;} = new ExperimentDTO();
        
        public TrialDTO trialDTO{get;set;} = new TrialDTO();

    }
}
