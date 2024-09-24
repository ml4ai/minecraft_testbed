package com.asist.asistmod.datamodels.GroundTruth.BlockageList;

import java.util.ArrayList;
import java.util.List;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.mqtt.InternalMqttClient;

public class BlockageListDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String mission = InternalMqttClient.currentTrialInfo.mission_name;
	public List<BlockageListBlockage> mission_blockage_list = new ArrayList<BlockageListBlockage>();
		
}