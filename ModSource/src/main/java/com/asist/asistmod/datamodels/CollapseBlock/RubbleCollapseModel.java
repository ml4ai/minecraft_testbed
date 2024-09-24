package com.asist.asistmod.datamodels.CollapseBlock;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.google.gson.Gson;

public class RubbleCollapseModel{
	
    public HeaderModel header = new HeaderModel();
	
	public RubbleCollapseMessageModel msg = new RubbleCollapseMessageModel();	
	
	public RubbleCollapseDataModel data = new RubbleCollapseDataModel();
	/*
	 * public String playername ;
	public String participant_id = "Not Set";
	public int triggerLocation_x ;
	public int triggerLocation_y ;
	public int triggerLocation_z ;
	public int fromBlock_x ; 
	public int fromBlock_y ;
	public int fromBlock_z ;
	public int toBlock_x ;
	public int toBlock_y ;
	public int toBlock_z ;
	*/
	
	
	public RubbleCollapseModel(String playername, String pid, int triggerx, int triggery, int triggerz, int fromBX,int fromBY,int fromBZ,
			int toBX, int toBY, int toBZ) {
		
		header.message_type = "event";
		
		data.playername = playername;
		data.participant_id = pid;
		data.triggerLocation_x = triggerx;
		data.triggerLocation_y = triggery;
		data.triggerLocation_z = triggerz;
		data.fromBlock_x = fromBX;
		data.fromBlock_y = fromBY;
		data.fromBlock_z = fromBZ;
		data.toBlock_x = toBX;
		data.toBlock_y = toBY;
		data.toBlock_z = toBZ;
		
		
	}
	
		
	public String toJsonString() {
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
