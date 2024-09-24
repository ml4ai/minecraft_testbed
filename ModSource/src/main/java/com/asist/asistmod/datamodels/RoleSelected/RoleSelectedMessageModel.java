package com.asist.asistmod.datamodels.RoleSelected;

import java.time.Clock;

public class RoleSelectedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:RoleSelected";
	public String version = "2.0";	
	
	
	
}
