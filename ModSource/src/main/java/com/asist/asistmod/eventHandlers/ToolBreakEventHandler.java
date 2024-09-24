package com.asist.asistmod.eventHandlers;

import java.util.List;

import com.asist.asistmod.datamodels.ItemUsed.ItemUsedModel;
import com.asist.asistmod.datamodels.ToolDepleted.ToolDepletedModel;
import com.asist.asistmod.missionhelpers.enums.ItemType;
import com.asist.asistmod.missionhelpers.mod.ModItems;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.TriageMessagePacket;

import net.minecraft.block.Block;
import net.minecraft.block.BlockLever;
import net.minecraft.block.properties.IProperty;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockAccess;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.item.ItemTossEvent;
import net.minecraftforge.event.entity.living.LivingEntityUseItemEvent;
import net.minecraftforge.event.entity.player.PlayerDestroyItemEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class ToolBreakEventHandler {
	
	
	MinecraftServer server;
	
	public ToolBreakEventHandler(MinecraftServer server) {
		
		this.server = server;
	}
	
	@SubscribeEvent	
	public void onPlayerItemBreak( PlayerDestroyItemEvent event ) {
		
		EntityPlayer player = event.getEntityPlayer();
		String playerName = player.getName();
		ItemStack item = event.getOriginal();
		ItemType heldModItem = ModItems.getEnum(item);
		
		ToolDepletedModel toolDepletedModel = new ToolDepletedModel();
		toolDepletedModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		toolDepletedModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		toolDepletedModel.data.playername = playerName;
		toolDepletedModel.data.participant_id = InternalMqttClient.name_to_pid(playerName);
		toolDepletedModel.data.tool_type = heldModItem.getName();
		InternalMqttClient.publish(toolDepletedModel.toJsonString(), "observations/events/player/tool_depleted", playerName);
		
		
	}
}
