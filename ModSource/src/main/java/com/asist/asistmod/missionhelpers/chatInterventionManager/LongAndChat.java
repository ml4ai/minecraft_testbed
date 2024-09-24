package com.asist.asistmod.missionhelpers.chatInterventionManager;

import java.util.List;

import com.asist.asistmod.datamodels.ModSettings.MinSec;

public class LongAndChat {
	
	long longTime;
	String content;
	String receiver;
	
	public LongAndChat(long t, String c, String receiver) {
		this.longTime = t;
		this.content = c;
		this.receiver = receiver;
	}
}
