import {IgnoreListItem} from './ignore-list-item';

export interface ReplayMessage {
  header: {
    timestamp: string,
    message_type: string,
    version: string
  };
  msg: {
    sub_type: string,
    source: string,
    experiment_id: string,
    trial_id: string,
    timestamp: string,
    version: string,
    replay_id: string,
    replay_parent_id: string;
    replay_parent_type: string,
  };
  data: {
    ignore_message_list: IgnoreListItem[],
    ignore_source_list: string[],
    ignore_topic_list: string[]
  };
}
