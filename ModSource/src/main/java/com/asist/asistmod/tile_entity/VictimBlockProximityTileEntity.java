package com.asist.asistmod.tile_entity;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicReference;

import com.asist.asistmod.block.BlockVictimBase;
import com.asist.asistmod.block.BlockVictim_2;
import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.ProximityBlockInteractionMessage.ProximityBlockInteractionDataModel;
import com.asist.asistmod.datamodels.ProximityBlockInteractionMessage.ProximityBlockInteractionModel;
import com.asist.asistmod.missionhelpers.RoleManager.RoleManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager.TriageState;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MouseInputMessage;
import com.asist.asistmod.network.messages.ParticlesUpdatePacket;
import com.asist.asistmod.network.messages.TriageMessagePacket;

import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.DestroyBlockProgress;
import net.minecraft.client.renderer.RenderGlobal;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.ITickable;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import net.minecraftforge.fml.relauncher.ReflectionHelper;

public class VictimBlockProximityTileEntity extends TileEntity implements ITickable  {	
	
	
	boolean isServerSide;
	
	String playerName = "Not Set";
	
	int tickCount = 0;
	
	int serverTick = 0;
	
	ModSettings modSettings = null;
	
	// read from modSettings
	final HashSet<String> playersInRange = new HashSet<String>();
	
	public int numPlayersInRange = 0;
	
	public boolean hasMedic = false;
	
	String blockType;
	
	@Override
	public NBTTagCompound writeToNBT(NBTTagCompound compound) {
		
		compound.setInteger("inRange", numPlayersInRange );
		
		compound.setBoolean("hasMedic", hasMedic);
		
		return super.writeToNBT(compound);
	}
	
	@Override
	public void readFromNBT(NBTTagCompound compound) {
		
		super.readFromNBT(compound);
		
		numPlayersInRange = compound.getInteger("inRange");	
		hasMedic = compound.getBoolean("hasMedic");	
		
	}
	
	
	@Override 
	public void update() {
		
		World world = this.getWorld();
		BlockPos blockPos = this.getPos();
		
		// ensures its serverside and not in singleplayermode ... apparently it ticks in singleplayermode which breaks things
		if( !world.isRemote && InternalMqttClient.isInitialized ) {			
			
			// A QUICK INITIALIZER
			if (modSettings == null ){
				
				modSettings = InternalMqttClient.modSettings;				
			}			
			
			serverTick ++ ;
			
			// only check once a second(ish), no reason to check all the time
			if(serverTick == 20 ) {								
				
				serverTick = 0;	
				
				List<EntityPlayer> players = world.playerEntities;
				
				int bx = blockPos.getX();
				int by = blockPos.getY();
				int bz = blockPos.getZ();
				
				// x and z is the ground plane			
						
				players.forEach( p -> {
					
					boolean playerFound = false;
					
					String name = p.getName();				
					
					BlockPos playerPos = p.getPosition();
					
					int px = playerPos.getX();
					int py = playerPos.getY();
					int pz = playerPos.getZ();				

					// No need to check each space for occupation - 25 times per player ... just do the below -ED W 4/11/2022.										

					if( (py == by) && (px>=bx-2) && (px<=bx+2) && (pz>=bz-2) && (pz<=bz+2) ) {							
						
						playerFound = true;							
					}				

					if(playerFound) {					
						
						// returns true if player is not already in this HashSet
						if( playersInRange.add(name) ) {
							
							numPlayersInRange = playersInRange.size();
							
							boolean shouldWake = false;
							
							this.markDirty();							
							
							if( playersInRange.size() >= modSettings.proximityVictimPlayerCount ) {								
								
								String[] playersArray = playersInRange.toArray(new String[playersInRange.size()]);
								
								// CHECK IF ONE IS THE MEDIC
								for(int i=0; i<playersArray.length;i++) {
									
									if(RoleManager.isPlayerMedic(playersArray[i])) {
										
										hasMedic = true;
										
										shouldWake = true;
										
										break;
										
									}
									
								}
								
								hasMedic=false;
							}
							
							ProximityBlockInteractionModel message = new ProximityBlockInteractionModel();		
							
							message.data.playername = name;
							message.data.participant_id = InternalMqttClient.currentTrialInfo.participant_ids.get(name);
							message.data.action_type = ProximityBlockInteractionDataModel.ACTION_TYPE.ENTERED_RANGE.name();
							message.data.players_in_range = numPlayersInRange;
							message.data.awake = shouldWake;
							message.data.victim_x = bx;
							message.data.victim_y = by;
							message.data.victim_z = bz;
							message.data.victim_id = MapBlockManager.getVictimId(blockPos);
							
							InternalMqttClient.publish(message.toJsonString(), "observations/events/player/proximity_block", name);
							
							if ( shouldWake) {
								
								String command = "setblock "+bx+" "+by+" "+bz+" asistmod:block_victim_2";
								// Replace the block with a partical block
								world.getMinecraftServer().commandManager.executeCommand(world.getMinecraftServer(), command);
								
							}						
							
						}	
						
					}
					else {	
						
						if (playersInRange.remove(name) ) {
							
							numPlayersInRange = playersInRange.size();
							this.markDirty();
							
							ProximityBlockInteractionModel message = new ProximityBlockInteractionModel();		
							
							message.data.playername = name;
							message.data.participant_id = InternalMqttClient.currentTrialInfo.participant_ids.get(name);
							message.data.action_type = ProximityBlockInteractionDataModel.ACTION_TYPE.LEFT_RANGE.name();
							message.data.players_in_range = numPlayersInRange;
							message.data.victim_x = bx;
							message.data.victim_y = by;
							message.data.victim_z = bz;
							message.data.victim_id = MapBlockManager.getVictimId(blockPos);
							
							InternalMqttClient.publish(message.toJsonString(), "observations/events/player/proximity_block", name);
							
						}											
						
					}				
				});				
				
				//System.out.println("Players in Range : " + playersInRange.size());			
				
			}			
		}		
	}
}
