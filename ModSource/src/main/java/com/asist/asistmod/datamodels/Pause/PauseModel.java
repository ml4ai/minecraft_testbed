package com.asist.asistmod.datamodels.Pause;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class PauseModel{
	
    public HeaderModel header = new HeaderModel();
	
	public PauseMessageModel msg = new PauseMessageModel();	
	
	public PauseDataModel data = new PauseDataModel();
	
	
	public PauseModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
