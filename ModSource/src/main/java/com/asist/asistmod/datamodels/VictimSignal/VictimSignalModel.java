package com.asist.asistmod.datamodels.VictimSignal;

import java.time.Clock;

import com.asist.asistmod.datamodels.Header.HeaderModel;

import com.google.gson.Gson;

public class VictimSignalModel {
	
	public HeaderModel header = new HeaderModel();
		
	public VictimSignalMessageModel msg = new VictimSignalMessageModel();	
	
	public VictimSignalDataModel data = new VictimSignalDataModel();
	
	public VictimSignalModel(String playername,String pid,String roomname,int x, int y, int z, String message) {
		
		header.message_type = "event";		
		
		data.playername = playername;
		data.participant_id = pid;
		data.roomname = roomname;
		data.x = x;
		data.y = y;
		data.z = z;
		data.message = message;
		
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this);		
	}

}
