package com.asist.asistmod.eventHandlers;

import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;

import net.minecraft.server.MinecraftServer;
import net.minecraftforge.event.world.WorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class WorldUnloadEventHandler {
	
int count = 0;
	
	MinecraftServer server;
	
	ModSettings modSettings;
	
	public WorldUnloadEventHandler(ModSettings m) {
		
		modSettings = m;
		
	}
	
	@SubscribeEvent
	public void onWorldSave( WorldEvent.Unload event) {
		
	}	

}
