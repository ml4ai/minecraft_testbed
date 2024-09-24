package com.asist.asistmod.datamodels.ItemDrop;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ItemDropDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String playername = null;
	public String participant_id = "Not Set";
	public String itemname = null;
	public int item_x = 0;
	public int item_y = 0;
	public int item_z = 0;	
}
