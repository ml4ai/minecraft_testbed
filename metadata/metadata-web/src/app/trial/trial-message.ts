export interface TrialMessage {
  header: {
    timestamp: string,
    message_type: string,
    version: string
  };
  msg: {
    sub_type: string,
    source: string,
    experiment_id: string
    trial_id: string,
    timestamp: string,
    version: string

  };
  data: {
    name: string,
    date: string,
    experimenter: string,
    subjects: string[],
    trial_number: string,
    group_number: string,
    study_number: string,
    condition: string,
    notes: string[],
    testbed_version: string,
    experiment_name: string,
    experiment_date: string,
    experiment_author: string,
    experiment_mission: string
  };
}
