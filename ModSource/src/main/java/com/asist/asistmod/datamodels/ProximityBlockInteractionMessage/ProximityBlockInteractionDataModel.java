package com.asist.asistmod.datamodels.ProximityBlockInteractionMessage;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ProximityBlockInteractionDataModel {
	
	public static enum ACTION_TYPE {
		ENTERED_RANGE,
		LEFT_RANGE,
		TRIAGE_ERROR
	}
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();	
	public String playername = null;
	public String participant_id = "Not Set";
	public String action_type = null;
	public int players_in_range = 0;
	public boolean awake = false;
	public int victim_x = 0;
	public int victim_y = 0;
	public int victim_z = 0;
	public int victim_id = -1;

}
