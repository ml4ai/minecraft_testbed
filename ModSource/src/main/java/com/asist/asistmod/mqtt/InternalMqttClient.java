package com.asist.asistmod.mqtt;
import java.time.Clock;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.atomic.AtomicReference;
import java.util.Set;
import java.util.UUID;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.datamodels.AgentChatIntervention.AgentChatInterventionModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.TrialInfo.TrialInfoModel;
import com.asist.asistmod.missionhelpers.chatInterventionManager.ChatInterventionManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager.MapBlockMode;
import com.asist.asistmod.missionhelpers.mapinfo.MapInfoManager;
import com.asist.asistmod.missionhelpers.markingblocks.MarkingBlockManager;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.HeadsUpChatPacket;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TextComponentTranslation;
import net.minecraft.world.WorldServer;
import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class InternalMqttClient {

	static int qos = 2;
	static String broker = "Not Set";
	static String clientId = "MinecraftInternalMqttClient";
	static MqttClient client;
	
	static MinecraftServer server;
	
	public static List<String> authorizedPlayers = new ArrayList<String>();
	
	public static TrialInfoModel currentTrialInfo = new TrialInfoModel();
	
	static Gson gson = new Gson();

	public static ModSettings modSettings;
	
	static int headsUpChatMessageId = 0;

	static MemoryPersistence persistence = new MemoryPersistence();
	
	public static boolean isInitialized = false;
	
	public static boolean blockLoadingSuccessful = false;

	public InternalMqttClient(MinecraftServer server, ModSettings modSettings) {		
		
	}
	public static void init () {
		
		try {
			client = new MqttClient("tcp://localhost:1883",clientId, persistence);
			
			MqttConnectOptions connOpts = new MqttConnectOptions();
			connOpts.setCleanSession(true);			
			System.out.println("Connecting to broker: " + broker);

			// connect
			client.connect(connOpts);
			System.out.println("Connected");
			isInitialized = true;

		} catch (MqttException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	public static void init ( ModSettings ms ) {
		
		modSettings = ms;
		broker = ms.mqtthost;
		
		FMLLog.log.info("-------------------- Attempting to start mqtt client----------------------------------");
		
		try {

			// create connection object
			client = new MqttClient(broker,clientId, persistence);

			MqttConnectOptions connOpts = new MqttConnectOptions();
			connOpts.setCleanSession(true);
			System.out.println("Connecting to broker: " + broker);

			// connect
			
			client.connect(connOpts);
			
			System.out.println("Connected");
			
			isInitialized = true;
			
		}
		
		catch (MqttException me) {

			System.out.println("reason " + me.getReasonCode());
			System.out.println("msg " + me.getMessage());
			System.out.println("loc " + me.getLocalizedMessage());
			System.out.println("cause " + me.getCause());
			System.out.println("excep " + me);
			me.printStackTrace();
		}
		
	}
	public static void linkServer ( MinecraftServer s ) {
		
		server = s;

		FMLLog.log.info("-------------------- Linking Minecraft Server object to mqtt client----------------------------------");

		try {
	
			client.subscribe("control/response/getTrialInfo", qos, (topic, message) -> {			
				
				// turn off random ticks while placing blocks to try and stop ticking world error 
				try {
					
					InternalMqttClient.blockLoadingSuccessful = false;
					
					server.commandManager.executeCommand(server, "gamerule randomTickSpeed 0");
					
					String trial_info = new String(message.getPayload());			
					
					currentTrialInfo = gson.fromJson(trial_info, TrialInfoModel.class);
					
					System.out.print( "Callsigns : ");
					System.out.print("\n");
					
					currentTrialInfo.callsigns.forEach((k,v)->{
						System.out.println(k+":"+v);
						authorizedPlayers.add(k);
					});
					
					System.out.print( "Participant IDs : ");
					System.out.print("\n");
					
					currentTrialInfo.participant_ids.forEach((k,v)->{
						System.out.println(k+":"+v);
					});
					
					//JsonObject jsonObject = gson.fromJson(trial_info, JsonObject.class);
					
					//Map<String, Object> attributes = new HashMap<String, Object>();
			        //Set<Entry<String, JsonElement>> entrySet = jsonObject.entrySet();
			        //for(Map.Entry<String,JsonElement> entry : entrySet){
			          //attributes.put(entry.getKey(), jsonObject.get(entry.getKey()));
			        //}
		
			        //for(Map.Entry<String,Object> att : attributes.entrySet()){
			            //System.out.println("key >>> "+att.getKey());
			            //System.out.println("val >>> "+att.getValue());
			            //} 
					
					
					System.out.print( "Observers : ");
					System.out.print("\n");
					
					currentTrialInfo.observer_info.forEach( n ->{
						System.out.print(n);
						authorizedPlayers.add(n);
					});
					
					System.out.print("\n");
					

					FMLLog.log.info("Experiment_ID : " + currentTrialInfo.experiment_id + " Trial_ID : " + currentTrialInfo.trial_id + " Mission_Name : " + currentTrialInfo.mission_name
							+ " Map_Name : " + currentTrialInfo.map_name + " MapBlockFile : " + currentTrialInfo.map_block_filename + " MapInfoFile : " + currentTrialInfo.map_info_filename);
					
					if( currentTrialInfo.map_info_filename != null && currentTrialInfo.map_info_filename.length()>0 ) {
						MapInfoManager.addMapInfoFromFile("./mods/"+currentTrialInfo.map_info_filename);					
					}
						
					if( currentTrialInfo.map_block_filename != null && currentTrialInfo.map_block_filename.length()>0 ) {					
						MapBlockManager.addBlocksFromFile("./mods/"+currentTrialInfo.map_block_filename, server.worlds[0],MapBlockMode.MISSION_START);					
					}
					
					// turn ticks back on to default 3
					server.commandManager.executeCommand(server, "gamerule randomTickSpeed 3");
					
					if (currentTrialInfo.active_agents != null ) {
						currentTrialInfo.active_agents.forEach( n -> {
							System.out.print("Active Agent: " + n);
							subscribeToInterventions(n);
						});
					}				
				}catch(Exception e){
					System.out.println("MQTTCLIENT ERROR - GET TRIAL INFO");
					e.printStackTrace();
				}
					//System.out.println(VictimLocations.printBeepMap());				
					
					Thread errorThread = new Thread() {			
						
						public void run() {				
							
							long elapsedMilliseconds = 0;
							long startTime = Clock.systemDefaultZone().millis();
							// WAIT 5 SECONDS TO VERIFY BLOCK LOADING CRASH DID NOT OCCUR
							while (elapsedMilliseconds <= 5000 ) {					
								try { 
									Thread.sleep(100); 
								} 
								catch (InterruptedException e) {
									e.printStackTrace();
								}						
								elapsedMilliseconds = Clock.systemDefaultZone().millis() - startTime;						
							}
							InternalMqttClient.blockLoadingSuccessful = true;
							System.out.println("Successfully Loaded MapBlocks File. No Tick Errors");
							InternalMqttClient.publish("{\"loaded\":\"100\"}", "status/minecraft/loading");
						}			
					}; // END THREAD DEFINITION
					
					errorThread.start();				
			
			}); // END SUBSCRIBE TO TOPIC		

		} // END TRY
		
		catch (MqttException me) {

			System.out.println("reason " + me.getReasonCode());
			System.out.println("msg " + me.getMessage());
			System.out.println("loc " + me.getLocalizedMessage());
			System.out.println("cause " + me.getCause());
			System.out.println("excep " + me);
			me.printStackTrace();
		}
	}

	// NO OBSERVER FILTERING
	public static void publish(String msg, String topic) {
		
		if(InternalMqttClient.isInitialized) {
			
			MqttMessage message = new MqttMessage(msg.getBytes());
			message.setQos(qos);
			try {
				client.publish(topic, message);
			} catch (MqttPersistenceException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (MqttException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			//System.out.println("Message published");
			
		}
		
	}
	
	// OBSERVER AND INTRUDER FILTERING	
	public static void publish(String msg, String topic, String playerName) {
		
		if(InternalMqttClient.isInitialized) {
			
			if ( !AsistMod.isObserver(playerName) && (InternalMqttClient.isAuthorized(playerName) || playerName.contentEquals("Server")) ) {
				
				MqttMessage message = new MqttMessage(msg.getBytes());
				message.setQos(qos);
				try {
					client.publish(topic, message);
				} catch (MqttPersistenceException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (MqttException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}			
		}		
	}
	
	public static boolean isAuthorized(String name) {
		
		return authorizedPlayers.contains(name);
	}
	
	public static String name_to_pid( String name ) {	
		
		String pid = currentTrialInfo.participant_ids.get(name);
		
		if(pid != null ) {return pid;}
		
		return "Not Set";
	}

	public static String pid_to_name (String pid) {
		
		AtomicReference<String> name = new AtomicReference<String>();
		
		name.set("Not Set");
		
		InternalMqttClient.currentTrialInfo.participant_ids.forEach((k,v) -> {
			if ( v.contentEquals(pid) ) {name.set(k);}
		});
		
		return name.get();
	}
	
	// do the same for callsign
	
	public static String name_to_callsign( String name ) {	
		
		String cs = currentTrialInfo.callsigns.get(name);
		
		if(cs != null ) {return cs;}
		
		return "Not Set";
	}
	
	public static String callsign_to_name (String cs) {
		
		AtomicReference<String> name = new AtomicReference<String>();
		
		name.set("Not Set");
		
		InternalMqttClient.currentTrialInfo.callsigns.forEach((k,v) -> {
			if ( v.contentEquals(cs) ) {name.set(k);}
		});
		
		return name.get();
	}
	
	public static void subscribeToInterventions(String agentName) {
		
		try {
			
			System.out.println( "Subscribing to interventions from : " + agentName);
			
			client.subscribe("agent/intervention/"+agentName+"/chat", qos, (topic, message) -> {
				System.out.println("HIT"  );
				String payload = new String(message.getPayload());
				System.out.println("Topic : " + topic);
				System.out.println("Message : " + payload );
				
				try {
					Gson gson = new Gson();				
					AgentChatInterventionModel model = gson.fromJson(payload, AgentChatInterventionModel.class);			
					
					model.data.receivers.forEach( r -> {
						
						// MINECRAFT CHAT
						if (model.data.renderers.contains("Minecraft_Chat")	&& model.data.content != null && !model.data.content.isEmpty()) {
								
							System.out.println("Minecraft_Chat to pid : " + r);						
							
							ChatInterventionManager.addChatIntervention(model.data.content, r ,model.data.start);						
						}					
						
					});
					
					
					
					// MINECRAFT OVERLAY
					//if (agentInterventionModel.data != null && agentInterventionModel.data.renderer != null && agentInterventionModel.data.renderer.contentEquals("Minecraft_Overlay")
							//&& agentInterventionModel.data.content != null && !agentInterventionModel.data.content.isEmpty()
							//&& agentInterventionModel.data.receiver != null && !agentInterventionModel.data.receiver.isEmpty()) {
						//EntityPlayer player = server.worlds[0].getPlayerEntityByName(agentInterventionModel.data.receiver);
						//if (player != null) {
							//System.out.println("Minecraft_Overlay");
							//NetworkHandler.sendToClient( new HeadsUpChatPacket(agentInterventionModel.data, headsUpChatMessageId++ ), player );
						//}
					//}
					
				}catch(Exception e) {
					System.out.println("--MQTTCLIENT ERROR - SUBSCRIBING TO INTERVENTIONS");
					e.printStackTrace();
				}				
			});
		}catch (MqttException me) {

			System.out.println("reason " + me.getReasonCode());
			System.out.println("msg " + me.getMessage());
			System.out.println("loc " + me.getLocalizedMessage());
			System.out.println("cause " + me.getCause());
			System.out.println("excep " + me);
			me.printStackTrace();
		}
		//client.subscribe("agent/intervention/+/block", qos, (topic, message) -> {
			
			//String payload = new String(message.getPayload());
			//System.out.println("Topic : " + topic);
			//System.out.println("Message : " + payload );
			
			//try {
				
				//Gson gson = new Gson();
			
				//AgentInterventionModel agentInterventionModel = gson.fromJson(payload, AgentInterventionModel.class);			
			
				//if (agentInterventionModel.data != null && agentInterventionModel.data.renderer.contentEquals("Minecraft_Block")
						//&& agentInterventionModel.data.block_type != null && !agentInterventionModel.data.block_type.isEmpty()
						//&& agentInterventionModel.data.receiver != null && !agentInterventionModel.data.receiver.isEmpty() ) {
					
					//int x  = agentInterventionModel.data.block_x;
					//int y  = agentInterventionModel.data.block_y;
					//int z  = agentInterventionModel.data.block_z;
					
					//BlockPos pos = new BlockPos(x,y,z);
					
					//String startTime = agentInterventionModel.data.start;
					
					//String endTime = agentInterventionModel.data.end;
					
					//String block_type = agentInterventionModel.data.block_type;
					
					//System.out.println(" Received Minecraft_Block Intervention! ");
					
					//IBlockState oldBlockState = server.worlds[0].getBlockState(pos);
					//IBlockState newBlockState = ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", block_type)).getDefaultState();
					
					//MarkingBlockManager.addAgentMarkingBlock(new BlockPos(x,y,z), newBlockState, oldBlockState, startTime,endTime);
					
					
					
					
				//}
				
				//if (agentInterventionModel.data != null && agentInterventionModel.data.renderer != null && agentInterventionModel.data.renderer.contentEquals("Minecraft_Overlay")
				//		&& agentInterventionModel.data.content != null && !agentInterventionModel.data.content.isEmpty()
				//		&& agentInterventionModel.data.receiver != null && !agentInterventionModel.data.receiver.isEmpty()) {
				//	EntityPlayer player = server.worlds[0].getPlayerEntityByName(agentInterventionModel.data.receiver);
				//	if (player != null) {
				//		System.out.println("Minecraft_Overlay");
				//		NetworkHandler.sendToClient( new HeadsUpChatPacket(agentInterventionModel.data, headsUpChatMessageId++ ), player );
				//	}
				//}
				
			//}catch(Exception e) {
				//e.printStackTrace();
			//}				
		//});
	}

}
