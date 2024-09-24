package com.asist.asistmod.datamodels.Chat;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ChatDataModel {
	
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
	public String sender = null;
	public String[] addressees = null;
	public String text = null;

}
