package metadata.msg.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Trial {
	private long id;
	private String trialId;
	private String name;
	private String date;
	private Experiment experiment;
	private List<String> subjects;
	private String trialNumber;
	private String groupNumber;
	private String studyNumber;
	private String condition;
	private List<String> notes;
	private String testbedVersion;
	private String experimenter;

	@JsonCreator
	public Trial(
			@JsonProperty("id") int id,
			@JsonProperty("trial_id") String trialId,
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
			@JsonProperty("experiment") Experiment experiment
			) {
		this.id = id;
		this.trialId = trialId;
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
		this.experiment = experiment;
	}

	@JsonProperty("id")
	public long getId() {
		return id;
	}
	@JsonProperty("id")
	public void setId(long id) {
		this.id = id;
	}

	@JsonProperty("trial_id")
	public String getTrialId() {
		return trialId;
	}
	@JsonProperty("trial_id")
	public void setTrialId(String trialId) {
		this.trialId = trialId;
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
	
	@JsonProperty("experiment")
	public Experiment getExperiment() {
		return experiment;
	}
	@JsonProperty("experiment")
	public void setExperiment(Experiment experiment) {
		this.experiment = experiment;
	}
}
