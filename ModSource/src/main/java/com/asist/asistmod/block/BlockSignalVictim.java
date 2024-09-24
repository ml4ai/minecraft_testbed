package com.asist.asistmod.block;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.datamodels.PlayerFrozen.PlayerFrozenDataModel;
import com.asist.asistmod.datamodels.PlayerFrozen.PlayerFrozenModel;
import com.asist.asistmod.datamodels.VictimSignal.VictimSignalModel;
import com.asist.asistmod.missionhelpers.freezeManager.FreezeManager;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.RoleManager.RoleManager;
import com.asist.asistmod.missionhelpers.victims.SignalData;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.Block;
import net.minecraft.block.BlockBasePressurePlate;
import net.minecraft.block.material.Material;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.MobEffects;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

public class BlockSignalVictim extends Block {
	
	boolean shouldActivate;
	
	long lastActivationTime = 0L;
	
	long interval = 0;

	protected BlockSignalVictim(Material materialIn) {
		super(materialIn);
		// TODO Auto-generated constructor stub
		shouldActivate=true;
		
	}
	
	
    /**
     * Triggered whenever an entity walks over this block (enters into the block)
     */
    @Override
	public void onEntityWalk(World worldIn, BlockPos pos, Entity entityIn)
    {
    	if(!worldIn.isRemote) {
    		
    		// MAKE SURE ITS ONLY THE TRANSPORTER GETTING THESE    		
    		if( interval == 0) {
    			
    			interval = AsistMod.modSettings.victimSignalResetInterval;
    		}
    		if(MissionTimer.getElapsedMillisecondsGlobal() - lastActivationTime >= interval ){shouldActivate = true;}
    		
    		if( shouldActivate && entityIn instanceof EntityPlayer && RoleManager.isPlayerTran(entityIn.getName()) ) { 
    			
    			lastActivationTime = MissionTimer.getElapsedMillisecondsGlobal();
    			
    			shouldActivate = false;
    			// shouldActivate = false;
    			
    			MinecraftServer server = worldIn.getMinecraftServer();	 
        		
        		String name = entityIn.getName();
        		
        		SignalData signal_data = VictimLocations.signalPosToSignalDataMap.get(pos);
        		
        		//System.out.println("Signal Data : " + signal_data.roomName + " : empty? " + signal_data.victimList.isEmpty());
        		
        		String signal = signal_data.getSignalString();
    			
        		if ( signal != null) {
    				
    				server.commandManager.executeCommand(server, "tellraw " + name +" {\"text\":\""+signal+"\",\"color\":\"green\"} ");
        			
        			VictimSignalModel message = new VictimSignalModel(name,InternalMqttClient.name_to_pid(name),signal_data.roomNames.get(0),
        					pos.getX(),pos.getY(),pos.getZ(),signal_data.getSignalString());
        			
        			InternalMqttClient.publish(message.toJsonString(), "observations/events/player/signal",name);
    				
    			}
        		else {
        			System.out.println("Signal String was null");
        		}
    		}    		
    	}
    }
}
