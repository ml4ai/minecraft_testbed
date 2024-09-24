package com.asist.asistmod.datamodels.MissionState;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class MissionStateDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String mission = "Not Set";
	public String mission_state = null;
		
}
