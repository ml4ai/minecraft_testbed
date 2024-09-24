package com.asist.asistmod.datamodels.GroundTruth.BlockageList;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager.MapBlockMode;
import com.google.gson.Gson;

public class BlockageListModel{
	
    public HeaderModel header = new HeaderModel();
	
	public BlockageListMessageModel msg = new BlockageListMessageModel();	
	
	public BlockageListDataModel data = new BlockageListDataModel();
	
	
	public BlockageListModel(MapBlockMode mode) {	
		
		if(mode.equals(MapBlockMode.PERTURBATION)) {
			header.message_type = "event";
			msg.sub_type = "Event:PerturbationRubbleLocations";
			msg.version = "2.0";
		}
		else {
			header.message_type = "groundtruth";
		}
	}
	
	
	public String toJsonString() { 
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
