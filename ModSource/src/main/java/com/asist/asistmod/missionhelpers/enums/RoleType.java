package com.asist.asistmod.missionhelpers.enums;

public enum RoleType {
	MED		(1, "medical", 11546150, ItemType.MEDICALKIT),
	TRAN		(2, "search", 6192150, ItemType.STRETCHER),
	ENG		(3, "hammer", 3949738, ItemType.HAMMER),
	ADMIN 	(4, "admin", 1908001, ItemType.NULL),
	NULL	(0, "null", 0, ItemType.NULL)
	;
	
	private final int code;
	private final String name;
	private final int color;
	private final ItemType tool;
	
	RoleType(int code, String name, int color, ItemType tool) {
		this.code = code;
		this.name = name;
		this.color = color;
		this.tool = tool;
	}
	
	public int getCode() {
		return this.code;
	}
	
	public String getName() {
		return this.name;
	}
	
	public int getColor() {
		return this.color;
	}
	
	public ItemType getTool() {
		return this.tool;
	}
	
	public boolean notNull() {
		return !this.name.equals("null");
	}
}
