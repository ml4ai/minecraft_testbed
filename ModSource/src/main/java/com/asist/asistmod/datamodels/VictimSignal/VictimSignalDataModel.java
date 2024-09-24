package com.asist.asistmod.datamodels.VictimSignal;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class VictimSignalDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();	
	public String message = null;
	public String playername;
	public String participant_id;
	public String roomname;
	public int x = 0;
	public int y = 0;
	public int z = 0;	

}
