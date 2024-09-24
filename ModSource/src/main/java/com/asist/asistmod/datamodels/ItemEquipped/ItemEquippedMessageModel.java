package com.asist.asistmod.datamodels.ItemEquipped;

import java.time.Clock;

public class ItemEquippedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:ItemEquipped";
	public String version = "0.5";			

}
