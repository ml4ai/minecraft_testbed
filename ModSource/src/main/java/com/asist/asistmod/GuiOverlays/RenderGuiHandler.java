package com.asist.asistmod.GuiOverlays;

import com.asist.asistmod.GuiOverlays.TestGui.TestGui;

import net.minecraft.client.Minecraft;
import net.minecraftforge.client.event.RenderGameOverlayEvent;
import net.minecraftforge.client.event.RenderGameOverlayEvent.ElementType;
import net.minecraftforge.fml.client.GuiNotification;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class RenderGuiHandler
{
	public static TestGui testGui;
	
	public RenderGuiHandler() {		
		
	}
	
    @SubscribeEvent
    public void onRenderGui(RenderGameOverlayEvent.Post event)
    {
    	new HeadsUpChatGui(Minecraft.getMinecraft());
    	
    	if (event.getType() != ElementType.EXPERIENCE) return;    	
    	    		
    	testGui = new TestGui(Minecraft.getMinecraft());
    	    	
    	
    }   
}