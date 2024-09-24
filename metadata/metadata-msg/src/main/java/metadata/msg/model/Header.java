package metadata.msg.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Header {
	
	private String timestamp;
	private String messageType;
	private String version;
	
	@JsonCreator
	public Header(@JsonProperty("timestamp") String timestamp, @JsonProperty("message_type") String messageType, @JsonProperty("version") String version) {
        this.timestamp = timestamp;
        this.messageType = messageType;
        this.version = version;
    }
	@JsonProperty("timestamp")
	public String getTimestamp() {
		return timestamp;
	}
	@JsonProperty("timestamp")
	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}
	
	
	@JsonProperty("messageType")
	public String getMessageType() {
		return messageType;
	}
	@JsonProperty("messageType")
	public void setMessageType(String messageType) {
		this.messageType = messageType;
	}
	
	@JsonProperty("version")
	public String getVersion() {
		return version;
	}
	@JsonProperty("version")
	public void setVersion(String version) {
		this.version = version;
	}
}
