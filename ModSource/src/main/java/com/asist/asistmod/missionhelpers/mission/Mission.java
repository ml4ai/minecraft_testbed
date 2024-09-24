package com.asist.asistmod.missionhelpers.mission;

import java.time.Clock;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.asist.asistmod.datamodels.GroundTruth.BlockageList.BlockageListModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimsExpired.VictimsExpiredModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimsRescued.VictimsRescuedModel;
import com.asist.asistmod.datamodels.IncidentCommander.IncidentCommanderModel;
import com.asist.asistmod.datamodels.MissionState.MissionStateModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.ModSettings.PerturbationDef;
import com.asist.asistmod.datamodels.ModSettings.MinSec;
import com.asist.asistmod.datamodels.Perturbation.PerturbationModel;
import com.asist.asistmod.datamodels.PlanningStage.PlanningStageModel;
import com.asist.asistmod.datamodels.Triage.TriageModel;
import com.asist.asistmod.missionhelpers.datastructures.Player;
import com.asist.asistmod.missionhelpers.datastructures.PlayerManager;

import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager.MapBlockMode;
import com.asist.asistmod.missionhelpers.missionmessages.MessageHandler;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.WorldServer;

public class Mission {
	
	
	private static ModSettings modSettings;
	private static MinSec missionTime;
	private static int elapsedSeconds;
	private static String missionName;
	
	private static Map<String,PerturbationDef[]> perturbations = new HashMap<String,PerturbationDef[]>();


	public static boolean isActive = false;	
	private static MinecraftServer server;
	
	public static void init(MinecraftServer s, ModSettings m) {
		if(Tutorial.isActive()) { Tutorial.endTutorial(); }		

		server = s;
		modSettings = m;
		missionTime = modSettings.missionLength;
		
		// USE ENUMS INSTEAD OF STRINGS WHEN YOU HAVE TIME
		perturbations.put("blackout", modSettings.blackout_perturbation);		
		
		perturbations.put("rubble", modSettings.rubble_perturbation);		
		
		missionName = InternalMqttClient.currentTrialInfo.mission_name;
		
		System.out.println("Misssion Name : " + missionName);
		
		isActive = true;		
				
		// REMOVE QR CODE BLOCK
		server.commandManager.executeCommand(server, "fill -2156 146 20 -2154 144 20 minecraft:air");
		
		// If this is a training mission
		if(  missionName.toLowerCase().contains("training") ) {
			
			// REMOVE THE WALL THAT BLOCKS INITIAL PROGRESS
			server.commandManager.executeCommand(server, "fill -2153 60 110 -2155 62 110 minecraft:air");
		}
		// If this is a regular mission
		else {
			
			PlanningStageModel model = new PlanningStageModel("Start");
			
			InternalMqttClient.publish(model.toJsonString(), model.getTopicString());
			
		}
		
	}
	
	public static void triggerPerturbation(int min, int sec) {
		
		
		perturbations.forEach((k,v)->{
			
			for(PerturbationDef def : v) {
				
				if( missionName.contentEquals(def.triggering_mission) ) {
					
					//System.out.println(" Triggering Perutrbation via mission name :" + def.triggering_mission );
					
					if(def.getStartMinute() == min && def.getStartSecond() == sec) {
						
						System.out.println( "PERTURBATION START MATCH!");
						
						if ( k.contentEquals("blackout") ){
							
							System.out.println( "BLACKOUT KEY MATCHES");
							
							PerturbationModel message = new PerturbationModel("blackout","start");
							
							InternalMqttClient.publish(message.toJsonString(), "observations/events/mission/perturbation");
						}
						
						if ( k.contentEquals("rubble") ){
							
							System.out.println( "RUBBLE KEY MATCHES");
							
							PerturbationModel message = new PerturbationModel("rubble","start");
							
							// call MapBlockManager and place rubble
							
							InternalMqttClient.publish(message.toJsonString(), "observations/events/mission/perturbation");
							
							MapBlockManager.addBlocksFromFile("./mods/"+def.file, server.worlds[0], MapBlockMode.PERTURBATION);						
							
							BlockageListModel model = new BlockageListModel(MapBlockMode.PERTURBATION);

							MapBlockManager.addPerturbationBlockageList(model);

							InternalMqttClient.publish(model.toJsonString(), "observations/events/mission/perturbation_rubble_locations");	
							
						}
					}
					else if (def.getEndMinute() == min && def.getEndSecond() == sec) {
						
						System.out.println( "PERTURBATION END MATCHES");
						
						if ( k.contentEquals("blackout") ){
							
							System.out.println( "BLACKOUT KEY MATCHES");
							
							PerturbationModel message = new PerturbationModel("blackout","stop");
							
							InternalMqttClient.publish(message.toJsonString(), "observations/events/mission/perturbation");
							
						}
						
						// RUBBLE PERTURBATION HAS NO END
						
					}
				}				
			}			
		});
		
	}
	
	
	public static void checkPlanningEndTime(int minute, int second) {
		
		MinSec checkTime = modSettings.planningEndTime;
		
		if( minute == checkTime.minute && second == checkTime.second ) {
			
			System.out.println("Planning Stage over.");			
			// Send a planning stage over message
			
			PlanningStageModel model = new PlanningStageModel("Stop");
			
			InternalMqttClient.publish(model.toJsonString(), model.getTopicString());
			
			// REMOVE THE WALL THAT BLOCKS INITIAL PROGRESS
			server.commandManager.executeCommand(server, "fill -2153 60 110 -2155 62 110 minecraft:air");
		}
	}

	public static void endMission(MinecraftServer server) {
		
		//CHECK THIS LATER TO SEE IF CORRECT COORDS
		
		server.commandManager.executeCommand(server, "fill -2153 60 110 -2155 62 110 minecraft:bedrock");
		server.commandManager.executeCommand(server, "tp @a -2152 60 120");

		if(isActive) {
	
			isActive = false;			
		
		}

	}

}
