
export interface TimeWindowExportMessage {
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
    index: string,
    metadata: {
      begin_date_time: string,
      end_date_time: string
    }
  };
}
