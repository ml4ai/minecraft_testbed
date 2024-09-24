package metadata.app.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class ReplayCompletedMessage {

	private String replayId;
	private ReplayCompletedReasonType reason;
	private long totalMessagesSent;
	private long totalMessageCount;
	
	@JsonCreator
	public ReplayCompletedMessage(
			@JsonProperty("replay_id") String replayId,
			@JsonProperty("reason") ReplayCompletedReasonType reason,
			@JsonProperty("total_messages_sent") long totalMessagesSent,
			@JsonProperty("total_message_count") long totalMessageCount
			) {
		this.replayId = replayId;
		this.reason = reason;
        this.totalMessagesSent = totalMessagesSent;
        this.totalMessageCount = totalMessageCount;
    }
	
	@JsonProperty("replay_id")
	public String getReplayId() {
		return replayId;
	}
	
	@JsonProperty("replay_id")
	public void setReplayId(String replayId) {
		this.replayId = replayId;
	}
	
	@JsonProperty("reason")
	public ReplayCompletedReasonType getReason() {
		return reason;
	}
	
	@JsonProperty("reason")
	public void setReason(ReplayCompletedReasonType reason) {
		this.reason = reason;
	}
	
	@JsonProperty("total_messages_sent")
	public long getTotalMessagesSent() {
		return totalMessagesSent;
	}
	
	@JsonProperty("total_messages_sent")
	public void setTotalMessagesSent(long totalMessagesSent) {
		this.totalMessagesSent = totalMessagesSent;
	}
	
	@JsonProperty("total_message_count")
	public long getTotalMessageCount() {
		return totalMessageCount;
	}
	
	@JsonProperty("total_message_count")
	public void setTotalMessageCount(long totalMessageCount) {
		this.totalMessageCount = totalMessageCount;
	}
}
