package com.asist.asistmod.datamodels.AgentChatIntervention;

import java.util.List;

import com.asist.asistmod.missionhelpers.timer.MissionTimer;

public class AgentChatInterventionDataModel {
	
	//public String id = "Not Set";
    //public String created = "Not Set";
    public long start = -1L;
    // public int duration = 0;
    public String content = "Not Set";
    //public String block_type = "Not Set";
    //public int block_x = 0;
    //public int block_y = 0;
    //public int block_z = 0;  
    public String type = "Not Set";
    public List<String> receivers = null;
    public List<String> renderers = null;
}
