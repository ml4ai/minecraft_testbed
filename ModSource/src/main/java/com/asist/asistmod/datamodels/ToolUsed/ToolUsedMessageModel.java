package com.asist.asistmod.datamodels.ToolUsed;

import java.time.Clock;

public class ToolUsedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:ToolUsed";
	public String version = "1.1";	
	
	
	
}
