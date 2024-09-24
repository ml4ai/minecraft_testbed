package com.asist.asistmod.datamodels.CollapseBlock;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class RubbleCollapseDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername ;
	public String participant_id = "Not Set";
	public int triggerLocation_x ;
	public int triggerLocation_y ;
	public int triggerLocation_z ;
	public int fromBlock_x ; 
	public int fromBlock_y ;
	public int fromBlock_z ;
	public int toBlock_x ;
	public int toBlock_y ;
	public int toBlock_z ;
	
		
}
