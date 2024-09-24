package com.asist.asistmod;

import java.time.Clock;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import com.asist.asistmod.GuiOverlays.RenderGuiHandler;
import com.asist.asistmod.block._Blocks;
import com.asist.asistmod.datamodels.Chat.ChatModel;
import com.asist.asistmod.datamodels.ItemEquipped.ItemEquippedModel;
import com.asist.asistmod.datamodels.ItemPickup.ItemPickupModel;
import com.asist.asistmod.datamodels.MapBlock.MapBlockModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.ModSettings.PerturbationDef;
import com.asist.asistmod.datamodels.Observation.ObservationModel;
import com.asist.asistmod.datamodels.PlayerSprinting.PlayerSprintingModel;
import com.asist.asistmod.datamodels.PlayerSwinging.PlayerSwingingModel;
import com.asist.asistmod.datamodels.TrialInfo.ObserverInfo;
import com.asist.asistmod.datamodels.VictimSignal.VictimSignalModel;
import com.asist.asistmod.eventHandlers.AttackEntityEventHandler;
import com.asist.asistmod.eventHandlers.BlockBreakEventHandler;
import com.asist.asistmod.eventHandlers.ChatEventHandler;
import com.asist.asistmod.eventHandlers.ClientKeyboardInputEventHandler;
import com.asist.asistmod.eventHandlers.CommandBlockInterceptEventHandler;
import com.asist.asistmod.eventHandlers.CommandEventHandler;
import com.asist.asistmod.eventHandlers.EntityItemDropEventHandler;
import com.asist.asistmod.eventHandlers.EntityItemPickupEventHandler;
import com.asist.asistmod.eventHandlers.FOVUpdateEventHandler;
import com.asist.asistmod.eventHandlers.GuiScreenEventHandler;
import com.asist.asistmod.eventHandlers.ItemTossEventHandler;
import com.asist.asistmod.eventHandlers.LivingEntityUseItemEventHandler;
import com.asist.asistmod.eventHandlers.LivingHurtEventHandler;
import com.asist.asistmod.eventHandlers.LivingJumpEventHandler;
import com.asist.asistmod.eventHandlers.PlayerInteractionEventHandler;
import com.asist.asistmod.eventHandlers.PlayerJoinEventHandler;
import com.asist.asistmod.eventHandlers.TickEventHandler;
import com.asist.asistmod.eventHandlers.ToolBreakEventHandler;
import com.asist.asistmod.eventHandlers.WorldLoadEventHandler;
import com.asist.asistmod.item._Items;
import com.asist.asistmod.missionhelpers.RoomManager.RoomManager;
import com.asist.asistmod.missionhelpers.Scoreboard.ScoreboardManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mapinfo.MapInfoManager;
import com.asist.asistmod.missionhelpers.markingblocks.MarkingBlockManager;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.victims.VictimData;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.proxy.CommonProxy;
import com.asist.asistmod.tile_entity._TileEntities;
import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;
import com.mojang.authlib.GameProfile;

import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;

import akka.actor.FSM.Event;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.init.Blocks;
import net.minecraft.server.dedicated.DedicatedPlayerList;
import net.minecraft.server.dedicated.DedicatedServer;
import net.minecraft.server.gui.MinecraftServerGui;
import net.minecraft.tileentity.CommandBlockBaseLogic;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.tileentity.TileEntityCommandBlock;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.TextComponentTranslation;
import net.minecraft.world.GameType;
import net.minecraft.world.WorldServer;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.Mod.Instance;
import net.minecraftforge.fml.common.SidedProxy;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;
import net.minecraftforge.fml.common.event.FMLServerStoppedEvent;
import net.minecraftforge.fml.common.event.FMLServerStoppingEvent;
import net.minecraftforge.fml.relauncher.Side;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Timestamp;
import java.time.Clock;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import org.apache.logging.log4j.Logger;

import java.util.Iterator;

import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.BlockCommandBlock;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.multiplayer.WorldClient;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.player.PlayerSetSpawnEvent;
import net.minecraftforge.event.world.WorldEvent.CreateSpawnPosition;
import net.minecraftforge.event.world.WorldEvent.Load;
import net.minecraftforge.event.world.WorldEvent.Unload;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.event.FMLServerStartedEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.PlayerEvent.PlayerLoggedInEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.common.network.NetworkRegistry;
import net.minecraftforge.fml.common.network.simpleimpl.SimpleNetworkWrapper;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.dedicated.*;

@Mod(modid = AsistMod.MODID, version = AsistMod.VERSION)
public class AsistMod {
	
	public static final String MODID = "asistmod";
	public static final String VERSION = "2.0.9";

	public Thread thread;

	public boolean executing = true;;

	public int count = 0;

	public int obCount = 0;
	
	// has to be MinecraftServer because DedicatedServer does not exist on Client
	public static MinecraftServer server;

	public static ModSettings modSettings;	

	@Instance
	public static AsistMod instance;


	@EventHandler
	public void preInit(FMLPreInitializationEvent e) throws Exception {		

		// LOAD CUSTOM BLOCKS AND ITEMS INTO THE WORLD
		// //////////////////////////////////////////

		_Blocks.commonPreInit();
		_Items.commonPreInit();				
		_TileEntities.init();
		
		NetworkHandler.init();
		
		
		try {
			
			FileReader fileReader  = new FileReader("./mods/ModSettings.json");
			JsonReader jr = new JsonReader(fileReader);
			jr.setLenient(true);			
			Gson gson = new Gson();
			modSettings = gson.fromJson(jr, ModSettings.class);		
				
			if (modSettings != null && e.getSide() == Side.SERVER) {					

				System.out.println(
						"______________________________Reading from settings file________________________________________");
				
				System.out.println("Modsettings:clientSideMapBuilder = " + modSettings.clientSideMapBuilder);

				System.out.println("Modsettings:mqtthost = " + modSettings.mqtthost);

				System.out.println("Modsettings:observationInterval = " + modSettings.observationInterval);
				
				System.out.println("Modsettings:triageScoreVisibleToPlayer = " + modSettings.triageScoreVisibleToPlayer);
				
				System.out.println("Modsettings:authorizePlayers = " + modSettings.authorizePlayers);
				
				System.out.println("Modsettings:rubbleCollapseInterval = " + modSettings.rubbleCollapseBlockInterval);
				
				System.out.println("Modsettings:missionLength = " + modSettings.missionLength.minute + " : " + modSettings.missionLength.second);
				
				System.out.println("Modsettings:criticalVictimExpirationTime = " + modSettings.criticalVictimExpirationTime.minute + " : " + modSettings.criticalVictimExpirationTime.second);
				
				System.out.println("Modsettings:triagePoints = Regular : " + modSettings.triagePoints.regular + " , Critical : " + modSettings.triagePoints.critical);
				
				System.out.println("Modsettings:observerNames = " + Arrays.deepToString(modSettings.observerNames));
				
				for(int i = 0; i < modSettings.pauseTimes.length; i++) {
					
					System.out.println( "Pause @ "+ modSettings.pauseTimes[i].minute + " : " + modSettings.pauseTimes[i].second);
					
				}
				
				System.out.println( " Blackout Perturbation : \n");
				for(PerturbationDef def : modSettings.blackout_perturbation) {
					System.out.println( def.triggering_mission);
					System.out.println( def.start.get("minute"));
					System.out.println( def.start.get("second"));
					System.out.println( def.end.get("minute"));
					System.out.println( def.end.get("second"));
				}
				
				for(PerturbationDef def : modSettings.rubble_perturbation) {
					System.out.println( def.triggering_mission);
					System.out.println( def.start.get("minute"));
					System.out.println( def.start.get("second"));
					System.out.println( def.end.get("minute"));
					System.out.println( def.end.get("second"));
				}
				
				
				

				System.out.println( " SAFE ZONES : \n");
				
				System.out.println( " ZONE A ");
				for(int i = 0; i < modSettings.safeZonesA.length; i++) {
					
					modSettings.safeZonesA[i].printDetails(); 
					
				}
				System.out.println( " ZONE B ");
				for(int i = 0; i < modSettings.safeZonesB.length; i++) {
					
					modSettings.safeZonesB[i].printDetails(); 
					
				}
				System.out.println( " ZONE C ");
				for(int i = 0; i < modSettings.safeZonesC.length; i++) {
	
					modSettings.safeZonesC[i].printDetails(); 
	
				}
				
				System.out.println( "\n");				
				
				// GIVE INTERNAL MQTTCLIENT ABILITY TO START WITHOUT REF TO SERVER - THEN GIVE IT THE SERVER IN POSTINIT
				
				InternalMqttClient.init(modSettings);
				
				
				// WE ARE NOT DOING THIS YET (SPIRAL 2) 
				// ONLY NECESSARY IF TRACKING VICTIM LOCATION ALL THE TIME - WOULD NEED COMPLETE ROOM DEFS
				if ( modSettings.useRoomDefinitionFile ) {
					
					RoomManager.readInRoomDefs(modSettings.roomDefinitionFile);
					
					RoomManager.printRoomDefs();
					
				}
				

				try {
					jr.close();
				} catch (IOException error) {				
					error.printStackTrace();
				}				
			}
			if( modSettings != null && e.getSide() == Side.CLIENT ){
				
				System.out.println("--------------------------CLIENTSIDE MODSETTINGS------------------------------------------");			
				
				System.out.println("--------------------------"+ ( modSettings.clientSideMapBuilder ) +"------------------------------------------");
				
				if (modSettings !=null && modSettings.clientSideMapBuilder) {				
					
					System.out.println("LOADING ClientSideMapBuilder!");
					
					WorldLoadEventHandler worldLoadEventHandler = new WorldLoadEventHandler( modSettings );
					MinecraftForge.EVENT_BUS.register(worldLoadEventHandler);
				}				
							
			}
		}		
		catch(FileNotFoundException error){				
			System.out.println("----------------------ModSettings.json is not present in the Mods folder. This is fine if you are a client.-----------------");
			System.out.println("----------------------If you would like to use the clientSideMapBuilder option, place the ModSettings.json file in the mods folder.-----------------");
		}
		
		InternalMqttClient.publish("{\"loaded\":\"33\"}", "status/minecraft/loading");
		

		/////////////////////////////////////////////////////////////////////////////////////////
	}	

	@EventHandler
	public void init(FMLInitializationEvent e) {
		
		InternalMqttClient.publish("{\"loaded\":\"66\"}", "status/minecraft/loading");
		
	}

	@EventHandler
	public void postInit(FMLPostInitializationEvent e) throws Exception {
		
		// NON MODSETTINGS RELATED CLIENTSIDE INITIALIZATION		
		if( e.getSide() == Side.CLIENT ){
			
			_Items.clientPostInit();
			MinecraftForge.EVENT_BUS.register( new RenderGuiHandler() );
			MinecraftForge.EVENT_BUS.register( new ClientKeyboardInputEventHandler() );
			
		}
		
		InternalMqttClient.publish("{\"loaded\":\"90\"}", "status/minecraft/loading");

	}
	
	
	
	@EventHandler
	public void serverStoppedHandler(FMLServerStoppedEvent event) {
		
		System.out.println(event.getEventType() + "------------------------------------------------------- SERVER HAS STOPPED ------------------------------------------");
		
		// Somehow we have to determine if the stopping was due to the tick error here
		

		System.out.println("InternalMqttClient.blockLoadingSuccessful : " + InternalMqttClient.blockLoadingSuccessful);

		InternalMqttClient.publish("{\"error\":"+!InternalMqttClient.blockLoadingSuccessful+"}", "status/server/stopped");
	}
	
	

	@EventHandler
	public void serverStarting(FMLServerStartingEvent event) {
			
		
		if (event.getSide() == Side.SERVER) {
			
			FMLLog.log.info(
					"______________________________FMLServerStartingEvent RECEIVED ON SERVER SIDE________________________________________");

			FMLLog.log.info("Working Directory = " + System.getProperty("user.dir"));

			server = event.getServer();
			
			// INITIALIZE CUSTOM CLIENT --> SERVER MESSAGING SYSTEM				
			
			System.out.println( "STARTING LEVEL : " + server.worlds[0].getWorldInfo().getWorldName() );
			
			// Actual dedicated server object ... the global server object can be passed to
			// clients, but this cannot
			// and has special dedicated capabilities

			
			DedicatedServer d_server = (DedicatedServer) server;
			
			

			// suppress command block logs
			server.commandManager.executeCommand(server, "gamerule logAdminCommands false");
			server.commandManager.executeCommand(server, "gamerule commandBlockOutput false");
			server.commandManager.executeCommand(server, "gamerule sendCommandFeedback false");
			server.commandManager.executeCommand(server, "save-off");
			
			server.commandManager.executeCommand(server, "defaultgamemode a");
			
			// 2 lines below hide player names above the avatar
			// remember players need to be added to asist team when they login
			server.commandManager.executeCommand(server, "scoreboard teams add asist asist");
			server.commandManager.executeCommand(server, "scoreboard teams option asist nametagVisibility never");		

			//for (int i = 0; i < server.worlds.length; i++) {

				// don't save changes after each experiment
				//server.worlds[i].disableLevelSaving = true;
			//}

			String mapName = server.worlds[0].getWorldInfo().getWorldName();

			// SET ALL NON-ADMIN SPAWN POINTS 			
			if (mapName.contains("Competency") || mapName.contains("Training")){			  
				FMLLog.log.info("Spawn Point : 2148 60 121"); 
				server.commandManager.executeCommand(server,"setworldspawn -2148 60 121"); 
			}
			else if (mapName.contains("Falcon")) { 
				FMLLog.log.info("Spawn Point : " + modSettings.Falcon.SpawnPoint.X + " " + modSettings.Falcon.SpawnPoint.Y + " " + modSettings.Falcon.SpawnPoint.Z); 
				server.commandManager.executeCommand(server,"setworldspawn " + modSettings.Falcon.SpawnPoint.X + " " + modSettings.Falcon.SpawnPoint.Y +" " + modSettings.Falcon.SpawnPoint.Z);
			}
			else if (mapName.contains("Custom")){
				FMLLog.log.info("Spawn Point : " + modSettings.Custom.SpawnPoint.X + " " + modSettings.Custom.SpawnPoint.Y + " " + modSettings.Custom.SpawnPoint.Z); 
				server.commandManager.executeCommand(server,"setworldspawn " + modSettings.Custom.SpawnPoint.X + " " + modSettings.Custom.SpawnPoint.Y +" " + modSettings.Custom.SpawnPoint.Z); 
			}
			 
			
			InternalMqttClient.linkServer(server);			
			
			// FETCH ID's FROM CONTROL GUI
			System.out.println("Obtaining Ids from Control");
			
			InternalMqttClient.publish("{}", "control/request/getTrialInfo");
			
			MarkingBlockManager.linkMinecraftServer(server);
			
			// MAPBLOCKS TESTING SECTION ----------------------------------------------
			
			
			// USE MAPINFO AND MAPBLOCK LINES BELOW ONLY WHEN DEBUGGING OUTSIDE OF THE DOCKER TESTBED, OTHERWISE
			// COMMENT OUT. WHEN IN TESTBED THIS IS DONE IN InternalMqttClient.init() WHICH PULLS CONFIG VIA MQTT FROM CONTROL GUI.
			
			// MapInfoManager.addMapInfoFromFile("./mods/MapInfo_Hard.csv");
			// MapBlockManager.addBlocksFromFile("./mods/MapBlocks_Adapt_Jan12.csv", server.worlds[0]);
			
			// END MAPBLOCKS TESTING SECTION ---------------------------------------------

			
			///////////////////////////////////////////////////////
			
			
			// REGISTER EVENT HANDLERS ON FORGE	EVENT BUS		
			
			// Register the Chat EventHandler on the Forge message bus
			ChatEventHandler chatEventHandler = new ChatEventHandler();
			MinecraftForge.EVENT_BUS.register(chatEventHandler);

			// Register command EventHandler on the Forge message bus

			CommandEventHandler commandEventHandler = new CommandEventHandler();
			MinecraftForge.EVENT_BUS.register(commandEventHandler);

			// Register VictimState EventHandler on the Forge message bus

			PlayerInteractionEventHandler playerInteractionEventHandler = new PlayerInteractionEventHandler(server,modSettings);
			MinecraftForge.EVENT_BUS.register(playerInteractionEventHandler);
			
			AttackEntityEventHandler attackEntityEventHandler = new AttackEntityEventHandler(server,modSettings);
			MinecraftForge.EVENT_BUS.register(attackEntityEventHandler);

			// Register Block EventHandler on the Forge message bus

			BlockBreakEventHandler blockEventHandler = new BlockBreakEventHandler( server);
			MinecraftForge.EVENT_BUS.register(blockEventHandler);

			// Register ToolBreak EventHandler on the Forge message bus
			ToolBreakEventHandler toolBreakEventHandler = new ToolBreakEventHandler(server);
			MinecraftForge.EVENT_BUS.register(toolBreakEventHandler);
			
			// Register CommandBlockIntercept EventHandler on the Forge message bus

			CommandBlockInterceptEventHandler commandBlockInterceptEventHandler = new CommandBlockInterceptEventHandler( modSettings );
			MinecraftForge.EVENT_BUS.register(commandBlockInterceptEventHandler);

			// Register PlayerJoinEventHandler on the Forge message bus

			PlayerJoinEventHandler playerJoinEventHandler = new PlayerJoinEventHandler(server);
			MinecraftForge.EVENT_BUS.register(playerJoinEventHandler);

			// Register Player item pickup event handler on the Forge message bus
			EntityItemPickupEventHandler entityItemPickupEventHandler = new EntityItemPickupEventHandler(server);
			MinecraftForge.EVENT_BUS.register(entityItemPickupEventHandler);			

			// Register Player item drop event handler on the Forge message bus
			EntityItemDropEventHandler entityItemDropEventHandler = new EntityItemDropEventHandler( server);
			MinecraftForge.EVENT_BUS.register(entityItemDropEventHandler);			

			// Register ItemToss EventHandler on the Forge message bus
			ItemTossEventHandler itemTossEventHandler = new ItemTossEventHandler(server);
			MinecraftForge.EVENT_BUS.register(itemTossEventHandler);
			
			// Register Player item used event handler on the Forge message bus
			LivingEntityUseItemEventHandler livingEntityUseItemEventHandler = new LivingEntityUseItemEventHandler(server);
			MinecraftForge.EVENT_BUS.register(livingEntityUseItemEventHandler);			

			// Register Player jumped event handler on the Forge message bus
			LivingJumpEventHandler livingJumpEventHandler = new LivingJumpEventHandler( server);
			MinecraftForge.EVENT_BUS.register(livingJumpEventHandler);	
			
			LivingHurtEventHandler livingHurtEventHandler = new LivingHurtEventHandler( );
			MinecraftForge.EVENT_BUS.register(livingHurtEventHandler);	
			
			// Register Player jumped event handler on the Forge message bus
			TickEventHandler tickEventHandler = new TickEventHandler( );
			MinecraftForge.EVENT_BUS.register(tickEventHandler);
			
			

			//////////////////////////////////////////////////////////////////////////////////////////
			
			// on the first Server Starting event - because there are 3 for some reason
			if (count == 0) {

				count++;

				thread = new Thread() {

					public void run() {

						// will hold the list of players
						EntityPlayerMP[] players;

						// holds the previous position of all players to get motionX/Y/Z bug working
						ConcurrentHashMap lastPosMap = new ConcurrentHashMap<String, double[]>();

						// holds the previous equipped item for all players
						ConcurrentHashMap lastEquippedItemMap = new ConcurrentHashMap<String, String>();

						// holds the previous sprinting state for all players
						ConcurrentHashMap lastSprintingMap = new ConcurrentHashMap<String, Boolean>();

						// holds the previous swinging state for all players
						ConcurrentHashMap lastSwingingMap = new ConcurrentHashMap<String, Boolean>();

						while (executing) {
							try {

								Thread.sleep(modSettings.observationInterval);

							} catch (InterruptedException e) {

								e.printStackTrace();
							}

							DedicatedPlayerList playerList = d_server.getPlayerList();
							
							if (playerList != null) {								
								
								// THIS IS FOR THE CONCURRENCY EXCEPTION ... CANNOT ALTER LIST SIZE DURING FOREACH BUT ARRAY OK
								players = playerList.getPlayers().toArray( new EntityPlayerMP[ playerList.getCurrentPlayerCount() ] );

								for(int i = 0; i<players.length; i++) {
									
									EntityPlayerMP player = players[i];
									
									String name = player.getName();
									
									if( !isObserver(name) && InternalMqttClient.isAuthorized(name)) {
										
										obCount++;
	
																				
										double currX = player.posX;
										double currY = player.posY;
										double currZ = player.posZ;
										ResourceLocation itemResourceLoc =  ForgeRegistries.ITEMS.getKey(player.getHeldItemMainhand().getItem());
										String equippedItem = itemResourceLoc.getResourceDomain() + ":" + itemResourceLoc.getResourcePath();
										String lastEquippedItem = "";
										boolean lastSprinting = false;
										boolean lastSwinging = false;
										boolean isSprinting = player.isSprinting();
										boolean isSwinging = player.isSwingInProgress;

										
										// add name to map if doesn't yet exist
										if (!lastPosMap.containsKey(name)) {
											lastPosMap.put(name, new double[] { player.posX, player.posY, player.posZ });
										}
										
										if (!lastEquippedItemMap.containsKey(name)) {
											lastEquippedItemMap.put(name, equippedItem);
										}									
										else {
											lastEquippedItem = (String) lastEquippedItemMap.get(name);										
										}
	
										if (!lastSprintingMap.containsKey(name)) {
											lastSprintingMap.put(name, isSprinting);
										}									
										else {
											lastSprinting = (boolean) lastSprintingMap.get(name);										
										}
	
										if (!lastSwingingMap.containsKey(name)) {
											lastSwingingMap.put(name, isSwinging);
										}									
										else {
											lastSwinging = (boolean) lastSwingingMap.get(name);										
										}
										
										ObservationModel observation = new ObservationModel();
	
										// data
										observation.data.observation_number = obCount;
										observation.data.timestamp = Clock.systemUTC().instant().toString();
										observation.data.playername = name;
										observation.data.participant_id = InternalMqttClient.name_to_pid(name);
										observation.data.world_time = server.worldServerForDimension(0).getWorldTime();
										observation.data.total_time = server.worldServerForDimension(0).getTotalWorldTime();
										observation.data.entity_type = "human";
										observation.data.yaw = player.rotationYaw;
										observation.data.x = currX;
										observation.data.y = currY;
										observation.data.z = currZ;
										observation.data.pitch = player.rotationPitch;
										observation.data.id = player.getUniqueID().toString();
	
										// pull last position to compare to current to see if moving
										double[] lastPosArray = (double[]) (lastPosMap.get(name));
	
										observation.data.motion_x = currX - lastPosArray[0];
										observation.data.motion_y = currY - lastPosArray[1];
										observation.data.motion_z = currZ - lastPosArray[2];									
	
										// set last position for next loop comparison
										lastPosMap.replace(name, new double[] { currX, currY, currZ });
	
										observation.data.life = player.getHealth();
	
										InternalMqttClient.publish(observation.toJsonString(), "observations/state");
										
										if (!equippedItem.equals(lastEquippedItem)) {
											// Send a message that the last equipped item changed
											ItemEquippedModel itemEquippedModel = new ItemEquippedModel();
											itemEquippedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
											itemEquippedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
											itemEquippedModel.data.playername = name;
											itemEquippedModel.data.participant_id = InternalMqttClient.name_to_pid(name);
											itemEquippedModel.data.equippeditemname = equippedItem;
											InternalMqttClient.publish(itemEquippedModel.toJsonString(), "observations/events/player/itemequipped",name);
										} 
										lastEquippedItemMap.replace(name, equippedItem);
	
										// Sprinting
										if (isSprinting != lastSprinting) {
											// Send a message that the last equipped item changed
											PlayerSprintingModel playerSprintingModel = new PlayerSprintingModel();
											playerSprintingModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
											playerSprintingModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
											playerSprintingModel.data.playername = name;
											playerSprintingModel.data.participant_id = InternalMqttClient.name_to_pid(name);
											playerSprintingModel.data.sprinting = isSprinting;
											InternalMqttClient.publish(playerSprintingModel.toJsonString(), "observations/events/player/sprinting",name);
										}
										lastSprintingMap.replace(name, isSprinting);
	
										// Swinging
										if (isSwinging != lastSwinging) {
											// Send a message that the last equipped item changed
											PlayerSwingingModel playerSwingingModel = new PlayerSwingingModel();
											playerSwingingModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
											playerSwingingModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
											playerSwingingModel.data.playername = name;
											playerSwingingModel.data.participant_id = InternalMqttClient.name_to_pid(name);
											playerSwingingModel.data.swinging = isSwinging;
											InternalMqttClient.publish(playerSwingingModel.toJsonString(), "observations/events/player/swinging",name);
										}
										lastSwingingMap.replace(name, isSwinging);
	
									}
									
								}

							} // END IF PLAYERLIST != NULL

						} // END WHILE

					}// END RUN

				}; // End Thread Definition

				thread.start();

			} // END IF COUNT

		} // End IF SERVER

	}// End serverStarting
	
	
	public static boolean isObserver(String name) {
		
		String[] observerNames = InternalMqttClient.modSettings.observerNames;
		
		// CHECK MODSETTINGS
		if(observerNames != null) {
			for(String n : observerNames) {
				if( name.contentEquals(n) ) {
					return true;
				}
			}
		}
		
		List<String> observers = InternalMqttClient.currentTrialInfo.observer_info;
		
		// CHECK FROM GUI
		if(observers != null && observers.contains(name)) return true;
				
		return false;
	}

/////////////////////////////////////////////////////////////////////////////////////////////	

	//TO DO	
	// implement safe thread joins later ... when world unloads Join thread back
	// into main ... not really necessary as entire container is deleted after experiment
	/*
	 * @SubscribeEvent public void playerPosition(Unload event) {
	 * 
	 * System.out.println(
	 * " --------------------- Unloading World -------------------------- ");
	 * 
	 * System.out.println(
	 * " --------------------- Stopping Position Thread -------------------------- "
	 * );
	 * 
	 * try { this.worldLoadEvent.stopExecution(); this.worldLoadEvent.count = 0;
	 * this.worldLoadEvent.thread.join(); } catch (InterruptedException e) { // TODO
	 * Auto-generated catch block e.printStackTrace(); }
	 */
//////////////////////////////////////////////////////////////////////////////////////////////
}
