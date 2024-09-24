package metadata.msg.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Msg {
	
	private String subType;
	private String source;
	private String experimentId;
	private String trialId;
	private String timestamp;
	private String version;
	private String replayRootId;
	private String replayId;
	
	@JsonCreator
	public Msg(
			@JsonProperty("sub_type") String subType,
			@JsonProperty("source") String source,
			@JsonProperty("experiment_id") String experimentId,
			@JsonProperty("trialId") String trialId,
			@JsonProperty("timestamp") String timestamp,
			@JsonProperty("version") String version,
			@JsonProperty("replay_root_id") String replayRootId,
			@JsonProperty("replay_id") String replayId
			) {
        this.subType = subType;
        this.source = source;
        this.experimentId = experimentId;
        this.trialId = trialId;
        this.timestamp = timestamp;
        this.version = version;
        this.replayRootId = replayRootId;
        this.replayId = replayId;
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
	
	@JsonProperty("replay_root_id")
	public String getReplayRootId() {
		return replayRootId;
	}
	@JsonProperty("replay_root_id")
	public void setReplayRootId(String replayRootId) {
		this.replayRootId = replayRootId;
	}
	
	@JsonProperty("replay_id")
	public String getReplayId() {
		return replayId;
	}
	@JsonProperty("replay_id")
	public void setReplayId(String replayId) {
		this.replayId = replayId;
	}
}


//| msg.sub_type | string | The subtype of the data.  This field describes the format of this particular type of data
//| msg.source | string | The name of the testbed component that published this data
//| msg.experiment_id | string | The experiment id this message is associated with
//| msg.trial_id | string | The trial id this message is associated with
//| msg.timestamp | string | Timestamp of when the data was generated in ISO 8601 format: YYYY-MM-DDThh:mm:ss.ssssZ
//| msg.version | string | The version of the sub_type format
//| msg.replay_root_id | string | The replay_root_id if being used for the root of a replay.
//| msg.replay_id | string | The replay_id if being used for a replay.