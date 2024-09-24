package com.asist.asistmod.network.messages;

import com.asist.asistmod.GuiOverlays.RenderGuiHandler;
import com.asist.asistmod.network.MessagePacket;

import io.netty.buffer.ByteBuf;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class VictimCountUpdatePacket  extends MessagePacket<VictimCountUpdatePacket> {	
	
	int regularVictimsSaved=0;
	int maxRegularVictimCount=0;
	
	int criticalVictimsSaved=0;
	int maxCriticalVictimCount=0;
	
	int teamScore=0;
	int maxTeamScore=0;
	
	public VictimCountUpdatePacket() {}
	
	public VictimCountUpdatePacket(int rvs, int mrv, int cvs, int mcv, int ts, int mts) {
		
		this.regularVictimsSaved = rvs;		
		this.maxRegularVictimCount = mrv;
		
		this.criticalVictimsSaved=cvs;
		this.maxCriticalVictimCount=mcv;
		
		this.teamScore=ts;
		this.maxTeamScore=mts;
	}
	
	

	@Override
	public void fromBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		this.regularVictimsSaved = buf.readInt();
		this.maxRegularVictimCount = buf.readInt();
		
		this.criticalVictimsSaved = buf.readInt();
		this.maxCriticalVictimCount = buf.readInt();
		
		this.teamScore = buf.readInt();
		this.maxTeamScore = buf.readInt();
	}

	@Override
	public void toBytes(ByteBuf buf) {
		// TODO Auto-generated method stub
		buf.writeInt(this.regularVictimsSaved);
		buf.writeInt(this.maxRegularVictimCount);
		buf.writeInt(this.criticalVictimsSaved);
		buf.writeInt(this.maxCriticalVictimCount);
		buf.writeInt(this.teamScore);
		buf.writeInt(this.maxTeamScore);
		
	}

	@Override
	@SideOnly(Side.CLIENT)
	public void handleClientSide(VictimCountUpdatePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		System.out.println("Handling Scoreboard Update ClientSide.");		
		
		RenderGuiHandler.testGui.onScoreboardChange( 
				
			message.regularVictimsSaved, message.maxRegularVictimCount, message.criticalVictimsSaved, 
			message.maxCriticalVictimCount,message.teamScore,message.maxTeamScore 
		);
		
	}

	@Override
	@SideOnly(Side.SERVER)
	public void handleServerSide(VictimCountUpdatePacket message, EntityPlayer player) {
		// TODO Auto-generated method stub
		
	}

}
