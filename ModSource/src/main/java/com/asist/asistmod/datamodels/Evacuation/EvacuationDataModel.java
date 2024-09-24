package com.asist.asistmod.datamodels.Evacuation;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class EvacuationDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername ;
	public String participant_id = "Not Set";
	public int victim_x ;
	public int victim_y ;
	public int victim_z ;
	public int victim_id;
	public String type; 
	public boolean success;
	
	
		
}
