package com.asist.asistmod.eventHandlers;

import java.util.List;

import com.asist.asistmod.datamodels.ItemUsed.ItemUsedModel;
import com.asist.asistmod.datamodels.ToolDepleted.ToolDepletedModel;
import com.asist.asistmod.missionhelpers.enums.ItemType;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.Block;
import net.minecraft.block.BlockLever;
import net.minecraft.block.properties.IProperty;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.item.EntityItem;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.EnumHand;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockAccess;
import net.minecraftforge.event.entity.item.ItemTossEvent;
import net.minecraftforge.event.entity.living.LivingEntityUseItemEvent;
import net.minecraftforge.event.entity.player.PlayerDestroyItemEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import scala.actors.threadpool.Arrays;

public class ItemTossEventHandler {
	
	
	MinecraftServer server;
	
	public ItemTossEventHandler(MinecraftServer server) {
		
		this.server = server;
	}
	
	@SubscribeEvent	
	public void onPlayerTossItem( ItemTossEvent event) {
		event.setCanceled(true);
		EntityItem item = event.getEntityItem();
		ItemStack itemStack = item.getEntityItem();
		EntityPlayer player = event.getPlayer();
		player.setHeldItem(EnumHand.MAIN_HAND, itemStack);
	}
}
