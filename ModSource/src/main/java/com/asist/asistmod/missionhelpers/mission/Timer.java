package com.asist.asistmod.missionhelpers.mission;

import java.time.Clock;

import net.minecraft.server.MinecraftServer;

public class Timer {
	
	public static int missionIndex;
	public static int missionTime;
	private static long startTime;
	
	private static long elapsedMillis;
	private static int elapsedSeconds;
	private static int lastSecond;
	
	private static MinecraftServer server;
	private static Thread thread;
	
	private static boolean isInitialized;
	private static boolean secondTick;
	
	public static void init(MinecraftServer s) {
		
		server = s;
		lastSecond = 0;
	
		startTime = Clock.systemDefaultZone().millis();

		isInitialized = true;
		secondTick = false;
		
	}
	
	public static int getSeconds() {
		return elapsedSeconds;
	}
	
	public static long getMillis() {
		return elapsedMillis;
	}
	
	public static void update() {		
		
		if(isInitialized) {	
			
			long currentTime = Clock.systemDefaultZone().millis();
			elapsedMillis = currentTime - startTime;
			elapsedSeconds = (int)Math.floorDiv(elapsedMillis, 1000);
					
			if( elapsedSeconds != lastSecond ) {		
		
				lastSecond = elapsedSeconds;
				secondTick = true;
			}						
			else
			{
				secondTick = false;
			}
		}		
	}
	
	public static void end() {
		
		isInitialized = false;
		startTime = 0;
		lastSecond = 0;
		
	}
	
	public static String getMissionTimeString() {		

		if(isInitialized) {
			int minutes = Math.floorDiv(elapsedSeconds, 60);
			int seconds = Math.floorMod(elapsedSeconds, 60);
			return minutes + ":" + seconds;
		}
		else return "Mission Timer not initialized.";
	}
	
	public static boolean secondTick() {
		return secondTick;
	}

}