package com.asist.asistmod.datamodels.Door;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class DoorModel {
	
	public HeaderModel header = new HeaderModel();
		
	public DoorMessageModel msg = new DoorMessageModel();	
	
	public DoorDataModel data = new DoorDataModel();
		
	public DoorModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
