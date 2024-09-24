package com.asist.asistmod.datamodels.PlayerJumped;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class PlayerJumpedModel {
	
	public HeaderModel header = new HeaderModel();
		
	public PlayerJumpedMessageModel msg = new PlayerJumpedMessageModel();	
	
	public PlayerJumpedDataModel data = new PlayerJumpedDataModel();
		
	public PlayerJumpedModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
