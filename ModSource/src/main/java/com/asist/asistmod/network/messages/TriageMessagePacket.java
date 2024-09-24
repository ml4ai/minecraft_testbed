package com.asist.asistmod.network.messages;

import com.asist.asistmod.missionhelpers.triage.TriageInstance;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.datamodels.Triage.TriageModel;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mod.ModBlocks;
import com.asist.asistmod.missionhelpers.pause.PauseManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.network.MessagePacket;
import com.asist.asistmod.network.NetworkHandler;

import io.netty.buffer.ByteBuf;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.fml.common.network.simpleimpl.IMessage;

public class TriageMessagePacket extends MessagePacket<TriageMessagePacket> {
	
	
	int messageId = -1;
	
	int blockType_String_length = 0;
	int triagingPlayer_String_length = 0;
	
	String blockType_String = "";
	String triagingPlayer_String = "";
	
	int blockX = 0;
	int blockY = 0;
	int blockZ = 0;
	
	int triageState = -1;
	
	public TriageMessagePacket() {}
	
	public TriageMessagePacket( int blockType_String_length, String blockType_String, int triagingPlayer_String_length, String triagingPlayer_String, int blockX, int blockY, int blockZ, int triageState, int messageId) {
		
		this.blockType_String_length = blockType_String_length;
		this.blockType_String = blockType_String;
		this.triagingPlayer_String_length = triagingPlayer_String_length;
		this.triagingPlayer_String = triagingPlayer_String;
		this.blockType_String = blockType_String;
		this.blockX = blockX;
		this.blockY=blockY;
		this.blockZ=blockZ;	
		this.triageState = triageState;
		this.messageId = messageId;
		
	}

	// NEEDS TO BE IN SAME ORDER AS toBytes
	@Override
	public void fromBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		
		StringBuilder builder = new StringBuilder("");		
		blockType_String_length = buf.readInt();
		
		for(int i=0; i<blockType_String_length; i++) {			
			builder.append(buf.readChar());			
		}
		
		blockType_String = builder.toString();
		
		builder = new StringBuilder("");
		
		triagingPlayer_String_length = buf.readInt();
		
		for(int i=0; i<triagingPlayer_String_length; i++) {			
			builder.append(buf.readChar());			
		}
		
		triagingPlayer_String = builder.toString();
		
		blockX = buf.readInt();
		blockY = buf.readInt();
		blockZ = buf.readInt();
		triageState = buf.readInt();
		messageId = buf.readInt();
		
		
	}

	// NEEDS TO BE IN SAME ORDER AS fromBytes
	@Override
	public void toBytes(ByteBuf buf) {
		// TODO Auto-generated method stub	
		
		
		buf.writeInt(blockType_String_length);
		for(int i=0; i<blockType_String_length; i++) {			
			buf.writeChar(blockType_String.charAt(i));			
		}
		
		buf.writeInt(triagingPlayer_String_length);
		for(int i=0; i<triagingPlayer_String_length; i++) {			
			buf.writeChar(triagingPlayer_String.charAt(i));			
		}
		
		buf.writeInt(blockX);
		buf.writeInt(blockY);
		buf.writeInt(blockZ);		
		buf.writeInt(triageState);
		buf.writeInt(messageId);
		
		
	}

	@Override
	public void handleClientSide(TriageMessagePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void handleServerSide(TriageMessagePacket message, EntityPlayer player) {
					
			
		    triagingPlayer_String = message.triagingPlayer_String;
		    
		    if( triagingPlayer_String.contentEquals( player.getName() ) ) {
		    	
		    	blockType_String = message.blockType_String;
				blockX = message.blockX;
				blockY = message.blockY;
				blockZ = message.blockZ;
				triageState = message.triageState;
				messageId = message.messageId;
				
				System.out.println( blockType_String + "," + triagingPlayer_String + "," +blockX+","+ blockY+","+blockZ+","+ triageState +"," + messageId );			
				
				//if(PauseManager.isInitialized) {
				//	PauseManager.updateTriageStatus(player.getName(), new TriageInstance(blockType_String, new BlockPos(blockX,blockY,blockZ),triageState) );
				//}
				
				String playerName = player.getName();
				//PUBLISH
				
				TriageModel triageModel = new TriageModel();
				triageModel.msg.experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
				triageModel.msg.trial_id = InternalMqttClient.currentTrialInfo.trial_id;
				triageModel.data.playername = playerName;
				triageModel.data.participant_id = InternalMqttClient.currentTrialInfo.participant_ids.get(playerName);
				triageModel.data.triage_state = ClientSideTriageManager.TriageState.values()[triageState].toString();
				triageModel.data.victim_x = blockX;
				triageModel.data.victim_y = blockY;
				triageModel.data.victim_z = blockZ;
				triageModel.data.type = ModBlocks.getEnumFromRegistryName(blockType_String).getName();	        		
				triageModel.data.victim_id = MapBlockManager.getVictimId(new BlockPos(blockX,blockY,blockZ));				
				if(InternalMqttClient.isInitialized) {
					InternalMqttClient.publish(triageModel.toJsonString(), "observations/events/player/triage", player.getName());
				}		    	
		    }
		    else {
		    	System.out.println("--------------- IGNORING ERRONEOUS TRIAGE PACKET FROM NEARBY PLAYER --------->  " + triagingPlayer_String);
		    }
	}

}
