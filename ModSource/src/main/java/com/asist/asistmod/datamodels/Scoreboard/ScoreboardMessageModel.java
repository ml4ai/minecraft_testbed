package com.asist.asistmod.datamodels.Scoreboard;

import java.time.Clock;

public class ScoreboardMessageModel {
	
	/*
	 * { "header": { "timestamp": "2019-12-26T14:05:02.3412Z", "message_type":
	 * "observation", "version": "0.2" }, "msg": { "trial_id":
	 * "123e4567-e89b-12d3-a456-426655440000", "timestamp":
	 * "2019-12-26T14:05:02.1412Z", "source": "simulator", "sub_type": "state",
	 * "version": "0.2", "data": { \<subtype specific format data\> } } }
	 */
	
	public String experiment_id = null;
	public String trial_id = null;
	public String timestamp = Clock.systemUTC().instant().toString();
	public String source = "simulator";
	public String sub_type = "Event:Scoreboard";
	public String version = "0.5";	
	
	
	

}
