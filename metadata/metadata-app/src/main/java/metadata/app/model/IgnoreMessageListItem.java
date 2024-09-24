package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class IgnoreMessageListItem {

	private String messageType;
	private String subType;
	
	@JsonCreator
	public IgnoreMessageListItem(
			@JsonProperty("message_type") String messageType,
			@JsonProperty("sub_type") String subType
			) {
        this.messageType = messageType;
        this.subType = subType;
    }

	@JsonProperty("message_type")
	public String getMessageType() {
		return messageType;
	}
	@JsonProperty("message_type")
	public void setMessageType(String messageType) {
		this.messageType = messageType;
	}
	
	@JsonProperty("sub_type")
	public String getSubType() {
		return subType;
	}
	@JsonProperty("sub_type")
	public void setSubType(String subType) {
		this.subType = subType;
	}

}
