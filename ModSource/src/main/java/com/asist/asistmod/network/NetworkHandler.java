package com.asist.asistmod.network;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.network.messages.MissionTimerPacket;
import com.asist.asistmod.network.messages.MouseInputMessage;
import com.asist.asistmod.network.messages.ParticlesUpdatePacket;
import com.asist.asistmod.network.messages.TeamScoreUpdatePacket;
import com.asist.asistmod.network.messages.TriageMessagePacket;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.World;
import net.minecraft.world.WorldServer;
import net.minecraftforge.fml.common.network.NetworkRegistry;
import net.minecraftforge.fml.common.network.simpleimpl.IMessage;
import net.minecraftforge.fml.common.network.simpleimpl.SimpleNetworkWrapper;
import net.minecraftforge.fml.relauncher.Side;

public class NetworkHandler {
	
	private static SimpleNetworkWrapper INSTANCE;
	

	
	public static void init(  ) {		
		
		INSTANCE = NetworkRegistry.INSTANCE.newSimpleChannel(AsistMod.MODID);	
		
		
		
		//INSTANCE.registerMessage(MouseInputMessage.class, MouseInputMessage.class, 0, Side.SERVER);
		
		INSTANCE.registerMessage(TriageMessagePacket.class, TriageMessagePacket.class, 0, Side.SERVER);	
		
		INSTANCE.registerMessage(MissionTimerPacket.class, MissionTimerPacket.class, 1, Side.CLIENT);
		
		INSTANCE.registerMessage(VictimCountUpdatePacket.class, VictimCountUpdatePacket.class, 2, Side.CLIENT);
		
		INSTANCE.registerMessage(TeamScoreUpdatePacket.class,TeamScoreUpdatePacket.class, 3, Side.CLIENT);		

	}	
	
	public static void sendToServer(IMessage message) {
		INSTANCE.sendToServer(message);		
	}
	
	public static void sendToClient(IMessage message, EntityPlayer player) {		
		
		if (player instanceof EntityPlayerMP) {
			INSTANCE.sendTo(message, (EntityPlayerMP) player);
		}
	}
}
