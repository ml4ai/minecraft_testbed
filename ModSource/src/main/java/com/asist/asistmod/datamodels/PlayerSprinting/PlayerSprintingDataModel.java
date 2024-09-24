package com.asist.asistmod.datamodels.PlayerSprinting;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class PlayerSprintingDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public Boolean sprinting = false;
}
