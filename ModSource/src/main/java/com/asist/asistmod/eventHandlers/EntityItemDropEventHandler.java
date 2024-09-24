package com.asist.asistmod.eventHandlers;

import java.util.List;

import com.asist.asistmod.datamodels.ItemDrop.ItemDropModel;
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
import net.minecraftforge.event.entity.item.ItemTossEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class EntityItemDropEventHandler {
	
	
	MinecraftServer server;
	
	public EntityItemDropEventHandler(MinecraftServer server) {
		
		this.server = server;
	}
	
	@SubscribeEvent	
	public void onItemDrop( ItemTossEvent event) {
		String playerName = event.getPlayer().getName();
		Item item = event.getEntityItem().getEntityItem().getItem();
		ResourceLocation itemResourceLoc =  ForgeRegistries.ITEMS.getKey(item);
		String itemName = itemResourceLoc.getResourceDomain() + ":" + itemResourceLoc.getResourcePath();
		
		ItemDropModel itemDropModel = new ItemDropModel();
		itemDropModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		itemDropModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		itemDropModel.data.playername = playerName;
		itemDropModel.data.participant_id = InternalMqttClient.name_to_pid(playerName);
		itemDropModel.data.itemname = itemName;
		itemDropModel.data.item_x = event.getEntityItem().getPosition().getX();
		itemDropModel.data.item_y = event.getEntityItem().getPosition().getY();
		itemDropModel.data.item_z = event.getEntityItem().getPosition().getZ();		
		InternalMqttClient.publish(itemDropModel.toJsonString(), "observations/events/player/itemdrop", playerName);

	}
}
