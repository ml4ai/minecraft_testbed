package com.asist.asistmod.datamodels.MarkerDestroyed;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class MarkerDestroyedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public MarkerDestroyedMessageModel msg = new MarkerDestroyedMessageModel();	
	
	public MarkerDestroyedDataModel data = new MarkerDestroyedDataModel();
	
	
	public MarkerDestroyedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
