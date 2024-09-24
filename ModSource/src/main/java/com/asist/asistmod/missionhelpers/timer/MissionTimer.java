package com.asist.asistmod.missionhelpers.timer;

import java.time.Clock;

import com.asist.asistmod.datamodels.MissionState.MissionStateModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.ModSettings.MinSec;
import com.asist.asistmod.datamodels.Triage.TriageModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimsExpired.VictimsExpiredModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimsRescued.VictimsRescuedModel;
import com.asist.asistmod.datamodels.IncidentCommander.IncidentCommanderModel;
import com.asist.asistmod.missionhelpers.Scoreboard.CustomScoreboardWrapper;
import com.asist.asistmod.missionhelpers.chatInterventionManager.ChatInterventionManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.markingblocks.MarkingBlockManager;
import com.asist.asistmod.missionhelpers.mission.Mission;
import com.asist.asistmod.missionhelpers.pause.PauseManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MissionTimerPacket;
import com.asist.asistmod.network.messages.TriageMessagePacket;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;

import net.minecraft.server.MinecraftServer;

public class MissionTimer {
	
	private static ModSettings modSettings;
	private static MinSec[] pauseTimes;
	public static int pauseIndex=0;
	
	
	private static long startTime;
	
	private static long lastSecond;
	
	public static int secondCount;
	public static int minuteCount;
	
	// THIS IS THE AMOUNT OF MILLISECONDS ELAPSED ATER MISSION START, DISREGARDING PAUSES
	private static long elapsedMillisecondsGlobal;
	
	// THIS IS THE AMOUNT OF MILLISECONDS ELAPSED ATER MISSION START, BUT INCORPORATES TIMER (FOR TICK CHECK)
	private static long elapsedMillisecondsForTimer;
	
	// MILLISECONDS OF SLEEP BETWEEN EACH TIMER LOOP
	private static int timerSleepInterval;
	
	// THIS TRACKS WHAT OUT CURRENT SECOND IS IN MILLISECONDS SO WE CAN CHECK IF WE SHOULD TICK
	private static long secondsElapsedAsMilli = 1000;
	
	private static long lastMinute;	
	
	public static boolean isInitialized = false;
	
	public static boolean inWindDown = false;
	
	public static boolean allVictimsRescued = false;
	
	public static boolean criticalVictimsExpired = false;
	
	public static MinecraftServer server;
	
	public static Thread thread;
	
	public static boolean training = false;
	
	public static void init(MinecraftServer s, ModSettings m) {
		
		server = s;
		modSettings = m;
		pauseTimes = m.pauseTimes;
		
		String missionName = InternalMqttClient.currentTrialInfo.mission_name.toLowerCase();
		
		if ( missionName.contains("competency") || missionName.contains("training")) { 
			
		    training = true;
			minuteCount = modSettings.missionLengthTraining.minute;
			secondCount = modSettings.missionLengthTraining.second + 3;
		}
		else {
			
			minuteCount = modSettings.missionLength.minute;
			secondCount = modSettings.missionLength.second + 3;
		}
		
		
		elapsedMillisecondsGlobal = 0;
		timerSleepInterval = 5;
		
		startTime = Clock.systemDefaultZone().millis();
		
		lastSecond = startTime;
		lastMinute = startTime;
		
		// SETTING THE TIMER DISPLAY
		//server.commandManager.executeCommand(server, "scoreboard objectives add Time dummy Time");
		
		//server.commandManager.executeCommand(server, "scoreboard players set "+minuteCount+" Time " + secondCount);	
		
		//server.commandManager.executeCommand(server,"scoreboard objectives setdisplay sidebar Time");
		
		isInitialized = true;
		
		PauseManager.init(server);
		
		// timer thread
		
		thread = new Thread() {			
			public void run() {				
				while (isInitialized) {					
					try { 
						Thread.sleep(timerSleepInterval); 
					} 
					catch (InterruptedException e) {
						e.printStackTrace();
					}
					decrementTimerLoop();
				}
			}			
		};
		thread.start();
	}
	
	
	public static void decrementTimerLoop() {		
			
		if(!PauseManager.pauseOn && isInitialized) {
			
			long currentTime = Clock.systemDefaultZone().millis();
			
			elapsedMillisecondsForTimer = currentTime - startTime;			
			
			// START ONE TICK
			if( elapsedMillisecondsForTimer >= secondsElapsedAsMilli ) {
				
				System.out.println("Timer Tick " + getMissionTimeString() );

				secondsElapsedAsMilli += 1000;
				
				if(secondCount == 0) {
					
					if(minuteCount == 0) {					
						
						isInitialized = false;
						
						System.out.println("Timer has hit zero.");
						
						server.commandManager.executeCommand(server, "scoreboard objectives remove Time");
						
						// teleport players to ending area
						server.commandManager.executeCommand(server, "tp @a -2159 60 147");
						
						// MISSION STOP MESSAGE
						MissionStateModel model2 = new MissionStateModel();
						
						model2.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
						model2.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
						
						model2.data.mission = InternalMqttClient.currentTrialInfo.mission_name;
						model2.data.mission_state = "Stop";
						
						InternalMqttClient.publish(model2.toJsonString(), "observations/events/mission");
						
						inWindDown = true;
						
						minuteCount = 0;
						secondCount = 5;
						
						
					}
					else {
						secondCount = 59;
						minuteCount -- ;
					}
				}
				else {
					
					secondCount --;
				}
				/*
				// CHECK THINGS EVERY TICK
				if( !allVictimsRescued) { checkVictimsRescued(); }
				
				if (modSettings.criticalVictimsShouldExpire && !criticalVictimsExpired) {				
					checkIfVictimExpirationTime(); 
				};			
					
				checkIfScheduledPauseTime();
								
				// THESE TWO RELATE TO THE PAUSE SYSTEM: IF NO ONE IS TRIAGING SET A PAUSE FOR FOLLOWING SECOND
				checkIfTriageOverAndSetQueuedTime();
				checkIfQueuedTime();
				
				// END CHECK THINGS EVERY TICK
				
				// UPDATE SUBSCRIBERS AND PLAYERS
				new MarkingBlockManager().onMissionTimeChange(minuteCount, secondCount);				
				
				*/
				
				// PLANNING STAGE
				if ( !training ) {
					
					Mission.checkPlanningEndTime(minuteCount, secondCount);
					
					// PERTURBATION CHECK AND TRIGGER
					Mission.triggerPerturbation(minuteCount, secondCount);
					
				}				
				
				// UPDATE CHAT INTERVENTION SUBSCRIBER
				ChatInterventionManager.onMissionTimeChange(minuteCount, secondCount, getElapsedMillisecondsGlobal() );
				
				// UPDATE GUI ON ALL CLIENTS WITH THE NEW TIME
				server.getPlayerList().getPlayers().forEach(player ->{
					NetworkHandler.sendToClient(new MissionTimerPacket(minuteCount,secondCount), player);
				});
				// ENDUPDATE SUBSCRIBERS AND PLAYERS
			}// END ONE TICK
		}		
	}
	
	public static void checkIfInWindDown() {
		
		if( inWindDown) {
			
			server.commandManager.executeCommand(server, "tell @a Removing all participants in " + secondCount + " seconds.");
			
			if(secondCount == 0) {				
				if(modSettings.removePlayersOnMissionEnd) {
					server.getPlayerList().removeAllPlayers();
				}
				isInitialized = false;
				try {
					thread.join();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}				
			}			
		}		
	}
	
	public static String getMissionTimeString() {
		
		if(isInitialized) {
			return minuteCount + " : " + secondCount;
		}
		else return "Mission Timer not initialized.";
	}
	
	public static long getElapsedMillisecondsGlobal() {
		
		if (isInitialized) {
			
			return Clock.systemDefaultZone().millis() - startTime;
		}
		
		return -1;
	}
	
	/*
	public static void checkIfVictimExpirationTime() {		
		
		if(minuteCount == modSettings.criticalVictimExpirationTime.minute && secondCount == modSettings.criticalVictimExpirationTime.second) {
			
			criticalVictimsExpired = true;
			
			System.out.println("... All critical victims have expired.");
			
			// CHECK PAUSEMANAGER.playerTriageStatus for an IN_PROGRESS(0). If exists send unsuccessful TRIAGE message for each player.
			
			if( PauseManager.anyPlayersTriaging() ) {
				PauseManager.playerTriageStatus.forEach((playerName,triageInstance)->{
					if(triageInstance.triageState == 0) {
						triageInstance.triageState = 1;
						
						// Publish Unsuccessful Message
						
						TriageModel triageModel = new TriageModel();
						triageModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
						triageModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
						triageModel.data.playername = playerName;
						triageModel.data.triage_state = ClientSideTriageManager.TriageState.UNSUCCESSFUL.toString();
						triageModel.data.victim_x = triageInstance.blockPosition.getX();
						triageModel.data.victim_y = triageInstance.blockPosition.getY();
						triageModel.data.victim_z = triageInstance.blockPosition.getZ();
						
						if(triageInstance.blockType.contains("1")) {
							triageModel.data.type = "REGULAR";
						}
						else if(triageInstance.blockType.contains("2")) {
							triageModel.data.type = "CRITICAL";
						}
						
						if(InternalMqttClient.isInitialized) {
							InternalMqttClient.publish(triageModel.toJsonString(), "observations/events/player/triage");
						}	
					}
				});
			}
			
			//
			
			VictimLocations.getYellowVictimLocations().forEach(pos ->{ 
				server.commandManager.executeCommand(server, 
						"setblock "+ pos.getX() + " " + pos.getY() + " " + pos.getZ() + " asistmod:block_victim_expired");
				VictimLocations.removeYellowVictim(pos);
				server.getPlayerList().getPlayers().forEach(player ->{
					NetworkHandler.sendToClient(new VictimCountUpdatePacket(-- MapBlockManager.victimCount), player);
				});
				
			});
			
			VictimsExpiredModel model = new VictimsExpiredModel();
			
			model.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			model.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;					
			
			InternalMqttClient.publish(model.toJsonString(), "ground_truth/mission/victims_expired");
		}
	}
	*/
	public static void checkVictimsRescued() {
		
		if( VictimLocations.allVictimsRescued() ) {
				
			allVictimsRescued = true;
			// isInitialized = false;
			
			// server.commandManager.executeCommand(server, "scoreboard objectives remove Time");
			
			// teleport players to ending area
			//server.commandManager.executeCommand(server, "tp @p -2159 60 147");			
			
			VictimsRescuedModel model = new VictimsRescuedModel();
			
			model.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			model.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;					
			
			InternalMqttClient.publish(model.toJsonString(), "ground_truth/mission/victims_rescued");
			
			// MISSION STOP MESSAGE
			// MissionStateModel model2 = new MissionStateModel();
			
			// model2.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			// model2.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
			
			// model2.data.mission = "Falcon";
			// model2.data.mission_state = "Stop";
			
			// InternalMqttClient.publish(model2.toJsonString(), "observations/events/mission");
			// END MISSION STOP MESSAGE
			
			// try {
			// 	thread.join();
			// } catch (InterruptedException e) {
				// TODO Auto-generated catch block
			//	e.printStackTrace();
			//}				
		}
	}
	
	public static void checkIfScheduledPauseTime() {
		
		for(int i=pauseIndex; i<pauseTimes.length; i++) {
			
			if( pauseTimes[i].minute == minuteCount && pauseTimes[i].second == secondCount) {				
				
				if( !PauseManager.pauseQueued ) {
					if( PauseManager.anyPlayersTriaging() ) {
						System.out.println("From CheckIfSchedulePauseTime: Player Triaging, Queueing a Pause");
						PauseManager.queuePause();					
					}
					else {					
						PauseManager.pauseMissionTimer();					
					}
				}
			}
		}
	}
	
	public static void checkIfTriageOverAndSetQueuedTime() {
		
		if(PauseManager.pauseQueued && !PauseManager.anyPlayersTriaging() && PauseManager.queuedTime == null ) {
			System.out.println("From CheckIfTriageOverAndSetQueuedTime: Pause was queued, players no longer triaging. Setting a queued pause time for one second from now.");
			// SET QUEUE TIME FOR PAUSE TO THE FOLLOWING SECOND --> GIVE BLOCK BREAK EVENT A CHANCE TO HAPPEN BEFORE THREAD INTERRUPTION
			PauseManager.queuedTime = new int[] { (secondCount==0)?minuteCount-1:minuteCount,(secondCount==0)?59:secondCount-1};
		}
	}
	
	public static void checkIfQueuedTime() {
		
		if(PauseManager.queuedTime != null ) {
			//System.out.println("From CheckIfQueuedTime: Not Null -->MINUTE: "+minuteCount+"<->"+PauseManager.queuedTime[0]+" SECOND: "+secondCount+" <->"+PauseManager.queuedTime[1]);
			if(PauseManager.queuedTime[0] == minuteCount && PauseManager.queuedTime[1]==secondCount) {
				System.out.println("From CheckIfQueuedTime: MissionTimer Matches Queued Time, we should pause now");
				PauseManager.pauseMissionTimer();
				PauseManager.unqueuePause();
				PauseManager.queuedTime = null;
			}
			
		}	 
	}
	
}
