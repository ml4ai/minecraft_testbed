package com.asist.asistmod.datamodels.ProximityBlockInteractionMessage;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class ProximityBlockInteractionModel {
	
	public HeaderModel header = new HeaderModel();
		
	public ProximityBlockInteractionMessageModel msg = new ProximityBlockInteractionMessageModel();	
	
	public ProximityBlockInteractionDataModel data = new ProximityBlockInteractionDataModel();
		
	public ProximityBlockInteractionModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
