package com.asist.asistmod.datamodels.GroundTruth.VictimsExpired;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class VictimsExpiredDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String expired_message = "All remaining yellow victims have succumbed to their injuries.";
		
}
