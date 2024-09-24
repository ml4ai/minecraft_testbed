package com.asist.asistmod.datamodels.GroundTruth.VictimList;

import java.time.Clock;

public class VictimListMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Mission:VictimList";
	public String version = "0.6";	
	
	
	
}
