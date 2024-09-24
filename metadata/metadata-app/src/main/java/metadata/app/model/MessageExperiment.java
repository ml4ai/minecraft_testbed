package metadata.app.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MessageExperiment {
	private Header header;
	private Msg msg;
	private DataExperiment data;
	
	@JsonCreator
	public MessageExperiment( 
		@JsonProperty("header") Header header,
		@JsonProperty("msg") Msg msg,
		@JsonProperty("data") DataExperiment data
		) {
	this.header = header;
	this.msg = msg;
	this.data = data;
	}
	
	@JsonProperty("header")
	public Header getHeader() {
		return header;
	}
	@JsonProperty("header")
	public void setHeader(Header header) {
		this.header = header;
	}
	
	@JsonProperty("msg")
	public Msg getMsg() {
		return msg;
	}
	@JsonProperty("msg")
	public void setMsg(Msg msg) {
		this.msg = msg;
	}

	@JsonProperty("data")
	public DataExperiment getData() {
		return data;
	}
	@JsonProperty("data")
	public void setData(DataExperiment data) {
		this.data = data;
	}
}
