package com.asist.asistmod.datamodels.IncidentCommander;

import java.time.Clock;

public class IncidentCommanderMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:IncidentCommander";
	public String version = "1.0";	
	
	
	
}
