export interface Replay {
  id: number;
  replay_id: string;
  replay_parent_id: string;
  replay_parent_type: string;
  date: string;
  ignore_message_list: any[];
  ignore_source_list: any[];
  ignore_topic_list: any[];
}

export interface IgnoreListItem {
  message_type: string;
  sub_type: string;
}
