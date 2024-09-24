package com.asist.asistmod.datamodels.MissionState;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class MissionStateModel{
	
    public HeaderModel header = new HeaderModel();
	
	public MissionStateMessageModel msg = new MissionStateMessageModel();	
	
	public MissionStateDataModel data = new MissionStateDataModel();
	
	
	public MissionStateModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
