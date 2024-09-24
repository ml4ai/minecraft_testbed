package com.asist.asistmod.missionhelpers.chatInterventionManager;

import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.datamodels.ModSettings.MinSec;
import com.asist.asistmod.missionhelpers.datastructures.Player;
import com.asist.asistmod.missionhelpers.datastructures.PlayerManager;
import com.asist.asistmod.missionhelpers.markingblocks.TimeAndBlock;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.missionhelpers.timer.MissionTimerListener;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.SoundEvents;
import net.minecraft.util.SoundCategory;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.math.BlockPos;

public class ChatInterventionManager{
	
	static int id = 0;
	static ConcurrentHashMap<Integer,LongAndChat> startIntervention =  new ConcurrentHashMap<Integer,LongAndChat>();
	
	
	public static void addChatIntervention ( String content, String receiver, long startTime) {	
					
	
		// CONVERT FROM PID TO NAME
		String playerName = InternalMqttClient.pid_to_name(receiver);
		
		startIntervention.put(id, new LongAndChat(startTime,content,playerName) );
		
		System.out.println("Entered Chat Intervention ID: " + id);
		
		id++;
				
		
	}
	
	
	
	public static void onMissionTimeChange(int m, int s, long elapsedMilliseconds) {		
		
		try {
			
			for( ConcurrentHashMap.Entry<Integer,LongAndChat> entry : startIntervention.entrySet() ) {
				
				System.out.println("Checking Chat ID : " + entry.getKey() );
				
				LongAndChat e = entry.getValue();
				
				if( (e.longTime < 0) || (e.longTime <= elapsedMilliseconds)  ) {				
					

					System.out.println("Triggering chat inervention for " + e.receiver +" @ "+m+" : "+s);
					
					MissionTimer.server.commandManager.executeCommand(MissionTimer.server, "tellraw " + e.receiver + " { \"text\": \"" + "ADVISOR : "+ e.content + "\", \"color\": \"yellow\"}");
					
					startIntervention.remove( entry.getKey() );				
					
					Player p = PlayerManager.getPlayerByName(e.receiver);
					
					EntityPlayer ep = p.getEntityPlayer();
					
					BlockPos pos = ep.getPosition();
					
					// play sound only for receiving player at their location
					AsistMod.server.commandManager.executeCommand(AsistMod.server, "playsound minecraft:block.note.pling voice "+e.receiver+" " + pos.getX() + " " + pos.getY() + " " + pos.getZ() );
					
					//ep.playSound(SoundEvents.BLOCK_NOTE_PLING,1.0f, 1.0f);
					//ep.getEntityWorld().playSound(ep, (double)ep.getPosition().getX(), (double)ep.getPosition().getY(), (double)ep.getPosition().getZ(), SoundEvents.BLOCK_NOTE_PLING, SoundCategory.NEUTRAL, 1.0f, 1.0f);
				}			
			}
		}
		catch (Exception e){
			
			System.out.println(" Tried to trigger a chat intervention, but something went wrong - make sure the receivers field is an array of participant id's, not names.");
			
			e.printStackTrace();
									
		}
		
	}

}
