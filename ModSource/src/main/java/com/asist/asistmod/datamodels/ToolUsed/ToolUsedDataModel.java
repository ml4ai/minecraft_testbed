package com.asist.asistmod.datamodels.ToolUsed;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ToolUsedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public String tool_type = null;
	public int durability = 0;
	public int count = 1;
	public int target_block_x = 0;
	public int target_block_y = 0;
	public int target_block_z = 0;
	public String target_block_type = null;
	
}
