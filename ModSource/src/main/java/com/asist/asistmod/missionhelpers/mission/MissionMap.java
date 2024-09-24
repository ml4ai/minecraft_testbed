package com.asist.asistmod.missionhelpers.mission;

import com.asist.asistmod.missionhelpers.datastructures.PositionRange;
import com.asist.asistmod.missionhelpers.datastructures.Position;

import net.minecraft.server.MinecraftServer;

public class MissionMap {

	PositionRange map1 = new PositionRange(-2225, 22, 60, -2083, 23, -12);
	
	PositionRange map2 = new PositionRange(-2228, 22, -14, -2086, 23, -86);
	
	Position target = new Position(-2225, 60, -11);
	
	public MissionMap() {
		
	}
	
	public void Reset(MinecraftServer server) {
		for(int height=24; height<30; height++) {
			String cloneString = "/clone -2225 " + height + " 60 -2083 " + height + " -12 -2225 " + (38+height) + " -11";
			server.commandManager.executeCommand(server, cloneString);
		}
	}
	
	public void Clone(MinecraftServer server, int map) {
		switch(map) {
			case 1:
				String cloneMap1 = "/clone " + map1.getString() + " " + target.getString();
				server.commandManager.executeCommand(server, cloneMap1);
				break;
			case 2:
				String cloneMap2 = "/clone " + map2.getString() + " " + target.getString();
				server.commandManager.executeCommand(server, cloneMap2);
				break;
			default:
				break;
		}
	}
}
