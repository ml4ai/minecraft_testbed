package com.asist.asistmod.eventHandlers;

import java.util.HashMap;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.block.BlockVictimBase;
import com.asist.asistmod.block.BlockVictim_1;
import com.asist.asistmod.block.BlockVictim_2;
import com.asist.asistmod.datamodels.MarkerRemoved.MarkerRemovedModel;
import com.asist.asistmod.datamodels.RubbleDestroyed.RubbleDestroyedModel;
import com.asist.asistmod.datamodels.Scoreboard.ScoreboardModel;
import com.asist.asistmod.datamodels.Triage.TriageModel;
import com.asist.asistmod.missionhelpers.Scoreboard.ScoreboardManager;
import com.asist.asistmod.missionhelpers.datastructures.Player;
import com.asist.asistmod.missionhelpers.datastructures.PlayerManager;
import com.asist.asistmod.missionhelpers.enums.BlockType;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mission.Mission;
import com.asist.asistmod.missionhelpers.mission.Scoreboard;
import com.asist.asistmod.missionhelpers.mod.ModBlocks;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.missionhelpers.victims.VictimsSavedManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.TeamScoreUpdatePacket;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;
import com.asist.asistmod.tile_entity.VictimBlockTileEntity;
import com.google.gson.Gson;

import net.minecraft.block.Block;
import net.minecraft.block.BlockLever;
import net.minecraft.block.BlockPrismarine;
import net.minecraft.block.state.IBlockState;
import net.minecraft.command.ICommandManager;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.Blocks;
import net.minecraft.item.ItemStack;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.event.world.BlockEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public class BlockBreakEventHandler {
	
MinecraftServer server;

String worldName;

boolean displayScore;

	public BlockBreakEventHandler(MinecraftServer server) {
		
		this.server = server;		
		worldName = server.worlds[0].getWorldInfo().getWorldName();
		displayScore = InternalMqttClient.modSettings.triageScoreVisibleToPlayer;
	}
	
	@SubscribeEvent	
	public void onBlockBreakEvent( BlockEvent.BreakEvent event) {		
		
		EntityPlayer entityPlayer = event.getPlayer();
		String playerName = entityPlayer.getName();
		
		IBlockState blockState = event.getState();
		Block block = blockState.getBlock();
		
		String blockName = block.getRegistryName().toString();

		BlockType modBlock = ModBlocks.getEnum(blockState);
		BlockPos blockPos = event.getPos();
		ItemStack toolItem = entityPlayer.getHeldItemMainhand();
		MinecraftServer server = event.getWorld().getMinecraftServer();
		World world = event.getWorld();
		
		
		// MARKER BLOCKS ACCIDENTALLY BROKEN BY RUBBLE
		
		if( PlayerInteractionEventHandler.isCustomCarpetBlockFromRegistryName(blockName) && !world.isRemote ) {
			
			System.out.println("----------------Removing marker broken during rubble placement----------------------------");
			
			String[] split = blockName.split("[_:]");
			
			MarkerRemovedModel markerRemovedModel = new MarkerRemovedModel();
			markerRemovedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			markerRemovedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
			markerRemovedModel.data.playername = "server";
			markerRemovedModel.data.participant_id = "server";
			markerRemovedModel.data.type = split[3] + "_" + split[4];
			markerRemovedModel.data.marker_x = blockPos.getX();
			markerRemovedModel.data.marker_y = blockPos.getY();
			markerRemovedModel.data.marker_z = blockPos.getZ();
			InternalMqttClient.publish(markerRemovedModel.toJsonString(), "observations/events/player/marker_removed", playerName);
			
		}

		
		// VICTIMS
		if( block instanceof BlockVictimBase && !world.isRemote ) {	
			
			int id = MapBlockManager.getVictimId(blockPos);	
			
			// COMMON VICTIM CODE										
			TriageModel triageModel = new TriageModel();
			triageModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			triageModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
			triageModel.data.playername = playerName;
			triageModel.data.participant_id = InternalMqttClient.name_to_pid(playerName);
			triageModel.data.triage_state = ClientSideTriageManager.TriageState.SUCCESSFUL.name();
			triageModel.data.victim_x = blockPos.getX();
			triageModel.data.victim_y = blockPos.getY();
			triageModel.data.victim_z = blockPos.getZ();
			triageModel.data.victim_id = id;	
			triageModel.data.type = modBlock.getName();
			
			// CHECK IF YOU ARE A VICTIM BLOCK IN A SCOREING AREA
			
			// HERE WE CHECK IF THIS IS THE CORRECT SCORING AREA AND INCREMENT THE SCORE IF SO
			
			BlockType replacementBlock = BlockType.NULL;
			if( modBlock.equals(BlockType.VICTIM_A)){replacementBlock = BlockType.VICTIM_SAVED_A;}
			else if (modBlock.equals(BlockType.VICTIM_B)){replacementBlock = BlockType.VICTIM_SAVED_B;}
			else if (modBlock.equals(BlockType.VICTIM_C)){replacementBlock = BlockType.VICTIM_SAVED_C;}
			
			// CHECK IF THEY SCORED
			ScoreboardManager.checkScoringZoneAndUpdateScore(replacementBlock, blockPos, playerName, server);	
			
			// UPDATE SIGNAL MAP AS IF VICTIM NO LONGER IN ROOM ( NOT TRACKING LOCATION THE WHOLE GAME JUST FIRST INTERACTION)			
			VictimLocations.removeVictimFromSignalMap(id);			
			
			if (worldName.contains("Competency")) {	
				
				int score = (int)ScoreboardManager.scoreKeeperMap.get(playerName);
				
				if( modBlock.getName().contentEquals("victim_a") || modBlock.getName().contentEquals("victim_b") ) {
					
					VictimLocations.removeRegularVictim(blockPos);				
					
				}
				else if(modBlock.getName().contentEquals("victim_c")) {
					
					VictimLocations.removeCriticalVictim(blockPos);					
				}
				
				if(displayScore) {
					server.commandManager.executeCommand(server, "xp 1L "+ playerName);
				}
				ScoreboardManager.scoreKeeperMap.replace(playerName, score+1);
				ScoreboardManager.addToTeamScore(1);
				
			}
			
			
			// MORE COMMON VICTIM CODE
			if(InternalMqttClient.isInitialized) {
				InternalMqttClient.publish(triageModel.toJsonString(), "observations/events/player/triage", playerName);
				
			}			
	
		}			
		
		// GRAVEL
		if( blockState.getBlock().equals(Blocks.GRAVEL) ){
			
			if( (toolItem.getItemDamage() == toolItem.getMaxDamage()-1) ) {
				Player player = PlayerManager.getPlayer(entityPlayer);
				player.removeEffects();
			}
			
			RubbleDestroyedModel rubbleDestroyedModel = new RubbleDestroyedModel();
			rubbleDestroyedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			rubbleDestroyedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
			rubbleDestroyedModel.data.playername = playerName;
			rubbleDestroyedModel.data.participant_id =InternalMqttClient.name_to_pid(playerName);
			rubbleDestroyedModel.data.rubble_x = blockPos.getX();
			rubbleDestroyedModel.data.rubble_y = blockPos.getY();
			rubbleDestroyedModel.data.rubble_z = blockPos.getZ();
			InternalMqttClient.publish(rubbleDestroyedModel.toJsonString(), "observations/events/player/rubble_destroyed", playerName);
		}		
		
	}		
}