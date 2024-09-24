package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DataTrialExport {
	private String index;
	private DataTrialMetadata metdata;

	@JsonCreator
	public DataTrialExport(
			@JsonProperty("index") String index,			
			@JsonProperty("metadata") DataTrialMetadata metdata
			) {
		this.index = index;		
		this.metdata = metdata;		
	}
	
	public DataTrialExport() {
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
	
	@JsonProperty("metadata")
	public DataTrialMetadata getMetadata() {
		return metdata;
	}
	@JsonProperty("metadata")
	public void setMetadata(DataTrialMetadata metdata) {
		this.metdata = metdata;
	}
}
