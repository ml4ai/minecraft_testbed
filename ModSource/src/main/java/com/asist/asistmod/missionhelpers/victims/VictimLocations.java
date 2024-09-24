package com.asist.asistmod.missionhelpers.victims;


import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.WorldServer;
import net.minecraftforge.fml.common.FMLLog;

public class VictimLocations {
	// Victim LOCATION SECTION
	private static CopyOnWriteArrayList<BlockPos> regularVictimLocations = new CopyOnWriteArrayList(); // concurrent array list (safe to remove an item while iterating)
	private static CopyOnWriteArrayList<BlockPos> criticalVictimLocations = new CopyOnWriteArrayList();
	private static CopyOnWriteArrayList<BlockPos> allVictimLocations = new CopyOnWriteArrayList();
	
	public static void addCriticalVictim(BlockPos bp) {
		criticalVictimLocations.add(bp);
		allVictimLocations.add(bp);
	}
	
	public static void addRegularVictim(BlockPos bp) {
		regularVictimLocations.add(bp);
		allVictimLocations.add(bp);
	}
	
	public static CopyOnWriteArrayList<BlockPos> getCriticalVictimLocations() {
		
		return criticalVictimLocations;
	}
	
	public static CopyOnWriteArrayList<BlockPos> getRegularVictimLocations() {
		
		return regularVictimLocations;
	}
	
	public static CopyOnWriteArrayList<BlockPos> getAllVictimLocations() {
		
		return allVictimLocations;
	}
	
	public static void removeRegularVictim(BlockPos pos) {
		regularVictimLocations.remove(pos);
	}
	
	public static void removeCriticalVictim(BlockPos pos) {
		criticalVictimLocations.remove(pos);
	}
	
	public static boolean allVictimsRescued() {
		return (regularVictimLocations.size() == 0) && (criticalVictimLocations.size() == 0);
	}
	// END VICTIM LOCATION SECTION
	
	// BEEP SYSTEM
	
	//public static ConcurrentHashMap<String, BlockPos> roomNameToSignalPosMap = new ConcurrentHashMap<String, BlockPos>();
	public static ConcurrentHashMap<BlockPos,SignalData> signalPosToSignalDataMap = new ConcurrentHashMap<BlockPos,SignalData>();
	
	public static String printSignalDataMap() {
		
		//System.out.println("BeepMap Count : " + signalPosToSignalDataMap.mappingCount());
		StringBuilder sb = new StringBuilder();
		
		signalPosToSignalDataMap.forEach((k,v)->{
			sb.append(k.toString());
			sb.append(" : ");
			sb.append((v.roomNames.toString()));
			sb.append("\n Victim List : \n");
			v.victimList.forEach( victimData -> {
				sb.append(victimData.printVictimData() );
				sb.append("\n");
			});
			
		});
		
		return sb.toString();
	}
	
	public static void addNewSignalPosKey(BlockPos bp, String[] roomNames) {
		
		if( !signalPosToSignalDataMap.containsKey(bp) ) {
			
			SignalData sdata = new SignalData();
			sdata.roomNames = Arrays.asList(roomNames);
			signalPosToSignalDataMap.put(bp, sdata);
			
		}
	}
	
	public static void addVictimToSignalMap(String victimType, String roomName,int victimId, BlockPos bp) {
		
		System.out.println( "in add VctimToSignalMap: " + roomName);
		signalPosToSignalDataMap.forEach((k,v)->{
			// if the roomname of the victim matches the roomname of the signal ( since there maybe multiple signals per room
			
			if( v.roomNames.contains(roomName) ) {
				System.out.println("Adding victim " + victimId + " to roomname " + roomName);
				v.victimList.add( new VictimData(victimType, bp, victimId) );
			}
		});	
		
	}
	
	public static void removeVictimFromSignalMap(int id) {
		
		System.out.println( "in removeVictimFromSignalMap: " + id);
		signalPosToSignalDataMap.forEach((k,v)->{
			// if the roomname of the victim matches the roomname of the signal ( since there maybe multiple signals per room
			List<VictimData> victimList = v.victimList;
			if (!victimList.isEmpty()) {
				for(int i = 0; i<victimList.size(); i++) {
					VictimData data = victimList.get(i);
					if(data.id == id) {
						victimList.remove(i);
						//System.out.println("Removing Signaling for ID : " + id + " room : " + v.roomName);
					}
				}
			}
			
		});		
	}
	// END BEEP SYSTEM
}


