package com.asist.asistmod.eventHandlers;

import java.util.List;

import com.asist.asistmod.datamodels.ItemPickup.ItemPickupModel;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.Block;
import net.minecraft.block.BlockLever;
import net.minecraft.block.properties.IProperty;
import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockAccess;
import net.minecraftforge.event.entity.player.EntityItemPickupEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class EntityItemPickupEventHandler {
	
	MinecraftServer server;
	
	public EntityItemPickupEventHandler(MinecraftServer server) {
		
		this.server = server;
	}
	
	@SubscribeEvent	
	public void onItemPickup( EntityItemPickupEvent event) {
		String playerName = event.getEntityPlayer().getName();
		ResourceLocation itemResourceLoc =  ForgeRegistries.ITEMS.getKey(event.getItem().getEntityItem().getItem());
		String itemName = itemResourceLoc.getResourceDomain() + ":" + itemResourceLoc.getResourcePath();
		
		ItemPickupModel itemPickupModel = new ItemPickupModel();
		itemPickupModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		itemPickupModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		itemPickupModel.data.playername = playerName;
		itemPickupModel.data.participant_id = InternalMqttClient.name_to_pid(playerName);
		itemPickupModel.data.itemname = itemName;
		itemPickupModel.data.item_x = event.getItem().getPosition().getX();
		itemPickupModel.data.item_y = event.getItem().getPosition().getY();
		itemPickupModel.data.item_z = event.getItem().getPosition().getZ();		
		InternalMqttClient.publish(itemPickupModel.toJsonString(), "observations/events/player/itempickup", playerName);

	}
}
