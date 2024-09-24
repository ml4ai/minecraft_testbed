package com.asist.asistmod.datamodels.ToolUsed;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class ToolUsedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public ToolUsedMessageModel msg = new ToolUsedMessageModel();	
	
	public ToolUsedDataModel data = new ToolUsedDataModel();
	
	
	public ToolUsedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
