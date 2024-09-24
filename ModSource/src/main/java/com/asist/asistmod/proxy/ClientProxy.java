package com.asist.asistmod.proxy;


import com.asist.asistmod.item._Items;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.client.Minecraft;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.entity.player.PlayerSetSpawnEvent;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.PlayerEvent;

public class ClientProxy extends CommonProxy {
	
	
    public void preInit(FMLPreInitializationEvent e) {
    	
    	super.preInit(e);
    }
	
	
    public void init(FMLInitializationEvent e) {
    	super.init(e);    	
    	
    }
	
	
    public void postInit(FMLPostInitializationEvent e) {
    	
    	super.postInit(e);
    	_Items.clientPostInit();
    	
    }
}
