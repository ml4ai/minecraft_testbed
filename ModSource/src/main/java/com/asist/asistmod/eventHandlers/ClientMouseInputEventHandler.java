package com.asist.asistmod.eventHandlers;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.settings.GameSettings;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent.MouseInputEvent;
import net.minecraftforge.fml.relauncher.Side;

import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.time.Clock;

import org.lwjgl.input.Mouse;

import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MouseInputMessage;

public class ClientMouseInputEventHandler {

	
	boolean down = false;
	long startClickTime = 0;
	long endClickTime = 0;
	
	@SubscribeEvent 
	public void onMouseInput (MouseInputEvent event){	
		
		GameSettings gs = Minecraft.getMinecraft().gameSettings;
		// only sends updates on change to not spam server
		
		if(gs.keyBindAttack.isKeyDown() && down == false) {			
			
			
			down = true;
			// NetworkHandler.sendToServer( new MouseInputMessage( true ) );
			// Start Timer
			startClickTime = Clock.systemDefaultZone().millis();
		}							
		else if( !gs.keyBindAttack.isKeyDown() && down == true ) {
			
			// STANDARD MOUSE UP
			down = false;								
			// NetworkHandler.sendToServer( new MouseInputMessage( false ) );
			// Stop Timer
			endClickTime = Clock.systemDefaultZone().millis();
			System.out.println("Elapsed Milliseconds : " + (endClickTime - startClickTime));
		}		
		return;	
	}
}
