package com.asist.asistmod.datamodels.RubbleDestroyed;

import java.time.Clock;

public class RubbleDestroyedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:RubbleDestroyed";
	public String version = "1.1";	
	
	
	
}
