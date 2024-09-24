package com.asist.asistmod.datamodels.Triage;

import java.time.Clock;

public class TriageMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:Triage";
	public String version = "2.0";	
	
	
	
}
