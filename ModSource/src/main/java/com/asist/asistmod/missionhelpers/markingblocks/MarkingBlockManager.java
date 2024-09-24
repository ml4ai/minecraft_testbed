package com.asist.asistmod.missionhelpers.markingblocks;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.datamodels.ModSettings.MinSec;
import com.asist.asistmod.missionhelpers.timer.MissionTimerListener;

import net.minecraft.block.Block;
import net.minecraft.block.BlockStone;
import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public class MarkingBlockManager implements MissionTimerListener {
	
	public static MinecraftServer server;
	// holds all marking block, player and agent placed
	public static ConcurrentHashMap<BlockPos,IBlockState> markingBlockMemory = new ConcurrentHashMap<BlockPos,IBlockState>();
	
	// associates a start time with an agent intervention block
	public static ConcurrentHashMap<BlockPos,TimeAndBlock> startIntervention = new ConcurrentHashMap<BlockPos,TimeAndBlock>();
	
	// associates an end time with an agent intervention block
	public static ConcurrentHashMap<BlockPos,TimeAndBlock> endIntervention = new ConcurrentHashMap<BlockPos,TimeAndBlock>();	
	
	public static void linkMinecraftServer(MinecraftServer s) {
		
		server = s;
	}
	
	public static void addPlayerMarkingBlock(BlockPos pos, IBlockState blockState) {		
			
			if( !markingBlockMemory.containsKey(pos) ) {
				
				// System.out.println(" POS KEY NOT FOUND. ADDING A BLOCK TO MEMORY @ POS");			
				// System.out.println(" PRINT MARKING BLOCK MEMORY JUST BEFORE ADD");			
				// markingBlockMemory.put(pos,blockType);
				
				markingBlockMemory.put(pos,blockState);
				
				// System.out.println(" PRINT MARKING BLOCK MEMORY JUST AFTER ADD");		
				// printMarkingBlockMemory();
			}
			else {
				// System.out.println(" POS KEY ALREADY ASSIGNED. BLOCK NOT REPLACEABLE UNTIL REVERTED.");			
			}		
	}
	
	public static void addAgentMarkingBlock(BlockPos pos, IBlockState newBlockType, IBlockState oldBlockState, String startTime, String endTime ) {		
		
		if(startTime != null && !startTime.isEmpty() ) {
			
			String[] splitString = startTime.split(":");
			MinSec startTimeTrigger = new MinSec( Integer.parseInt(splitString[0]) , Integer.parseInt(splitString[1]) );
			
			startIntervention.put(pos, new TimeAndBlock(startTimeTrigger,newBlockType) );
		}
		
		if(endTime != null && !endTime.isEmpty() ) {
			
			String[] splitString = endTime.split(":");
			MinSec endTimeTrigger = new MinSec( Integer.parseInt(splitString[0]) , Integer.parseInt(splitString[1]) );
			
			endIntervention.put( pos, new TimeAndBlock(endTimeTrigger,oldBlockState));
		}
	}
	
	public static void revertMarkingBlock(BlockPos pos, World world) {
		
		// System.out.println(" PRINT MARKING BLOCK MEMORY JUST BEFORE REVERT");		
		// printMarkingBlockMemory();
		
		IBlockState revertedBlock = markingBlockMemory.get(pos);		
		world.setBlockState(pos, revertedBlock);		
		markingBlockMemory.remove(pos);
			
		
		// System.out.println(" PRINT MARKING BLOCK MEMORY JUST AFTER REVERT");		
		// printMarkingBlockMemory();		
	}
	
	public static void printMarkingBlockMemory() {
		
		StringBuilder sb = new StringBuilder();
		
		markingBlockMemory.forEach( (k,v) ->
			{				
				sb.append(k.toString());
				sb.append(" : ");
				sb.append(v.getBlock().getRegistryName().toString());
				sb.append(", ");			
			}
		);		
		System.out.println(sb.toString());		
	}
	
	public void onMissionTimeChange(int m, int s) {
		
		for( ConcurrentHashMap.Entry<BlockPos,TimeAndBlock> entry : startIntervention.entrySet() ) {
			
			if( (entry.getValue().timeTrigger.minute == m && entry.getValue().timeTrigger.second == s) || (entry.getValue().timeTrigger.minute == -1 && entry.getValue().timeTrigger.second == -1)  ) {
				
				String block_name = entry.getValue().block.getBlock().getRegistryName().toString();
				BlockPos pos = entry.getKey();
				System.out.println(" Setting "+ block_name + " at " + pos.toString() );
				
				String command = "setblock "+ 
						entry.getKey().getX() + " " + entry.getKey().getY() + " " + entry.getKey().getZ() + " " + entry.getValue().block.getBlock().getRegistryName().toString();
				
				System.out.println(command);
				
				server.commandManager.executeCommand(server, command );
				
				startIntervention.remove( entry.getKey() );				
			}			
		}
		
		for( ConcurrentHashMap.Entry<BlockPos,TimeAndBlock> entry : endIntervention.entrySet() ) {
			
			if( entry.getValue().timeTrigger.minute == m && entry.getValue().timeTrigger.second == s ) {
				
				String block_name = entry.getValue().block.getBlock().getRegistryName().toString();
				BlockPos pos = entry.getKey();
				System.out.println(" Setting "+ block_name + " at " + pos.toString() );
				
				String command = "setblock "+ 
						entry.getKey().getX() + " " + entry.getKey().getY() + " " + entry.getKey().getZ() + " " + entry.getValue().block.getBlock().getRegistryName().toString();
				
				System.out.println(command);
				
				server.commandManager.executeCommand(server, command );
				
				endIntervention.remove( entry.getKey() );				
			}			
		}		
	}
}
