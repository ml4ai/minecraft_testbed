package com.asist.asistmod.datamodels.GroundTruth.FreezeBlockList;

import java.util.ArrayList;
import java.util.List;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class FreezeBlockListDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String mission = "Not Set";
	public List<FreezeBlockListItem> mission_freezeblock_list = new ArrayList<FreezeBlockListItem>();
		
}