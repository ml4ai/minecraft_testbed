package com.asist.asistmod.missionhelpers.victims;

import net.minecraft.util.math.BlockPos;

public class VictimData {
	
	public String type;
	
	public BlockPos pos;
	
	public int id;
	
	public VictimData( String type, BlockPos bp, int id) {
		
		this.type = type;
		this.pos = bp;
		this.id = id;
		
	}
	
	public String printVictimData() {
		
		return "Type : " + this.type + " , Pos : " + this.pos  + " , ID : " + this.id; 
	}

}
