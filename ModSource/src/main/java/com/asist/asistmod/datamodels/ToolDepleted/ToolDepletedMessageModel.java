package com.asist.asistmod.datamodels.ToolDepleted;

import java.time.Clock;

public class ToolDepletedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:ToolDepleted";
	public String version = "1.1";	
	
	
	
}
