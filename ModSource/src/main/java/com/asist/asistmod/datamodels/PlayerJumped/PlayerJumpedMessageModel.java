package com.asist.asistmod.datamodels.PlayerJumped;

import java.time.Clock;

public class PlayerJumpedMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:PlayerJumped";
	public String version = "0.5";	
	
	

}
