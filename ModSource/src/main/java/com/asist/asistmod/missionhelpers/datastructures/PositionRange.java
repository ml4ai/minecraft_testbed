package com.asist.asistmod.missionhelpers.datastructures;

import net.minecraft.util.math.BlockPos;

public class PositionRange {

	private String commandLineOut;
	
	private int fromX;
	private int fromY;
	private int fromZ;
	private int toX;
	private int toY;
	private int toZ;
	
	public BlockPos from;
	public BlockPos to;
	
	public PositionRange(int fromX, int fromY, int fromZ, int toX, int toY, int toZ) {
		this.fromX = fromX;
		this.fromY = fromY;
		this.fromZ = fromZ;
		this.toX = toX;
		this.toY = toY;
		this.toZ = toZ;
		
		this.from = new BlockPos( this.fromX, this.fromY, this.fromZ );
		this.to = new BlockPos ( this.toX, this.toY, this.toZ );
		this.commandLineOut = this.fromX + " " + this.fromY + " " + this.fromZ + " " + this.toX + " " + this.toY + " " + this.toZ;
	}
	
	public String getString() {
		return commandLineOut;
	}
}
