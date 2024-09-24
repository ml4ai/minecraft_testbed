package com.asist.asistmod.datamodels.ItemDrop;

import java.time.Clock;

public class ItemDropMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:ItemDrop";
	public String version = "0.5";	
	
	

}
