package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Replay {

	private long id;
	private String replayId;
	private String replayParentId;
	private String replayParentType;
	private String date;
	private List<IgnoreMessageListItem> ignoreMessageList;
	private List<String> ignoreSourceList;
	private List<String> ignoreTopicList;
	
	@JsonCreator
	public Replay(
			@JsonProperty("id") long id,
			@JsonProperty("replay_id") String replayId,
			@JsonProperty("replay_parent_id") String replayParentId,
			@JsonProperty("replay_parent_type") String replayParentType,
			@JsonProperty("date") String date,
			@JsonProperty("ignore_message_list") List<IgnoreMessageListItem> ignoreMessageList,
			@JsonProperty("ignore_source_list") List<String> ignoreSourceList,
			@JsonProperty("ignore_topic_list") List<String> ignoreTopicList
			) {
        this.id = id;
        this.replayId = replayId;
        this.replayParentId = replayParentId;
        this.replayParentType = replayParentType;
        this.date = date;
        this.ignoreMessageList = ignoreMessageList;
        this.ignoreSourceList = ignoreSourceList;
        this.ignoreTopicList = ignoreTopicList;
    }
	@JsonProperty("id")
	public long getId() {
		return id;
	}
	@JsonProperty("id")
	public void setId(long id) {
		this.id = id;
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
	public void setReplayParentId(String replayParent) {
		this.replayParentId = replayParent;
	}
	
	@JsonProperty("replay_parent_type")
	public String getReplayParentType() {
		return replayParentType;
	}
	@JsonProperty("replay_parent_type")
	public void setReplayParentType(String replayParentType) {
		this.replayParentType = replayParentType;
	}
	
	@JsonProperty("date")
	public String getDate() {
		return date;
	}
	@JsonProperty("date")
	public void setDate(String date) {
		this.date = date;
	}
	
	@JsonProperty("ignore_message_list")
	public List<IgnoreMessageListItem> getIgnoreMessageList() {
		return ignoreMessageList;
	}
	@JsonProperty("ignore_message_list")
	public void setIgnoreMessageList(List<IgnoreMessageListItem> ignoreMessageList) {
		this.ignoreMessageList = ignoreMessageList;
	}
	
	@JsonProperty("ignore_source_list")
	public List<String> getIgnoreSourceList() {
		return ignoreSourceList;
	}
	@JsonProperty("ignore_source_list")
	public void setIgnoreSourceList(List<String> ignoreSourceList) {
		this.ignoreSourceList = ignoreSourceList;
	}
	
	@JsonProperty("ignore_topic_list")
	public List<String> getIgnoreTopicList() {
		return ignoreTopicList;
	}
	@JsonProperty("ignore_topic_list")
	public void setIgnoreTopicList(List<String> ignoreTopicList) {
		this.ignoreTopicList = ignoreTopicList;
	}

}
