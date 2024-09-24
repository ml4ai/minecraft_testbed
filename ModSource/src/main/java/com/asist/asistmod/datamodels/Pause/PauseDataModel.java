package com.asist.asistmod.datamodels.Pause;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class PauseDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public Boolean paused;
		
}
