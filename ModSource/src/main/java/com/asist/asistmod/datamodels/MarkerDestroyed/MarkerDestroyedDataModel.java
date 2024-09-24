package com.asist.asistmod.datamodels.MarkerDestroyed;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class MarkerDestroyedDataModel {

	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String type = null;
	public int marker_x = 0;
	public int marker_y = 0;
	public int marker_z = 0;	
	
}
