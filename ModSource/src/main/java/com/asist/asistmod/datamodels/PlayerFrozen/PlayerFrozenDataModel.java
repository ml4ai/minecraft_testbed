package com.asist.asistmod.datamodels.PlayerFrozen;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class PlayerFrozenDataModel {
	
	public static enum frozenStates {
		FROZEN,
		UNFROZEN
	}
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername ;
	public String participant_id = "Not Set";
	public int player_x ;
	public int player_y ;
	public int player_z ;
	public String state_changed_to;
	public String medic_playername;
	public String medic_participant_id;
		
}
