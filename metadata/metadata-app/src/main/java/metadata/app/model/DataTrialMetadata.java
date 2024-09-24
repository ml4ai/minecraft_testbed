package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DataTrialMetadata {
	private DataTrial trial;

	@JsonCreator
	public DataTrialMetadata(
			@JsonProperty("trial") DataTrial trial
			) {
		this.trial = trial;
	}
	
	public DataTrialMetadata() {
		// TODO Auto-generated constructor stub
	}
	
	@JsonProperty("trial")
	public DataTrial getTrial() {
		return trial;
	}
	@JsonProperty("trial")
	public void setTrial(DataTrial trial) {
		this.trial = trial;
	}
}
