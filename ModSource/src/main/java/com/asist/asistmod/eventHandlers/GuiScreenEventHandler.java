package com.asist.asistmod.eventHandlers;


import net.minecraftforge.client.event.GuiScreenEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class GuiScreenEventHandler {
	
	@SideOnly(Side.CLIENT)	
	@SubscribeEvent	
	public void onGuiScreenEvent( GuiScreenEvent event) {
		//System.out.println("There was a gui event");
	}
		

}
