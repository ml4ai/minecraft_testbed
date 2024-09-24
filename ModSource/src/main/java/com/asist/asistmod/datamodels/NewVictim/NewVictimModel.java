package com.asist.asistmod.datamodels.NewVictim;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.asist.asistmod.missionhelpers.datastructures.Position;
import com.google.gson.Gson;

public class NewVictimModel{
	
    public HeaderModel header = new HeaderModel();
	
	public NewVictimMessageModel msg = new NewVictimMessageModel();	
	
	public NewVictimDataModel data = new NewVictimDataModel();
	
	
	public NewVictimModel(Position pos) {
		
		header.message_type = "event";
		data.AddLocation(pos);
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
