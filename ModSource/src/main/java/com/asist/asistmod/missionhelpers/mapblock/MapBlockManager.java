package com.asist.asistmod.missionhelpers.mapblock;

import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

import com.asist.asistmod.block.BlockRubble_Collapse;
import com.asist.asistmod.datamodels.GroundTruth.BlockageList.BlockageListBlockage;
import com.asist.asistmod.datamodels.GroundTruth.BlockageList.BlockageListModel;
import com.asist.asistmod.datamodels.GroundTruth.FreezeBlockList.FreezeBlockListItem;
import com.asist.asistmod.datamodels.GroundTruth.FreezeBlockList.FreezeBlockListModel;
import com.asist.asistmod.datamodels.GroundTruth.ThreatSignList.ThreatSignListItem;
import com.asist.asistmod.datamodels.GroundTruth.ThreatSignList.ThreatSignListModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimList.VictimListModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimList.VictimListVictim;
import com.asist.asistmod.datamodels.MapBlock.MapBlockModel;
import com.asist.asistmod.datamodels.PositionRange.PositionRangeModel;
import com.asist.asistmod.datamodels.MissionState.MissionStateModel;
import com.asist.asistmod.datamodels.ModSettings.TriagePointMapping;
import com.asist.asistmod.missionhelpers.Scoreboard.ScoreboardManager;
import com.asist.asistmod.missionhelpers.mapinfo.MapInfoManager;
import com.asist.asistmod.missionhelpers.rubble_collapse.RubbleCollapseManager;
import com.asist.asistmod.missionhelpers.victims.SignalData;
import com.asist.asistmod.missionhelpers.victims.VictimData;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.google.common.collect.HashBiMap;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;

import net.minecraft.block.Block;
import net.minecraft.block.BlockCommandBlock;
import net.minecraft.block.state.BlockStateContainer;
import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.CommandBlockBaseLogic;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.tileentity.TileEntityCommandBlock;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraft.world.WorldServer;
//import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public class MapBlockManager {
	
	public static CopyOnWriteArrayList<MapBlockModel> victimList = new CopyOnWriteArrayList<MapBlockModel>();
	public static CopyOnWriteArrayList<MapBlockModel> blockageList = new CopyOnWriteArrayList<MapBlockModel>();
	public static CopyOnWriteArrayList<MapBlockModel> perturbationBlockageList = new CopyOnWriteArrayList<MapBlockModel>();
	public static CopyOnWriteArrayList<MapBlockModel> freezeBlockList = new CopyOnWriteArrayList<MapBlockModel>();
	public static CopyOnWriteArrayList<MapBlockModel> threatSignList = new CopyOnWriteArrayList<MapBlockModel>();
	
	public static ConcurrentHashMap<BlockPos,Integer> victimIdMap = new ConcurrentHashMap<BlockPos,Integer>();	
	
	public static int uniqueVictimIdCounter=0;
	
	public static enum MapBlockMode{MISSION_START,PERTURBATION}

	public static void addBlocksFromFile(String blockFilename, WorldServer world, MapBlockMode mode) {

	
		MinecraftServer server = world.getMinecraftServer();
		
		CsvToBean<MapBlockModel> csvData = MapBlockManager.readAllDataAtOnce(blockFilename);
		if (csvData == null) {
			return;
		}
		
        // print Data
		Iterator<MapBlockModel> csvUserIterator = csvData.iterator();
        
		System.out.println("Adding MapBlocks from " + blockFilename);
        
        int count = 0;
        
        while (csvUserIterator.hasNext()) {
        	
        	count ++;
        	MapBlockModel mapBlockModel = csvUserIterator.next();
        	 
        	String msg = "Location: " + mapBlockModel.getLocationXYZ() + "    BlockType = " + mapBlockModel.getBlockType() +
        			 "    Command = " + mapBlockModel.getCommand() + "    CommandOption = " + mapBlockModel.getCommandOptions() +
        			 "    RoomName = " + mapBlockModel.getRoomName() + "    FeatureType = " + mapBlockModel.getFeatureType();                     	 
        	System.out.println(msg); 
            
            String[] coords = mapBlockModel.getLocationXYZ().split("\\s+");
            String blockType = mapBlockModel.getBlockType();
            BlockPos bp = new BlockPos(Integer.parseInt(coords[0]), Integer.parseInt(coords[1]), Integer.parseInt(coords[2]));
            IBlockState block;
            
            Boolean shouldPlace = true;
            
            if (coords.length == 3) {
            	
            	// FOR ASISTMOD CUSTOM BLOCKS
            	if( blockType.contains("block_victim") || blockType.contains("block_freeze") 
            			|| blockType.contains("block_rubble") || blockType.contains("block_signal") ){
            		
            		block = ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", mapBlockModel.getBlockType())).getDefaultState();
            		BlockPos blockPos = new BlockPos(Integer.parseInt(coords[0]), Integer.parseInt(coords[1]), Integer.parseInt(coords[2]));
            		
					if (blockType.contains("block_victim")) {
            			
            			victimList.add(mapBlockModel);
            			
            			victimIdMap.put(bp,++uniqueVictimIdCounter);
            			
            			if (blockType.contains("block_victim_1")) {
            				
                			VictimLocations.addRegularVictim(bp);
                			
                			VictimLocations.addVictimToSignalMap("block_victim_1",mapBlockModel.getRoomName(),uniqueVictimIdCounter,bp);
                			
                			ScoreboardManager.maxRegularVictims++;
                			
                			System.out.println("ScoreboardManager.maxRegularVictims : " + ScoreboardManager.maxRegularVictims);
                		}
                		else if (blockType.contains("block_victim_2")  || blockType.contains("block_victim_proximity")) {
                			
                			VictimLocations.addCriticalVictim(bp);
                			
                			VictimLocations.addVictimToSignalMap("block_victim_2",mapBlockModel.getRoomName(),uniqueVictimIdCounter,bp);
                			
                			ScoreboardManager.maxCriticalVictims++;
                			
                			System.out.println("ScoreboardManager.maxCriticalVictims : " + ScoreboardManager.maxCriticalVictims);
                		}
            		}
            		
            		else if (blockType.contains("block_freeze")) {
            			freezeBlockList.add(mapBlockModel);
            		}
            		
            		else if (blockType.contains("block_signal")) {
            			
            			String[] splitRooms = mapBlockModel.getRoomName().split("-");
            			
            			
            			VictimLocations.addNewSignalPosKey(bp, splitRooms);
            		}
					
					else if (blockType.contains("block_rubble")) {
						
						System.out.println("Rubble: Options = " + mapBlockModel.getCommandOptions());
						
						if (block.getBlock() instanceof BlockRubble_Collapse && !mapBlockModel.getCommandOptions().isEmpty()) {							
							
							// link the rubblecollapse block with the rubble area
							RubbleCollapseManager.createCollapseLink(blockPos, new PositionRangeModel(mapBlockModel.getCommandOptions()) );
							
							// set all times to 0 as naturally no one will hit the first collapse block in 5 seconds
							RubbleCollapseManager.setCollapseTime(blockPos, 0L);
							
							threatSignList.add(mapBlockModel);

						}
					}
            	}
            	
            	// FOR MINECRAFT BLOCKS
            	else {            		
            		block = ForgeRegistries.BLOCKS.getValue(new ResourceLocation("minecraft", mapBlockModel.getBlockType())).getDefaultState();            		
            		
            		if ( mapBlockModel.getFeatureType().contentEquals("obstruction") ) {            			
            			
            			blockageList.add(mapBlockModel);
            			
            			if(mode.equals(MapBlockMode.PERTURBATION)) {
            				
            				perturbationBlockageList.add(mapBlockModel);            				
            				
            			}
            		};
            	}
				
				BlockPos blockPos = new BlockPos(Integer.parseInt(coords[0]), Integer.parseInt(coords[1]), Integer.parseInt(coords[2]));
				
				//System.out.println(count + " : " + blockType + " : " + blockPos.toString());
				
				try {
					System.out.println("Block # :" + count);
					
					IBlockState blockState = world.getBlockState(blockPos);
					Block _block = blockState.getBlock();					
					
					/*
					 *if( _block == null ) {
						System.out.println("Block was null ( we're going too fast? )" );
						_block = blockState.getBlock();
					}
					
					
					ResourceLocation resourceLocation = _block.getRegistryName();
					if( resourceLocation == null ) {
						System.out.println("Resource Location was null ( we're going too fast? )" );
						System.out.println(_block.getLocalizedName() );
						resourceLocation = _block.getRegistryName();
					}
					*/
					
					String type = _block.getLocalizedName().toLowerCase();
					
					//String type = world.getBlockState(blockPos).getBlock().getRegistryName().toString();
					if ( blockType.contentEquals("gravel") ) {						
						if ( type.contains("air") || type.contains("door") ) {
							world.setBlockState(blockPos, block);
						}
						else {
							System.out.println( " Trying to place gravel, but encountered a non air or door block of type " + type );
						}						
					}
					else {
						world.setBlockState(blockPos, block);
					}
					
				}catch(Exception e){
					System.out.println("--MAPBLOCKS ERROR - #1");
					e.printStackTrace();
				}
								
				/*
				if (block.getBlock() instanceof BlockCommandBlock && !mapBlockModel.getCommand().isEmpty()) {					
					BlockCommandBlock commandBlock = (BlockCommandBlock) block.getBlock();					
					boolean hasTileEntity = commandBlock.hasTileEntity(block);
					TileEntity tileEntity = world.getTileEntity(blockPos);
					
					if (tileEntity instanceof TileEntityCommandBlock) {					
						TileEntityCommandBlock tileEntityCommandBlock = (TileEntityCommandBlock) tileEntity;						
						CommandBlockBaseLogic logic = tileEntityCommandBlock.getCommandBlockLogic();
						logic.setCommand(mapBlockModel.getCommand());
						
						// Process command block options
			            String[] commandOptions = mapBlockModel.getCommandOption().split("\\|");
			            for (String commandOption : commandOptions) {
							commandOption = commandOption.trim();
							if (commandOption.contains("Conditional")) {
								block = block.withProperty(BlockCommandBlock.CONDITIONAL, true);								
								world.setBlockState(blockPos, block);
							}
							else if (commandOption.contains("Unconditional")) {
								block = block.withProperty(BlockCommandBlock.CONDITIONAL, false);								
								world.setBlockState(blockPos, block);								
							}
							else if (commandOption.contains("AlwaysActive")) {
								tileEntityCommandBlock.setAuto(true);
							}
							else if (commandOption.contains("NeedsRedstone")) {
								tileEntityCommandBlock.setAuto(false);								
							}						
						}
					}
				}
				*/
            }
        }
        
        try {
        	TriagePointMapping points = InternalMqttClient.modSettings.triagePoints;
        	
        	if(  InternalMqttClient.currentTrialInfo.mission_name.toLowerCase().contains("training") ) {
        		ScoreboardManager.maxRegularVictims -= 4;
        		ScoreboardManager.maxCriticalVictims -= 2;        	
        	}
        	
        	ScoreboardManager.maxTeamScore = (ScoreboardManager.maxRegularVictims*points.regular) + (ScoreboardManager.maxCriticalVictims*points.critical);
        
        	System.out.println( "Placed " + count + " blocks.");
        }catch(Exception e) {
        	System.out.println("--MAPBLOCKS ERROR - #2");
        	e.printStackTrace();
        }
        
        // FOR DEBUGGING VICTIM ID's
        //victimIdMap.forEach((k,v)->{
        	//System.out.println( k.toString() + ":" + v);
        //});
	}

    public static CsvToBean<MapBlockModel> readAllDataAtOnce(String file) 
    { 
        try { 
  
            FileReader filereader = new FileReader(file); 
  
            // create csvReader object and skip first Line 
           
            CsvToBean<MapBlockModel> csvToBean = new CsvToBeanBuilder(filereader)
                    .withType(MapBlockModel.class)
                    .withIgnoreLeadingWhiteSpace(true)
                    .withIgnoreEmptyLine(true)
                    .build();
  
            return csvToBean;
        } 
        catch (Exception e) { 
        	System.out.println("--MAPBLOCKS ERROR - #0");
            e.printStackTrace(); 
            return null;
        }        
    }

    
    // alters the incoming model as it's passed by reference, hence no return value 
	public static void addVictimList(VictimListModel model) {
		
		model.data.mission_victim_list.clear();
		
		for (MapBlockModel mapBlockModel : victimList) {
			VictimListVictim victimListVictim = new VictimListVictim();
            String[] coords = mapBlockModel.getLocationXYZ().split("\\s+");
            if (coords.length == 3) {
            	victimListVictim.x = Double.parseDouble(coords[0]);
            	victimListVictim.y = Double.parseDouble(coords[1]);
            	victimListVictim.z = Double.parseDouble(coords[2]);
            }
            victimListVictim.block_type = mapBlockModel.getBlockType();
            victimListVictim.room_name = mapBlockModel.getRoomName();
            victimListVictim.unique_id = victimIdMap.get(new BlockPos(victimListVictim.x,victimListVictim.y,victimListVictim.z));
            
			model.data.mission_victim_list.add(victimListVictim);
		}
	}
	
	// alters the incoming model as it's passed by reference, hence no return value 
	public static void addBlockageList(BlockageListModel model) {
		model.data.mission_blockage_list.clear();
		
		for (MapBlockModel mapBlockModel : blockageList) {
			BlockageListBlockage blockageListBlockage = new BlockageListBlockage();
            String[] coords = mapBlockModel.getLocationXYZ().split("\\s+");
            if (coords.length == 3) {
            	blockageListBlockage.x = Double.parseDouble(coords[0]);
            	blockageListBlockage.y = Double.parseDouble(coords[1]);
            	blockageListBlockage.z = Double.parseDouble(coords[2]);
            }
            blockageListBlockage.block_type = mapBlockModel.getBlockType();
            blockageListBlockage.room_name = mapBlockModel.getRoomName();
            blockageListBlockage.feature_type = mapBlockModel.getFeatureType();
            
			model.data.mission_blockage_list.add(blockageListBlockage);
		}
	}
	
	public static void addPerturbationBlockageList(BlockageListModel model) {
		
		model.data.mission_blockage_list.clear();
		
		for (MapBlockModel mapBlockModel : perturbationBlockageList) {
			BlockageListBlockage blockageListBlockage = new BlockageListBlockage();
            String[] coords = mapBlockModel.getLocationXYZ().split("\\s+");
            if (coords.length == 3) {
            	blockageListBlockage.x = Double.parseDouble(coords[0]);
            	blockageListBlockage.y = Double.parseDouble(coords[1]);
            	blockageListBlockage.z = Double.parseDouble(coords[2]);
            }
            blockageListBlockage.block_type = mapBlockModel.getBlockType();
            blockageListBlockage.room_name = mapBlockModel.getRoomName();
            blockageListBlockage.feature_type = mapBlockModel.getFeatureType();
            
			model.data.mission_blockage_list.add(blockageListBlockage);
		}
	}
	
	// alters the incoming model as it's passed by reference, hence no return value 
	public static void addFreezeBlockList (FreezeBlockListModel model) {
		
		model.data.mission_freezeblock_list.clear();
		
		for (MapBlockModel mapBlockModel : freezeBlockList) {
			FreezeBlockListItem freezeBlockListItem = new FreezeBlockListItem();
            String[] coords = mapBlockModel.getLocationXYZ().split("\\s+");
            if (coords.length == 3) {
            	freezeBlockListItem.x = Double.parseDouble(coords[0]);
            	freezeBlockListItem.y = Double.parseDouble(coords[1]);
            	freezeBlockListItem.z = Double.parseDouble(coords[2]);
            }
            freezeBlockListItem.block_type = mapBlockModel.getBlockType();
            freezeBlockListItem.room_name = mapBlockModel.getRoomName();
            freezeBlockListItem.feature_type = mapBlockModel.getFeatureType();
            
			model.data.mission_freezeblock_list.add(freezeBlockListItem);
		}		
	}
	
	// alters the incoming model as it's passed by reference, hence no return value 
	public static void addThreatSignList (ThreatSignListModel model) {
		
		model.data.mission_threatsign_list.clear();
		
		for (MapBlockModel mapBlockModel : threatSignList) {
			ThreatSignListItem threatSignListItem = new ThreatSignListItem();
            String[] coords = mapBlockModel.getLocationXYZ().split("\\s+");
            if (coords.length == 3) {
            	threatSignListItem.x = Double.parseDouble(coords[0]);
            	threatSignListItem.y = Double.parseDouble(coords[1]);
            	threatSignListItem.z = Double.parseDouble(coords[2]);
            }
            threatSignListItem.block_type = mapBlockModel.getBlockType();
            threatSignListItem.room_name = mapBlockModel.getRoomName();
            threatSignListItem.feature_type = mapBlockModel.getFeatureType();
            
			model.data.mission_threatsign_list.add(threatSignListItem);
		}		
	}
	
	public static int getVictimId(BlockPos pos) {
		
		Integer id = null;
		
		id = MapBlockManager.victimIdMap.get(pos);
		
		if( id == null ) {
			
			System.out.println( pos.toString() + " has no victim id, returning -1. It was probably not placed with a MapBlock.csv file.");
			
			return -1;
		}
		else {
			
			return id;
		}		
	}
	
}
