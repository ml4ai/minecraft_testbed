package com.asist.asistmod.datamodels.Door;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class DoorDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public Boolean open = null;		
	public int door_x = 0;
	public int door_y = 0;
	public int door_z = 0;	

}
