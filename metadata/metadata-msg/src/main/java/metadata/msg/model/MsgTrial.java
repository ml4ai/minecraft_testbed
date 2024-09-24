package metadata.msg.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MsgTrial {
	private Header header;
	private Msg msg;
	private DataTrial data;

	@JsonCreator
	public MsgTrial(
			@JsonProperty("header") Header header,
			@JsonProperty("msg") Msg msg,
			@JsonProperty("data") DataTrial data
			) {
		this.header = header;
		this.msg = msg;
		this.data = data;
	}

	public MsgTrial() {
		// TODO Auto-generated constructor stub
	}

	@JsonProperty("header")
	public Header getHeader() {
		return header;
	}
	@JsonProperty("header")
	public void setId(Header header) {
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
	public DataTrial getData() {
		return data;
	}
	@JsonProperty("data")
	public void setData(DataTrial data) {
		this.data = data;
	}
}