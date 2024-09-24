package com.asist.asistmod.datamodels.GroundTruth.FreezeBlockList;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class FreezeBlockListModel{
	
    public HeaderModel header = new HeaderModel();
	
	public FreezeBlockListMessageModel msg = new FreezeBlockListMessageModel();	
	
	public FreezeBlockListDataModel data = new FreezeBlockListDataModel();
	
	
	public FreezeBlockListModel() {
		
		header.message_type = "groundtruth";		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
