package com.asist.asistmod.datamodels.MarkerRemoved;

import java.time.Clock;

public class MarkerRemovedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:MarkerRemoved";
	public String version = "2.1";	
	
	
	
}
