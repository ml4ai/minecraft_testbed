package com.asist.asistmod.datamodels.Perturbation;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class PerturbationModel{
	
    public HeaderModel header = new HeaderModel();
	
	public PerturbationMessageModel msg = new PerturbationMessageModel();	
	
	public PerturbationDataModel data = new PerturbationDataModel();
	
	
	public PerturbationModel(String type, String state) {
		
		header.message_type = "event";
		data.type = type;
		data.mission_state = state;
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
