package metadata.app.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class LogMessage {

	private String encodedString;
	
	@JsonCreator
	public LogMessage(@JsonProperty("encoded_string") String encodedString) {
        this.encodedString = encodedString;
    }
	
	@JsonProperty("encoded_string")
	public String getEncodedString() {
		return encodedString;
	}
	
	@JsonProperty("encoded_string")
	public void setEncodedString(String encodedString) {
		this.encodedString = encodedString;
	}
}
