package metadata.app.model;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ExportTrialBody {

	@JsonProperty("index")
	private String index;
	@JsonProperty("trialId")
	private String trialId;
	
	public ExportTrialBody() {
		// TODO Auto-generated constructor stub
	}
	
	@JsonProperty("index")
	public String getIndex() {
		return index;
	}
	@JsonProperty("index")
	public void setIndex(String index) {
		this.index = index;
	}
	
	@JsonProperty("trialId")
	public String getTrialId() {
		return trialId;
	}
	@JsonProperty("trialId")
	public void setTrialId(String trialId) {
		this.trialId = trialId;
	}
}