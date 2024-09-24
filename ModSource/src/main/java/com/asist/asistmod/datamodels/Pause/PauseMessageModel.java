package com.asist.asistmod.datamodels.Pause;

import java.time.Clock;

public class PauseMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:Pause";
	public String version = "1.0";	
	
	
	
}
