package com.asist.asistmod.missionhelpers.Scoreboard;

import java.util.Collection;

import com.asist.asistmod.missionhelpers.Scoreboard.CustomBaseClasses.BaseServerScoreboard;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.timer.MissionTimerListener;

import net.minecraft.command.server.CommandScoreboard;
import net.minecraft.scoreboard.IScoreCriteria;
import net.minecraft.scoreboard.Score;
import net.minecraft.scoreboard.ScoreObjective;
import net.minecraft.scoreboard.ServerScoreboard;
import net.minecraft.server.MinecraftServer;


public class CustomScoreboardWrapper  {
	
	private static BaseServerScoreboard scoreBoard;
	private static ScoreObjective mainDisplay;	
	private static Score timerMinute;
	private static Score victimsSaved;
	private static Score taskNumber;
	
	private static int currentSecond;
	private static int currentMinute;

	public static void Init(MinecraftServer server) {
		
		if(scoreBoard == null) { scoreBoard = new BaseServerScoreboard(server); }
		
		currentMinute = MissionTimer.minuteCount;
		currentSecond = MissionTimer.secondCount;
		
		Collection<ScoreObjective> objectives = scoreBoard.getScoreObjectives();
		
		mainDisplay = scoreBoard.addScoreObjective("MainDisplay", IScoreCriteria.DUMMY); 
		mainDisplay.setDisplayName("ASIST");		
		
		timerMinute = scoreBoard.getOrCreateScore(Integer.toString(currentMinute), mainDisplay);
		
		victimsSaved = scoreBoard.getOrCreateScore("Victims", mainDisplay);
		
	
		timerMinute.setScorePoints(currentSecond);
		
		victimsSaved.setScorePoints(30);
		
		scoreBoard.setObjectiveInDisplaySlot(1, mainDisplay);
		
	}
	
	//public static void reset() {
		
		//time.setScorePoints(0);
		//victimsSaved.setScorePoints(0);
		
	//}
	
	public static void stop() {
		timerMinute.setScorePoints(0);
	}
	
	public static void showTutorial() {
		scoreBoard.setObjectiveInDisplaySlot(1, mainDisplay);;		
	}
	
	public static void showMission() {
		scoreBoard.setObjectiveInDisplaySlot(1, mainDisplay);
	}
	
	public static void taskComplete() {
		taskNumber.incrementScore();
	}
	
	public static void addScore(int score) {
		if(scoreBoard != null) {
			victimsSaved.increaseScore(score);			
		}
	}
	
	public static void setTime(int newTime) {
		timerMinute.setScorePoints(newTime);
	}
	
	public static void onMissionTimeChange(int m, int s) {
		
		if(m != currentMinute) {
			
			timerMinute = scoreBoard.getOrCreateScore(Integer.toString(m), mainDisplay);
			scoreBoard.removeObjectiveFromEntity(Integer.toString(m+1), mainDisplay);
		}
		
		if(s != currentSecond) {
			timerMinute.setScorePoints(s);
		}
		
	}

}
