package com.asist.asistmod.datamodels.PlayerSprinting;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class PlayerSprintingModel {
	
	public HeaderModel header = new HeaderModel();
		
	public PlayerSprintingMessageModel msg = new PlayerSprintingMessageModel();
	
	public PlayerSprintingDataModel data = new PlayerSprintingDataModel();
		
		
	public PlayerSprintingModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
