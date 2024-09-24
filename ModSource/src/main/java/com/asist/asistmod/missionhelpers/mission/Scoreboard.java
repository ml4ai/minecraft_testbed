package com.asist.asistmod.missionhelpers.mission;

import java.util.Collection;

import net.minecraft.command.server.CommandScoreboard;
import net.minecraft.scoreboard.IScoreCriteria;
import net.minecraft.scoreboard.Score;
import net.minecraft.scoreboard.ScoreObjective;
import net.minecraft.scoreboard.ServerScoreboard;
import net.minecraft.server.MinecraftServer;
import net.minecraftforge.fml.common.FMLLog;

public class Scoreboard {
	
	private static ServerScoreboard scoreBoard;
	private static ScoreObjective mission;
	private static ScoreObjective tutorial;
	private static Score time;
	private static Score victimsRemaining;
	private static Score taskNumber;

	public static void Init(MinecraftServer server) {		
		
		scoreBoard = new CustomScoreboard(server);		
		
		System.out.println( "Initializing Scoreboard Now.");		
		
		mission = scoreBoard.addScoreObjective("SearchAndRescue", IScoreCriteria.DUMMY);
		
		victimsRemaining = scoreBoard.getOrCreateScore("VictimsRemaining", mission);		
		
		victimsRemaining.setScorePoints(545);
		
		victimsRemaining.notifyAll();
		
		scoreBoard.setObjectiveInDisplaySlot(1, mission);
		scoreBoard.broadcastScoreUpdate("VictimsRemaining", mission);
		
		
		
		//tutorial = scoreBoard.addScoreObjective("Tutorial", IScoreCriteria.DUMMY);
		
		
		//time = scoreBoard.getOrCreateScore("TimeLeft", mission);
		
		//time.setScorePoints(600);
		
		
		
		//victimsRemaining = scoreBoard.getOrCreateScore("VictimsRemaining", mission);

		//taskNumber = scoreBoard.getOrCreateScore("Task", tutorial);

		//reset();
		
		
		
		//if(scoreBoard == null) { 
			
		//	scoreBoard = new ServerScoreboard(server);
			
			
		//}
		//boolean missionExists = false;
		//boolean tutorialExists = false;
		//Collection<ScoreObjective> objectives = scoreBoard.getScoreObjectives();
		//if(objectives.isEmpty()) { 
		//	mission = scoreBoard.addScoreObjective("SearchAndRescue", IScoreCriteria.DUMMY); 
		//	tutorial = scoreBoard.addScoreObjective("Tutorial", IScoreCriteria.DUMMY);
		//}
		//else {
		//	for(ScoreObjective objective:objectives) {
		//		if(objective.getDisplayName().equals("SearchAndRescue")) {
		//			mission = scoreBoard.getObjective("SearchAndRescue");
		//			missionExists = true;
		//		}
		//		else if(objective.getDisplayName().equals("Tutorial")) {
		//			mission = scoreBoard.getObjective("Tutorial");
		//			tutorialExists = true;
		//		}
		//		if(missionExists && tutorialExists) { break; }
		//	}
		//	if(!missionExists) {
		//		mission = scoreBoard.addScoreObjective("SearchAndRescue", IScoreCriteria.DUMMY);				
		//	}
		//	if(!tutorialExists) {
		//		tutorial = scoreBoard.addScoreObjective("Tutorial", IScoreCriteria.DUMMY);
		//	}
		//}
		
		//time = scoreBoard.getOrCreateScore("TimeLeft", mission);
		//victimsRemaining = scoreBoard.getOrCreateScore("VictimsRemaining", mission);

		//taskNumber = scoreBoard.getOrCreateScore("Task", tutorial);

		//reset();
	}
	
	
	
	public static void stop() {
		time.setScorePoints(0);
	}
	
	public static void showTutorial() {
		scoreBoard.setObjectiveInDisplaySlot(1, tutorial);;		
	}

	public static void showMission() {
		scoreBoard.setObjectiveInDisplaySlot(1, mission);
	}
	
	public static void taskComplete() {
		taskNumber.incrementScore();
	}
	
	public static void addScore(int score) {
		if(scoreBoard != null) {
			victimsRemaining.decreaseScore(score);			
		}
		if(Tutorial.isActive()) {
			Tutorial.victimSaved();
		}
	}
	
	public static void setTime(int newTime) {
		//time.setScorePoints(newTime);
	}
}
