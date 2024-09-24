package com.asist.asistmod.block;

import com.asist.asistmod.datamodels.PlayerFrozen.PlayerFrozenDataModel;
import com.asist.asistmod.datamodels.PlayerFrozen.PlayerFrozenModel;
import com.asist.asistmod.missionhelpers.freezeManager.FreezeManager;
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

public class BlockFreezePlayer extends Block {
	
	boolean shouldActivate;

	protected BlockFreezePlayer(Material materialIn) {
		super(materialIn);
		// TODO Auto-generated constructor stub
		shouldActivate=true;
	}
	
	
    /**
     * Triggered whenever an entity collides with this block (enters into the block)
     */
    @Override
	public void onEntityWalk(World worldIn, BlockPos pos, Entity entityIn)
    {
    	if(!worldIn.isRemote) {
    		
    		if( shouldActivate && entityIn instanceof EntityPlayer) { 
    			
    			// shouldActivate = false;
    			
    			MinecraftServer server = worldIn.getMinecraftServer();	 
        		
        		String name = entityIn.getName();
        		
    			// STOP MOVEMENT
    			server.commandManager.executeCommand(server, "effect "+ name +" blindness 99999 255");
    			// BLINDNESS
    			server.commandManager.executeCommand(server, "effect "+ name +" slowness 99999 10");
    			// NO JUMP
    			// 1-127 Boosts, 128-251 gives no jump, 252-256 work as normal --> This no longer works in minecraft 1.12    			
    			
    			//PotionEffect noJump = new PotionEffect(MobEffects.JUMP_BOOST, 100000, 128, true, false);    		
    			//((EntityPlayer)entityIn).addPotionEffect(noJump);
    			// reference the freeze manager and freeze the player    			
    			
    			FreezeManager.setFrozenPlayer(name,true);
    			
    			server.commandManager.executeCommand(server, "setblock "+ pos.getX() +" "+ pos.getY() + " "+ pos.getZ()+" minecraft:stone 6");
    			
    			PlayerFrozenModel message = new PlayerFrozenModel();
    			
    			message.data.playername = name;
    			message.data.participant_id = InternalMqttClient.currentTrialInfo.participant_ids.get(name);
    			message.data.player_x = pos.getX();
    			message.data.player_y = pos.getY();
    			message.data.player_z = pos.getZ();
    			message.data.state_changed_to = PlayerFrozenDataModel.frozenStates.FROZEN.name();
    			
    			InternalMqttClient.publish(message.toJsonString(), "observations/events/player/freeze",name);
    		}    		
    	}
    }
}
