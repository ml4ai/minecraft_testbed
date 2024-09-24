package com.asist.asistmod.network.messages;

import com.asist.asistmod.missionhelpers.triage.TriageInstance;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.GuiOverlays.HeadsUpChatGui;
import com.asist.asistmod.datamodels.AgentChatIntervention.AgentChatInterventionDataModel;
import com.asist.asistmod.datamodels.AgentChatIntervention.AgentChatInterventionModel;
import com.asist.asistmod.datamodels.Triage.TriageModel;
import com.asist.asistmod.missionhelpers.pause.PauseManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.network.MessagePacket;
import com.asist.asistmod.network.NetworkHandler;
import com.google.gson.Gson;

import io.netty.buffer.ByteBuf;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.fml.common.network.simpleimpl.IMessage;

public class HeadsUpChatPacket extends MessagePacket<HeadsUpChatPacket> {
	
	
	int messageId = -1;
	
	public AgentChatInterventionDataModel agentInterventionDataModel = null;

	
	public HeadsUpChatPacket() {}
	
	public HeadsUpChatPacket( AgentChatInterventionDataModel agentInterventionDataModel, int messageId) {
		
		this.agentInterventionDataModel = agentInterventionDataModel;
		this.messageId = messageId;
		
	}

	// NEEDS TO BE IN SAME ORDER AS toBytes
	@Override
	public void fromBytes(ByteBuf buf) {
		int string_length = 0;
		
		StringBuilder builder = new StringBuilder("");
		string_length = buf.readInt();
		
		for(int i=0; i<string_length; i++) {			
			builder.append(buf.readChar());			
		}
		String payload = builder.toString();
		
		Gson gson = new Gson();
		this.agentInterventionDataModel = gson.fromJson(payload, AgentChatInterventionDataModel.class);

		messageId = buf.readInt();		
	}

	// NEEDS TO BE IN SAME ORDER AS fromBytes
	@Override
	public void toBytes(ByteBuf buf) {
		
		Gson gson = new Gson();
		String payload = gson.toJson(this.agentInterventionDataModel); 
		
		buf.writeInt(payload.length());
		
		for(int i=0; i<payload.length(); i++) {			
			buf.writeChar(payload.charAt(i));			
		}
		buf.writeInt(messageId);				
	}

	@Override
	public void handleClientSide(HeadsUpChatPacket message, EntityPlayer player) {
		System.out.println("HeadsUpChatPacket: Received message");
		
		HeadsUpChatGui.processHeadsUpChatPacket(message);
		
		
	}

	@Override
	public void handleServerSide(HeadsUpChatPacket message, EntityPlayer player) {					
					
	}

}
