package com.asist.asistmod.datamodels.Scoreboard;

import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class ScoreboardData {
	
	public String mission_timer = MissionTimer.getMissionTimeString();public long elapsed_milliseconds = MissionTimer.getElapsedMillisecondsGlobal();
    public ConcurrentHashMap<String, Integer> scoreboard = null;
}
