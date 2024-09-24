package com.asist.asistmod.eventHandlers;

import java.time.Clock;
import java.util.Arrays;

import org.eclipse.paho.client.mqttv3.MqttClient;

import com.asist.asistmod.datamodels.Chat.ChatModel;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraftforge.client.event.ClientChatReceivedEvent;
import net.minecraftforge.event.CommandEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class CommandEventHandler {
	
	public CommandEventHandler() {}
	
	@SubscribeEvent	
	public void onChat(CommandEvent event){		
	
		
		// THIS STILL NEEDS PLAYERNAME TO PID CONVERSION
		if (event.getCommand().getName().equals("tell") || event.getCommand().getName().equals("tellraw")) {
			
			String[] params = event.getParameters();			
			
			String sender = event.getSender().getName();

			ChatModel chatMessage = new ChatModel();
			
			//header
			chatMessage.header.message_type = "chat";
			//msg
			chatMessage.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
			chatMessage.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
			//msg.data
			// check if this is the server or not then decide what the name or pid should be
			chatMessage.data.sender = sender.contentEquals("Server")?sender:InternalMqttClient.name_to_pid(sender);
			if (params.length >= 2) {
				chatMessage.data.addressees = new String[1];
				chatMessage.data.addressees[0] = InternalMqttClient.name_to_pid(params[0]);
				chatMessage.data.text = String.join(" ", Arrays.copyOfRange(params, 1, params.length));			
			}		
			
			InternalMqttClient.publish(chatMessage.toJsonString(), "minecraft/chat", sender);
		
		}
	}
}

