package com.asist.asistmod.datamodels.GroundTruth.ThreatSignList;

import java.util.ArrayList;
import java.util.List;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ThreatSignListDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String mission = "Not Set";
	public List<ThreatSignListItem> mission_threatsign_list = new ArrayList<ThreatSignListItem>();
		
}