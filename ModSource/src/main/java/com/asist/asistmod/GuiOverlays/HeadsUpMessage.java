package com.asist.asistmod.GuiOverlays;

public class HeadsUpMessage
{
	String message;
	long removalTime;
	
	public HeadsUpMessage(String message, long removalTime) {
		this.message = message;
		this.removalTime = removalTime;
	}	
}