import { Version } from "@angular/core";

export interface ArrayDTO {
    data: string[];
}

export interface StringDTO {
   data: string;
}

export interface OpenExternalPortDTO {
  internalPort: string;
  instanceNumber: string;
  externalPort: string;
  dockerNetwork: string;
}

export interface MissionDTO {
  MissionName: string;
  MapName: string;
  MapBlockFilename: string;
  MapInfoFilename: string;
  ObserverInfo: ObserverInfoDTO[];
}

export interface InterventionAgentsDTO {
  AgentName: string;
}

export interface TrialDTO {
  header?: HeaderDTO;
  msg?: TrialMessageDTO;
  data: TrialDataDTO;
}

export interface TrialMessageDTO {

  sub_type?: string;
  experiment_id: string;
  trial_id?: string;
  source?: string;
  version?: string;
  timestamp?: string;
  replay_root_id?: string;
  replay_id?: string;

}

export interface TrialDataDTO {
 // "name", "date", "experimenter", "subjects", "testbed_version", "experiment_name", "experiment_date", "experiment_author", "experiment_mission"
 
 date?: string;
 name: string;
 experimenter: string;
 subjects: string[];
 trial_number: string;
 group_number: string;
 study_number: string;
 condition: string;
 notes: string[];
 testbed_version?: string;
 experiment_name: string;
 experiment_date?: string;
 experiment_author: string;
 experiment_mission: string;
 map_name: string;
 map_block_filename: string; 
 client_info: ClientInfoDTO[];
 intervention_agents: string[];
}

export interface ClientInfoDTO {
  playername: string;
  callsign?: string;
  participant_id?: string;
  staticmapversion?: string;
  markerblocklegend?: string;
  unique_id?: string;
}

export interface ObserverInfoDTO {
  playername: string;
}

export interface HeaderDTO {
  timestamp: string;
  message_type: string;
  version: string;
}

export interface FetchedExperimentDTO{
  experiment_id: string;
  name: string;
  author: string;
  mission: string;
}

export interface ExperimentDTO {
  header?: HeaderDTO;
  msg?: ExperimentMessageDTO ;
  data: ExperimentDataDTO;
}

export interface ExperimentMessageDTO {

    sub_type: string;
    source: string;
    experiment_id: string;
    timestamp?: string;
    version: string;
    replay_root_id?: string;
    replay_id?: string;
}

export interface ExperimentDataDTO {

  date?: string;
  name: string;
  author: string;
  mission: string;

}

export interface CurrentTrialInfo {
  experiment_id: string;
  trial_id: string;
  mission_name: string;
}

export interface AgentControlDTO {

  header: HeaderDTO;
  msg: AgentMessageDTO;

}

export interface AgentMessageDTO {

  trial_id: string;
  command: string;
  experiment_name: string;

}

export interface RoleTextDTO {
  mission_name: string;
  medic_text: string;
  transport_text: string;
  engineer_text: string;
}

export interface CommonHeaderModel{
  timestamp?:string;
  message_type?:string;
  version?:string;
}
export interface CommonMessageModel{
  experiment_id?:string;
  trial_id?:string;
  timestamp?:string;
  source?:string;
  sub_type?:string;
  version?:string;
  replay_parent_type?:string;
  replay_parent_id?:string;
  replay_id?:string 
}
export interface AgentControlDataModel{
  agent_identifier:string;
  command:string;
  
}

