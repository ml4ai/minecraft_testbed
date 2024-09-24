package com.asist.asistmod.datamodels.GroundTruth.VictimsRescued;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class VictimsRescuedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public VictimsRescuedMessageModel msg = new VictimsRescuedMessageModel();	
	
	public VictimsRescuedDataModel data = new VictimsRescuedDataModel();
	
	
	public VictimsRescuedModel() {
		
		header.message_type = "groundtruth";
		
	}	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
