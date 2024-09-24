package com.asist.asistmod.datamodels.Evacuation;

import com.asist.asistmod.datamodels.Header.HeaderModel;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.google.gson.Gson;

import net.minecraft.util.math.BlockPos;

public class EvacuationModel{
	
    public HeaderModel header = new HeaderModel();
	
	public EvacuationMessageModel msg = new EvacuationMessageModel();	
	
	public EvacuationDataModel data = new EvacuationDataModel();
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
	
	
	public EvacuationModel(String playername, int vx, int vy, int vz,String type,boolean correct_area) {
		
		header.message_type = "event";
		
		data.playername = playername;
		data.participant_id = InternalMqttClient.name_to_pid(playername);
		data.victim_x = vx;
		data.victim_y = vy;
		data.victim_z = vz;
		data.victim_id = MapBlockManager.getVictimId(new BlockPos(vx,vy,vz));		
		data.type = type;
		data.success = correct_area;

		
		
	}
	
		
	public String toJsonString() {
		
		Gson gson = new Gson();
		return gson.toJson(this); 
		
	}
}
