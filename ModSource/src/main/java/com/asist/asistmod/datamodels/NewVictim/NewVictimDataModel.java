package com.asist.asistmod.datamodels.NewVictim;

import com.asist.asistmod.missionhelpers.datastructures.Position;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class NewVictimDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;	
	public String type = null;
	public int victim_x = 0;
	public int victim_y = 0;
	public int victim_z = 0;
	
	public void AddLocation(Position pos) {
		victim_x = pos.getX();
		victim_y = pos.getY();
		victim_z = pos.getZ();
	}
		
}
