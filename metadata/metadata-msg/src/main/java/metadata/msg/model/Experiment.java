package metadata.msg.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Experiment {

	private long id;
	private String experimentId;
	private String name;
	private String date;
	private String author;
	private String mission;
	
	@JsonCreator
	public Experiment(@JsonProperty("id") long id, @JsonProperty("experiment_id") String experimentId, @JsonProperty("name") String name, @JsonProperty("date") String date, @JsonProperty("author") String author,  @JsonProperty("mission") String mission) {
        this.id = id;
        this.experimentId = experimentId;
        this.name = name;
        this.date = date;
        this.author = author;
        this.mission = mission;
    }
	@JsonProperty("id")
	public long getId() {
		return id;
	}
	@JsonProperty("id")
	public void setId(long id) {
		this.id = id;
	}	

	@JsonProperty("experiment_id")
	public String getExperimentId() {
		return experimentId;
	}
	@JsonProperty("experiment_id")
	public void setExperimentId(String experimentId) {
		this.experimentId = experimentId;
	}
	
	@JsonProperty("name")
	public String getName() {
		return name;
	}
	@JsonProperty("name")
	public void setName(String name) {
		this.name = name;
	}
	
	@JsonProperty("date")
	public String getDate() {
		return date;
	}
	@JsonProperty("date")
	public void setDate(String date) {
		this.date = date;
	}
	
	@JsonProperty("author")
	public String getAuthor() {
		return author;
	}
	@JsonProperty("author")
	public void setAuthor(String author) {
		this.author = author;
	}
	
	@JsonProperty("mission")
	public String getMission() {
		return mission;
	}
	@JsonProperty("mission")
	public void setMission(String mission) {
		this.mission = mission;
	}
}
