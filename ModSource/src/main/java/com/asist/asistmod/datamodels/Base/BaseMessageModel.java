package com.asist.asistmod.datamodels.Base;

import java.time.Clock;

public class BaseMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String version = "0.5";	
		
}
