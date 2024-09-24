package com.asist.asistmod.block;

import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class BlockPerturbation_Victim extends BlockVictimBase {

	public BlockPerturbation_Victim() {
		this.setHardness(3f);
	}
	
	@SubscribeEvent
	public void onTickEvent() {
		
	}
}

