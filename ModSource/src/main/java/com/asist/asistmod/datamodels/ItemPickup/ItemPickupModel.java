package com.asist.asistmod.datamodels.ItemPickup;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class ItemPickupModel {
	
	public HeaderModel header = new HeaderModel();
		
	public ItemPickupMessageModel msg = new ItemPickupMessageModel();	
	
	public ItemPickupDataModel data = new ItemPickupDataModel();
		
	public ItemPickupModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
