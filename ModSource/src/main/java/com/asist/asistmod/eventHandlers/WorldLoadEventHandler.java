package com.asist.asistmod.eventHandlers;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Iterator;

import com.asist.asistmod.datamodels.MapBlock.MapBlockModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager.MapBlockMode;
import com.google.gson.Gson;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;

import akka.actor.FSM.Event;
import net.minecraft.block.BlockCommandBlock;
import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.CommandBlockBaseLogic;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.tileentity.TileEntityCommandBlock;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.WorldServer;
import net.minecraftforge.client.ClientCommandHandler;
import net.minecraftforge.event.world.WorldEvent;
import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.PlayerEvent.PlayerLoggedInEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public class WorldLoadEventHandler {
	
	int count = 0;
	
	MinecraftServer server;
	
	ModSettings modSettings;
	
	public WorldLoadEventHandler(ModSettings m) {
		
		modSettings = m;
		
	}
	
	@SubscribeEvent
	public void onClientWorldLoad( WorldEvent.Load event) {
		
		server = event.getWorld().getMinecraftServer();
		
		// on the first Load Event
		
		if (count == 0) {
			
			++count;
			
			System.out.println(" --------------------------------------"); 
			System.out.println(" CLIENT MAPBLOCK FUNCTIONALITY IS ACTIVATED! ");
			System.out.println(" LOADING THE FOLLOWING BLOCKS! ");
			System.out.println(" --------------------------------------");
			
			// THIS SHOULD BE CHANGED TO SPECIFY WHAT TO LOAD FROM MODSETTINGS
			MapBlockManager.addBlocksFromFile("./mods/"+modSettings.clientSideMapBuilderMapBlockFile,event.getWorld().getMinecraftServer().worlds[0], MapBlockMode.MISSION_START);
		}		
	}	
}