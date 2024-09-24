package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DataReplayMetadata {
	private Replay replay;
	private List<Object> parents;

	@JsonCreator
	public DataReplayMetadata(
			@JsonProperty("replay") Replay replay,
			@JsonProperty("parents") List<Object> parents
			) {
		this.replay = replay;
		this.parents = parents;
	}
	
	public DataReplayMetadata() {
		// TODO Auto-generated constructor stub
	}
	
	@JsonProperty("replay")
	public Replay getReplay() {
		return replay;
	}
	@JsonProperty("replay")
	public void setReplay(Replay replay) {
		this.replay = replay;
	}
	
	@JsonProperty("parents")
	public List<Object> getParents() {
		return parents;
	}
	@JsonProperty("parents")
	public void setParents(List<Object> parents) {
		this.parents = parents;
	}
}
