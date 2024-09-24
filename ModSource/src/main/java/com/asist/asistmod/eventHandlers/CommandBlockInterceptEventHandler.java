package com.asist.asistmod.eventHandlers;

import java.time.Clock;
import java.util.ArrayList;
import java.util.List;

import com.asist.asistmod.datamodels.Chat.ChatModel;
import com.asist.asistmod.datamodels.CompetencyTask.CompetencyTaskModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimList.VictimListModel;
import com.asist.asistmod.datamodels.MissionState.MissionStateModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.VictimSignal.VictimSignalModel;
import com.asist.asistmod.datamodels.Woof.WoofModel;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import net.minecraft.block.BlockDirt;
import net.minecraft.command.ICommandSender;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityLiving;
import net.minecraft.entity.item.EntityItem;
import net.minecraft.entity.passive.EntityWolf;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.item.ItemStack;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.NonNullList;
import net.minecraft.util.math.AxisAlignedBB;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockAccess;
import net.minecraftforge.event.CommandEvent;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.player.EntityItemPickupEvent;
import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.PlayerEvent.ItemPickupEvent;
import java.util.Arrays;

public class CommandBlockInterceptEventHandler {
	
	int missionStartCount = 0;
	int[] matchFill = {-2155, 62, 64, -2153, 60, 64};
	
	ModSettings modSettings;
	
	public CommandBlockInterceptEventHandler(ModSettings modSettings) {
		this.modSettings = modSettings;
	}
	
	public void publishCompetencyTaskMessage(String playerName,String taskMessage) {	
		CompetencyTaskModel model = new CompetencyTaskModel(playerName,taskMessage);		
		InternalMqttClient.publish(model.toJsonString(), "observations/events/competency/task");	
	}
	
	public void publishTrainingTaskMessage(String playerName,String taskMessage) {
		
		System.out.println("Publishing " + playerName + ":" +taskMessage + "on Bus");
		CompetencyTaskModel model = new CompetencyTaskModel(playerName,taskMessage);
		model.msg.sub_type= "Event:TrainingTask";
		model.msg.version = "2.0";
		InternalMqttClient.publish(model.toJsonString(), "observations/events/training/task");	
	}
	
	@SubscribeEvent	
	public void onCommand (CommandEvent event){
		
		ICommandSender sender = event.getSender();	
		
		MinecraftServer server = sender.getServer();
		
		String[] parameters = event.getParameters();
		
		String commandName = event.getCommand().getName();
		
		String worldName = server.worlds[0].getWorldInfo().getWorldName();		
		
		if( worldName.contains("Training")) {
			
			if( commandName.contentEquals("tp") ) {
				
				//System.out.println( "Command Name : " + commandName);
				//System.out.println( "Command Position : " + sender.getPosition());
				//System.out.println( "Params : " + String.join( " ", parameters) );
				
				// check the last 3 indexes of params
				
				int x = Integer.parseInt(parameters[1]);
				int y = Integer.parseInt(parameters[2]);
				int z = Integer.parseInt(parameters[3]);
				
				int[] tpDestination = {x,y,z};
				
				// CHECK VS provided positions
				
				//System.out.println(Arrays.toString(tpDestination));		
				
				//  -----------------------------RED---------------------------------------------------------
				if( Arrays.equals(tpDestination, new int[]{-2178, 60, 110} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Training: Start");
					
				}
				else if( Arrays.equals(tpDestination, new int[]{-2178, 60, 89} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Training: Task #1 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2204, 60, 110} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Training: Task #2 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2204, 60, 89} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Training: Task #3 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2154, 60, 72} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Training: Task #4 Complete");
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Training: End");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2152, 60, 118} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Team Training: End");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2146, 60, 109} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Competency: Start");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2146, 60, 89} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Competency: Task #1 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2120, 60, 110} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Competency: Task #2 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2120, 60, 89} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Competency: Task #3 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2120, 60, 70} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Competency: Task #4 Complete");
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Competency: End");
				}
				
			//  ----------------------------- Green ---------------------------------------------------------
				else if( Arrays.equals(tpDestination, new int[]{-2170 ,60 ,110} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Training: Start");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2170 ,60 ,89} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Training: Task #1 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2196 ,60 ,110} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Training: Task #2 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2196 ,60 ,89} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Training: Task #3 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2154 ,60 ,71} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Training: Task #4 Complete");
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Training: End");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2154 ,60 ,118} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Team Training: End");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2138 ,60 ,109} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Competency: Start");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2138 ,60 ,89} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Competency: Task #1 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2112 ,60 ,110} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Competency: Task #2 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2112 ,60 ,89} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Competency: Task #3 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2112 ,60 ,70} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Competency: Task #4 Complete");
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Competency: End");
				}
				
				//  ----------------------------- Blue ---------------------------------------------------------
				else if( Arrays.equals(tpDestination, new int[]{-2162 ,60 ,110} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Training: Start");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2162 ,60 ,89} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Training: Task #1 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2188 ,60 ,110} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Training: Task #2 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2188 ,60 ,89} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Training: Task #3 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2154 ,60 ,70} )) {
					
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Training: Task #4 Complete");
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Training: End");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2156 ,60 ,118} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Team Training: End");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2130 ,60 ,109} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Competency: Start");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2130 ,60 ,89} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Competency: Task #1 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2104 ,60 ,110} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Competency: Task #2 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2104 ,60 ,89} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Competency: Task #3 Complete");
				}
				else if( Arrays.equals(tpDestination, new int[]{-2104 ,60 ,70} )) {
					
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Competency: Task #4 Complete");
					publishCompetencyTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Competency: End");
				}
				
				//-----------RED----------------------
				//START [-2178 60 110] - START TRAINING
				// #1 [-2178 60 89] - END OF 1
				// #2 [-2204 60 110] - END OF 2
				// #3 [-2204 60 89] - END OF 3
				// #4 [-2154 60 72] - END OF 4 -- TO HOLDING AREA
				
				// SOMETHING HAPPENS
				// TEAM TRAINING START - FILL CHECK FOR WHOLE TEAMS
				// TEAM TRAINING ENDS [ -2152 60 118]
								
				// COMPETENCY TEST STARTS/ [ -2146 60 109]
				
				// END TASK 1 - [-2146 60 89]
				// END TASK 2 - [-2120 60 110]
				// END TASK 3 - [ -2120 60 89]
				// END TASK 4 / END COMP TEST - [ -2120 60 70]
				
				
				
				//-----------GREEN----------------------
				//START [-2170 60 110] - START TRAINING
				// #1 [ -2170 60 89] - END OF 1
				// #2 [-2196 60 110] - END OF 2
				// #3 [ -2196 60 89] - END OF 3
				// #4 [ -2154 60 71] - END OF 4 -- TO HOLDING AREA
				
				// SOMETHING HAPPENS
				// TEAM TRAINING START []
				// TEAM TRAINING ENDS[  -2154 60 118]
				
				// COMPETENCY TEST STARTS [ -2138 60 109]				
				
				// END TASK 1 - [ -2138 60 89]
				// END TASK 2 - [ -2112 60 110]
				// END TASK 3 - [  -2112 60 89]
				// END TASK 4 / END COMP TEST - [  -2112 60 70]				
				
				
				//-----------BLUE----------------------
				//START [-2162 60 110] - START TRAINING
				// #1 [ -2162 60 89] - END OF 1
				// #2 [ -2188 60 110] - END OF 2
				// #3 [ -2188 60 89] - END OF 3
				// #4 [ -2154 60 70] - END OF 4 -- TO HOLDING AREA
				
				// SOMETHING HAPPENS
				// TEAM TRAINING START []				
				
				// TEAM TRAINING ENDS[   -2156 60 118]
				// COMPETENCY TEST STARTS [ -2130 60 109]
				
				// END TASK 1 - [   -2130 60 89]
				// END TASK 2 - [   -2104 60 110]
				// END TASK 3 - [   -2104 60 89]
				// END TASK 4 /END COMP TEST - [  -2104 60 70]			
			}
			
			else if (commandName.contentEquals("fill" ) ) {
				
				//System.out.println( "Command Name : " + commandName);
				//System.out.println( "Command Position : " + sender.getPosition());
				//System.out.println( "Params : " + String.join( " ", parameters) );
				
				// fill -2155 62 64 -2153 60 64 air
				
				int x0 = Integer.parseInt(parameters[0]);
				int y0 = Integer.parseInt(parameters[1]);
				int z0 = Integer.parseInt(parameters[2]);
				
				int x1 = Integer.parseInt(parameters[3]);
				int y1 = Integer.parseInt(parameters[4]);
				int z1 = Integer.parseInt(parameters[5]);
				
				int[] incoming = {x0,y0,z0,x1,y1,z1};
				
				if( Arrays.equals(incoming,matchFill)) {
					// print new competency message
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Red"),"Red Team Training: Start");
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Green"),"Green Team Training: Start");
					publishTrainingTaskMessage(InternalMqttClient.callsign_to_name("Blue"),"Blue Team Training: Start");
					
				}				
			}			
		}		
	}
}
