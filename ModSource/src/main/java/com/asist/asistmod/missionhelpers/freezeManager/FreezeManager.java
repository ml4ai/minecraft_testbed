package com.asist.asistmod.missionhelpers.freezeManager;

import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.missionhelpers.RoleManager.RoleTypeLight;

public class FreezeManager {
	
	private static final ConcurrentHashMap<String,Boolean> freezeMap = new ConcurrentHashMap<String,Boolean>();
	
	public static void setFrozenPlayer (String name, Boolean frozen ){
		
		if( freezeMap.containsKey(name) ) {			
			freezeMap.replace(name, frozen);		
		}
		else {			
			freezeMap.put(name, frozen);			
		}		
	}	
	
	public static boolean isPlayerFrozen(String name) {
		
		
		if ( freezeMap.contains(name)) {
			return freezeMap.get(name);
		}
		
		return false;
	}
	
	public static String printFreezeMap() {
		StringBuilder sb = new StringBuilder("");
		
		freezeMap.forEach((k,v) -> {
			sb.append(k);
			sb.append( " : ");
			sb.append( v );
			sb.append( "\n" );
		});
		
		return sb.toString();
	}

}
