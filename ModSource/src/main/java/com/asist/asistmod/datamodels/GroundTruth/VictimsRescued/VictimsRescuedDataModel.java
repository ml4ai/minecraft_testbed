package com.asist.asistmod.datamodels.GroundTruth.VictimsRescued;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class VictimsRescuedDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String rescued_message = "All victims have been rescued.";
		
}
