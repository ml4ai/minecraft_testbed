export interface ExperimentMessage {
  header: {
    timestamp: string,
    message_type: string,
    version: string
  };
  msg: {
    sub_type: string,
    source: string,
    experiment_id: string,
    timestamp: string,
    version: string
  };
  data: {
    name: string,
    date: string,
    author: string,
    mission: string
  };
}
