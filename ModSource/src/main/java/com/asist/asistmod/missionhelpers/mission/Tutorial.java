package com.asist.asistmod.missionhelpers.mission;

import java.time.Clock;

import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.missionhelpers.datastructures.Player;
import com.asist.asistmod.missionhelpers.datastructures.PlayerManager;
import com.asist.asistmod.missionhelpers.datastructures.Position;
import com.asist.asistmod.missionhelpers.enums.ItemType;
import com.asist.asistmod.missionhelpers.enums.RoleType;
import com.asist.asistmod.missionhelpers.missionmessages.MessageHandler;


import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;

public class Tutorial {
	
	public static MessageHandler messageHandler;
	private static PlayerManager playerManager;
	private static int elapsedSeconds;
	private static int victimsSaved;
	private static int nVictims;
	private static boolean isActive = false;
	private static boolean isMapReset = false;
	private static int taskNumber;
	
	private static MinecraftServer server;
	private static Thread thread;
	
	public static void init(MinecraftServer s, EntityPlayer p) {
		if(Mission.isActive) { Mission.endMission(s); }		
		
		server = s;		
		messageHandler = new MessageHandler(server);
		playerManager = new PlayerManager();

		messageHandler.sendMessage("Tutorial running.", p.getName(), "green");
		
		isActive = true;
		taskNumber = 0;
		victimsSaved = 0;
		
		try { Scoreboard.Init(server); }
		catch(Exception e) { System.out.println("Scoreboard already initialized"); }	
		
		teleportToTutorial();
		
		run();
	}
	
	private static void run() {
		Timer.init(server);
		thread = new Thread() {			
			public void run() {				
				while (isActive) {					
					try { 
						Thread.sleep(5); 
					} 
					catch (InterruptedException e) {
						e.printStackTrace();
					}
					Timer.update();
					if(Timer.secondTick()) {
						elapsedSeconds = Timer.getSeconds();
						messageHandler.doMessage(elapsedSeconds);						
					}
				}
			}			
		};
		thread.start();
	}
	
	public static Player getOrCreatePlayer(EntityPlayer entityPlayer) {
		if(playerManager == null) { playerManager = new PlayerManager(); }
		Player player = playerManager.getPlayer(entityPlayer);
		return player;
	}
	
	public static void playerTaskComplete(EntityPlayer player) {
		if(playerManager.getPlayerTask(player) <= taskNumber) { 
			playerManager.playerTaskComplete(player, server); 
			doMission(player);
			if(playerManager.getCurrentTask() > taskNumber) { doNextTask(); }
		}
		else { sendWaitMessage(player); }
	}
	
	public static void doNextTask() {
		String[] messages = {};
		taskNumber++; 
		switch(taskNumber) {
			case 1:
				resetMap(1);
				messageHandler.setMessage("Use WASD to move, right click to interact");
				break;
			case 2:
				messageHandler.setMessage("Right click to open doors");
				break;
			case 3:
				messageHandler.setMessage("Use your mouse and keyboard to navigate obstacles");
				break;
			case 4:
				messageHandler.setMessage("Use a blue marker to indicate that there's rubble in the room");
				break;
			case 5:
				messageHandler.setMessage("Use a red marker to indicate that there are victims in the room");
				break;
			case 6:
				resetMap(2);
				messageHandler.setMessage("Use a green marker to indicate that the room is clear");
				break;
			case 7:
				messageHandler.setMessage("Hold left click with the hammer to break rubble");
				break;
			case 8:
				messageHandler.setMessage("Hold left click with the medical kit to save victims");
				nVictims = 3;
				break;
			case 9:
				messageHandler.setMessage("Right click with a stretcher to pick up and place victims");
				break;
			case 10:
				messageHandler.setMessage("Right click to change your role to medic; save the victims");
				nVictims = 9;
				break;
			case 11:
				messageHandler.setMessage("Right click to change your role to search specialist; move the victims");
				break;
			case 12:
				messageHandler.setMessage("Right click to change your role to hammer specialist; break the rubble");
				break;
			case 13:
				messageHandler.setMessage("Save all the victims!");
				nVictims = 8;
				break;
			default:
				break;
		}
		Scoreboard.taskComplete(); 
	}
	
	public static void victimSaved() {
		victimsSaved++;
		if(victimsSaved >= nVictims) {
			for(Player player:playerManager.players) {
				playerTaskComplete(player.getEntityPlayer());
				victimsSaved = 0;
			}
		}
	}
	
	private static void sendWaitMessage(EntityPlayer player) {
		String message = "Your teammates have not completed the previous task yet!";
		messageHandler.sendMessage(message, player.getName(), "red");
	}
	
	private static void doMission(EntityPlayer entityPlayer) {
		Player player = playerManager.getPlayer(entityPlayer);
		Position nextTaskLocation = new Position(player.getTaskNumber(), player.getPlayerNumber());
		player.teleport(nextTaskLocation, server);
		player.removeEffects();
		
		switch(player.getTaskNumber()) {
			case 1:
				player.clearInventory();
				break;
			case 2:
				player.clearInventory();
				break;
			case 3:
				player.clearInventory();
				break;
			case 4:
				player.giveItem(" adaptmod:item_marker_rubble 1 0", server);
				break;
			case 5:
				player.giveItem(" adaptmod:item_marker_victim 1 0", server);
				break;
			case 6:
				player.giveItem(" adaptmod:item_marker_clear 1 0", server);
				break;
			case 7:
				player.giveItem(ItemType.HAMMER.getCommandText(), server);
				break;
			case 8:
				player.giveItem(ItemType.MEDICALKIT.getCommandText(), server);
				break;
			case 9:
				player.giveItem(ItemType.STRETCHER.getCommandText(), server);
				break;
			case 10:
				player.clearInventory();
				break;
			case 11:
				player.clearInventory();
				break;
			case 12:
				player.clearInventory();
				break;
			case 13:
				player.clearInventory();
				break;
			case 14:
				player.clearInventory();
				break;
			default:
				player.clearInventory();
				break;
		}
	}
	
	private static void teleportToTutorial() {
		server.commandManager.executeCommand(server, "tp @a -7 23 3");
	}
	
	private static void resetMap(int half) {
		String resetCommand = "";
		if(half == 1) { resetCommand = "clone -11 22 15 70 26 26 -11 22 -1"; }
		else if(half == 2) { resetCommand = "clone 70 22 15 166 26 26 70 22 -1";}
		server.commandManager.executeCommand(server, resetCommand);
	}
	
	public static boolean isActive() {
		return isActive;
	}
	
	public static void endTutorial() {
		if(isActive) {
			isActive = false;
			Scoreboard.showMission();
			messageHandler.stopMessage();
			server.commandManager.executeCommand(server, "tp @a -2152 60 120");
			
			try {
				thread.join();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}	
		}
	}
}
