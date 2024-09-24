package com.asist.asistmod.datamodels.IncidentCommander;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class IncidentCommanderDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String incident_string = "NOT SET";
		
}
