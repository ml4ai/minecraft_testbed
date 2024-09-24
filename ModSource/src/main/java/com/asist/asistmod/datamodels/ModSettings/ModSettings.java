package com.asist.asistmod.datamodels.ModSettings;

// NEED TO IMPORT AT LEAST ONE THING CUS OF STRANGE BUG WITH BUILD.GRADLE
import java.util.HashMap;

public class ModSettings {
	
	public boolean clientSideMapBuilder;
	
	public String clientSideMapBuilderMapBlockFile;
	
	public boolean useRoomDefinitionFile;
	
	public String roomDefinitionFile;
	
	public String mqtthost = null;
	
	public int observationInterval;
	
	public MinSec missionLength = new MinSec(10,0);
	
	public MinSec planningEndTime = new MinSec(10,0);
	
	public MinSec missionLengthTraining = new MinSec(10,0);
	
	public boolean removePlayersOnMissionEnd;
	
	public boolean criticalVictimsShouldExpire = false;	
	
	public boolean authorizePlayers = true;
	
	public long rubbleCollapseBlockInterval = 5000L;
	
	public long victimSignalResetInterval = 1000L;
	
	public MinSec criticalVictimExpirationTime = new MinSec(5,0);
	
	public TriagePointMapping triagePoints = new TriagePointMapping(1,0);
	
	public int proximityVictimPlayerCount = 3;
	
	public boolean triageScoreVisibleToPlayer;
	
	public boolean markerBlocksActive = false;
	
	public MapSettings Test = new MapSettings();
	
	public MapSettings Training = new MapSettings();
	
	public MapSettings Competency = new MapSettings();
	
	public MapSettings Falcon = new MapSettings();

	public MapSettings Custom = new MapSettings();	
	
	public MinSec[] pauseTimes = {};
	
	public String[] observerNames = {};
	
	public PerturbationDef[] blackout_perturbation = null;
	
	public PerturbationDef[] rubble_perturbation = null;
	
	public SafeZone[] safeZonesA = null;
	public SafeZone[] safeZonesB = null;
	public SafeZone[] safeZonesC = null;

}
