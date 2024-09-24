package com.asist.asistmod.datamodels.ItemDrop;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class ItemDropModel {
	
	public HeaderModel header = new HeaderModel();
		
	public ItemDropMessageModel msg = new ItemDropMessageModel();	
	
	public ItemDropDataModel data = new ItemDropDataModel();
		
	public ItemDropModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
