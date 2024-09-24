package metadata.app.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Msg {
	
	private String subType;
	private String source;
	private String experimentId;
	private String trialId;
	private String timestamp;
	private String version;
	private String replayId;
	private String replayParentId;
	private String replayParentType;
	
	@JsonCreator
	public Msg(
			@JsonProperty("sub_type") String subType,
			@JsonProperty("source") String source,
			@JsonProperty("experiment_id") String experimentId,
			@JsonProperty("trialId") String trialId,
			@JsonProperty("timestamp") String timestamp,
			@JsonProperty("version") String version,
			@JsonProperty("replay_id") String replayId,
			@JsonProperty("replay_parent_id") String replayParentId,
			@JsonProperty("replay_parent_type") String replayParentType
			) {
        this.subType = subType;
        this.source = source;
        this.experimentId = experimentId;
        this.trialId = trialId;
        this.timestamp = timestamp;
        this.version = version;
        this.replayId = replayId;
        this.replayParentId = replayParentId;
        this.replayParentType = replayParentType;
    }
	@JsonProperty("sub_type")
	public String getSubType() {
		return subType;
	}
	
	@JsonProperty("sub_type")
	public void setSubType(String subType) {
		this.subType = subType;
	}	
	
	@JsonProperty("source")
	public String getSource() {
		return source;
	}
	@JsonProperty("source")
	public void setSource(String source) {
		this.source = source;
	}
	
	@JsonProperty("experiment_id")
	public String getExperimentId() {
		return experimentId;
	}
	@JsonProperty("experiment_id")
	public void setExperimentId(String experimentId) {
		this.experimentId = experimentId;
	}
	
	@JsonProperty("trial_id")
	public String getTrialId() {
		return trialId;
	}
	@JsonProperty("trial_id")
	public void setTrialId(String trialId) {
		this.trialId = trialId;
	}
	
	@JsonProperty("timestamp")
	public String getTimestamp() {
		return timestamp;
	}
	@JsonProperty("timestamp")
	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}
	
	@JsonProperty("version")
	public String getVersion() {
		return version;
	}
	@JsonProperty("version")
	public void setVersion(String version) {
		this.version = version;
	}
	
	@JsonProperty("replay_id")
	public String getReplayId() {
		return replayId;
	}
	@JsonProperty("replay_id")
	public void setReplayId(String replayId) {
		this.replayId = replayId;
	}
	
	@JsonProperty("replay_parent_id")
	public String getReplayParentId() {
		return replayParentId;
	}
	@JsonProperty("replay_parent_id")
	public void setReplayParentId(String replayParentId) {
		this.replayParentId = replayParentId;
	}
	
	@JsonProperty("replay_parent_type")
	public String getReplayParentType() {
		return replayParentType;
	}
	@JsonProperty("replay_parent_type")
	public void setReplayParentType(String replayParentType) {
		this.replayParentType = replayParentType;
	}
}