package com.asist.asistmod.datamodels.MarkerPlaced;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class MarkerPlacedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public MarkerPlacedMessageModel msg = new MarkerPlacedMessageModel();	
	
	public MarkerPlacedDataModel data = new MarkerPlacedDataModel();
	
	
	public MarkerPlacedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
