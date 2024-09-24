package com.asist.asistmod.datamodels.GroundTruth.VictimsExpired;

import java.time.Clock;

public class VictimsExpiredMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:VictimsExpired";
	public String version = "0.5";	
	
	
	
}
