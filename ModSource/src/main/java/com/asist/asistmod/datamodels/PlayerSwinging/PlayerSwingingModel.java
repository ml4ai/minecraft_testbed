package com.asist.asistmod.datamodels.PlayerSwinging;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class PlayerSwingingModel {
	
	public HeaderModel header = new HeaderModel();
		
	public PlayerSwingingMessageModel msg = new PlayerSwingingMessageModel();
	
	public PlayerSwingingDataModel data = new PlayerSwingingDataModel();
		
		
	public PlayerSwingingModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
