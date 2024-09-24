package com.asist.asistmod.missionhelpers.markingblocks;

import com.asist.asistmod.datamodels.ModSettings.MinSec;

import net.minecraft.block.state.IBlockState;

public class TimeAndBlock {
	
	MinSec timeTrigger;
	IBlockState block;
	
	
	public TimeAndBlock(MinSec t, IBlockState block) {
		this.timeTrigger = t;
		this.block = block;
	}

}
