import { Trial } from '../trial/trial';
import {IgnoreListItem, Replay} from './replay';

export interface ReplayExportMessage {
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
    version: string,
    replay_id: string,
    replay_parent_id: string,
    replay_parent_type: string

  };
  data: {
    index: string,
    ignore_message_list: IgnoreListItem[],
    ignore_source_list: string[],
    ignore_topic_list: string[],
    metadata: {
      replay: Replay,
      parents: (Trial|Replay)[]
    }
  };
}
