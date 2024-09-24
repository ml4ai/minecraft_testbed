package com.asist.asistmod.datamodels.MarkerDestroyed;

import java.time.Clock;

public class MarkerDestroyedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:MarkerDestroyed";
	public String version = "2.0";	
	
	
	
}
