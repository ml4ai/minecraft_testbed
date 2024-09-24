package com.asist.asistmod.missionhelpers.missionmessages;

import java.util.List;

import com.asist.asistmod.missionhelpers.victims.VictimLocations;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.dedicated.DedicatedPlayerList;
import net.minecraft.server.management.PlayerList;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TextComponentString;

public class MessageHandler {

	private MinecraftServer server;
	private String[] messages;
	private String message;
	private String color;
	private int index;
	private int lastTime = 0;
	private int messageDuration;
	private boolean displayMessage;
	
	public MessageHandler(MinecraftServer server) {
		this.server = server;
		this.messages = new String[] {" "};
		this.color = "white";
		this.messageDuration = 120;
		this.displayMessage = false;
	}
	
	public void setNewMessage(String[] messages, String color, int duration) {
		this.messages = messages;
		this.color = color;
		this.index = 0;
		this.messageDuration = duration;
		this.displayMessage = true;
	}
	
	public void setMessage(String message) {
		this.message = message;
		this.displayMessage = true;
	}
	
	public void stopMessage() {
		this.displayMessage = false;
	}
	
	public void sendMessage(String message, String playerName, String color) {
		String newMessage = "tellraw " + playerName + " {\"text\":\"" + message + "\",\"color\":\"" + color + "\"}";	
		this.server.commandManager.executeCommand(this.server, newMessage);	
	}
	
	public void doMessage(int currentTime) {
		if (this.displayMessage && currentTime > this.lastTime) {
			String newMessage = "title @a actionbar {\"text\":\"" + message + "\"}";
			this.server.commandManager.executeCommand(this.server, newMessage);	
			this.lastTime = currentTime;
		}			
	}
	
	public void doMessages(int currentTime) {
		
		if (this.displayMessage && this.index < this.messages.length && currentTime > this.lastTime + 1) {
			if (this.index < this.messages.length-1)
			{							
				String message = "tellraw @a {\"text\":\"" + messages[index] + "\",\"color\":\"" + color + "\"}";
				this.server.commandManager.executeCommand(this.server, message);	
				this.lastTime = currentTime;
				index++;
			}
			else if (currentTime > (lastTime + 5) && currentTime < (lastTime + messageDuration + 5)) {
				String message = "title @a actionbar {\"text\":\"" + messages[index] + "\"}";
				this.server.commandManager.executeCommand(this.server, message);	
			}
			else if (currentTime > lastTime + messageDuration + 5) {
				this.displayMessage = false;
			}
			
		}
	}
	
}
