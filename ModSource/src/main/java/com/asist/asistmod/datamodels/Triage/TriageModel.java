package com.asist.asistmod.datamodels.Triage;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class TriageModel{
	
    public HeaderModel header = new HeaderModel();
	
	public TriageMessageModel msg = new TriageMessageModel();	
	
	public TriageDataModel data = new TriageDataModel();
	
	
	public TriageModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
