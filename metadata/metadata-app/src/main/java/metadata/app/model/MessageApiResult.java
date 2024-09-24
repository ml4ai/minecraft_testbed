package metadata.app.model;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MessageApiResult {
	private String result;
	private String message;
	private Map<String, String> data;

	@JsonCreator
	public MessageApiResult(
			@JsonProperty("result") String result,
			@JsonProperty("message") String message,
			@JsonProperty("data") Map<String, String> data
			) {
		this.result = result;
		this.message = message;
		this.data = data;
	}

	public MessageApiResult() {
		// TODO Auto-generated constructor stub
	}

	@JsonProperty("result")
	public String getResult() {
		return result;
	}
	@JsonProperty("result")
	public void setResult(String result) {
		this.result = result;
	}
	
	@JsonProperty("message")
	public String getMessage() {
		return message;
	}
	@JsonProperty("message")
	public void setMessage(String message) {
		this.message = message;
	}
	
	@JsonProperty("data")
	public Map<String, String> getData() {
		return data;
	}
	@JsonProperty("data")
	public void setData(Map<String, String> data) {
		this.data = data;
	}
	
}