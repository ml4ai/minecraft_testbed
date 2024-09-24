package com.asist.asistmod.eventHandlers;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.missionhelpers.Scoreboard.ScoreboardManager;
import com.asist.asistmod.missionhelpers.freezeManager.FreezeManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MissionTimerPacket;
import com.asist.asistmod.network.messages.TeamScoreUpdatePacket;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;

import net.minecraft.server.MinecraftServer;
import net.minecraftforge.fml.common.eventhandler.Event.Result;
import net.minecraftforge.fml.common.eventhandler.IEventListener;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.PlayerEvent.PlayerLoggedInEvent;

public class PlayerJoinEventHandler {
	
	MinecraftServer server;
	String worldName;
	
	public PlayerJoinEventHandler( MinecraftServer server) {
		this.server = server;
		this.worldName = server.worlds[0].getWorldInfo().getWorldName();
	}
	
	
	@SubscribeEvent
	public void onPlayerJoin(PlayerLoggedInEvent event) {		
		
		
		String name = event.player.getName();
		boolean isObserver = AsistMod.isObserver(name);
		
		if(!isObserver) {
			ScoreboardManager.addPlayerToMap(name);
		}		
		
		// AUTHORIZE PLAYERS
		if( InternalMqttClient.modSettings.authorizePlayers) {
			
			if( InternalMqttClient.authorizedPlayers.contains(name)) {
				
				// Players need to be OPPED to use Starting Switch, is removed after teleportation
				server.commandManager.executeCommand(server, "op " + name);
				
				System.out.println("OPPING "+ name);
				
				server.commandManager.executeCommand(server, "scoreboard teams join asist " + name);
				
				// RESET THE SCOREBAORD FOR THE PLAYER ON LOGIN
				//NetworkHandler.sendToClient(new MissionTimerPacket( 0,0 ), event.player);
				//NetworkHandler.sendToClient(new VictimCountUpdatePacket( 0 ), event.player);
				//NetworkHandler.sendToClient(new TeamScoreUpdatePacket( 0 ), event.player);
				
				if(isObserver) {					
					// IF IT'S THE ACTUAL SATURN LEVEL
					if( worldName.contains("Saturn")) {								
						System.out.println("Teleporting observer "+ name +" to observation location with rotation : -2155 144 25 179.9 90");
						System.out.println("No messages will be published for " + name );
						server.commandManager.executeCommand(server, "tp "+ name +" -2155 144 25 179.9 90");						
					}					
				}
				else {
					System.out.println("Teleporting player "+ name +" to start location : -2153 60 120");
					server.commandManager.executeCommand(server, "tp "+ name +" -2153 60 120");
				}				
			}
			else {	
				
				System.out.println("Unauthorized player " + name + " is being kicked from the server.");			
				server.commandManager.executeCommand(server, "kick " + name);
			}			
		}		
		// END AUTHORIZE PLAYERS
		else {
			
			// all we do is OP them because this is not a normal trial
			
			server.commandManager.executeCommand(server, "op " + name);	
			
		}
	}
}
