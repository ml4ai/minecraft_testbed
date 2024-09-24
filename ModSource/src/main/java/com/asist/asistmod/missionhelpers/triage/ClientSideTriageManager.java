package com.asist.asistmod.missionhelpers.triage;

import java.time.Clock;
import java.util.HashMap;
import java.util.List;

import com.asist.asistmod.datamodels.Triage.TriageModel;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.google.gson.Gson;

import net.minecraft.block.Block;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;

public class ClientSideTriageManager {
	
	public static int messageId = 0;
	
	public static enum TriageState {IN_PROGRESS, UNSUCCESSFUL, SUCCESSFUL;}
}

