package com.asist.asistmod.datamodels.PlanningStage;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class PlanningStageModel{
	
	
	
    public HeaderModel header = new HeaderModel();
	
	public PlanningStageMessageModel msg = new PlanningStageMessageModel();	
	
	public PlanningStageDataModel data = new PlanningStageDataModel();
	
	public PlanningStageModel(String state) {
		
		header.message_type = "event";
		data.state = state;
		
	}	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
	
	public String getTopicString() {
		return "observations/events/mission/planning";
	}
}
