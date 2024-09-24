package com.asist.asistmod.datamodels.ModSettings;

import java.util.Map;

public class PerturbationDef {
	
	public String triggering_mission;
	
	public Map<String,Integer> start;
	
	public Map<String,Integer> end;
	
	public String file;

	public PerturbationDef() {
		// TODO Auto-generated constructor stub
	}
	
	public int getStartMinute() {		
		Integer out = (Integer) start.get("minute");		
		if (out != null) return out;		
		return -1;
	}
	
	public int getStartSecond() {
		Integer out = (Integer) start.get("second");
		if (out != null) return out;		
		return -1;
	}
	
	public int getEndMinute() {
		Integer out = (Integer) end.get("minute");
		if (out != null) return out;		
		return -1; 
	}
	
	public int getEndSecond() {
		Integer out = (Integer) end.get("second");
		if (out != null) return out;		
		return -1; 
	}

}
