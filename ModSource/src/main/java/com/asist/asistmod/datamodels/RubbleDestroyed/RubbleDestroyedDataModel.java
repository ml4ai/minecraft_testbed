package com.asist.asistmod.datamodels.RubbleDestroyed;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class RubbleDestroyedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public int rubble_x = 0;
	public int rubble_y = 0;
	public int rubble_z = 0;

}
