package com.asist.asistmod.datamodels.GroundTruth.ThreatSignList;

import java.time.Clock;

public class ThreatSignListMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Mission:ThreatSignList";
	public String version = "0.1";	

}
