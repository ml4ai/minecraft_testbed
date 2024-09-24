package com.asist.asistmod.datamodels.ItemUsed;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class ItemUsedModel {
	
	public HeaderModel header = new HeaderModel();
		
	public ItemUsedMessageModel msg = new ItemUsedMessageModel();	
	
	public ItemUsedDataModel data = new ItemUsedDataModel();
		
	public ItemUsedModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
