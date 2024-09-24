using System;
using MalmoControl.DTO;
using Newtonsoft.Json.Linq;


namespace MalmoControl.Interfaces
{
    public interface IExperiment
    {
        string experiment_id {get;set;}
        string trial_id {get;set;}
        string mission_name {get;set;}
        MissionDTO missionDTO { get;set; }

        ExperimentDTO experimentDTO {get;set;}
        TrialDTO trialDTO {get;set;}
       
    }
}
