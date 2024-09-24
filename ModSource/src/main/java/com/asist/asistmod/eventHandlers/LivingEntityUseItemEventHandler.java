package com.asist.asistmod.eventHandlers;

import java.util.List;

import com.asist.asistmod.datamodels.ItemUsed.ItemUsedModel;
import com.asist.asistmod.missionhelpers.pause.PauseManager;
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
import net.minecraftforge.event.entity.living.LivingEntityUseItemEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class LivingEntityUseItemEventHandler {
	
	
	MinecraftServer server;
	
	public LivingEntityUseItemEventHandler(MinecraftServer server) {
		
		this.server = server;
	}
	
	@SubscribeEvent	
	public void onItemUse( LivingEntityUseItemEvent.Finish event) {
		String playerName = event.getEntity().getName();
		Item item = event.getItem().getItem();
		ResourceLocation itemResourceLoc =  ForgeRegistries.ITEMS.getKey(item);
		String itemName = itemResourceLoc.getResourceDomain() + ":" + itemResourceLoc.getResourcePath();		
		
		ItemUsedModel itemUsedModel = new ItemUsedModel();
		itemUsedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		itemUsedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		itemUsedModel.data.playername = playerName;
		itemUsedModel.data.participant_id = InternalMqttClient.name_to_pid(playerName);
		itemUsedModel.data.itemname = itemName;
		itemUsedModel.data.item_x = event.getEntity().getPosition().getX();
		itemUsedModel.data.item_y = event.getEntity().getPosition().getY();
		itemUsedModel.data.item_z = event.getEntity().getPosition().getZ();		
		InternalMqttClient.publish(itemUsedModel.toJsonString(), "observations/events/player/itemuse", playerName);

	}
	
	
}
