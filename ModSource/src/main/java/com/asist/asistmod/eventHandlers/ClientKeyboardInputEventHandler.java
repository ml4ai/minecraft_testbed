package com.asist.asistmod.eventHandlers;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.settings.GameSettings;
import net.minecraft.client.settings.GameSettings.Options;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent.KeyInputEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent.MouseInputEvent;
import net.minecraftforge.fml.relauncher.Side;

import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.time.Clock;

import org.lwjgl.input.Mouse;

import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MouseInputMessage;

public class ClientKeyboardInputEventHandler {
	
	Minecraft minecraft;
	GameSettings gs;
	EntityPlayerSP player;
	int code;
	
	
	@SubscribeEvent 
	public void onKeyboardInput (KeyInputEvent event){		
		
		// INITIALIZATION
		if (player == null ) {			
			if( minecraft == null) {				
				minecraft = Minecraft.getMinecraft();				
			}
			
			if( gs == null) {				
				
				gs = minecraft.gameSettings;			
				
				if(gs.autoJump == true) {					
					gs.setOptionValue(Options.AUTO_JUMP, 0);
				}			
			}			
			player = minecraft.player;			
			code = gs.keyBindJump.getKeyCode();		
		
		}		
		
		if( !player.isCreative() ) {
			
			// CANCEL JUMP
			if( gs.keyBindJump.isPressed() ) {			
				
				if(!player.isCreative()) {				
					gs.keyBindJump.setKeyBindState(code, false);				
				}
				
				// RECANCEL IF PLAYER TURNS IT BACK ON
				if(gs.autoJump == true) {				
					gs.setOptionValue(Options.AUTO_JUMP, 0);
				}			
			}
			else if( gs.keyBindTogglePerspective.isPressed() ) {			
										
				gs.keyBindTogglePerspective.setKeyBindState(gs.keyBindTogglePerspective.getKeyCode(), false);			
							
			}
			else if( gs.keyBindInventory.isPressed() ) {			
				
				gs.keyBindInventory.setKeyBindState(gs.keyBindInventory.getKeyCode(), false);			
							
			}
			else if (gs.keyBindSwapHands.isPressed() ) {
				
				gs.keyBindSwapHands.setKeyBindState(gs.keyBindSwapHands.getKeyCode(), false);
				
			}
			
		}		

		return;	
	}
}
