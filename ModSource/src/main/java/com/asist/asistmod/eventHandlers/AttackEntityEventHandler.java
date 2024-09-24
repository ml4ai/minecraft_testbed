package com.asist.asistmod.eventHandlers;

import com.asist.asistmod.datamodels.ModSettings.ModSettings;
import com.asist.asistmod.datamodels.PlayerFrozen.PlayerFrozenDataModel;
import com.asist.asistmod.datamodels.PlayerFrozen.PlayerFrozenModel;
import com.asist.asistmod.missionhelpers.RoleManager.RoleManager;
import com.asist.asistmod.missionhelpers.freezeManager.FreezeManager;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.event.entity.player.AttackEntityEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class AttackEntityEventHandler {
	
	MinecraftServer server;
	ModSettings modSettings;
	
	public AttackEntityEventHandler( MinecraftServer server, ModSettings modSettings){
		this.server = server;
		this.modSettings = modSettings;
	}
	
	@SubscribeEvent	
	public void onEntityAttacked( AttackEntityEvent event) {
		
		// Cancelling the event will remove any damage dealt and deal with the
		// attackee being launched after multiple hits bug, the function will still run after line 33
		
		event.setCanceled(true);
		
		// Get ATTACKER and ATTACKEE
		
		String attacker = event.getEntityPlayer().getName();
		String attackee = event.getTarget().getName();
		
		// check if attacker is medic
		if( event.getTarget() instanceof EntityPlayer ) {
			
			if ( RoleManager.isPlayerMedic(attacker) ) {
				
				if( FreezeManager.isPlayerFrozen(attackee) ) {					
					
					EntityPlayer player = (EntityPlayer) event.getTarget();					
					
					// RESET THE ROLE EFFECTS FOR THAT ROLE					
					RoleManager.setRoleEffects(player, RoleManager.getPlayerRole(attackee) );
					
					// reference the freeze manager and unfreeze					
					FreezeManager.setFrozenPlayer(attackee,false);						
					
					BlockPos pos = event.getTarget().getPosition();
					
					PlayerFrozenModel message = new PlayerFrozenModel();
	    			
	    			message.data.playername = attackee;
	    			message.data.participant_id = InternalMqttClient.name_to_pid(attackee);
	    			message.data.player_x = pos.getX();
	    			message.data.player_y = pos.getY();
	    			message.data.player_z = pos.getZ();
	    			message.data.state_changed_to = PlayerFrozenDataModel.frozenStates.UNFROZEN.name();
	    			message.data.medic_playername = attacker;
	    			message.data.medic_participant_id = message.data.participant_id = InternalMqttClient.name_to_pid(attacker);
	    			
	    			
	    			InternalMqttClient.publish(message.toJsonString(), "observations/events/player/freeze",attackee);
					
				}
				
			}
			
		}
		
	}

}
