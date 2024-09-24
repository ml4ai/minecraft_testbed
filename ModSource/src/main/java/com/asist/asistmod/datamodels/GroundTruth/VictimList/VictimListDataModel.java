package com.asist.asistmod.datamodels.GroundTruth.VictimList;

import java.util.ArrayList;
import java.util.List;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class VictimListDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String mission = "Not Set";
	public List<VictimListVictim> mission_victim_list = new ArrayList<VictimListVictim>();
		
}
