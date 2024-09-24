package metadata.app.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DataTrial {
	private String name;
	private String date;
	private String experimenter;
	private List<String> subjects;
	private String trialNumber;
	private String groupNumber;
	private String studyNumber;
	private String condition;
	private List<String> notes;
	private String testbedVersion;
	private String experimentName;
	private String experimentDate;
	private String experimentAuthor;
	private String experimentMission;

	@JsonCreator
	public DataTrial(
			@JsonProperty("name") String name,
			@JsonProperty("date") String date,
			@JsonProperty("experimenter") String experimenter,
			@JsonProperty("subjects") List<String> subjects,
			@JsonProperty("trial_number") String trialNumber,
			@JsonProperty("group_number") String groupNumber,
			@JsonProperty("study_number") String studyNumber,
			@JsonProperty("condition") String condition,
			@JsonProperty("notes") List<String> notes,
			@JsonProperty("testbed_version") String testbedVersion,
			@JsonProperty("experiment_name") String experimentName,
			@JsonProperty("experiment_date") String experimentDate,
			@JsonProperty("experiment_author") String experimentAuthor,
			@JsonProperty("experiment_mission") String experimentMission
			) {
		this.name = name;
		this.date = date;
		this.experimenter = experimenter;
		this.subjects = subjects == null ? new ArrayList<String>() : subjects;
		this.trialNumber = trialNumber;
		this.groupNumber = groupNumber;
		this.studyNumber = studyNumber;
		this.condition = condition;
		this.notes = notes == null ? new ArrayList<String>() : notes;
		this.testbedVersion = testbedVersion;
		this.experimentName = experimentName;
		this.experimentDate = experimentDate;
		this.experimentAuthor = experimentAuthor;
		this.experimentMission = experimentMission;
	}
	
	public DataTrial() {
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

	@JsonProperty("experimenter")
	public String getExperimenter() {
		return experimenter;
	}
	@JsonProperty("experimenter")
	public void setExperimenter(String experimenter) {
		this.experimenter = experimenter;
	}

	@JsonProperty("subjects")
	public List<String> getSubjects() {
		return subjects == null ? new ArrayList<String>() : subjects;
	}
	@JsonProperty("subjects")
	public void setSubjects(List<String> subjects) {
		this.subjects = subjects == null ? new ArrayList<String>() : subjects;
	}
	
	@JsonProperty("trial_number")
	public String getTrialNumber() {
		return trialNumber;
	}
	@JsonProperty("trial_number")
	public void setTrialNumber(String trialNumber) {
		this.trialNumber = trialNumber;
	}
	
	@JsonProperty("group_number")
	public String getGroupNumber() {
		return groupNumber;
	}
	@JsonProperty("group_number")
	public void setGroupNumber(String groupNumber) {
		this.groupNumber = groupNumber;
	}
	
	@JsonProperty("study_number")
	public String getStudyNumber() {
		return studyNumber;
	}
	@JsonProperty("study_number")
	public void setStudyNumber(String studyNumber) {
		this.studyNumber = studyNumber;
	}
	
	@JsonProperty("condition")
	public String getCondition() {
		return condition;
	}
	@JsonProperty("condition")
	public void setCondition(String condition) {
		this.condition = condition;
	}
	
	@JsonProperty("notes")
	public List<String> getNotes() {
		return notes == null ? new ArrayList<String>() : notes;
	}
	@JsonProperty("notes")
	public void setNotes(List<String> notes) {
		this.notes = notes == null ? new ArrayList<String>() : notes;
	}

	@JsonProperty("testbed_version")
	public String getTestbedVersion() {
		return testbedVersion;
	}
	@JsonProperty("testbed_version")
	public void setTestbedVersion(String testbedVersion) {
		this.testbedVersion = testbedVersion;
	}
	
	@JsonProperty("experiment_name")
	public String getExperimentName() {
		return experimentName;
	}
	@JsonProperty("experiment_name")
	public void setExperimentName(String experimentName) {
		this.experimentName = experimentName;
	}
	
	@JsonProperty("experiment_date")
	public String getExperimentDate() {
		return experimentDate;
	}
	@JsonProperty("experiment_date")
	public void setExperimentDate(String experimentDate) {
		this.experimentDate = experimentDate;
	}
	
	@JsonProperty("experiment_author")
	public String getExperimentAuthor() {
		return experimentAuthor;
	}
	@JsonProperty("experiment_author")
	public void setExperimentAuthor(String experimentAuthor) {
		this.experimentAuthor = experimentAuthor;
	}
	
	@JsonProperty("experiment_mission")
	public String getExperimentMission() {
		return experimentMission;
	}
	@JsonProperty("experiment_mission")
	public void setExperimentMission(String experimentMission) {
		this.experimentMission = experimentMission;
	}
}
