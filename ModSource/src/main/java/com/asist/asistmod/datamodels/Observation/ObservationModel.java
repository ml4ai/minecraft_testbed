package com.asist.asistmod.datamodels.Observation;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class ObservationModel{	 
	
	public HeaderModel header = new HeaderModel();
	
	public ObservationMessageModel msg = new ObservationMessageModel();
	
	public ObservationData data = new ObservationData();
	
	public ObservationModel() {
		header.message_type = "observation";
	}
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}

}
