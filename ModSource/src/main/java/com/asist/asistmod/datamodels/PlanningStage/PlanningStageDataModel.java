package com.asist.asistmod.datamodels.PlanningStage;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class PlanningStageDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long 
	elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String state = "Not Set";
		
}
