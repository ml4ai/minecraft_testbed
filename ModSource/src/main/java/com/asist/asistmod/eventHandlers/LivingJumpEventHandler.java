package com.asist.asistmod.eventHandlers;

import java.util.List;

import com.asist.asistmod.datamodels.PlayerJumped.PlayerJumpedModel;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.Block;
import net.minecraft.block.BlockLever;
import net.minecraft.block.properties.IProperty;
import net.minecraft.block.state.IBlockState;
import net.minecraft.item.Item;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockAccess;
import net.minecraftforge.event.entity.living.LivingEvent.LivingJumpEvent;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class LivingJumpEventHandler {
	
	MinecraftServer server;
	
	public LivingJumpEventHandler(MinecraftServer server) {
		
		this.server = server;
	}
	
	@SubscribeEvent	
	public void onJump(LivingJumpEvent event) {
		String playerName = event.getEntity().getName();
		
		PlayerJumpedModel playerJumpedModel = new PlayerJumpedModel();
		playerJumpedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		playerJumpedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		playerJumpedModel.data.playername = playerName;
		playerJumpedModel.data.participant_id = InternalMqttClient.name_to_pid(playerName);
		playerJumpedModel.data.player_x = event.getEntity().getPosition().getX();
		playerJumpedModel.data.player_y = event.getEntity().getPosition().getY();
		playerJumpedModel.data.player_z = event.getEntity().getPosition().getZ();		
		InternalMqttClient.publish(playerJumpedModel.toJsonString(), "observations/events/player/jumped", playerName);
	}
}
