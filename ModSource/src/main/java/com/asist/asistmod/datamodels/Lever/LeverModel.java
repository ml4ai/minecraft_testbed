package com.asist.asistmod.datamodels.Lever;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class LeverModel {
	
	public HeaderModel header = new HeaderModel();
		
	public LeverMessageModel msg = new LeverMessageModel();	
	
	public LeverDataModel data = new LeverDataModel();
		
	public LeverModel() {		
		
		header.message_type = "event";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
