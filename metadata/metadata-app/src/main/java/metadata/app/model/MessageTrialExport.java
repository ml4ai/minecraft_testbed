package metadata.app.model;

import java.util.List;

import org.joda.time.Instant;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MessageTrialExport {
	private Header header;
	private Msg msg;
	private DataTrialExport data;

	@JsonCreator
	public MessageTrialExport(
			@JsonProperty("header") Header header,
			@JsonProperty("msg") Msg msg,
			@JsonProperty("data") DataTrialExport data
			) {
		this.header = header;
		this.msg = msg;
		this.data = data;
	}

	public MessageTrialExport() {
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
	public DataTrialExport getData() {
		return data;
	}
	@JsonProperty("data")
	public void setData(DataTrialExport data) {
		this.data = data;
	}
	
	@JsonIgnore()
	public static MessageTrialExport generate(Trial trial, String index) {
		String timestamp = Instant.now().toString();
		Header header = new Header(timestamp, "export", "1.0");
		Msg msg = new Msg("trial", "rest-api", trial.getExperiment().getExperimentId(), trial.getTrialId(), timestamp, "0.6", null, null, null);
		DataTrialExport dataTrialExport = new DataTrialExport(index, new DataTrialMetadata(new DataTrial(trial.getName(), trial.getDate(), trial.getExperimenter(), trial.getSubjects(), trial.getTrialNumber(), trial.getGroupNumber(), trial.getStudyNumber(), trial.getCondition(), trial.getNotes(), trial.getTestbedVersion(), trial.getExperiment().getName(), trial.getExperiment().getDate(), trial.getExperiment().getAuthor(), trial.getExperiment().getMission()))); 
		return new MessageTrialExport(header, msg, dataTrialExport);
	}
}