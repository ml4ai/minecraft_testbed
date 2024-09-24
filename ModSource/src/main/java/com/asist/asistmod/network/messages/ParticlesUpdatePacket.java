package com.asist.asistmod.network.messages;

import com.asist.asistmod.GuiOverlays.RenderGuiHandler;
import com.asist.asistmod.block.BlockVictim_2;
import com.asist.asistmod.network.MessagePacket;

import io.netty.buffer.ByteBuf;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class ParticlesUpdatePacket  extends MessagePacket<ParticlesUpdatePacket> {
	
	boolean particlesOn;
	
	int xPos;
	int yPos;
	int zPos;
	
	
	public ParticlesUpdatePacket() {}
	
	public ParticlesUpdatePacket(boolean on,int x,int y,int z) {
		
		this.particlesOn = on;
		this.xPos = x;
		this.yPos = y;
		this.zPos = z;
		
	}

	@Override
	public void fromBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		this.particlesOn = buf.readBoolean();
		this.xPos = buf.readInt();
		this.yPos = buf.readInt();
		this.zPos = buf.readInt();
	}

	@Override
	public void toBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		buf.writeBoolean(this.particlesOn);
		buf.writeInt(this.xPos);
		buf.writeInt(this.yPos);
		buf.writeInt(this.zPos);
		
	}

	@Override
	@SideOnly(Side.CLIENT)
	public void handleClientSide(ParticlesUpdatePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		System.out.println("Handling ParticlesOn ClientSide.");
		// NEED A REF TO TEST GUI
		System.out.println("ParticlesOn : " + message.particlesOn);
		// FIND THE BLOCK IN THE WORLD AND SE PARTICLES TO ON
		BlockPos pos = new BlockPos(message.xPos,message.yPos,message.zPos);
		
		IBlockState state  = player.getEntityWorld().getBlockState(pos);
		
		
	}

	@Override
	@SideOnly(Side.SERVER)
	public void handleServerSide(ParticlesUpdatePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		
	}

}
