package com.asist.asistmod.datamodels.VictimPickedUp;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class VictimPickedUpModel{
	
    public HeaderModel header = new HeaderModel();
	
	public VictimPickedUpMessageModel msg = new VictimPickedUpMessageModel();	
	
	public VictimPickedUpDataModel data = new VictimPickedUpDataModel();
	
	
	public VictimPickedUpModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
