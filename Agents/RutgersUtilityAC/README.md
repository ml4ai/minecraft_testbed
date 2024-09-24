# Rutgers Utility Agent


## Threat room coordination AC

### Overview
Measure of time from threat plate activation until the associated threat rubble is removed, and which player activates the threat plate. This measure is intended to capture how efficiently the team coordinates to rescue team mates stuck in threat rooms.

### Inputs
rubble collapse event, rubble removal event

### Measurements

The output will be a dictionary of lists.
- **room_id:** Room id of activated threat plate
- **threat_activation_time:** Threat plate activation time in seconds from mission start
- **threat_activation_player:** Player id of the player who activated the threat plate
- **wait_time:** Difference in seconds from threat_activation_time until the threat rubble is removed
- **threshold:** Single entry giving the threshold for wait time for the AC to flag that a participant appears to be stuck. The threshold is set to 10 seconds, which corresponds to five seconds less than the median wait time in the pilot data.
- **time_in_seconds:** The mission time relative to mission start

### Bus message format
```
{
"header": {"timestamp": "2022-03-14T02:39:21.862254Z", "message_type": "agent", "version": "0.1"},
"msg": {"sub_type": "AC:threat_room_coordination", "version": 0.1, "source": "AC_Rutgers_TA2_Utility", "timestamp": "2022-03-14T02:39:21.862254Z", "experiment_id": "934c548a-54ef-4e1e-bdbb-613bd395764b", "trial_id": "add1aeef-a1c0-4621-b7d6-51efe129c99c"},
"data": {
    "room_id": ["H1A", "J4", "H1A", "J4", "K2", "M3", "D3"],
    "threat_activation_time": [80.745, 87.143, 120.742, 173.342, 310.041, 408.342, 539.691],
    "threat_activation_player": ["RED_ASIST2", "BLUE_ASIST2", "RED_ASIST2", "RED_ASIST2", "RED_ASIST2", "RED_ASIST2", "RED_ASIST2"],
    "wait_time": [Infinity, 20.947000000000003, 14.897999999999982, 1.899000000000001, 29.25, 2.4530000000000314, Infinity],
    "threshold:": 10,
    "time_in_seconds": 552.521}
}
```

### Frequency of measurement
Updating of (and posting of) the dictionary will be event based. The dictionary will be updated whenever:

1. A player who is not the engineer activates a threat plate. 
2. The engineer removes the associated threat rubble
3. The threshold is reached without the rubble having been removed (Infinity is shown as the wait time for that entry). This entry will be overwritten once the threat rubble has been removed. 

### AC usage
Higher wait_time means worse performance, because it implies longer times that at least one player is not productively contributing to the team. 
All entries in wait_time can be summed for a mission-level performance metric, or grouped into player-specific sums to assess specific breakdowns of team-work, or be kept at the event-level (e.g. for further analysis of outliers). The median total 

wait_time equalling Infinity means wait_time passed threshold and rubble is still present, which can serve as a flag for intervention.

We propose two potential applications of this AC (that also rely on the threat room communication AC to generate more actionable recommendations).
1. Within missions, when wait_time exceeds threshold, an ASI can check the room_id record of this AC to check if a player has been stuck in this threat room before and use the threat room communication AC to check whether there was a threat room markerblock outside of this threat room. Collectively this information can be used to a) encourage the engineer to free the stuck team member, encourage the stuck team member to use the "emergency" marker blocks to make themselves easier to find, and to encourage the team to use threat room marker blocks to avoid unnecessary entries into threat rooms.
2. Between missions, the total time spent in threat rooms during the first mission can be compared to the median time spent in threat rooms during the pilot, to either encourage the continuation of a successful strategy (if the team wait_time is lower than the pilot median), or encourage changes to marker block usage and/or engineer prioritization otherwise.

### Quantitative measures of process
- Targeted process: coordination
- Characterization: total wait time (sum of wait_time of instances < outlier_threshold [200 seconds] )
- Recommendation: lower is better (pilot mean = 133, pilot SD = 108)
- Message: key = ruac_m1, value = [float]



## Threat room communication AC

### Overview
Measures whether a threat room marker block is placed outside of a threat room. Captures how effectively players use marker blocks to communicate about threat rooms.

### Inputs
marker placement event, room door coordinates, rubble collapse event (for detecting known threat room)

### Measurements
The output will be a dictionary of lists.
- **player_placed:** The ID of the player who placed the marker block
- **time_placed:** The time the marker block is placed in seconds, relative to mission start
- **nearest_room:** The id of the room closest to the threat room marker block
- **is_observed_threat_room:** Whether this room is a known threat room
- **time_in_seconds:** The mission time relative to mission start

## Bus message format
```
{
"header": {"timestamp": "2022-03-14T02:40:26.567636Z", "message_type": "agent", "version": "0.1"}, 
"msg": {"sub_type": "AC:threat_room_communication", "version": 
0.1, "source": "AC_Rutgers_TA2_Utility", "timestamp": "2022-03-14T02:40:26.567636Z", "experiment_id": "934c548a-54ef-4e1e-bdbb-613bd395764b", "trial_id": "add1aeef-a1c0-4621-b7d6-51efe129c99c"}, 
"data": {
    "player_placed": ["BLUE_ASIST2", "RED_ASIST2", "RED_ASIST2", "BLUE_ASIST2", "BLUE_ASIST2", "BLUE_ASIST2"], 
    "time_placed": [110.591, 236.991, 327.89, 342.545, 343.341, 713.341], 
    "nearest_room": ["J4", "K2", "K2", "K2", "K2", "A4"], 
    "is_observed_threat_room": [true, false, true, true, true, false],
    "time_in_seconds:"609.317}
}
```

### Frequency of measurement
Updating of (and posting of) the dictionary will be event based. The dictionary will be updated whenever a player places a threat room marker block.

### AC usage
During a mission, is_known_threat_room indicates if the threat room marker block is placed near a threat room, and can thus indicate mistakes. In unison with threat room coordination, it can help diagnose reasons why players get stuck in threat room, and identify how they might communicate better, see the text on AC usage for threat room coordination.

### Quantitative measures of process
- Targeted process: communication
- Characterization: number of unique nearest_room_id on known_threat_room divided by total number of threat rooms
- Recommendation: higher is better (max = 1)
- Message: key = ruac_m2, value = [float]



## Victim type communication AC 

### Overview
Measures whether victim type marker blocks are placed near victims of the appropriate types. This is intended to capture whether the team use the marker blocks to effectively communicate about victim types.

### Inputs
marker placement event, all victim-action related events (triage, pick up, drop off)

### Measurements
The output will be a dictionary of lists.
- **player_placed:** The ID of the player who placed the marker block.
- **time_placed:** The time the marker block is placed in seconds, relative to mission start.
- **marker_block_type:** what type of victim marker block is placed.
- **victim_type_in_vicinity:** what types of victims are within the vicinity_threshold_in_blocks of the marker block (can contain multiple entries.
- **victims_match_marker_block:** victim_ids in the vicinity that matches the type of the marker block.
- **vicinity_threshold_in_blocks:** integer that indicated what counts as "vicinity" for the purpose of this AC.
- **time_in_seconds:** The mission time relative to mission start

### Bus message format
```
{
"header": {"timestamp": "2022-03-14T02:40:28.088641Z", "message_type": "agent", "version": "0.1"}, 
"msg": {"sub_type": "AC:victim_type_communication", "version": 
0.1, "source": "AC_Rutgers_TA2_Utility", "timestamp": "2022-03-14T02:40:28.088641Z", "experiment_id": "934c548a-54ef-4e1e-bdbb-613bd395764b", "trial_id": "add1aeef-a1c0-4621-b7d6-51efe129c99c"}, 
"data": {
    "player_placed": ["RED_ASIST2", "RED_ASIST2", "BLUE_ASIST2", "GREEN_ASIST2", "RED_ASIST2", "RED_ASIST2", "GREEN_ASIST2", "RED_ASIST2", "GREEN_ASIST2", "RED_ASIST2", "RED_ASIST2", "RED_ASIST2", "RED_ASIST2"], 
    "time_placed": [107.141, 182.34, 199.992, 210.591, 342.542, 368.59, 406.491, 422.141, 533.991, 546.84, 598.891, 711.64, 716.341], 
    "marker_block_type": ["A", "B", "A", "B", "B", "A", "B", "B", "B", "B", "B", "B", "A"], 
    "victim_type_in_vicinity": ["A,C", "B", "B", "", "B", "A,B", "", "B", "B", "B", "B", "A,B", "A,B"], 
    "victims_match_marker_block": ["24", "15", "", "", "28", "29", "", "6", "28", "21", "28", "14", "12"],
    "vicinity_threshold_in_blocks": 2, 
    "time_in_seconds": 716.341}
}
```

### Frequency of measurement
Updating of (and posting of) the dictionary will be event based. The dictionary will be updated whenever a player places a victim type marker block (for A, B, or C).

### AC usage
During a mission, The proportion of np.nans in marker_matched_victim_id_in_vicinity indicates the precision of victim marker block placements, and the number of entries indicate how frequently victim marker blocks are used.

This AC can also be used to diagnose misplaced victims as indicated by the `victim_evacuated_event_message` on the message bus in two ways.
1. When a victim is placed in the wrong evacuation zone, we check for that marker_matched_victim_id_in_vicinity in the Victim type communication AC. If the victim_id is present in marker_matched_victim_id_in_vicinity, it implies that the victim had been placed next to an appropriate marker block at some point, so the ASI should encourage the player dropping the victim to pay more attention.
2. If the victim_id is not included in marker_matched_victim_id_in_vicinity, it implies that the victim was never near a marker block of the appropriate type, so the ASI can encourage the group to consistently use the marker blocks to communicate victim types.

### Quantitative measures of process
- Targeted process: communication
- Characterization: number of mistaken marker blocks [sum( (marker_block_type not in victim_type_in_vicinity) and (victim_type_in_vicinity non-empty)] 
- Recommendation: lower is better (Rare events, 4 events in total during pilot, max 1 per mission)
- Message: key = ruac_m3, value = [int]



## Belief difference AC

### Overview
Computes the beliefs about victim distribution under three different assumptions: (1) players share information perfectly, (2) players don't share any information, and (3) players only share information via marker blocks.

### Inputs
marker placement event, transported signal event, movement data

### Measurements
- **room_id:** all room ids in sequence, ending with an "overall" entry, for the summed value across all rooms
- **shared:** entropy on victim type and number for each room, and summed across rooms (for the full map overview)
- **RED_indiv:** entropy on victim type and number based on direct information for the medic
- **BLUE_indiv:** entropy on victim type and number based on direct information for the engineer
- **GREEN_indiv:** entropy on victim type and number based on direct information for the transporter
- **RED_marker:** entropy on victim type and number based on direct information for the medic and marker block information
- **BLUE_marker:** entropy on victim type and number based on direct information for the engineer and marker block information
- **GREEN_marker:** entropy on victim type and number based on direct information for the transporter and marker block information
- **time_in_seconds:** The mission time relative to mission start

### Bus message format
```
{
"header": {"timestamp": "2022-03-14T02:39:45.853896Z", "message_type": "agent", "version": "0.1"}, 
"msg": {"sub_type": "AC:belief_diff", "version": 0.1, "source": "AC_Rutgers_TA2_Utility", "timestamp": "2022-03-14T02:39:45.853896Z", "experiment_id": "934c548a-54ef-4e1e-bdbb-613bd395764b", "trial_id": "add1aeef-a1c0-4621-b7d6-51efe129c99c"}, 
"data": {
    "room_id": ["A1", "A2", "A3", "A4", "A4A", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "D1", "D2", "D3", "D4", "E1", "E2", "E3", "E4", "E5", "F1", "F2", "F3", "F4", "G1", "G2", "G3", "H1", "H1A", "H2", "I1", "I2", "I3", "I4", "I1A", "I2A", "I3A", "I4A", "J1", "J2", "J3", "J4", "K1", "K2", "K3", "K4", "L1", "L2", "L3", "M1", "M2", "M3", "overall"],
    "shared": [1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 0.0, 0.0, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 0.0, 1.116, 0.0, 0.0, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.116, 1.116, 1.116, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 36.839], 
    "RED_indiv": [0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.0, 0.0, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.0, 0.998, 0.0, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.998, 0.998, 0.0, 0.998, 0.998, 0.998, 0.0, 0.998, 0.998, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.998, 0.0, 38.936], 
    "BLUE_indiv": [1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 0.0, 0.0, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 0.0, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 1.049, 0.0, 0.0, 0.0, 0.0, 0.0, 1.049, 1.049, 0.0, 1.049, 0.0, 1.049, 1.049, 1.049, 0.0, 1.049, 0.0, 1.049, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.049, 1.049, 0.0, 0.0, 0.0, 44.078], 
    "GREEN_indiv": [1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 0.0, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 0.0, 0.0, 0.0, 0.0, 1.249, 1.249, 0.0, 0.0, 0.0, 0.0, 1.249, 1.249, 1.249, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 48.717], 
    "RED_marker": [1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 0.0, 0.0, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 0.0, 1.116, 0.0, 0.0, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 1.116, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.116, 1.116, 1.116, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 36.839], 
    "BLUE_marker": [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 0.0, 0.0, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 0.0, 0.0, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 0.0, 0.0, 0.0, 0.0, 0.0, 1.18, 0.0, 0.0, 0.0, 0.0, 1.18, 1.18, 1.18, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 41.328], 
    "GREEN_marker": [1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 0.653, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 0.0, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 1.249, 0.0, 0.0, 0.0, 0.0, 0.653, 1.249, 0.0, 0.0, 0.0, 0.0, 1.249, 1.249, 1.249, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 47.525], 
    "time_in_seconds": 609.317}
}
```

### Frequency of measurement
The entropy recordings will be updated every 30 seconds.

### AC usage
We propose three usages for the Belief difference AC.
1. During a mission, the difference between the marker block entropy of different players when one player has information about the distribution of victims that they are not sharing via the marker blocks. Practically this involves comparing the marker knowledge map overall entropy for each player with the mean marker block entropy of the other two players. If this difference exceeds 9 (corresponding to the 90th percentile in the pilot data), the ASI can encourage the player with additional information to use the marker blocks more.
2. Between missions, the difference between individual level entropy and full_knowledge entropy can be used to measure how clumped together players were during the mission. If the greatest difference between individual entropy and full knowledge entropy is less than 15 this implies that all three players were lumped together throughout the mission. The ASI can then inform players of what proportion of time they were lumped together and compare that to the proportions of successful teams during the pilot, to help players reflect on their strategy for the second mission.
3. Between missions, the mean proportion between the difference between the individual knowledge map and the marker block knowledge map and the individual knowledge map and the shared knowledge map, captures how effectively the whole team offloaded information via the marker blocks. The ASI can share this information with the team, and how this value compares with the team distribution during the pilot to help them reflect on how they can use the marker blocks to communicate more effectively.

### Quantitative measures of process
- Targeted process: team exploration
- Characterization: In each 30-second time point we take the maximum unsigned difference among individual models' overall entropy, identifying the team mates that have most distinct knowledge at that point in time. We then take the maximum over all time steps within a mission. Teams with a low maximum on this metric has consistently moved together, and thus explored the space inefficiently.
- Recommendation: larger is better (pilot MEAN = 21.02, pilot SD = 9.48)
- Message: key = ruac_m4, value = [float]

- targeted process: communication efficiency of marker blocks
- characterization: We take the maximum ratio between players for each 30-second time point: max[(marker model_{p} - individual model_{p}) / (shared model_{p} - individual model_{p})] where p stands for a unique player. We then take the mean across time points per mission. The ratio here captures what proportion of the information about the victim distribution that could be shared by marker blocks is actually shared, so higher values are better.
- Recommendation: larger is better (max = 1; pilot MEAN = 0.47, pilot SD = 0.19)
- Message: key = ruac_m5, value = [float]

## Standard readme info
Our AC is built on `/ReferenceAgents/IHMCPythonAgentStarter.` Configuring, building, running, and stopping the AC will follow similar procedures. We will update this shortly.

## Configuration
- The configuration files is available at `testbed/Agents/RutgersUtilityAgent/ConfigFolder`
- The file at `testbed/Agents/RutgersUtilityAgent/ConfigFolder/config.json` contains the settings for the MQTT mesaage bus host and the agent's version_info.

## Local Development (Without Docker)
  * **Requirements**
     - Python 3.8 or higher
     - Git
  1. Install the Libraries using `pip install -r requirements`
  2. Configure the MQTT bus host at `testbed/Agents/RutgersUtilityAgent/ConfigFolder/config.json`.
  3. Agent can be started started by running scripts below:
    - Windows: `run_locally.cmd`
    - Mac/Linux: `run_locally.sh`

## Local Development (With Docker)
  1. **Build Container**
     - Container can be built by running the scripts located at `testbed/Agents/RutgersUtilityAgent`
     - Container needs to be re-built every time if changes are made to the Agent.
      - Windows: `agent.cmd build`
      - Linux: `./agent.sh build`

  2. **Start Container**
     - Container can be started by running the scripts located at `testbed/Agents/RutgersUtilityAgent`
      - Windows: `agent.cmd up` or `agent.cmd upd` for running container in background
      - Linux:  `./agent.sh up` or `./agent.sh upd` for running container in background

  3. **Stop Container**
     - Container can be stopped by running the scripts located at `testbed/Agents/RutgersUtilityAgent`
      - Windows: `./agent.sh down`
      - Linux: `./agent.sh down`
