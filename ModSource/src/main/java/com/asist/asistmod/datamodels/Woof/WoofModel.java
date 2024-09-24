package com.asist.asistmod.datamodels.Woof;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class WoofModel {
	
	public HeaderModel header = new HeaderModel();
		
	public WoofMessageModel msg = new WoofMessageModel();	
	
	public WoofDataModel data = new WoofDataModel();
		
	public WoofModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
