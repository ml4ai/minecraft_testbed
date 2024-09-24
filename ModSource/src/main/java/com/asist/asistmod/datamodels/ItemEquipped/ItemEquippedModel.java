package com.asist.asistmod.datamodels.ItemEquipped;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class ItemEquippedModel {
	
	public HeaderModel header = new HeaderModel();
		
	public ItemEquippedMessageModel msg = new ItemEquippedMessageModel();
	
	public ItemEquippedDataModel data = new ItemEquippedDataModel();
		
		
	public ItemEquippedModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
