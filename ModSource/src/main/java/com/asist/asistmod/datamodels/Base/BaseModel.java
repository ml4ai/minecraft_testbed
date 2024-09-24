package com.asist.asistmod.datamodels.Base;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class BaseModel{
	
    public HeaderModel header = new HeaderModel();
	
	public BaseMessageModel msg = new BaseMessageModel();	
	
	public BaseDataModel data = new BaseDataModel();
	
	
	public BaseModel() {
		
		header.message_type = "event";
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
