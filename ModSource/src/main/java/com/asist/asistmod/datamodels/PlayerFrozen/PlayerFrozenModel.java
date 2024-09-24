package com.asist.asistmod.datamodels.PlayerFrozen;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class PlayerFrozenModel{
	
    public HeaderModel header = new HeaderModel();
	
	public PlayerFrozenMessageModel msg = new PlayerFrozenMessageModel();	
	
	public PlayerFrozenDataModel data = new PlayerFrozenDataModel();
	
	
	public PlayerFrozenModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
