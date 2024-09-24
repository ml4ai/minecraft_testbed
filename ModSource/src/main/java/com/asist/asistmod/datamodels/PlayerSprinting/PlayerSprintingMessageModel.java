package com.asist.asistmod.datamodels.PlayerSprinting;

import java.time.Clock;

public class PlayerSprintingMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:PlayerSprinting";
	public String version = "0.5";			

}
