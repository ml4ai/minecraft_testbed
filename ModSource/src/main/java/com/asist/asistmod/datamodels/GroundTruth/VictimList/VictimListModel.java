package com.asist.asistmod.datamodels.GroundTruth.VictimList;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class VictimListModel{
	
    public HeaderModel header = new HeaderModel();
	
	public VictimListMessageModel msg = new VictimListMessageModel();	
	
	public VictimListDataModel data = new VictimListDataModel();
	
	
	public VictimListModel() {
		
		header.message_type = "groundtruth";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
