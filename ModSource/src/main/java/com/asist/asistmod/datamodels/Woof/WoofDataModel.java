package com.asist.asistmod.datamodels.Woof;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class WoofDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String source_entity = "Search and Rescue Dog";
	public String message = null;		
	public int woof_x = 0;
	public int woof_y = 0;
	public int woof_z = 0;	

}
