package com.asist.asistmod.datamodels.VictimPlaced;

import java.time.Clock;

public class VictimPlacedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:VictimPlaced";
	public String version = "2.1";	
	
	
	
}
