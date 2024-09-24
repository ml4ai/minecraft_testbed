package com.asist.asistmod.datamodels.Base;

import com.asist.asistmod.missionhelpers.datastructures.PositionRange;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class BaseDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	
}
