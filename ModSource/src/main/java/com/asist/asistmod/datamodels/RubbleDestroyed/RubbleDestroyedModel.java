package com.asist.asistmod.datamodels.RubbleDestroyed;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class RubbleDestroyedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public RubbleDestroyedMessageModel msg = new RubbleDestroyedMessageModel();	
	
	public RubbleDestroyedDataModel data = new RubbleDestroyedDataModel();
	
	
	public RubbleDestroyedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
