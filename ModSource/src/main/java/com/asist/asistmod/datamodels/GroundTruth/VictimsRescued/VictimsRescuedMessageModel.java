package com.asist.asistmod.datamodels.GroundTruth.VictimsRescued;

import java.time.Clock;

public class VictimsRescuedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:VictimsRescued";
	public String version = "0.5";	
	
	
	
}
