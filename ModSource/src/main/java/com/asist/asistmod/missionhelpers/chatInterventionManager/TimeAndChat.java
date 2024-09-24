package com.asist.asistmod.missionhelpers.chatInterventionManager;

import java.util.List;

import com.asist.asistmod.datamodels.ModSettings.MinSec;

import net.minecraft.block.state.IBlockState;

public class TimeAndChat {
	
	MinSec timeTrigger;
	String content;
	List receivers;
	
	
	public TimeAndChat(MinSec t, String c, List r) {
		
		this.timeTrigger = t;
		this.content = c;
		this.receivers = r;
		
	}

}
