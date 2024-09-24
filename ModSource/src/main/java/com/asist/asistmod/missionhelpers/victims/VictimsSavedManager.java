package com.asist.asistmod.missionhelpers.victims;

import java.util.ArrayList;
import java.util.List;

public class VictimsSavedManager {

	public static List<Integer> savedIds = new ArrayList<Integer>();
	
	public VictimsSavedManager() {
		// TODO Auto-generated constructor stub
		
	}
	
	public static void addSavedVictimId(int id) {
		savedIds.add(id);
	}
	
	public static boolean victimIsSaved(int id) {
		return savedIds.contains(id);
	}

}
