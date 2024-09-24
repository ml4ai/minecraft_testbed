package com.asist.asistmod.datamodels.ItemPickup;

import java.time.Clock;

public class ItemPickupMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:ItemPickup";
	public String version = "0.5";	
	
	

}
