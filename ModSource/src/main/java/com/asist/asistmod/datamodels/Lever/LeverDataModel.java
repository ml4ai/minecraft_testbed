package com.asist.asistmod.datamodels.Lever;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class LeverDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public Boolean powered = null;		
	public int lever_x = 0;
	public int lever_y = 0;
	public int lever_z = 0;	

}
