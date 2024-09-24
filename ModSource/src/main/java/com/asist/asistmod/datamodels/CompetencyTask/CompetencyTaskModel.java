package com.asist.asistmod.datamodels.CompetencyTask;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.google.gson.Gson;

public class CompetencyTaskModel{
	
    public HeaderModel header = new HeaderModel();
	
	public CompetencyTaskMessageModel msg = new CompetencyTaskMessageModel();	
	
	public CompetencyTaskDataModel data = new CompetencyTaskDataModel();
	
	
	public CompetencyTaskModel( String playerName, String taskMessage) {
		
		header.message_type = "event";
		data.playerName = playerName;
		data.callsign = InternalMqttClient.name_to_callsign(playerName);
		data.participant_id = InternalMqttClient.name_to_pid(playerName);
		data.task_message = taskMessage;
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
