package com.asist.asistmod.datamodels.Observation;

import java.time.Clock;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ObservationData {
	
	/*
	 * "name" : "Aptiminier1", "world_time" : 2000, "total_time" : 5179290,
	 * "entity_type" : "human", "yaw" : 0.0, "x" : -2145.5, "y" : 33.0, "z" :
	 * 154.1162109375, "pitch" : 0.0, "id" : "2aa66a93-ce78-3ee2-b0df-a46c9fce8441",
	 * "motion_x" : 0.0, "motion_y" : 0.0, "motion_z" : 0.0, "life" : 20.0
	 */
	public String mission_timer = MissionTimer.getMissionTimeString();
	public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
    public int observation_number = 0;
    public String timestamp = Clock.systemUTC().instant().toString();
	public String playername = null;
	public String participant_id = "Not Set";
	public Long world_time = null;
	public Long total_time = null;
	public String entity_type = null;
	public Float yaw = null;
	public Double x = null;
	public Double y = null;
	public Double z = null;
	public Float pitch = null;
	public String id = null;
	public Double motion_x= null;
	public Double motion_y = null;
	public Double motion_z = null;
	public Float life = null;
  

}
