package com.asist.asistmod.datamodels.ToolDepleted;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ToolDepletedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public String tool_type = null;
		
}
