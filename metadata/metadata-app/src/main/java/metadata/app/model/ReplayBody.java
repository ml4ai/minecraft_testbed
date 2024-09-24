package metadata.app.model;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import io.micronaut.http.annotation.Body;

public class ReplayBody {

	@JsonProperty("ignore_message_list")
	private List<IgnoreMessageListItem> ignoreMessageList;
	@JsonProperty("ignore_source_list")
	private List<String> ignoreSourceList;
	@JsonProperty("ignore_topic_list")
	private List<String> ignoreTopicList;
	
	public ReplayBody() {
		// TODO Auto-generated constructor stub
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