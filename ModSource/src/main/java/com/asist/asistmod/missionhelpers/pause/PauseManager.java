package com.asist.asistmod.missionhelpers.pause;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.stream.Stream;

import com.asist.asistmod.datamodels.GroundTruth.VictimsExpired.VictimsExpiredModel;
import com.asist.asistmod.datamodels.Pause.PauseModel;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager.TriageState;
import com.asist.asistmod.missionhelpers.triage.TriageInstance;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;

public class PauseManager {
	
	public static String[] pausablePlayers = {};
	public static ConcurrentHashMap<String,TriageInstance> playerTriageStatus;
	public static MinecraftServer server;
	public static boolean pauseOn = false;
	public static boolean isInitialized = false;
	public static boolean pauseQueued = false;
	public static int[] queuedTime = null;
	
	public static void init(MinecraftServer s) {
		server = s;
		playerTriageStatus = new ConcurrentHashMap<String,TriageInstance>();
		isInitialized = true;
	}
	
	public static void pauseMissionTimer() {
		
		// DO THE PAUSE STUFF
		System.out.println("We should pause now! @ " + MissionTimer.minuteCount + " : " + MissionTimer.secondCount);	
		
		PauseManager.pauseOn = true;			
		
		PauseManager.pauseAllPausablePlayers();				
		
		MissionTimer.pauseIndex++;
	}
	
	public static void unpauseMissionTimer() {
		
		if(isInitialized) {
			
			for(int i = 0; i<pausablePlayers.length; i++) {
				
				String command = "/give "+ pausablePlayers[i] + 
						" asistmod:item_first_aid 1 0 {CanDestroy:[\"asistmod:block_victim_1\",\"asistmod:block_victim_2\"]}";
				
				server.commandManager.executeCommand(server, command);			
				
			}		
			
			pauseOn = false;
			
			pauseQueued = false;
			
			PauseModel model = new PauseModel();
			
			model.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			model.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
			
			model.data.paused = pauseOn;
			
			InternalMqttClient.publish(model.toJsonString(), "observations/events/pause");
			
		}
	}
	
	public static void queuePause() {
		
		pauseQueued = true;
		
	}
	
	public static void unqueuePause() {
		
		pauseQueued = false;
		
	}
	
	public static void pauseAllPausablePlayers() {
		
		for(int i =0; i<pausablePlayers.length; i++) {
			
			// STOP MOVEMENT
			server.commandManager.executeCommand(server, "effect "+ pausablePlayers[i] +" blindness 99999 255");
			// BLINDNESS
			server.commandManager.executeCommand(server, "effect "+ pausablePlayers[i] +" slowness 99999 10");
			
			server.commandManager.executeCommand(server, "clear "+ pausablePlayers[i] +" asistmod:item_first_aid");
			
		}
		
		pauseOn = true;
		
		PauseModel model = new PauseModel();
		
		model.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		model.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		
		model.data.paused = pauseOn;
		
		InternalMqttClient.publish(model.toJsonString(), "observations/events/pause");
	}
	
	public static void addPausablePlayer(String playerName){
		
		String[] temp = new String[pausablePlayers.length+1];
		for(int i = 0; i< temp.length-1; i++ ) {
			temp[i] = pausablePlayers[i];
		}
		temp[temp.length-1] = playerName;
		pausablePlayers = temp;
		
		playerTriageStatus.put(playerName, new TriageInstance("NotInitialized", new BlockPos(0,0,0), -1) );
	}
	
	public static void updateTriageStatus(String playerName,TriageInstance instance) {
		
		if(isInitialized) {
			System.out.println("TriageStatus from PauseManager : " + instance.triageState + " BOOLEAN : " + (instance.triageState==0) );
			playerTriageStatus.put(playerName, instance);
		}
	}
	
	public static void removePausablePlayer(String playerName){
		
		String[] temp = new String[pausablePlayers.length-1];		
		int j=0;
		for(int i = 0; i< temp.length-1; i++ ) {
			j=i;
			
			if( pausablePlayers[i].contentEquals(playerName)) {
				i++;
			}
			temp[j] = pausablePlayers[i];
		}
		
		pausablePlayers = temp;
		
		playerTriageStatus.remove(playerName);
	}
	

	
	public static boolean anyPlayersTriaging(){			
		
		Stream<TriageInstance> triageInstances = playerTriageStatus.values().stream();
		
		return triageInstances.anyMatch((instance)->(instance.triageState==0));
	}

}
