package metadata.app.model;

import java.util.List;

import org.joda.time.Instant;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MessageReplayExport {
	private Header header;
	private Msg msg;
	private DataReplayExport data;

	@JsonCreator
	public MessageReplayExport(
			@JsonProperty("header") Header header,
			@JsonProperty("msg") Msg msg,
			@JsonProperty("data") DataReplayExport data
			) {
		this.header = header;
		this.msg = msg;
		this.data = data;
	}

	public MessageReplayExport() {
		// TODO Auto-generated constructor stub
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
	public DataReplayExport getData() {
		return data;
	}
	@JsonProperty("data")
	public void setData(DataReplayExport data) {
		this.data = data;
	}
	
	@JsonIgnore()
	public static MessageReplayExport generate(List<Object> parents, Trial root, Replay replay, String index) {
		String timestamp = Instant.now().toString();
		Header header = new Header(timestamp, "export", "1.0");
		Msg msg = new Msg("replay", "rest-api", root.getExperiment().getExperimentId(), root.getTrialId(), timestamp, "0.6", replay.getReplayId(), replay.getReplayParentId(), replay.getReplayParentType());
		DataReplayExport dataReplayExport = new DataReplayExport(index, new DataReplayMetadata(replay, parents)); 
		return new MessageReplayExport(header, msg, dataReplayExport);
	}
}