package com.asist.asistmod.missionhelpers.victims;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicReference;

public class SignalData {
	
	public CopyOnWriteArrayList<VictimData> victimList = new CopyOnWriteArrayList<VictimData>();
	public List<String> roomNames;
	

	public SignalData() {
		// TODO Auto-generated constructor stub
	}
	
	public String getSignalString() {
		
		String out = "No Victim Detected";
		
		if(!victimList.isEmpty()) {
			
			out = "Regular Victim Detected";
			
			for(int i = 0; i < victimList.size(); i++) {			
				
				VictimData data = victimList.get(i);
				
				if( data.type.contentEquals("block_victim_proximity") || data.type.contentEquals("block_victim_2")) {
					out = ("Critical Victim Detected");
					break;
				}				
			};			
		}
		
		return out;
	}

}
