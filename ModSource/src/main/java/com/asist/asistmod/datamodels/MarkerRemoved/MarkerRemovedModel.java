package com.asist.asistmod.datamodels.MarkerRemoved;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class MarkerRemovedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public MarkerRemovedMessageModel msg = new MarkerRemovedMessageModel();	
	
	public MarkerRemovedDataModel data = new MarkerRemovedDataModel();
	
	
	public MarkerRemovedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
