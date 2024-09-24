package com.asist.asistmod.datamodels.VictimsExpired;

import java.time.Clock;

public class VictimsExpiredMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:VictimsExpire";
	public String version = "0.5";	
	
	
	
}
