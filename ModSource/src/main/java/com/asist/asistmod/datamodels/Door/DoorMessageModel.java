package com.asist.asistmod.datamodels.Door;

import java.time.Clock;

public class DoorMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:Door";
	public String version = "0.5";	
	
	

}
