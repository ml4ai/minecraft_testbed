package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DataReplayExport {
	private String index;
	private DataReplayMetadata metdata;

	@JsonCreator
	public DataReplayExport(
			@JsonProperty("index") String index,
			@JsonProperty("metadata") DataReplayMetadata metdata
			) {
		this.index = index;
		this.metdata = metdata;		
	}
	
	public DataReplayExport() {
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
	public DataReplayMetadata getMetadata() {
		return metdata;
	}
	@JsonProperty("metadata")
	public void setMetadata(DataReplayMetadata metdata) {
		this.metdata = metdata;
	}
}
