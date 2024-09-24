package com.asist.asistmod.datamodels.TrialInfo;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TrialInfoModel {
	
	public String experiment_id = "Not Set";
	public String trial_id = "Not Set";
	public String mission_name = "Not Set";
	public String map_name = "Not Set";
	public String map_block_filename = "Not Set";
	public String map_info_filename = "Not Set";
	public List<String> observer_info = null;
	public List<String> active_agents = null;
	public Map<String,String> callsigns = new HashMap<String,String>();
	public Map<String,String> participant_ids = new HashMap<String,String>();
	
}
