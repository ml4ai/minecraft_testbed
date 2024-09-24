package com.asist.asistmod.datamodels.GroundTruth.VictimsExpired;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class VictimsExpiredModel{
	
    public HeaderModel header = new HeaderModel();
	
	public VictimsExpiredMessageModel msg = new VictimsExpiredMessageModel();	
	
	public VictimsExpiredDataModel data = new VictimsExpiredDataModel();
	
	
	public VictimsExpiredModel() {
		
		header.message_type = "groundtruth";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
