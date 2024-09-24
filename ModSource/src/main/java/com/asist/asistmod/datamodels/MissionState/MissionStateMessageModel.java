package com.asist.asistmod.datamodels.MissionState;

import java.time.Clock;

import com.asist.asistmod.mqtt.InternalMqttClient;

public class MissionStateMessageModel {
	
	public String experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;
	public String trial_id = InternalMqttClient.currentTrialInfo.trial_id;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:MissionState";
	public String version = "0.5";	
	
	
	
}
