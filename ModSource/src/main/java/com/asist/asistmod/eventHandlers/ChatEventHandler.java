package com.asist.asistmod.eventHandlers;

import java.time.Clock;
import java.util.List;

import org.eclipse.paho.client.mqttv3.MqttClient;

import com.asist.asistmod.datamodels.Chat.ChatModel;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraftforge.client.event.ClientChatReceivedEvent;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class ChatEventHandler {
	
	public ChatEventHandler() {}
	
	@SubscribeEvent	
	public void onChat(ServerChatEvent event){
		
		System.out.println(event.getMessage());
		
		// THIS STILL NEEDS PLAYERNAME TO PID CONVERSION
		
		// Get player list
		List<EntityPlayerMP> playersArray = event.getPlayer().getServer().getPlayerList().getPlayers();
		// create mutable sb object
		StringBuilder nameString = new StringBuilder("");
		// append names with comma delimiter
		playersArray.forEach( (player)->{
			
			nameString.append(player.getName() + ',');
			
		});
		
		ChatModel chatMessage = new ChatModel();		
		
		//header
		chatMessage.header.message_type = "chat";
		
		//msg
		chatMessage.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
		chatMessage.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
		
		
		chatMessage.data.sender = event.getUsername();
		
		//msg.data
		chatMessage.data.addressees = nameString.toString().split(",");
		chatMessage.data.text = event.getMessage();
		
		InternalMqttClient.publish(chatMessage.toJsonString(), "minecraft/chat", event.getUsername() );
		
	}
}
