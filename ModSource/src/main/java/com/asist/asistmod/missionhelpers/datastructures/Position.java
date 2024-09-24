package com.asist.asistmod.missionhelpers.datastructures;

import net.minecraft.util.math.BlockPos;

public class Position {

	private String commandLineOut;
	
	private int posX;
	private int posY;
	private int posZ;
	
	public BlockPos blockPos;
	
	public Position(int x, int y, int z) {
		this.posX = x;
		this.posY = y;
		this.posZ = z;
		
		blockPos = new BlockPos(x, y, z);
		commandLineOut = this.posX + " " + this.posY + " " + this.posZ;
	}
	
	public Position(BlockPos pos) {
		this.posX = pos.getX();
		this.posY = pos.getY();
		this.posZ = pos.getZ();	
		
		blockPos = pos;
		commandLineOut = this.posX + " " + this.posY + " " + this.posZ;
	}
	
	public Position(int taskNumber, int playerNumber) {
		if(taskNumber == 14) {
			this.posX = -2152;
			this.posY = 61;
			this.posZ = 120;
		}
		else 
		{
			int playerOffset = (playerNumber-1) * 4;
			this.posX = 0 + playerOffset + ((taskNumber-1) * 13);
			this.posY = 23;
			this.posZ = 0;			
		}
		
		blockPos = new BlockPos(this.posX, this.posY, this.posZ);
		commandLineOut = this.posX + " " + this.posY + " " + this.posZ;
	}
	
	public String getString() {
		return commandLineOut;
	}
	
	public int getX() {
		return this.posX;
	}
	
	public int getY() {
		return this.posY;
	}
	
	public int getZ() {
		return this.posZ;
	}
}
