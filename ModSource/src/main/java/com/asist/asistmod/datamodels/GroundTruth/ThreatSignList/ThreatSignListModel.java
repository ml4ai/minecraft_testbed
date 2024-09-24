package com.asist.asistmod.datamodels.GroundTruth.ThreatSignList;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class ThreatSignListModel{
	
    public HeaderModel header = new HeaderModel();
	
	public ThreatSignListMessageModel msg = new ThreatSignListMessageModel();	
	
	public ThreatSignListDataModel data = new ThreatSignListDataModel();
	
	
	public ThreatSignListModel() {
		
		header.message_type = "groundtruth";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
