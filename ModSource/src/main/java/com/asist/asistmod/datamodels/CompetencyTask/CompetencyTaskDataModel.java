package com.asist.asistmod.datamodels.CompetencyTask;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class CompetencyTaskDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playerName = "Not Set";
	public String participant_id = "Not Set";
	public String callsign = "Not Set";
	public String task_message = "Not Set";
		
}
