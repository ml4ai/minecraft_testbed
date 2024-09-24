package com.asist.asistmod.eventHandlers;

import java.time.Clock;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.block.BlockRole_HS;
import com.asist.asistmod.block.BlockRole_Med;
import com.asist.asistmod.block.BlockRole_SS;
import com.asist.asistmod.block.BlockVictim_1;
import com.asist.asistmod.block.BlockVictim_1_Marking;
import com.asist.asistmod.block.BlockVictim_2;
import com.asist.asistmod.block.BlockVictim_2_Marking;
import com.asist.asistmod.block.BlockVictim_Proximity;
import com.asist.asistmod.datamodels.CompetencyTask.CompetencyTaskModel;
import com.asist.asistmod.datamodels.Door.DoorModel;
import com.asist.asistmod.datamodels.GroundTruth.BlockageList.BlockageListModel;
import com.asist.asistmod.datamodels.GroundTruth.FreezeBlockList.FreezeBlockListModel;
import com.asist.asistmod.datamodels.GroundTruth.ThreatSignList.ThreatSignListModel;
import com.asist.asistmod.datamodels.GroundTruth.VictimList.VictimListModel;
import com.asist.asistmod.datamodels.Lever.LeverModel;
import com.asist.asistmod.datamodels.MarkerPlaced.MarkerPlacedModel;
import com.asist.asistmod.datamodels.MarkerRemoved.MarkerRemovedModel;
import com.asist.asistmod.datamodels.MissionState.MissionStateModel;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.ProximityBlockInteractionMessage.ProximityBlockInteractionDataModel;
import com.asist.asistmod.datamodels.ProximityBlockInteractionMessage.ProximityBlockInteractionModel;
import com.asist.asistmod.datamodels.RoleSelected.RoleSelectedModel;
import com.asist.asistmod.datamodels.ToolDepleted.ToolDepletedModel;
import com.asist.asistmod.datamodels.ToolUsed.ToolUsedModel;
import com.asist.asistmod.datamodels.VictimPickedUp.VictimPickedUpModel;
import com.asist.asistmod.datamodels.VictimPlaced.VictimPlacedModel;
import com.asist.asistmod.missionhelpers.RoleManager.RoleManager;
import com.asist.asistmod.missionhelpers.RoleManager.RoleTypeLight;
import com.asist.asistmod.missionhelpers.Scoreboard.CustomScoreboardWrapper;
import com.asist.asistmod.missionhelpers.Scoreboard.ScoreboardManager;
import com.asist.asistmod.missionhelpers.datastructures.Player;
import com.asist.asistmod.missionhelpers.datastructures.PlayerManager;
import com.asist.asistmod.missionhelpers.datastructures.Position;
import com.asist.asistmod.missionhelpers.enums.BlockType;
import com.asist.asistmod.missionhelpers.enums.ItemType;
import com.asist.asistmod.missionhelpers.enums.RoleType;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager.MapBlockMode;
import com.asist.asistmod.missionhelpers.markingblocks.MarkingBlockManager;
import com.asist.asistmod.missionhelpers.mission.Mission;
import com.asist.asistmod.missionhelpers.mission.MissionMap;
import com.asist.asistmod.missionhelpers.mission.Scoreboard;
import com.asist.asistmod.missionhelpers.mission.Tutorial;
import com.asist.asistmod.missionhelpers.mod.ModBlocks;
import com.asist.asistmod.missionhelpers.mod.ModItems;
import com.asist.asistmod.missionhelpers.pause.PauseManager;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.missionhelpers.victims.VictimsSavedManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MissionTimerPacket;
import com.asist.asistmod.network.messages.TeamScoreUpdatePacket;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;
import com.asist.asistmod.tile_entity.VictimBlockProximityTileEntity;
import com.asist.asistmod.tile_entity.VictimBlockTileEntity;

import net.minecraft.block.Block;
import net.minecraft.block.BlockButton;
import net.minecraft.block.BlockDoor;
import net.minecraft.block.BlockLever;
import net.minecraft.block.BlockSign;
import net.minecraft.block.BlockStone;
import net.minecraft.block.properties.IProperty;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.Blocks;
import net.minecraft.init.Items;
import net.minecraft.init.SoundEvents;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.SoundCategory;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockAccess;
import net.minecraft.world.World;

import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import net.minecraftforge.fml.common.registry.IForgeRegistryEntry;
import scala.actors.threadpool.Arrays;
import scala.swing.event.Key;

public class PlayerInteractionEventHandler {

MinecraftServer server;
ModSettings modSettings;
Boolean missionStarted = false;
String worldName;

//HashMap< String, BlockPos > triageManager = new HashMap();
	
	public PlayerInteractionEventHandler( MinecraftServer server, ModSettings modSettings) {
		
		this.server = server;
		this.modSettings = modSettings;
	}
	
	@SubscribeEvent	
	public void onPlayerInteraction( PlayerInteractEvent event) {
		
		BlockPos blockPos = event.getPos();
		int x = blockPos.getX();
		int y = blockPos.getY();
		int z = blockPos.getZ();
		World world = event.getWorld();
		IBlockState blockState = world.getBlockState(blockPos);
		
		Block block = blockState.getBlock();		
		
		worldName = world.getWorldInfo().getWorldName();		
		
		EntityPlayer entityPlayer = event.getEntityPlayer();
		
		// will create player if it does not exist
		Player player = PlayerManager.getPlayer(entityPlayer);
		
		String playerName = entityPlayer.getName();
		String participant_id = InternalMqttClient.name_to_pid(playerName);
		
		String blockName = block.getRegistryName().toString();		
	
		BlockType modBlock = ModBlocks.getEnum(blockState);
		
		IBlockState air = Blocks.AIR.getDefaultState();		
		
		ItemStack heldItem = entityPlayer.getHeldItemMainhand();
		String heldItemName = heldItem.getItem().getRegistryName().toString();
		ItemType heldModItem = ModItems.getEnum(heldItem);
		int currentSlot = entityPlayer.inventory.currentItem;		
		
		try {
			/*********************** LEFT CLICK INTERACTIONS **************************************************************************************************/		

			if(event instanceof PlayerInteractEvent.LeftClickBlock) {	
				
				
				
				if(!heldModItem.equals(ItemType.NULL)) {
					String itemName = heldModItem.getName();
					int uses = 0;
					int maxUses = 0;
					int durability = 0;
								
					uses = heldItem.getItemDamage();
					maxUses = heldItem.getMaxDamage();
					durability = maxUses - uses;
					
					ToolUsedModel toolUsedModel = new ToolUsedModel();
					toolUsedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
					toolUsedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
					toolUsedModel.data.playername = playerName;
					toolUsedModel.data.participant_id = participant_id;
					toolUsedModel.data.tool_type = itemName;
					toolUsedModel.data.durability = durability;
					toolUsedModel.data.target_block_x = x;
					toolUsedModel.data.target_block_y = y;
					toolUsedModel.data.target_block_z = z;
					toolUsedModel.data.target_block_type = blockName;
					InternalMqttClient.publish(toolUsedModel.toJsonString(), "observations/events/player/tool_used",playerName);
				}
				// break marker blocks
				if( isCustomCarpetBlockFromRegistryName(blockName) ) {
					
					world.setBlockState(blockPos, air);				
		        	
		        	String[] split = blockName.split("[_:]");
					
					MarkerRemovedModel markerRemovedModel = new MarkerRemovedModel();
					markerRemovedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
					markerRemovedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
					markerRemovedModel.data.playername = playerName;
					markerRemovedModel.data.participant_id = participant_id;
					markerRemovedModel.data.type = split[3] + "_" + split[4];
					markerRemovedModel.data.marker_x = x;
					markerRemovedModel.data.marker_y = y;
					markerRemovedModel.data.marker_z = z;
					InternalMqttClient.publish(markerRemovedModel.toJsonString(), "observations/events/player/marker_removed", playerName);
					
				}
				// PROXIMITY BLOCK
				if( block instanceof BlockVictim_Proximity) {
					
					// PROXIMITY VICTIM SHOULD NEVER BE BROKEN, BUT WILL SWAP WITH BLOCKVICTIM_2 WHEN 3 PLAYERS ARE IN RANGE
					event.setCanceled(true);
					
					TileEntity tE = world.getTileEntity(blockPos);
					
					if ( tE instanceof VictimBlockProximityTileEntity ) {
						
						VictimBlockProximityTileEntity tileEntity = (VictimBlockProximityTileEntity) tE;
						
						int playerCount = modSettings.proximityVictimPlayerCount;
						
						server.commandManager.executeCommand(server, "tellraw "+playerName+" {\"text\":\""+ playerCount +" players - including 1 Medic - must be within a 2 block radius of this victim to start a Triage.\",\"color\":\"red\"} ");
						
						ProximityBlockInteractionModel message = new ProximityBlockInteractionModel();		
						
						message.data.playername = playerName;
						message.data.participant_id = participant_id;
						message.data.action_type = ProximityBlockInteractionDataModel.ACTION_TYPE.TRIAGE_ERROR.name();
						message.data.players_in_range = tileEntity.numPlayersInRange;
						message.data.victim_x = x;
						message.data.victim_y = y;
						message.data.victim_z = z;
						message.data.victim_id = MapBlockManager.getVictimId(blockPos);
						
						InternalMqttClient.publish(message.toJsonString(), "observations/events/player/proximity_block", playerName);					
					}			
				}
			}

			/*********************** RIGHT CLICK INTERACTIONS **************************************************************************************************/
			if(event instanceof PlayerInteractEvent.RightClickBlock) {				
				
				/*********************** LEVER EVENT *****************************************************************/
				if(  block instanceof BlockLever){	
		
					LeverModel leverModel = new LeverModel();
					leverModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
					leverModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
					leverModel.data.playername = playerName;
					leverModel.data.participant_id = participant_id;
					leverModel.data.powered = !(Boolean) blockState.getProperties().get( BlockLever.POWERED );
					leverModel.data.lever_x = x;
					leverModel.data.lever_y = y;
					leverModel.data.lever_z = z;			
					InternalMqttClient.publish(leverModel.toJsonString(), "observations/events/player/lever", playerName);								
					
				}
				/*********************** DOOR EVENT *****************************************************************/
				else if ( block instanceof BlockDoor) {
					
					String half = blockState.getProperties().get( BlockDoor.HALF).toString();
					
					DoorModel doorModel = new DoorModel();
					doorModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
					doorModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
					doorModel.data.playername = playerName;
					doorModel.data.participant_id = participant_id;
					doorModel.data.door_x = x;
					doorModel.data.door_y = y;
					doorModel.data.door_z = z;
					
					if(half.equals("lower")) {
						
						doorModel.data.open = !(Boolean) blockState.getProperties().get( BlockDoor.OPEN );					
					}
					
					else {			
						
						IBlockState lowerBlockState = event.getWorld().getBlockState(new BlockPos(x,y-1,z));
										
						doorModel.data.open = !(Boolean) lowerBlockState.getProperties().get( BlockDoor.OPEN );				
					}
					
					InternalMqttClient.publish(doorModel.toJsonString(), "observations/events/player/door",playerName);
				}
				
				// ADAPT STUFF
				if (event.getHand() == entityPlayer.getActiveHand()){	// Only triggers once per click				
					
					/*********************** ROLE SELECTION BUTTONS *****************************************************/		
					
					if(ModBlocks.isRoleBlock(modBlock))
					{
						if(!player.isCarryingVictim) {
							
							entityPlayer.inventory.clear();					
							// TY'S PLAYER CLASS FROM ADAPT
							RoleType role = ModBlocks.getRole(modBlock);
							player.assignCallSign();
							player.updateRole(role);					
							player.giveEffect(role);
							player.giveArmor(server);
							player.giveRoleTools(server);					
							
							System.out.println("Callsign = " + player.callSign);
							
							// ED'S MUCH LIGHTER ROLE TRACKER
							String prevRole = RoleManager.getPlayerRole(playerName).getDisplayName();
							RoleTypeLight roleTypeLight = RoleTypeLight.NULL;
							
							if(block instanceof BlockRole_Med) {
								roleTypeLight = RoleTypeLight.MED;						
							}
							else if (block instanceof BlockRole_HS) {
								roleTypeLight = RoleTypeLight.ENG;
							}
							else if (block instanceof BlockRole_SS) {
								roleTypeLight = RoleTypeLight.TRAN;
							}
							
							RoleManager.assignRoleToPlayer(playerName, roleTypeLight);
							
							// END ED's MUCH LIGHTER ROLE TRACKER
							
							RoleSelectedModel roleModel = new RoleSelectedModel();
							roleModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
							roleModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
							roleModel.data.playername = playerName;
							roleModel.data.participant_id = participant_id;
							roleModel.data.prev_role = prevRole;
							roleModel.data.new_role = roleTypeLight.getDisplayName();			
							InternalMqttClient.publish(roleModel.toJsonString(), "observations/events/player/role_selected", playerName);						
						}
						else {
							server.commandManager.executeCommand(server, "tell " + playerName + " You cannot change roles while carrying a victim.");
						}
					}
					
					/*********************** CARRY VICTIM INTERACTIONS ***********************************************/		
	    			
		    		// Pickup victim with stretcher
			        if( ModBlocks.canPickUp(modBlock) && (ModItems.isItem(heldItem, ItemType.STRETCHER) || ModItems.isItem(heldItem, ItemType.MEDICALKIT) || 
		        		    ModItems.isItem(heldItem, ItemType.HAMMER ))) {
			        	
			        	// GRAB UNIQUE ID OF PICKED UP VICTIM	        		
			        	int id = player.carryVictim(blockPos,modBlock);		        					
			        	
			        	// TOOL USED EVENT
						String itemName = heldModItem.getName();
						int uses = 0;
						int maxUses = 0;
						int durability = 0;
									
						uses = heldItem.getItemDamage();
						maxUses = heldItem.getMaxDamage();
						durability = maxUses - uses;
						
						
						ToolUsedModel toolUsedModel = new ToolUsedModel();
						toolUsedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
						toolUsedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
						toolUsedModel.data.playername = playerName;
						toolUsedModel.data.participant_id = participant_id;
						toolUsedModel.data.tool_type = itemName;
						toolUsedModel.data.durability = durability;
						toolUsedModel.data.target_block_x = x;
						toolUsedModel.data.target_block_y = y;
						toolUsedModel.data.target_block_z = z;
						toolUsedModel.data.target_block_type = blockName;
						InternalMqttClient.publish(toolUsedModel.toJsonString(), "observations/events/player/tool_used", playerName);
						// END TOOL USED EVENT
			        	
			        	ItemStack newItem = ItemType.STRETCHER_OCCUPIED.getItemStack();
			        	int itemDamage = heldItem.getItemDamage();						// Item damage is how much an item has been damaged (i.e. measure of durability)
			    		newItem.setItemDamage(itemDamage);								// Transferring durability to new item
			    		
			    		//String victimType = modBlock.getName();
			    		//NBTTagCompound nbt = new NBTTagCompound();						// NBT tag stores meta data of victim type onto the occupied stretcher

			    		//nbt.setString("VictimType", victimType);
			    		//newItem.setTagCompound(nbt);
			    		
			    		entityPlayer.replaceItemInInventory(currentSlot, newItem);		// Swaps stretcher with occupied_stretcher
						world.setBlockState(blockPos, air);								// "Picks up" block by replacing with air
						
						// Apply effects to the player based on their role.  Transporters are not effected,
						// but Medics and Engineers are because their main role is not to transport.
						//player.giveEffect(player.getRole());
						
						// Lixao asked to keep speed the same
						//RoleManager.setRoleEffects(entityPlayer, RoleManager.getPlayerRole(player.getName()));					
						
						
						VictimPickedUpModel victimPickedUpModel = new VictimPickedUpModel();
						victimPickedUpModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
						victimPickedUpModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
						victimPickedUpModel.data.playername = playerName;
						victimPickedUpModel.data.participant_id = participant_id;
						victimPickedUpModel.data.victim_x = x;
						victimPickedUpModel.data.victim_y = y;
						victimPickedUpModel.data.victim_z = z;
						victimPickedUpModel.data.type = modBlock.getName();
						victimPickedUpModel.data.victim_id = id;
						InternalMqttClient.publish(victimPickedUpModel.toJsonString(), "observations/events/player/victim_picked_up", playerName);
						
						// UPDATE SIGNAL MAP AS IF VICTIM NO LONGER IN ROOM ( NOT TRACKING LOCATION THE WHOLE GAME JUST FIRST INTERACTION)			
						VictimLocations.removeVictimFromSignalMap(id);					
						
			        }
			        
			        // Place victim with occupied_stretcher
			        else if(ModItems.isItem(heldItem, ItemType.STRETCHER_OCCUPIED) && blockState.getBlock().equals(Blocks.STONE)) {
			        	
			        	BlockType blockType = player.carriedVictimType;
			        	
			        	BlockPos targetPos = blockPos.add(0, 1, 0);						// The block above the block we're clicking	
			        	
			        	IBlockState targetBlock = world.getBlockState(targetPos);        	
			        	
			        	if(targetBlock.equals(air))	{
			        		
			        		// deals with settings the victim id correctly
			        		player.placeVictim(targetPos);
			        		
			        		System.out.println( targetPos.toString() + ":" + MapBlockManager.getVictimId(targetPos));
			        		
			        		// HERE WE CHECK IF THIS IS THE CORRECT SCORING AREA AND INCREMENT THE SCORE IF SO
			        		ScoreboardManager.checkScoringZoneAndUpdateScore(blockType, targetPos, playerName, server);
			        		
			        		// TOOL USED EVENT
			        		String itemName = heldModItem.getName();
							int uses = 0;
							int maxUses = 0;
							int durability = 0;
										
							uses = heldItem.getItemDamage();
							maxUses = heldItem.getMaxDamage();
							durability = maxUses - uses;
							
							ToolUsedModel toolUsedModel = new ToolUsedModel();
							toolUsedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
							toolUsedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
							toolUsedModel.data.playername = playerName;
							toolUsedModel.data.participant_id = participant_id;
							toolUsedModel.data.tool_type = itemName;
							toolUsedModel.data.durability = durability;
							toolUsedModel.data.target_block_x = x;
							toolUsedModel.data.target_block_y = y;
							toolUsedModel.data.target_block_z = z;
							toolUsedModel.data.target_block_type = blockName;
							InternalMqttClient.publish(toolUsedModel.toJsonString(), "observations/events/player/tool_used", playerName);
			        		ItemStack newItem = new ItemStack(Blocks.AIR, 1, 0);
			        		IBlockState newBlock = blockType.getDefaultState();
			        		// END TOOL USED EVENT

				    		int itemDamage = heldItem.getItemDamage() + 1;	// "Reduce" durability by 1				    	
				    		
				    		if(durability >= 0) {
					    		
				    			player.giveItems(new String[] {player.getRole().getTool().getCommandText()}, server);
					    		newItem = entityPlayer.getHeldItemMainhand();
					    		newItem.setItemDamage(itemDamage);
				    		}
				    		else {
				    			ToolDepletedModel toolDepletedModel = new ToolDepletedModel();
				    			toolDepletedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
				    			toolDepletedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
				    			toolDepletedModel.data.playername = playerName;
				    			toolDepletedModel.data.participant_id = participant_id;
				    			toolDepletedModel.data.tool_type = ItemType.STRETCHER.getName();
				    			InternalMqttClient.publish(toolDepletedModel.toJsonString(), "observations/events/player/tool_depleted", playerName);
				    		}			    		
				        				    		
				    		entityPlayer.replaceItemInInventory(currentSlot, newItem);
							
				    		world.setBlockState(targetPos, newBlock);		    		
							
				    		// Lixao asked to keep the speed the same regardless
				    		// RoleManager.setRoleEffects(entityPlayer, RoleManager.getPlayerRole(player.getName()));						
							
							VictimPlacedModel victimPlacedModel = new VictimPlacedModel();
							victimPlacedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
							victimPlacedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
							victimPlacedModel.data.playername = playerName;
							victimPlacedModel.data.participant_id = participant_id;
							victimPlacedModel.data.victim_x = targetPos.getX();
							victimPlacedModel.data.victim_y = targetPos.getY();
							victimPlacedModel.data.victim_z = targetPos.getZ();
							victimPlacedModel.data.type = blockType.getName();
							victimPlacedModel.data.victim_id = MapBlockManager.getVictimId(targetPos);
							InternalMqttClient.publish(victimPlacedModel.toJsonString(), "observations/events/player/victim_placed", playerName);
			        	}
			        }
			        
			        /*********************** PLACE CARPET MARKERS *****************************************************/		          
			        
			        // Place carpet markers into the world
			        if( isHoldingMarkerItem(heldItem) ){
			        	
			        	String itemRegistryName = heldItem.getItem().getRegistryName().toString();
			        	
			        	String[] split = itemRegistryName.split("[_:]");
			        	
			        	split[1] = "block";
			        	
			        	String blockToPlaceRegistryName = split[0] + ":" + split[1] + "_" + split[2] + "_" + split[3] + "_" + split[4];
			        	
			        	if( isCustomCarpetBlockFromRegistryName(blockName) )	{
			        		
			        		String command = "setblock " + x + " " + y + " " + z + " " + blockToPlaceRegistryName;		        		
	        		
			        		server.commandManager.executeCommand(server, command );
			        		
			        		MarkerPlacedModel markerPlacedModel = new MarkerPlacedModel();
							markerPlacedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
							markerPlacedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
							markerPlacedModel.data.playername = playerName;
							markerPlacedModel.data.participant_id = participant_id;
							markerPlacedModel.data.type = split[3] + "_" + split[4];
							markerPlacedModel.data.marker_x = x;
							markerPlacedModel.data.marker_y = y;
							markerPlacedModel.data.marker_z = z;
							InternalMqttClient.publish(markerPlacedModel.toJsonString(), "observations/events/player/marker_placed", playerName);
			        		
				        }
			        	
			        	else if ( block instanceof BlockStone) {
			        		
			        					        	
				        	String command = "setblock " + x + " " + (y+1) + " " + z + " " + blockToPlaceRegistryName;
			        		
			        		server.commandManager.executeCommand(server, command );
			        		
			        		MarkerPlacedModel markerPlacedModel = new MarkerPlacedModel();
							markerPlacedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
							markerPlacedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
							markerPlacedModel.data.playername = playerName;
							markerPlacedModel.data.participant_id = participant_id;
							markerPlacedModel.data.type = split[3] + "_" + split[4];
							markerPlacedModel.data.marker_x = x;
							markerPlacedModel.data.marker_y = y+1;
							markerPlacedModel.data.marker_z = z;
							InternalMqttClient.publish(markerPlacedModel.toJsonString(), "observations/events/player/marker_placed", playerName);						
							
			        	}         	
			        }
			        
			        /*********************** MISSION START BLOCKS *****************************************************/	
			        
					if(ModBlocks.isMissionBlock(modBlock)) {
						
						if(modBlock.equals(BlockType.MISSION)) {		
							
							if(missionStarted == false) {
								saturnMissionStartProcedure( playerName );
							}						
						}
					}						
					
					/*********************** TRAINING/COMPETENCY TASKS *****************************************************************/
											
					else if( InternalMqttClient.currentTrialInfo.mission_name.toLowerCase().contains("training") ) {
					
						// Doors for lever advisor adherence task	
						
						if(z == 102) {
							if( y == 60 || y == 61 ) {
								if( x == -2176 || x == -2175 || x == -2168 || x == -2167 || x == -2160 || x == -2159) {
									String advisorString = "tellraw "+playerName+" {\"text\":\"ADVISOR : Toggle the levers in the following order : [-- UP -- UP -- DOWN -- DOWN -- UP].\",\"color\":\"yellow\"} ";
									server.commandManager.executeCommand(server, advisorString );
									AsistMod.server.commandManager.executeCommand(AsistMod.server, "playsound minecraft:block.note.pling voice "+playerName+" " + x + " " + y + " " + z );
								}							
							}						
						}
					}
				}
			}
			
		}
		catch(Exception e) {
			
			System.out.println("Something went wrong in the PlayerInteractionEventHandler Class - summary below");
			
			System.out.println( "BlockPos : " + blockPos.toString() );
			System.out.println( "BlockPos : " + blockPos.toString() );
			System.out.println( "IBlockStateObjectNull : " + (blockState==null?"True":"False"));
			System.out.println( "WorldObjectNull : " + (world==null?"True":"False"));
			System.out.println( "BlockObjectNull : " + (block==null?"True":"False"));
			System.out.println( "BlockName : " + (blockName==null?"null":blockName));
			System.out.println( "ModBlock : " + (modBlock==null?"null":modBlock.getName()));
			System.out.println( "HeldItem : " + (heldItemName==null?"null":heldItemName));
			System.out.println( "PID : " + (participant_id==null?"null":participant_id));
			
			e.printStackTrace();
			
		}
		
	}	
	
	public void saturnMissionStartProcedure( String playerName ) {
		
		missionStarted = true;
		
		String[] opped_players = server.getPlayerList().getOppedPlayerNames();
		System.out.println("DEOPPING ANYONE WHO DID NOT START MISSION :");
		for (String player : opped_players) {
			
			if( !player.contentEquals(playerName) ) {
				
				System.out.println(playerName);			
				server.commandManager.executeCommand(server, "deop " + player);		
			}			
		}
		
		// CREATE TIMER
		
		Mission.init(server, modSettings);
		
		MissionTimer.init(server, modSettings);
		
		// CustomScoreboardWrapper.Init(server);
		
		// PauseManager.addPausablePlayer(playerName);
		
		// END CREATE TIMER
		
		// MISSION START MESSAGE
		
		String missionName = InternalMqttClient.currentTrialInfo.mission_name;					
		
		MissionStateModel model = new MissionStateModel();
		
		model.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		model.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		
		model.data.mission = missionName;
		model.data.mission_state = "Start";
		
		InternalMqttClient.publish(model.toJsonString(), "observations/events/mission");
		
		// PUBLISH GROUNDTRUTH VICTIM LIST
		
		VictimListModel model2 = new VictimListModel();
		
		model2.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		model2.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		model2.data.mission = missionName;					

		MapBlockManager.addVictimList(model2);
		
		// UPDATE CONNECTED CLIENT SCOREBOARDS
		server.getPlayerList().getPlayers().forEach(p ->{		
				
			VictimCountUpdatePacket packet = new VictimCountUpdatePacket(
					
					ScoreboardManager.regularVictimsSaved,ScoreboardManager.maxRegularVictims,
					ScoreboardManager.criticalVictimsSaved,ScoreboardManager.maxCriticalVictims,
					ScoreboardManager.teamScore,ScoreboardManager.maxTeamScore
			);								
			NetworkHandler.sendToClient(packet, p);			
									
		});
		
		InternalMqttClient.publish(model2.toJsonString(), "ground_truth/mission/victims_list");
		
		// PUBLISH GROUNDTRUTH BLOCKAGE LIST
		
		BlockageListModel model3 = new BlockageListModel(MapBlockMode.MISSION_START);
		
		model3.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		model3.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		model3.data.mission = missionName;

		MapBlockManager.addBlockageList(model3);

		InternalMqttClient.publish(model3.toJsonString(), "ground_truth/mission/blockages_list");
		
		// PUBLISH GROUNDTRUTH FREEZE BLOCK LIST
		
		FreezeBlockListModel model4 = new FreezeBlockListModel();
		
		model4.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		model4.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		model4.data.mission = missionName;

		MapBlockManager.addFreezeBlockList(model4);

		InternalMqttClient.publish(model4.toJsonString(), "ground_truth/mission/freezeblock_list");
		
		// PUBLISH GROUNDTRUTH THREAT SIGN LIST
		
		ThreatSignListModel model5 = new ThreatSignListModel();
		
		model5.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		model5.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		model5.data.mission = missionName;
		MapBlockManager.addThreatSignList(model5);

		InternalMqttClient.publish(model5.toJsonString(), "ground_truth/mission/threatsign_list");		
		
		
				
	}
	
	public static boolean isHoldingMarkerItem(ItemStack stack) {
		String itemString = stack.getItem().getRegistryName().toString();
		return isCustomCarpetItemFromRegistryName(itemString);
	}
	
	public static boolean isCustomCarpetItemFromRegistryName(String registryName) {
		
		return registryName.contains("asistmod:item_marker");
		//return registryName.contentEquals("asistmod:item_marker_1_red" ) || registryName.contentEquals("asistmod:item_marker_1_green") || registryName.contentEquals("asistmod:item_marker_1_blue") 
		//		|| registryName.contentEquals("asistmod:item_marker_2_red" ) || registryName.contentEquals("asistmod:item_marker_2_green") || registryName.contentEquals("asistmod:item_marker_2_blue") 
		//		|| registryName.contentEquals("asistmod:item_marker_3_red" ) || registryName.contentEquals("asistmod:item_marker_3_green") || registryName.contentEquals("asistmod:item_marker_3_blue");
	}
	
	public static boolean isCustomCarpetBlockFromRegistryName(String registryName) {
		return registryName.contains("asistmod:block_marker");
		//return registryName.contentEquals("asistmod:block_marker_1_red" ) || registryName.contentEquals("asistmod:block_marker_1_green") || registryName.contentEquals("asistmod:block_marker_1_blue") 
		//		|| registryName.contentEquals("asistmod:block_marker_2_red" ) || registryName.contentEquals("asistmod:block_marker_2_green") || registryName.contentEquals("asistmod:block_marker_2_blue") 
		//		|| registryName.contentEquals("asistmod:block_marker_3_red" ) || registryName.contentEquals("asistmod:block_marker_3_green") || registryName.contentEquals("asistmod:block_marker_3_blue");
	}
}
