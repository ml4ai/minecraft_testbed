package com.asist.asistmod.datamodels.RubblePlaced;

import com.asist.asistmod.missionhelpers.datastructures.PositionRange;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class RubblePlacedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public int from_x = 0;
	public int from_y = 0;
	public int from_z = 0;
	public int to_x = 0;
	public int to_y = 0;
	public int to_z = 0;
	
	public void AddValues( PositionRange range ) {
		from_x = range.from.getX();
		from_y = range.from.getY();
		from_z = range.from.getZ();
		to_x = range.to.getX();
		to_y = range.to.getY();
		to_z = range.to.getZ();
	}
		
}
