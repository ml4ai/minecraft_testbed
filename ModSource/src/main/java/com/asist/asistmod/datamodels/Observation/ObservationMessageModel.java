package com.asist.asistmod.datamodels.Observation;

import java.time.Clock;

import com.asist.asistmod.mqtt.InternalMqttClient;

public class ObservationMessageModel {
	
	/*
	 * { "header": { "timestamp": "2019-12-26T14:05:02.3412Z", "message_type":
	 * "observation", "version": "0.2" }, "msg": { "trial_id":
	 * "123e4567-e89b-12d3-a456-426655440000", "timestamp":
	 * "2019-12-26T14:05:02.1412Z", "source": "simulator", "sub_type": "state",
	 * "version": "0.2", "data": { \<subtype specific format data\> } } }
	 */
	
	public String experiment_id = InternalMqttClient.currentTrialInfo.experiment_id;;
	public String trial_id = InternalMqttClient.currentTrialInfo.trial_id;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "state";
	public String version = "1.1";
	
}
