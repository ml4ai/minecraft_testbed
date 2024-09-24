package com.asist.asistmod.missionhelpers.triage;

import java.util.Iterator;

import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager.TriageState;

import net.minecraft.util.math.BlockPos;

public class TriageInstance implements java.lang.Iterable{
	
	public String blockType = null;
	public BlockPos blockPosition = null;
	public int triageState = -1;
	
	
	public TriageInstance( ) { 
		
	}
	
	public TriageInstance( String blockType, BlockPos blockPosition, int triageState ) { 
		this.blockType = blockType;
		this.blockPosition = blockPosition;
		this.triageState = triageState;
	}
	
    public boolean compareBlockPos( BlockPos pos) {
		
		return ( pos.getX() == blockPosition.getX() ) && ( pos.getY() == blockPosition.getY() ) && ( pos.getZ() == blockPosition.getZ() );
	}

	@Override
	public Iterator iterator() {
		// TODO Auto-generated method stub
		return null;
	}
}
