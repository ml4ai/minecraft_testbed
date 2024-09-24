package com.asist.asistmod.datamodels.Chat;

import java.time.Clock;

import com.asist.asistmod.datamodels.Door.DoorDataModel;

public class ChatMessageModel {
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:Chat";
	public String version = "1.0";	
	
}
