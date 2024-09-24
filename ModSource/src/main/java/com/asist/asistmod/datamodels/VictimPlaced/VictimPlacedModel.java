package com.asist.asistmod.datamodels.VictimPlaced;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class VictimPlacedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public VictimPlacedMessageModel msg = new VictimPlacedMessageModel();	
	
	public VictimPlacedDataModel data = new VictimPlacedDataModel();
	
	
	public VictimPlacedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
