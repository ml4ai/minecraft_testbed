package com.asist.asistmod.missionhelpers.RoleManager;

public enum RoleTypeLight {	
	NULL("None"),
	ADMIN("Admin"),
	MED("Medical_Specialist"),
	ENG("Engineering_Specialist"),
	TRAN("Transport_Specialist");
	
	private String displayName;
	
	RoleTypeLight(String displayName){
		this.displayName = displayName;
	}
	
	public String getDisplayName() {
		return displayName;
	}
}
