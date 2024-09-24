package com.asist.asistmod.datamodels.RoleSelected;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class RoleSelectedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public RoleSelectedMessageModel msg = new RoleSelectedMessageModel();	
	
	public RoleSelectedDataModel data = new RoleSelectedDataModel();
	
	
	public RoleSelectedModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
