package com.asist.asistmod.datamodels.PlayerJumped;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class PlayerJumpedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public int player_x = 0;
	public int player_y = 0;
	public int player_z = 0;	
}
