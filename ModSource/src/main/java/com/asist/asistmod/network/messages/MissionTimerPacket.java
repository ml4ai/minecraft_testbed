package com.asist.asistmod.network.messages;

import com.asist.asistmod.GuiOverlays.RenderGuiHandler;
import com.asist.asistmod.GuiOverlays.TestGui.TestGui;
import com.asist.asistmod.network.MessagePacket;

import io.netty.buffer.ByteBuf;
import net.minecraft.entity.player.EntityPlayer;

public class MissionTimerPacket extends MessagePacket<MissionTimerPacket> {
	
	int minutes;
	int seconds;
	
	public MissionTimerPacket() {}
	
	public MissionTimerPacket(int minutes, int seconds) {
		
		this.minutes = minutes;
		this.seconds = seconds;
		
	}

	@Override
	public void fromBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		this.minutes = buf.readInt();
		this.seconds = buf.readInt();
	}

	@Override
	public void toBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		buf.writeInt(minutes);
		buf.writeInt(seconds);
	}

	@Override
	public void handleClientSide(MissionTimerPacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		
		
		System.out.println("Handling ClientSide.");
		// NEED A REF TO TEST GUI
		System.out.println(message.minutes+","+message.seconds);
		RenderGuiHandler.testGui.onMissionTimeChange(message.minutes,message.seconds);
		
	}

	@Override
	public void handleServerSide(MissionTimerPacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		
	}

}
