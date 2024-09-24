package com.asist.asistmod.datamodels.RubblePlaced;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.asist.asistmod.missionhelpers.datastructures.PositionRange;
import com.google.gson.Gson;

public class RubblePlacedModel{
	
    public HeaderModel header = new HeaderModel();
	
	public RubblePlacedMessageModel msg = new RubblePlacedMessageModel();	
	
	public RubblePlacedDataModel data = new RubblePlacedDataModel();
	
	
	public RubblePlacedModel(PositionRange range) {
		
		header.message_type = "event";
		data.AddValues(range);
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
