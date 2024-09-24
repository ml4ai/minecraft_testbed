package metadata.msg.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class DataExperiment {
	private String name;
	private String date;
	private String author;
	private String mission;


	@JsonCreator
	public DataExperiment(
			@JsonProperty("name") String name,
			@JsonProperty("date") String date,
			@JsonProperty("author") String author,
			@JsonProperty("mission") String mission
			) {
		this.name = name;
		this.date = date;
		this.author = author;
		this.mission = mission;
	}
	
	public DataExperiment() {
		// TODO Auto-generated constructor stub
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
	public void setMssion(String mission) {
		this.mission = mission;
	}
}
