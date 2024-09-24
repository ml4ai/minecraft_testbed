package com.asist.asistmod.datamodels.AgentChatIntervention;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class AgentChatInterventionModel {
	
	public HeaderModel header = new HeaderModel();
		
	public AgentChatInterventionMessageModel msg = new AgentChatInterventionMessageModel();	
	
	public AgentChatInterventionDataModel data = new AgentChatInterventionDataModel();	
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
