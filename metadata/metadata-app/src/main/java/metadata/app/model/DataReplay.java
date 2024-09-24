package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class DataReplay {
	private List<IgnoreMessageListItem> ignoreMessageList;
	private List<String> ignoreSourceList;
	private List<String> ignoreTopicList;

	@JsonCreator
	public DataReplay(
			@JsonProperty("ignore_message_list") List<IgnoreMessageListItem> ignoreMessageList,
			@JsonProperty("ignore_source_list") List<String> ignoreSourceList,
			@JsonProperty("ignore_topic_list") List<String> ignoreTopicList
			) {
		this.ignoreMessageList = ignoreMessageList;
		this.ignoreSourceList = ignoreSourceList;
		this.ignoreTopicList = ignoreTopicList;
	}
	
	public DataReplay() {
		// TODO Auto-generated constructor stub
	}

	@JsonProperty("ignore_message_list")
	public List<IgnoreMessageListItem> getIgnoreMessageList() {
		return ignoreMessageList;
	}
	@JsonProperty("ignore_message_list")
	public void setIgnoreMessageList(List<IgnoreMessageListItem> ignoreList) {
		this.ignoreMessageList = ignoreList;
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
