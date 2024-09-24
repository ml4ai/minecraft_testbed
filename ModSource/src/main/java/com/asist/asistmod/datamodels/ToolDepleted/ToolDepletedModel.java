package com.asist.asistmod.datamodels.ToolDepleted;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class ToolDepletedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public ToolDepletedMessageModel msg = new ToolDepletedMessageModel();	
	
	public ToolDepletedDataModel data = new ToolDepletedDataModel();
	
	
	public ToolDepletedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
