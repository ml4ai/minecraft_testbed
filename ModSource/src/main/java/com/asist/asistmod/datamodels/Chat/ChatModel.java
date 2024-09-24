package com.asist.asistmod.datamodels.Chat;

import com.google.gson.Gson;
import com.asist.asistmod.datamodels.Header.*;

public class ChatModel {
	
	public HeaderModel header = new HeaderModel();
	public ChatMessageModel msg = new ChatMessageModel();
	public ChatDataModel data = new ChatDataModel();
	
public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
}

}
