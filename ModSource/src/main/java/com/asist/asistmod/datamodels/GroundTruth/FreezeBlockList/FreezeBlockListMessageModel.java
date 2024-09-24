package com.asist.asistmod.datamodels.GroundTruth.FreezeBlockList;

import java.time.Clock;

public class FreezeBlockListMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Mission:FreezeBlockList";
	public String version = "0.1";	

}
