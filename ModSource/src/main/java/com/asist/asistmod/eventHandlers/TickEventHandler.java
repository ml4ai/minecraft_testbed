package com.asist.asistmod.eventHandlers;


import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;

public class TickEventHandler {
	
	int ticks = 0;
	@SubscribeEvent	
	public void tick(TickEvent event) {
		
		//ticks++;
		//System.out.println("------------------------------------------------------- TICK "+ (ticks++) +" ------------------------------------------");
		
		//if(ticks % 1000 == 0) {
			
			// InternalMqttClient.publish("{\"ticks\":"+ticks+"}", "status/server/tick");
			
		//}
		
		
	}

}
