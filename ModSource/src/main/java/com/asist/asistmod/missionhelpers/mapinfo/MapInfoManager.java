package com.asist.asistmod.missionhelpers.mapinfo;

import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

import com.asist.asistmod.datamodels.MapInfo.MapInfoModel;
import com.asist.asistmod.missionhelpers.victims.VictimData;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;

import net.minecraft.block.BlockCommandBlock;
import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.CommandBlockBaseLogic;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.tileentity.TileEntityCommandBlock;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.WorldServer;
import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public class MapInfoManager {
	
	public static ConcurrentHashMap<String,CopyOnWriteArrayList<BlockPos>> doorWayMap = new ConcurrentHashMap<String,CopyOnWriteArrayList<BlockPos>>();
	
	public static void addMapInfoFromFile(String mapInfoFilename) {	
		CsvToBean<MapInfoModel> csvData = MapInfoManager.readAllDataAtOnce(mapInfoFilename);
		if (csvData == null) {
			return;
		}
		
        // print Data
		Iterator<MapInfoModel> csvUserIterator = csvData.iterator();
        FMLLog.log.info("Loading MapInfo from " + mapInfoFilename); 

        while (csvUserIterator.hasNext()) {
        	MapInfoModel mapInfoModel = csvUserIterator.next();
        	 
        	String msg = "Location: " + mapInfoModel.getLocationXYZ() + "    FeatureType = " + mapInfoModel.getFeatureType() +
        			 "    FeatureSubType = " + mapInfoModel.getFeatureSubType() + "    RoomName = " + mapInfoModel.getRoomName(); 
            FMLLog.log.info(msg); 
            
            String[] coords = mapInfoModel.getLocationXYZ().split("\\s+");
          
            if (mapInfoModel.getFeatureType().contentEquals("doorway")) {
            	if (!doorWayMap.containsKey(mapInfoModel.getRoomName())) {
            		CopyOnWriteArrayList<BlockPos> doorWayList = new CopyOnWriteArrayList<BlockPos>();
            		doorWayList.add(new BlockPos(Integer.parseInt(coords[0]), Integer.parseInt(coords[1]), Integer.parseInt(coords[2])));
            		
            		doorWayMap.put(mapInfoModel.getRoomName(), doorWayList);
            	}
            	else {
            		CopyOnWriteArrayList<BlockPos> doorWayList = doorWayMap.get(mapInfoModel.getRoomName());
            		doorWayList.add(new BlockPos(Integer.parseInt(coords[0]), Integer.parseInt(coords[1]), Integer.parseInt(coords[2])));            		
            	}
            }
        }    
        
        FMLLog.log.info("Finished loading MapInfo from " + mapInfoFilename);         
	}

    public static CsvToBean<MapInfoModel> readAllDataAtOnce(String file) 
    { 
        try { 
  
            FileReader filereader = new FileReader(file); 
  
            // create csvReader object and skip first Line 
           
            CsvToBean<MapInfoModel> csvToBean = new CsvToBeanBuilder(filereader)
                    .withType(MapInfoModel.class)
                    .withIgnoreLeadingWhiteSpace(true)
                    .withIgnoreEmptyLine(true)
                    .build();
  
            return csvToBean;
        } 
        catch (Exception e) { 
            e.printStackTrace(); 
            return null;
        }        
    }
}
