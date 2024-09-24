package com.asist.asistmod.datamodels.Perturbation;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class PerturbationDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String type = "Not Set";
	public String mission_state = null;
		
}
