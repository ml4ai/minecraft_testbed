package com.asist.asistmod.datamodels.VictimPlaced;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class VictimPlacedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public String type = null;
	public int victim_x = 0;
	public int victim_y = 0;
	public int victim_z = 0;
	public int victim_id = -1;
		
}
