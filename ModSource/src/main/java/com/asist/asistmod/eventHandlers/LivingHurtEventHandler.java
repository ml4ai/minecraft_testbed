package com.asist.asistmod.eventHandlers;


import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraftforge.event.entity.living.LivingHurtEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class LivingHurtEventHandler {

	public LivingHurtEventHandler() {
		// TODO Auto-generated constructor stub
	}
	
	@SubscribeEvent	
	public void onHurt(LivingHurtEvent event) {
		
		event.setCanceled(true);
	}

}
