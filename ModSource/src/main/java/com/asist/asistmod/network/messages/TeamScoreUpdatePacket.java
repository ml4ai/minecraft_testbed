package com.asist.asistmod.network.messages;

import com.asist.asistmod.GuiOverlays.RenderGuiHandler;
import com.asist.asistmod.network.MessagePacket;

import io.netty.buffer.ByteBuf;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class TeamScoreUpdatePacket  extends MessagePacket<TeamScoreUpdatePacket> {
	
	int teamScore;
	
	public TeamScoreUpdatePacket() {}
	
	public TeamScoreUpdatePacket(int ts) {
		this.teamScore = ts;
	}

	@Override
	public void fromBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		this.teamScore = buf.readInt();
	}

	@Override
	public void toBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		buf.writeInt(this.teamScore);
		
	}

	@Override
	@SideOnly(Side.CLIENT)
	public void handleClientSide(TeamScoreUpdatePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		System.out.println("Handling Team Score ClientSide.");
		
		System.out.println("teamScore : " + message.teamScore);
		RenderGuiHandler.testGui.onTeamScoreChange( message.teamScore ) ;
		
	}

	@Override
	@SideOnly(Side.SERVER)
	public void handleServerSide(TeamScoreUpdatePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		
	}

}
