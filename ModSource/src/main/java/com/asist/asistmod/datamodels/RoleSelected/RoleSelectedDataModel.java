package com.asist.asistmod.datamodels.RoleSelected;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class RoleSelectedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public String new_role = null;
	public String prev_role = null;
		
}
