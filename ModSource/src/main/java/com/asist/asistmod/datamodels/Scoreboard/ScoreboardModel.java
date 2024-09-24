package com.asist.asistmod.datamodels.Scoreboard;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class ScoreboardModel{
		
	 
	
	public HeaderModel header = new HeaderModel();
	
	public ScoreboardMessageModel msg = new ScoreboardMessageModel();
	
	public ScoreboardData data = new ScoreboardData();
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}

}
