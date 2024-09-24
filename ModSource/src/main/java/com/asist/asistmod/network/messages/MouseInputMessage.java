package com.asist.asistmod.network.messages;


import com.asist.asistmod.network.MessagePacket;

import io.netty.buffer.ByteBuf;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraftforge.fml.common.network.simpleimpl.IMessage;

public class MouseInputMessage extends MessagePacket<MouseInputMessage> {
	
	boolean mouseDown = false;
	
	public MouseInputMessage() {}
	
	public MouseInputMessage( boolean mouseDown) {		
		
		this.mouseDown = mouseDown;		
	}

	// NEEDS TO BE IN SAME ORDER AS toBytes
	@Override
	public void fromBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		mouseDown = buf.readBoolean();
		
	}

	// NEEDS TO BE IN SAME ORDER AS fromBytes
	@Override
	public void toBytes(ByteBuf buf) {
		// TODO Auto-generated method stub					
		buf.writeBoolean(mouseDown);
	}

	@Override
	public void handleClientSide(MouseInputMessage message, EntityPlayer player) {
		// TODO Auto-generated method stub
		// do something with this server data now that we are on the client
	}

	@Override
	public void handleServerSide(MouseInputMessage message, EntityPlayer player) {
		mouseDown = message.mouseDown;
		// do something with this client data now that we are on the server
	}

}
