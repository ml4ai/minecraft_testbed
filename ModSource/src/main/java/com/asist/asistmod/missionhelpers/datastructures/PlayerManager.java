package com.asist.asistmod.missionhelpers.datastructures;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;

public class PlayerManager {

	public static List<Player> players = new ArrayList<Player>();
	private static int nPlayers = 0 ;		
	public static int getPlayerTask(EntityPlayer entityPlayer) {
		Player player = getPlayer(entityPlayer);
		return player.getTaskNumber();
	}
	
	public static int getCurrentTask() {
		int taskNumber = 0;
		for(Player player:players) {
			if(taskNumber == 0) { taskNumber = player.getTaskNumber(); }
			else { taskNumber = player.getTaskNumber() < taskNumber ? player.getTaskNumber() : taskNumber; }
		}
		return taskNumber;
	}
	
	public static void playerTaskComplete(EntityPlayer entityPlayer, MinecraftServer server) {
		Player player = getPlayer(entityPlayer);
		player.taskComplete(server);
	}
	
	public static Player getPlayer(int playerNumber) {
		for(Player player:players) {
			if(player.getPlayerNumber() == playerNumber) {
				return player;
			}
		}
		return null;
	}
	
	public static Player getPlayer(EntityPlayer entityPlayer) {
		
		String playerName = entityPlayer.getName();
		for(Player player:players) {
			if(player.getName().equals(playerName)) {
				return player;
			}
		}		
		nPlayers++;
		Player newPlayer = new Player(entityPlayer, nPlayers);
		players.add(newPlayer);
		return newPlayer;
	}
	
	public static Player getPlayerByName(String name) {
		
		Player out = null;
		
		for(Player player:players) {
			if(player.getName().contentEquals(name)) {
				out = player;
			}
		}
		
		return out;
	}
	
}
