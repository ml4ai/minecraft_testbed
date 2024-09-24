package com.asist.asistmod.datamodels.Woof;

import java.time.Clock;

public class WoofMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:Woof";
	public String version = "0.5";	
	
	

}
