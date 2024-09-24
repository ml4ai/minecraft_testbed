package com.asist.asistmod.missionhelpers.Scoreboard;

import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.datamodels.Evacuation.EvacuationModel;
import com.asist.asistmod.datamodels.ModSettings.SafeZone;
import com.asist.asistmod.datamodels.Scoreboard.ScoreboardModel;
import com.asist.asistmod.missionhelpers.enums.BlockType;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.victims.VictimsSavedManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;

import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;

public class ScoreboardManager {
	
	public static ConcurrentHashMap scoreKeeperMap = new ConcurrentHashMap<String,Integer>();	
	
	public static int regularVictimsSaved = 0;
	public static int maxRegularVictims = 0;
	
	public static int criticalVictimsSaved = 0;
	public static int maxCriticalVictims = 0;
	
	public static int maxTeamScore=0;
	public static int teamScore=0;
	
	public static int getTeamScore() {
		
		if(scoreKeeperMap.get("TeamScore") == null) {
			scoreKeeperMap.put("TeamScore",0);
			return 0;
		}
		
		return (int) scoreKeeperMap.get("TeamScore");
	}
	
	public static void addToTeamScore(int points) {
		
		int score = getTeamScore();
		scoreKeeperMap.replace("TeamScore", score+points);
	}
	
	public static void addPlayerToMap(String name) {
		ScoreboardManager.scoreKeeperMap.put(name, 0);
	}

	public static void publishScoreboardMessage() {
		
		// publish scoreboard event				
		ScoreboardModel scoreboardModel = new ScoreboardModel();			
		//header
		scoreboardModel.header.message_type = "observation";			
		// msg
		scoreboardModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		scoreboardModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;			
		//msg.data
		scoreboardModel.data.scoreboard = scoreKeeperMap;			
		InternalMqttClient.publish(scoreboardModel.toJsonString(), "observations/events/scoreboard");
	}
	
	public static void checkScoringZoneAndUpdateScore(BlockType blockType, BlockPos targetPos, String playerName, MinecraftServer server ) {
				
		int x = targetPos.getX();
		int y = targetPos.getY();
		int z = targetPos.getZ();
		
		SafeZoneEnum zone = checkSafeZone(x,y,z);
		
		if ( zone.equals(SafeZoneEnum.A)) {
			int id = MapBlockManager.getVictimId(targetPos);			
			// INCORRECT BLOCK FOR THIS SPOT will not flip to true
			boolean success = false;
			boolean saved = VictimsSavedManager.victimIsSaved(id);
			// IF CORRECT BLOCK FOR THIS SPOT
			if(blockType.equals(BlockType.VICTIM_SAVED_A)) {
				if(!saved) {
					if(id!=-1) {											
						ScoreboardManager.updateScoreboard(playerName,blockType,server);
						VictimsSavedManager.addSavedVictimId(id);
						success = true;							
					}					
				}						        					
			}
			if(!saved) {
				EvacuationModel model = new EvacuationModel(playerName,x,y,z,blockType.getName(),success);
				InternalMqttClient.publish(model.toJsonString(), "observations/events/server/victim_evacuated",playerName);
			}
			
		}		
		else if(zone.equals(SafeZoneEnum.B) ) {			
			int id = MapBlockManager.getVictimId(targetPos);
			// INCORRECT BLOCK FOR THIS SPOT will not flip to true
			boolean success = false;
			boolean saved = VictimsSavedManager.victimIsSaved(id);
			// IF CORRECT BLOCK FOR THIS SPOT
			if(blockType.equals(BlockType.VICTIM_SAVED_B)) {
				if(!saved) {
					if(id!=-1) {
						ScoreboardManager.updateScoreboard(playerName,blockType,server);
						VictimsSavedManager.addSavedVictimId(id);
						success = true;
					}					
				}						        					
			}
			if(!saved) {
				EvacuationModel model = new EvacuationModel(playerName,x,y,z,blockType.getName(),success);	
				InternalMqttClient.publish(model.toJsonString(), "observations/events/server/victim_evacuated",playerName);
			}
		}
		else if(zone.equals(SafeZoneEnum.C)) {			
			int id = MapBlockManager.getVictimId(targetPos);
			// INCORRECT BLOCK FOR THIS SPOT will not flip to true
			boolean success = false;
			boolean saved = VictimsSavedManager.victimIsSaved(id);
			// IF CORRECT BLOCK FOR THIS SPOT
			if(blockType.equals(BlockType.VICTIM_SAVED_C)) {
				if(!VictimsSavedManager.victimIsSaved(id)) {
					if(id!=-1) {					
						ScoreboardManager.updateScoreboard(playerName,blockType,server);
						VictimsSavedManager.addSavedVictimId(id);
						success = true;
					}					
				}					        					
			}
			if(!saved) {
				EvacuationModel model = new EvacuationModel(playerName,x,y,z,blockType.getName(),success);	
				InternalMqttClient.publish(model.toJsonString(), "observations/events/server/victim_evacuated",playerName);
			}
		}			
	}
	
	public static void updateScoreboard(String playerName, BlockType victimType , MinecraftServer server) {
		
		int score = (int)ScoreboardManager.scoreKeeperMap.get(playerName);		
		
		int greenScore = InternalMqttClient.modSettings.triagePoints.regular;
		int yellowScore = InternalMqttClient.modSettings.triagePoints.critical;	
		
		int pointsToAdd = 0;

		if( victimType.equals(BlockType.VICTIM_SAVED_A) || victimType.equals(BlockType.VICTIM_SAVED_B) ) {
			// increment score
			ScoreboardManager.regularVictimsSaved++;
			pointsToAdd = greenScore;
		}
		else if (victimType.equals(BlockType.VICTIM_SAVED_C)) {
			ScoreboardManager.criticalVictimsSaved++;
			pointsToAdd = yellowScore;
		}
		
		
		ScoreboardManager.teamScore += pointsToAdd;
		
		ScoreboardManager.scoreKeeperMap.replace(playerName, score+pointsToAdd);
		
		boolean displayScore = InternalMqttClient.modSettings.triageScoreVisibleToPlayer;
		
		if(displayScore) {
			server.commandManager.executeCommand(server, "xp "+pointsToAdd+"L "+ playerName);
		}
		ScoreboardManager.addToTeamScore(pointsToAdd);
		ScoreboardManager.publishScoreboardMessage();
		// UPDATE CONNECTED CLIENT SCOREBOARDS
		server.getPlayerList().getPlayers().forEach(p ->{		
				
			VictimCountUpdatePacket packet = new VictimCountUpdatePacket(
				
					ScoreboardManager.regularVictimsSaved,ScoreboardManager.maxRegularVictims,
					ScoreboardManager.criticalVictimsSaved,ScoreboardManager.maxCriticalVictims,
					ScoreboardManager.teamScore,ScoreboardManager.maxTeamScore
			);
			
			NetworkHandler.sendToClient(packet, p);		
									
		});			
	}
	
	public static enum SafeZoneEnum {A,B,C,NONE}
	
	public static SafeZoneEnum checkSafeZone (int x,int y,int z) {
		
		SafeZone[] safeZonesA = AsistMod.modSettings.safeZonesA;
		SafeZone[] safeZonesB = AsistMod.modSettings.safeZonesB;
		SafeZone[] safeZonesC = AsistMod.modSettings.safeZonesC;		
		
		for(int i = 0; i<safeZonesA.length; i++) {
			if(x >= safeZonesA[i].minX  && x <= safeZonesA[i].maxX ) {
				if(z >= safeZonesA[i].minZ  && z <= safeZonesA[i].maxZ ) {
					return SafeZoneEnum.A;
				}
			}
		}
		
		for(int i = 0; i<safeZonesB.length; i++) {
			if(x >= safeZonesB[i].minX  && x <= safeZonesB[i].maxX ) {
				if(z >= safeZonesB[i].minZ  && z <= safeZonesB[i].maxZ ) {
					return SafeZoneEnum.B;
				}
			}
		}
		
		for(int i = 0; i<safeZonesC.length; i++) {
			if(x >= safeZonesC[i].minX  && x <= safeZonesC[i].maxX ) {
				if(z >= safeZonesC[i].minZ  && z <= safeZonesC[i].maxZ ) {
					return SafeZoneEnum.C;
				}
			}
		}
		
		return SafeZoneEnum.NONE;
	}
	
	
}
