package com.asist.asistmod.eventHandlers;

import com.google.common.eventbus.Subscribe;

import net.minecraftforge.client.event.FOVUpdateEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class FOVUpdateEventHandler {
	
	@SideOnly(Side.CLIENT)
	@SubscribeEvent
	public void onFOVUpdateEvent( FOVUpdateEvent e) {
		
		//System.out.println("FOV UPDATE");
		
		//e.getFov();
		
	}

}
