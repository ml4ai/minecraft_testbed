package com.asist.asistmod.datamodels.IncidentCommander;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class IncidentCommanderModel{
	
    public HeaderModel header = new HeaderModel();
	
	public IncidentCommanderMessageModel msg = new IncidentCommanderMessageModel();	
	
	public IncidentCommanderDataModel data = new IncidentCommanderDataModel();
	
	
	public IncidentCommanderModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
