package com.asist.asistmod.GuiOverlays;

import java.util.ArrayList;
import java.util.Queue;

import org.apache.commons.collections4.queue.CircularFifoQueue;

import com.asist.asistmod.network.messages.HeadsUpChatPacket;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.ScaledResolution;

public class HeadsUpChatGui extends Gui
{
    String text = "Hello world!";
    static boolean showMessage = false;
    static Queue<HeadsUpMessage> messageList = new CircularFifoQueue<HeadsUpMessage>(5);
    
    static public void processHeadsUpChatPacket(HeadsUpChatPacket message) {
    	showMessage = true;
    	
    	//if (message.agentInterventionDataModel != null && message.agentInterventionDataModel.renderer != null && message.agentInterventionDataModel.renderer.contains("Minecraft_Overlay")
		//		&& message.agentInterventionDataModel.content != null && !message.agentInterventionDataModel.content.isEmpty()
		//		&& message.agentInterventionDataModel.receiver != null && !message.agentInterventionDataModel.receiver.isEmpty()) {
    	//	long removalTime = System.currentTimeMillis();
    	//	int timeout = 10000;
    		//if (message.agentInterventionDataModel.end != null && !message.agentInterventionDataModel.end.isEmpty()) {
    		//	try {
    		//		timeout = Integer.parseInt(message.agentInterventionDataModel.end);
			//	} catch (Exception e) {
			//	}    			
    		//}
			//removalTime += timeout;
			
    	//	HeadsUpMessage headsUpMessage = new HeadsUpMessage(message.agentInterventionDataModel.content, removalTime);
    	//	messageList.add(headsUpMessage);
    	//}
    }
    
    public HeadsUpChatGui(Minecraft mc)
    {
		//  System.out.println("HeadsUpChatGui: Drawing message");
        ScaledResolution scaled = new ScaledResolution(mc);
        int width = scaled.getScaledWidth();
        int height = scaled.getScaledHeight();
        int i = 0;
        ArrayList<HeadsUpMessage> removalList = new ArrayList<HeadsUpMessage>();
        
        for (HeadsUpMessage headsUpMessage : messageList) {
        	if (System.currentTimeMillis() > headsUpMessage.removalTime) {
        		removalList.add(headsUpMessage);
        	}
        	else {
        		drawString(mc.fontRendererObj, headsUpMessage.message, 10, 10+ i*10, Integer.parseInt("FFFF00", 16));
        	}
        	i++;
		}
        
        if (!removalList.isEmpty()) {
            Queue<HeadsUpMessage> newMessageList = new CircularFifoQueue<HeadsUpMessage>(5);
            for (HeadsUpMessage headsUpMessage : messageList) {
            	if (!removalList.contains(headsUpMessage)) {
            		newMessageList.add(headsUpMessage);
            	}
            }
            messageList = newMessageList;
        }
    }
}