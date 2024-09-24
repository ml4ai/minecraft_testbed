package metadata.app.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class ReplayMessageCountMessage {

	private String replayId;
	private long currentMessageCount;
	private long totalMessageCount;
	
	@JsonCreator
	public ReplayMessageCountMessage(
			@JsonProperty("replay_id") String replayId,
			@JsonProperty("current_message_count") long currentMessageCount,
			@JsonProperty("total_message_count") long totalMessageCount
			) {
		this.replayId = replayId;
        this.currentMessageCount = currentMessageCount;
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
	
	@JsonProperty("current_message_count")
	public long getCurrentMessageCount() {
		return currentMessageCount;
	}
	
	@JsonProperty("current_message_count")
	public void setCurrentMessageCount(long currentMessageCount) {
		this.currentMessageCount = currentMessageCount;
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
