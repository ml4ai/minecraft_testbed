export interface ReplayCompletedMessage {
  replay_id: string;
  reason: string;
  total_messages_sent: number;
  total_message_count: number;
}
