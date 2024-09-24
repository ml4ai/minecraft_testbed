# Release Notes for the ASIST Testbed

## V3.5.1 Study-3 Spiral 5 Rev 1
**Testbed**

**ASI Agents**

*ASI_CMU_TA1_ATLAS*
- Renamed agent to ASI_CMU_TA1_ATLAS to conform to naming convention
- Extended TToM model to include second-order beliefs
- Extended TToM model to include intent predictions
- Minor changes to logic of some interventions

*ASI_DOLL_TA1_RITA*
- Integration with ACs
- Updated external volume settings to accomodate restarts in between trials.
- Produce interventions, anomaly messages and prediction actions.
- The changes fix some critical bugs whereby key variables were not being reset at the end of a trial, which would lead to some interventions not being selected in trial 2.
- Updates to handle non Saturn maps (Ex: Training) and improve intervention generation for trial-2.
- Improved perturbation intervention to be more player specific.
- Simple fixes of spelling errors and calculation of evacuated and triaged victims.
- Fix suboptimally evacuated victims
- Minor bug fixes and intervention text updates.

*ASI_UAZ_TA1_ToMCAT*
- Updating version to 3.5.0
- Adapting agent’s reasoning engine to use general ML models.
- Implementing introduction and motivation interventions.
- Limiting interventions to the second mission only.
- 4/11/2022
  - Updating version to 3.5.1
  - Switches intervention topic from agent/intervention/tomcat/chat to agent/intervention/ASI_UAZ_TA1_ToMCAT/chat
  - Updating version to 3.5.2
  - Implements Communication-Marker intervention. ToMCAT encourages participants to speak about the markers they placed.
- 4/18/2022
  - Updating version to 3.5.3
  - Reduces the number of markers that trigger communication intervention
  - Adds ask-for-help and help-on-the-way interventions
  - Updating version to 3.5.4
  - Implements all 3 communication interventions
- Updating heartbeat container to 1.1.0 to reduce cpu usage
- Updating version to 3.5.5
- Removes the config/ directory from the list of ignored folders in the .dokerignore file
- Updating version to 3.5.6
- Restricts the agent introduction to the first mission only
- Disables motivation intervention
- Writes file logs to the terminal as well to be captured by Dozzle
- Fixes log directory mount in docker-compose file
- Updating version to 3.5.7
- Fixes the following bugs:
- Do not intervene on marker if the marker was removed by another player
- Do not intervene on room-escape if players see door obstructions from another room
- 5/12/2022
  - Updating version to 3.5.8
  - Pins Ubuntu version to Focal
  - Resolves crash on TA3 Alma Linux VM

*atomic_agent*
- Upgrading to version 0.0.2
- Updating documentation
- Adding knowledge structure for tracking information acquired by players during mission
- Adding planning period chat messages
- Expanding subscriptions to keep knowledge structure updated

**Analytic Components (ACs)**

*AC_UAZ_TA1_ToMCAT-ASRAgent*
- Updating heartbeat container to 1.1.0 to reduce cpu usage
- 5/10/2022
  - Updates ASR_Agent to 4.0.3
  - NOTE: Version 4.0.2 updates have been reverted due to an unknown error when running on TA3 systems. 4.0.3 is based on version 4.0.1, so does not include these updates.
  - Adds logging to file support

*AC_UAZ_TA1_ToMCAT-SpeechAnalyzer*
- 5/26/2022
  - Updates speechAnalyzer to 4.1.0
  - Optimizes CPU usage for speechAnalyzer container
  - Updates mmc to 1.1.0
- 5/17/2022
  - Updates speechAnalyzer to 4.1.3
  - Further improves logging messages
  - Updates speechAnalyzer to 4.1.4
  - Switches to publishing using QOS 0 due to unknown bug
- 5/10/2022
  - Updates speechAnalyzer to 4.1.2
  - NOTE: Version 4.1.1 updates have been reverted due to an unknown error when running on TA3 systems. 4.1.2 is based on version 4.1.0, so does not include these updates.
  - Adds logging to file support
- 5/2/2022
  - Updates speechAnalyzer to 4.1.1
  - Publishes raw binary audio chunks to internal message bus instead of base64
  - Further reduces CPU usage
- 4/19/2022
  - Updating heartbeat container to 1.1.0 to reduce cpu usage
- 3/28/2022
  - Updates speechAnalyzer to version 4.0.0
  - Splits speechAnalyzer into two ACs: AC_UAZ_TA1_ASR_AGENT and AC_UAZ_TA1_SpeechAnalyzer
  - Adds additional Mosquitto container for internal speechAnalyzer use
  - Removes data.sentiment field from agent/asr/final message
  - Adds agent/speech_analyzer/sentiment agent/speech_analyzer/personality message type


*Rutgers_TA2*
- 3/14/2022 - Added three AC messages
  - `agent/ac/threat_room_communication`
  - `agent/ac/victim_type_communication`
  - `agent/ac/belief_diff`
- 3/14/2022 - Added Message specs for the new AC messages

*Cornell TA2*
- 4/15/2022 - Fixed minor issues that came up after 1st set of replay (v 1.0.3)
- 4/11/2022 - Improved Goal alignment message error handling; improved player compliance in case of missing FoV messages (v 1.0.0)
- 3/22/2022 - Team trust AC bug fixes.
- 3/14/2022 - Added Goal alignment measures message from Team Trust AC; README files updated.
- 3/11/2022 - Added New Facework AC (V0.0.3)
- 3/11/2022 - Updated Player compliance message of Team Trust AC (V0.0.5)

*CMU TA2 TED*
- 3/10/2022 - v0.0.3. Updated `total_triage_time_s` to be 105 and all calculations concerning communications (i.e. message_freq, message_equity, message_consistency_agg) are updated to comms_total_words and comms_equity.

*CMU TA2 BEARD*
- 3/18/2022 - v0.0.7. Add stronger error handling to survey data and competency data. Future-proof survey variables
- 3/15/2022 - v0.0.6. Agent state resets after every experiment/team
- 3/14/2022 - v0.0.5. Fix pylint issues.
- 3/10/2022 - v0.0.4. Added calculation of competency skill variables to the BEARD agent, renamed directory to adhere to agent naming convention in agent dev guide, and ensured survey variables only use Sections 0 and 1 of survey.


*Rutgers TA2*
- 3/2/2022 - Add threat room coord AC
- 3/2/2022 - Remove unused message specification, remove messages without specification(Fixes #197 issue) and add message specification for threat room coordination ac.

*IHMC TA2*
- 4/05/2022
  - Fixes joint activity interdependence topic usage
  - Fixes missing critical component in joint activity summary
  - Reverts some joint activity summary values to be in milliseconds
  - Updates message spec documentation to be more consistent
  - Updates log retrieval process
- 3/14/2022
  - Updated The Proximity agent so that it preloads a distance matrix for the default (Saturn_2.6_3D) map and uses it when needed instead of loading it again.
- 3/10/2022
  - Adds joint activity interdependence ac
  - Added CMUFMS Cognitive Load ac
  - Updates to AgentHelper to support setting subscription and publication quality of service (qos) values from the configuration file and from the subscribe and send methods.
- 3/1/2022  - Updated the Readme.md files for Location Monitor, Proximity, and Dyad AC Agents to include the topics used (pub & sub) by each.

*AC_UAZ_TA1_ToMCAT-DialogAgent*
- 5/2/2022 (v4.1.5)
  - Now responds to rollcall request messsages
  - Some small fixes for insights from the eval. Addressing certain rules overmatching.
  - Broadened coverage of the "WhichVictimType" question and "Type" label.
  - Expanded "KnowledgeShare" to also pick up utterances such as: "I have some rubble here."
  - Fixed an issue with the critical victim label, also fixed issues with RoleDeclare and LocationQuestion.
  - Release notes here:  https://github.com/clulab/tomcat-text/releases/tag/v4.1.5
- 4/15/2022 (v4.1.1)
    * Add "could you take care of.." pattern to Instruction by @Yuweien in https://github.com/clulab/tomcat-text/pull/282
    * Modelling team requests by @remo-help in https://github.com/clulab/tomcat-text/pull/283
    * **Full Changelog**: https://github.com/clulab/tomcat-text/compare/v4.1.0...v4.1.1
- 4/11/2022 (v4.1.0)
    - Updated output format for attachments
        * Renamed Negation.value field to Negation.negation by @jastier in
          https://github.com/clulab/tomcat-text/pull/277
        * Added "type" field  to the Negation JSON output by @jastier in
          https://github.com/clulab/tomcat-text/pull/280
    - Taxonomy and rule updates
        * The "Save" label is now a subset of "TriageInteractions" by
          @remo-help in https://github.com/clulab/tomcat-text/pull/266
        * Added SOSMarker and threatrooms by @remo-help in
          https://github.com/clulab/tomcat-text/pull/275
        * Victim type coverage by @remo-help in
          https://github.com/clulab/tomcat-text/pull/279
    - Decoupling TDAC and IDC from DialogAgent
        * We ran into issues running the TAMU dialogue act classifier (TDAC)
          via HTTP requests driven by the UAZ DialogAgent on the ASU VM, so we
          are decoupling the TDAC from the DialogAgent
          (https://github.com/clulab/tomcat-text/pull/267)
        * Similarly, we are decoupling the interdependence detection component
          (IDC) (https://github.com/clulab/tomcat-text/pull/268)
    - Miscellaneous/bug fixes
        * Updated the Dockerfile to use a specific tag of the `mozilla/sbt`
          image as the base rather than `latest`, since they updated their
          image to use an incompatible version of Java
          (https://github.com/clulab/tomcat-text/pull/269)
        * Fixed bug in webapp caused by TDAC decoupling
          (https://github.com/clulab/tomcat-text/pull/272)
        * Updating version number to 4.1.0 by @adarshp in
          https://github.com/clulab/tomcat-text/pull/281
    - **Full Changelog**: https://github.com/clulab/tomcat-text/compare/v4.0.6...v4.1.0
- 3/25/2022 (v4.0.6)
  - Meeting and damage labels, fixed minor issues. by @remo-help in https://github.com/clulab/tomcat-text/pull/259
  - Eval fixes spiral4 by @remo-help in https://github.com/clulab/tomcat-text/pull/261
  - Updated the documentation and scripts to generate tree-structure extraction by @chencc33 in https://github.com/clulab/tomcat-text/pull/263
  - Meeting fix, marker block updated by @remo-help in https://github.com/clulab/tomcat-text/pull/264
- 3/7/2022 (v4.0.3)
  - Integrated room names from ASIST Study 3
  - Added a ThreatRoom label
  - Added Labels for the new Marker Blocks, threat signs, and unspecified threats.
  - Knowledge sharing on threat rooms works as expected, for example: ""There is a threat in room C3."
  - Added labels for victim types A&B (subset of the regular victims label)
  - Type C is extracted under the CriticalVictim label
  - added a label for victim types (unspecified): Type
  - added a label for players asking after victim types: WhichVictimType
  - Made file names for room-related rules consistent.
  - Default "Room" label now only publishes if it used as an argument in another rule
  - Added the python script used to generate the rules to the /scripts/ folder
  - Amended rules to allow for threat markers and threat signs, with the difference explained.
  - Added rules to capture and report threat rooms.
  - Added label for players stating that they are on their way: OnMyWay
  - Full Changelog: https://github.com/clulab/tomcat-text/compare/v4.0.0...v4.0.3

*AC_UAZ_TA1_ToMCAT-SpeechAnalyzer*
- 3/17/2022
  - Updates uaz_speech_analyzer to version 3.5.1
  - Disables Opensmile components for stability
- 3/9/2022
  - Updates uaz_speech_analyzer to version 3.5.0
  - Resolved a number of edge case bugs that could cause the speechAnalyzer to crash on startup or shutdown
  - Implemented improved ASR 'video' model as well as speech adaption for
    domain words to improve transcription quality
  - Updated get_all_logs.sh to represent updated name of speechAnalyzer
  - speechAnalyzer version now set from .env file in Agents/AC_UAZ_TA1_ToMCAT-SpeechAnalyzer directory
- 3/1/2022
    - re-enabled Google ASR backend
    - Updates uaz_speech_analyzer to version 3.4.1
    - Changes name of uaz_speech_analyzer to AC_UAZ_TA1_ToMCAT-SpeechAnalyzer
    - Created seperate docker-compose files for Vosk and Google ASR backend
    - Vosk container no longer brought up when Google speech backend used

*GOLD*
- 3/15/22 - Updates to ReadMe documentation, docker container up/down scripts
- 3/10/22 Introducing Gallup Agent GOLD (v1.1)
  - The Gallup Object Library Distributor (GOLD) Agent is intended to publish a variety of small factor, component data messages to the message bus for reference and use by other agents.
  - Please refer to gallup_gold_message.md for more information on this agent, its behavior, and output message schema.
  - Note: output is differentiated by msg.sub_type
    - "standard": feature inventory, published immediately upon trial start
    - "bullion": feature data, published each minute for each participant according to available input data

*GOLD*
- 3/15/22 - Updates to ReadMe documentation, docker container up/down scripts
- 3/10/22 Introducing Gallup Agent GOLD (v1.1)
  - The Gallup Object Library Distributor (GOLD) Agent is intended to publish a variety of small factor, component data messages to the message bus for reference and use by other agents.
  - Please refer to gallup_gold_message.md for more information on this agent, its behavior, and output message schema.
  - Note: output is differentiated by msg.sub_type
    - "standard": feature inventory, published immediately upon trial start
    - "bullion": feature data, published each minute for each participant according to available input data

*GELP*
- 3/15/22 - Updates to ReadMe documentation, docker container up/down scripts
- 3/4/22 Upgrading Gallup GELP Agent to v0.5.2.
  - Trial Continuity Enhancements: introduced chmod permissions to dockerfile resource copy, python code artifact file write operations in hopes of being able to read artifact files on subsequent trials within same testbed container instance
  - Survey event handling: urlencode approach to re-escaping nested double-quotes in survey events mappings object (\" --> %22) to facilitate parsing, artifact file read/write
- Upgrading Gallup GELP Agent to v0.5.1.
  - re-introduction of missingness_factor expanded to per-participant scoring results, lending insight into the degree of imputation model employs to account for features not available at time of calculation
  - improvements to handling of trial continuity (same team, subsequent trial) and prediction calculation resiliency
    - enhancements allowing for scoring despite few and/or no available features
    - move from os.path.join approach to path construction for artifact file to fixed relative directory assignment (test to see if resolves artifact file detection in subsequent trials)
  - feature engineering changes:
    - filtering of participant lookup data to current trial only prior (facilitates continuity)
    - ensure null equivalence prior to calculation (None objects --> NaN)
  - bug handling and logging improvements
    - further compensation for "kitchen sink" survey event structure (direct, and indirect impact fixes for spillover effect on continuity and coincident event messages)
      - ex: accommodating nested, non-escaped quotes within survey HTML element attributes undoes quote handling for stringified objects within agent/asr/final messaging
    - placeholders for in-progress output
- Upgrading Gallup GELP Agent to v0.5.0.
  - improvements to event handling to compensate for changes in survey, agent/dialog, agent/asr/final event objects... in general tesbed messaging study3, spiral3+
  - improvements to handling of trial continuity (same team, subsequent trial) and resiliency
  - feature engineering changes to accommodate event handling, retain modeling compatibility
  - minor bug handling and logging improvements

*UCF TA2*
 - Upgrading to version 0.0.3
 - Adopted agent naming convention.
 - Upgrading to version 0.0.4
   - Publishes player profile based on the player's behavior in the game.
 - Upgrading to version 0.0.5
   - Updated player parameters
 - Upgrading to version 0.0.6
   - For first trial, publishes static player profile from survey data
   - For second trial, publish dynamic player profile when survey message is received.
   - Starts learning from player's behavior at T=2 minutes or when planning stop message is received.
   - Creates and uses the default player profile when survey messages are not available.
 - Upgrading to version 0.0.7
   - Fixed parameters and use competency scores when available.
   - AC subscribes to victim_evacuated on both player and server topics.
   - Has an option to use Header timestamps when publishing messages to the bus.
 - Upgrading to version 0.0.8
   - AC is now resilient to messages coming outside of trial start and stop messages.
   - print complete internal state to stdout for regression analysis.

*Aptima TA3 measures*
- use 17 min mission timer
- updated to version 3.5
- renamed measure directory, images, and containers
- updated measures references in testbed scripts
- added measures readme.md


## V3.4.1 Study-3 Spiral 4 Rev 1
**Testbed**

**ASI Agents**

**AC Agents**

*IHMC TA2*
- 2/14/2022 - Renamed the Location Monitor, Proximity, and Dyad AC agents to be inline with the Agent Naming Conventions in the ASIST Agent Development Guide.
- 2/14/2022 - Fixed an issue with the Proximity monitor's current version of the basemap which did not remove the Mission Start wall and so paths to the starting area were not valid once players left.

*CMU TA2 BEARD*
- Add information about BEARD agent to README in `Agents/CMUTA2BEARDAC/README.md`. Information specifically contains measures that the agent computes and their descriptions.

*CMU TA2 TED*
- Add information about TED agent to README in `Agents/CMUTA2TEDAC/README.md`. Information specifically contains measures that the agent computes and their descriptions.

*uaz_speech_analyzer*
- Updates uaz_speech_analyzer to version 3.4.0
- Removes a number of unused/redunded fields from ASR messages
- Adds additional fields to features database
- Intermediate transcriptions re-enabled and additional fields added
- New command line option to disable all but initial intermediate transcription messages

*Aptima TA3 measures*
- updated to version 3.4
- added measure ASI-M14 - Risk
- round m14 properly and only count players not trapped in rubble

*UCF TA2 player-profile*
- Initial release

**Tools**

- added measure rollup csv tool to output all measures from a metadata file


### Message Updates
See message log in the MessageSpecs directory



## V3.3.4 Study-3 Spiral 3 Rev 3 -

**Testbed**
- All surveys for participants in the trial are published on the message bus and included in the .metadata file
- A QR code appears on the client map when the mission starts
- The engineers client map shows the location of the threat rooms

**ASI Agents**

*TMM Agent*
- Version 3.3.0: Adds the following intervention types:
1. Time alerts halfway through the mission and two minutes before the end
2. Suggestion to explore a different section of the map
- Version 3.3.1: Resolves crashing on mission start and updates grammer in intervention messages
- Version 3.3.2: Updates mission time from 10 minutes to 15 minutes to remove message inconsistency

*Rita Agent*
 Version `2.0.2022-1-14-spiral-3` adopts agent naming convention and is henceforth named as `ASI_DOLL_TA1_RITA`

**AC Agents**

*FoV*
- Added Profile Message
- Speed up on message parsing
- Updated marker block names to Spiral 2 versions
- Updated world model to match dynamics of Spiral 2 experiment
- Incorporated RubbleCollapse effects

*Dialog Agent*
- Version 4.0.0 of the uaz_dialog_agent does not send null JSON values on the message bus.
- This is a major-digit release because output formats will change if fields are null.
- The file agent can now use the IDC and TDAC features the same way the MQTT agent does now.
- Message objects can now build themselves leaving the DialogAgent base class to handle the Rule Engine.
- [Full release notes are here](https://github.com/clulab/tomcat-text/releases/tag/v4.0.0)
- For Linux-gnu OSs, hostname for Dialouge Act Classifier now configurable. For MacOS/Windows it is set automatically.

*speechAnalyzer*
- uaz_speech_analyzer 3.3.1: Bug fixes and error handling
- Fixes bug when Vosk leaves out start or end timestamp in response message
- Adds additional error handling for Vosk message processing
- Removes sending word-aligned features on message bus
- Prevents multiple concurrent connections with the same participant_id
- uaz_speech_analyzer 3.3.2: Re-enables intermediate transcriptions
- Re-enables agents/asr/intermediate messages
- Adds data.is_initial and data.start_timestamp fields to intermediate messages

*IHMC DyadAC, ProximityAC and Location Monitor*
- Added and using a semantic map for Saturn 2.6 3D with the latest room labels.

*GELP*
- Upgrading Gallup GELP Agent to v0.4.2.
  - improve differentiation between trial and mission Start/Stop, handling of observations/events/mission events
  - resolve error in calc call related to calc_minute not being provided as parameter
  - polish data pipelines to improve handling of python vs json object formatting (ex: True/False), formatting of data handed to imputer (ensure NaN as opposed to string nulls)
  - improve logging around participant matching related to continuity artifact object
- Upgrading Gallup GELP Agent to v0.4.
- Added:
  - /resource/minute_model_goodies.pickle  (new version of model resource file)
  - Additional library package requirements added at container spinup (spacy)
    - Modified spacy models extension (spacy-model-en_core_web_sm) from general pip install with version to source direct from package repository (in hopes of preventing future gitlab pipeline build failures)
- Updated:
  - gallup_agent_gelp.py: Same team subsequent trial continuity, Improved prediction model + scoring for Emergent Leadership, Corrected message publication, Improved time stamp handling during and before trial start, ...)
  - Updated code and requirements to operate on Python 3.8 to be more consistent with overall Testbed environment, resolving former scikit-learn dependency on Python 3.6
  - settings.env: to reflect preferred naming convention for agent --> ac_gallup_ta2_gelp

*Measures*
- add additional logging statements
- fix typos
- handle error when no perturbation occurs
- reset certain values at trial/mission end
- Updated measures to calculate ASI-M1 through ASI-M4
- Update measures messagespec

*CRA PSI-Coach*
- Added marker intervention
- Upgraded agent version to 3.4.0
  - Performance and stability improvements
- Upgraded agent version to 3.5.0
  - Renamed agent to ASI_CRA_TA1_psicoach
  - Removed VictimAppearsEvent from agent output
- Upgraded agent version to 3.5.1
  - Fixed bug where interventions were being published to wrong topic
  - Updated agent name where it had not been updated already
- Upgraded agent version to 3.5.2
  - Publishing metrics at the end of each mission
  - Improvements to generated interventions and inferences
  - Performance improvements
- Upgraded agent version to 3.5.3
  - Improvements to Cognitive Inverter and generated inferences
  - Improved intervention messaging to encourage proper player grouping
- Upgraded agent version to 3.5.4
  - Added new encouragement interventions
  - Modified intervention wording to maximize effect on player
  - Added new actions interventions
- Upgraded agent version to 3.5.5
  - Performance and concurrency improvements
- Upgraded agent version to 3.5.6
  - Additional concurrency improvements and bugfixes
- Upgraded agent version to 3.5.6.1
  - Fix to intervention text character encoding

*Rutgers Utility Agent*
- Updates the agent name as recommended in the guidelines
- Updates the publish message to publish critical and non critical victim info for each room

*Cornell Team Trust AC*
- Updated Compliance measures to produce player-wise metrics
- Updated agent name as recommended in the guidelines; agent name is now `AC_CORNELL_TA2_TEAMTRUST`

### Message Updates
See message log in the MessageSpecs directory

## V3.3.2 Study-3 Spiral 3 Rev 2 - Jan 2022
### New Features

**Testbed**

***Features***

1. Timed rubble collapse is implemented and the time the collapse occurs is defined in the ModSettings.json file
2. The client map page displays a QR code when the mission starts.

***Fixes***

1. Event:VictimEvacuated now published on observations/events/server/victim_evacuated* to match schema
2. Event:Perturnation "state" key changed to "mission_state" to match schema

**ASI Agents**

**Agents**

*Gallup Agent GELP v0.2*
- Upgraded Agent GELP to now include live calculation and publication of results back to the message bus. Schema for message publication has been streamlined as well. Updated examples are incorporated into Message Specs for both the /MessageSpecs/GallupAgentGELP/gallup_gelp_message.json and .md (markdown readme) files. Note that our /Agents/gallup_agent_gelp/requirements.txt (docker container environment setup) now lists additional dependencies on Python version (3.6), scikit-learn (0.21), and Pandas (1.1) to facilitate Docker containerizationat at setup time. Specific mix of Python & scikit-learn is to suppress non-material deprecation warnings from populating in log files.

### Message updates
| Generating Agent Name | Topic | Message Type | Message Sub-type | Changes | Notes |
| --------------------- | ----- |------------- |----------------- | ------- | ----- |
| gelp | agent/gelp | event | agent:gallup_agent_gelp | new message | schema notes and examples here: /MessageSpecs/GallupAgentGELP/gallup_gelp_message.json and .md (markdown readme) files  |

*PsiCoach*
 - the victim appears message has been moved from the topic psicoach/victim_appears to agent/psicoach/victim_appears

**ACs**

### Enhancements

**Testbed**
1. Added list of block types that are used by the Minecraft in the file docs/ASIST_Custom_Block_Types.txt
2. Tansporter role signal device now reports no victim found when transporter moves over trigger point for a room with no victims
3. the SoS marker on the client map now blinks
4. The list of agents in the agent monitoring window is now sorted with the ones that have not been sending heartbeats at the top.
5. Medic proximity is required to unlock critical victim along with one other player
6. Timed rubble collapse is implemented and the time the collapse occurs is defined in the ModSettings.json file
7. the height of the survey response window displayed on the client map page when taking the survey is larger.
8. All players can transport victims, with some restrictions such as a critical victim cannot be transported until they are treated. the engineer and medic have reduced speed when transporting victims.


**ASI Agents**

**Agents**

**ACs**

### Bug Fixes

**Testbed**
1. Incorporated patches for the Log4J vulnerability in several components such as Minecraft and the metadata dashboard

**ASI Agents**

*DOLL RITA*: 2.0.2021-12-09-spiral-2: Updates to state estimator to handle missing roles (which resulted in some missing interventions).

**ACs**

### Message updates
A more complete list of message updates can be found in the MessageSpecs directory.
| Generating Agent Name | Topic | Message Type | Message Sub-type | Changes | Notes |
| --------------------- | ----- |------------- |----------------- | ------- | ----- |
| Testbed | ground_truth/mission/role_text | groundtruth | Mission:RoleText | new message | experiment new feature |
| Testbed | trial | trial | start or stop | added role_text field | new role text feature |
| Testbed | control/response/getTrialInfo | na | na | add active_agents | enahanced info about agent availability |
| Testbed | observation/events/player/signal | event | Event:Signal | msg.sub_type changed from Event:VistimsSignal to Event:Signal | more generalized message |
| Testbed | observations/events/player/proximity_victim changed to .../proximity_block | event | ProximityVictimInteraction changed to ProximityBlockInteraction| topic and documentation | inconsistency in documentation and the topic have been fixed so that all references now use block instead of victim |
| Testbed | status/asistdataingester/surveyresponse | status | Status:SurveyResponse | data.survey_response is now json format instead of string | json format is preferred for easier parsing |

## V3.2.1 Study-3 Spiral 2 Rev 1 - Nov 2021
### New Features
**Testbed**
1. Added agent and analytic component naming convention to agent development guide documentation
2. Added new optional field to rollcall and versioninfo message to indentify the type of agent as being either ASI, AC or other
3. Updated Saturn world file to remove the QR code blocking wall.  Added the Saturn 2.1 Dev world.
4. Players can now remove marker blocks by left clicking (breaking) them with another marker block.  A message with msg.sub_type:Event:MarkerRemoved is generated when this occurs and the block location is restored it its original state.

**Agents**

*SIFT Asistant Agent version 0.2.1*
- Add interventions to agent

*UAZ speech analyzer 3.1.0
- Integrates Vosk speech backend into speechAnalyzer (control with --disable_asr_vosk command line option)

**ACs**
1. IHMCLocationMonitor and IHMCProximityAC now have updated Semantic and Base maps for Saturn_2.1_3D

    The Treatment areas were moved and duplicated so the following changes were made to the semantic map:
    - 'Treatment Area C' <tac> is now split into 'Critical South' <tacs> and 'Critical North' <tacn>
    - 'Treatment Area A' <taa> is now split into 'Abrasion South' <taas> and 'Abrasion North' <taan>
    - 'Treatment Area B' <tab> is now split into 'Bone Damage South' <tabs> and 'Bone Damage North' <tabn>

# Enhancements
**Testbed**
1. upgraded the version field versioninfo message to handle a more general version identifier.
2. The client map image is updated to reflect the current configuration of evacuation locations with 2 location for each victim type
3. The set of marker blocks allocated to each player has been changed to include the following blocks:
   - Type A victim
   - Type B victim
   - No victim
   - Critical victim
   - Regular victim
   - Threat
   - Rubble
   - SOS


**Agents**

*uaz_tmm_agent 3.0.1*
- Adds support for versioninfo, heartbeat, and rollcall messages

**ACs**
1. new ac enhancement example

# Bug Fixes
**Testbed**
1. Correct the spelling of abrasion in the names of the marker blocks in the message documentation and schemas
2. Fixed marker block schemas. The spelling of the abrasion blocks was incorrect.

**Agents**

*SIFT Asistant Agent version 0.2.1*
- Minor bug fixes
- Add timestamp to `msg` field
- Update intervention message to match the specification from testbed 3.2.1

*uaz_tmm_agent 3.0.1*
- Fixes intervention message format
- Fixes bug where agent could crash on Mission start
- Fixes msg.version field to represent correct version number
- Fixes stringification of data.features field

**ACs**
1. ac bug fix example

## V2.1.0 Minor Release 2-JUL-2021
This minor release of the testbed includes several minor fixes and additional features to the testbed to support running experiments.
Changes included are:
* Added a setup mission for use during Session I
* ASIST mod update to 1.0.62
* Update to speech analyzer container to improve reliability
* Added session I competency test
* Update to competency test and training world files
* Testbed user walkthough document has been updated to include how to start the mission without an obsesrver.
See docs/ASIST_testbed_run_walkthough_V2.0.docx
* Updated some timeout durations so the testbed continues to function after sitting idle for period of time.
* Metadata dashboard enhancements to better support experiments and trials
* Improvements to firstlook_file.py for updated messages and additional checkes and statistics

## V2.0.0 Major Release, 2-JUN-2021
This is a major release of the testbed that supports multiple players, new missing maps, additional player behaviors and significantly more data collection.
Here is a list of issues that were addressed in this release.  Additional information can be found in the ASIST Gitlab repository issues list.  Also see the Experiment walkthough document in the Docs directory of the software repository.

Issue ID | Description |
| --- | --- |
8 | Add `elapsed_time` or `mission_time` to all testbed messages.
9 | When multiple players are present, triage and beep messages incorrectly get assigned to multiple players.
13 | Stretcher Tool use event message missing
14 | Participant, Call sign and playername mapping
15 | Video time marker
16 | Victim IDs
19 | Player frozen messages are missing
21 | metadata-web dashboard does not work out of the box
22 | Search specialists can unfreeze themselves
23 | Team mate shoots into air after being hit multiple times
35 | Datasets should contain the version of the testbed that was used to create it
36 | Capture and manage player audio files
37 | Stretcher role should not slow down when carrying a victim
38 | Bring back marker blocks
40 | Replace the victim skins with the new skins
41 | Add client information maps to the clientMap page
42 | Specify the observer player name in the control gui
43 | Displayed scoreboard enhancements
45 | Implement new measures
47 | Change freeze point block material to match floor
48 | ASR messages require msg.experiment_id and msg.trial_id
49 | testbed_down.sh stops non-testbed containers
50 | Update down scripts to optionally remove all containers
51 | Add unique id to the player mapping table
52 | publish the freeze block locations as ground truth
53 | Study 2 surveys
54 | Integrated replay
56 | Changing Searcher role can remove victim from existence
62 | Create container registry cleanup policy
63 | Player specific marker blocks
64 | Publish the map and mapblock versions.
65 | MarkerPlacedEvent messages stack marker blocks when placed in same location
66 | Callsign and color coordination
68 | Client info not captured
71 | map and block updates from ASU
72 | timestamp in msg section of trial stop not updated
73 | integrate updated FoV agent
74 | Integrate updated Speech Analyzer
75 | A blank username crashes the client map container
76 | Open and close audio files based on trial messages
78 | audio file rolls over when the mute button is pressed
81 | create agent version_info message type
82 | Turn the client microphone on at trial start
83 | Display client maps at mission start not trial start
84 | refactor measure message to remove dynamic property names
86 | update measures message spec to include object definitions


## V 1.2.0 Release Update, TBD

### Features
* Added testbed configuration tool

## V 1.1.0 Release Update, 15-JAN-2021
This is a major patch, with new features being introduced in an alpha state

### Features
* Client Map System alpha released. See ClientMapSystem directory Readme for details.
* Test Agent released for basic agent testing of chat,block,and map interventions. See ReferenceAgents/TestAgent directory Readme for details.
* MessageSpecs updated Agent/agent_intervention_message.json --> covers the above messages.
* a number of message definitions have been reconciled with the messages so that the message validator correctly validates them
* Marker blocks are availabl in Minecraft.  There are two block types and an erase block.
* Import and Export now handles importing a trial into a different testbed where it will create the metadata in the target testbed.
* Logging for all docker containers are now available via the Dozzle dashboard at `https://<testbed ip>:9000/Logger`
* the MQTT broker has been separated from the Elasticsearch container into its own container.
* there are now parameters in the modsettings.json file to set the mission time duration, when the yellow victims expire, if the scoreboard should be displayed

### Bug Fixes
* Observer names entered in ModSettings.json are now filtered out using full string matching, rather than substrings to avoid false positives
* The data.name field has been renamed to data.playername in the observation/state message.  This is to make it consistent with all of the other references to the player name.  The msg.version was updated to 0.6
* the name field in the observations/state messages has been changed to playername so that it is compatible with other playername values in other messages.
* the version number in the trial message is now set correctly.
* the `message` field in the message export (metadata file) has been removed.  All of the data is parsed into the appropriate field.
* On Linux systems, the permissions.sh script does not need to be run anymore.

## V 1.03
  *
  *

## V 1.0.2 Experiment 1 Release update, 23-SEP-2020
This is a minor release to fix a few issues for current experiment study and to provide some additional testbed parameterization to support more flexibility for other program performers.

### Features
*	The mission no longer terminates if all of the victims have either been triaged or expired.  The entire length of the mission will occur
*	Local/MinecraftServer/data/mods/ModSettings.json has settings for:
    * If the triage score should be visible to the player.  Default is True
    * Set the total mission time length.  The default is 10 minutes and 0 seconds
    * Set the time when the yellow victims expire.  The default is 5 minutes and 0 seconds
    * Option to end data collection several seconds after the player is teleported to the end mission room. (removePlayerOnMissionEnd).  If set to False, will teleport the player to the exit room and just leave them there. This option will continue to collect data until the client disconnects or the experimenter stops the trial.
    * Specify a list of Minecraft player usernames that are observers and for which data should not be published to the message bus.
    * Set the times when game play should be paused
    * Set the number of points received for triaging each victim type
###	Message Updates
*	The groundTruth SemanticMap Updates connection, location and object have had their bounds property set to optional


## V 1.0.1 Experiment 1 Release update, 9-SEP-2020
This is a minor release with no major new functionality to support data collection in the ASU experiment.
*	Upgrade to testbed version 1.0.1
*	Some documentation fixes to remove references to the old malmo mod
*	Within a browser session, the create trial form maintains the for fields between trials and populates them with the values from the last trial.  This is helpful when you are running a number of similar trials and don't have to re-type all of the trial information.
*	Publish message MissionState:Stop when the mission timer runs out.
*	Added support to filter messages from the observer.  Add a string to Local/MinecraftServer/data/mods/ModSettings.json in the observerNames array with the user name of the observer(s) that you don't want messages to be generated for.
*	A new asist mod has been created -  asistmod-1.0.9.jar.  Make sure to copy the asist mod from Local/MinecraftServer/data/mods to your local Minecraft mods directory.
*	Several thread safety bugs were identified and fixed.


## V 1.0 Experiment I Release, 3-AUG-2020
* New Features
  * New Deployed message bus agents
    * Field of View from CMU  this agent is included in the Local/testbed_* scripts to build/up/down all of the containers
  * New Tools
    * There are now 3 replay tools.  They all can be found in subdirectories of Tools/replayers.
	  * elkless_replayer from UA
		* doesn't need ELK stack
		* replays from a file
	  * testbed_playback from CRA
	    * plays back in real time
	  * replayer from testbed dev team
	    * can replay replays
		* can filter by topic messages that get replayed
  * New/Enhanced capabilities
    * the testbed now contains 4 missions that can be run.  Falcon_Easy, Falcon_Medium, Falcon_Hard and Competency_Test.
	All of the falcon missions are based on the same map.  Each falcon mission has a which contains the layout of the victims,
	blockages and new openings for that difficulty level.  Those blocks are applied to the base falcon map just before the mission is instanciated for play.
	These files can be found in `Local/MinecraftServer/data/mods/` and are named: MapBlocks_Easy.csv, MapBlocks_Medium.csv and MapBlocks_Hard.csv
	* there is an significantly enhanced version of the asist Minecraft mod.
	  This should be installed on all clients that work with the testbed
	* The export/import tool can how export and import replays
	* The testbed developed replyer tool has several new features. See Tools/replayers/replayer/readme.md for details.
	  * you can replay replays.  Replays now have a parent replay ID in the msg section
	  * the tool can generate a list of the trials and replays (with parent)
	  * you can filter out messages to be replayed by topic.  This is use full to re-run a trial to do testing of agent messages.
	* The startup script testbed_up.sh can take parameters to not start up the IHMClocationMonitor and/or the CMU FoV agents
	* The create trial window collects several new pieces of information which is stored in the metadata database.
	  NOTE: this update requires that the old metadata database be removed.
	  To do this deleted all of the docker volumes that start with `metadata-docker_`
	* the testbed now has a pause feature.  The time points are defined in `Local/MinecraftServer/data/mods/ModSettings.json`.
	  The player is prevented from moving and the scene is dimmed.  The player is given a stash of cookies.  When the eat a cookie, the pause ends.
	  This feature is used to stop the game action while the commander inquires are verbally given to the subject.  If the subject is in the middle
	  of triaging a victim when the pause point occurs, the pause is delayed until the triage ends (either successfully or unsuccessfully)
	* the configurer tool can now edit the config files with just one command.  To set the IP address for all of the containers just go to the configurer direction and run
	  `python testbed_config.py -ip <the broker ip>`  and supply the IP of the MQTT broker.  This will update all of the config files for all of the containers.
  * New or Enhanced Message Bus Information
    * Messages are published:
      * when the critical victims expire
	  * When the mission timer has expired
	* An event is published when the player swings, but doesn't hit anything
	* A Beep message is published with the victim finder device triggers. one beep for non-critical victim and two beeps for critical victims.
	  The trigger locations for beeps can be found in `Local/MinecraftServer/data/mods/` MapInfo_Easy.csv, MapInfo_Medium.csv ad MapInto_Hard.csv
	* At the beginning of the mission a list of the static blockages and new openings are published on the ground truth topic
	* At the beginning of the mission a list of the victims is published on the ground truth topic
	* a machine readable version of the basic map is available.
	* The trial message contains additional meta data about the trial.
	* The mission timer displayed on the screen now counts down in Minutes and Seconds.
	* Many observation and event messages now contain a mission timer field which reflects the time displayed in Minecraft to the player.
	* The competency test publishes the same messages for movement and events that are published for the falcon mission.  In addition, the competency test
	  also publishes an end message for each of the tasks.
  * There is a new mod that supports a Picture-in-Picture mini-map.  This needs to be installed on the Minecraft client
  * The asistmod now has a more detailed version number to make it easier to determine if you have the latest version of the mod.

## V 0.5 Field Test, 9-JUN-2020
* New features
  * The security login has been removed from Elastic/Kibana.  You don't need to use a password anymore
  * Many new message bus messages.  See MessageSpecs/message_summary.md for a list of all of the messages
  * New testbed data Export/Import tool.  This tool will dump a trial out of the testbed and
    create a json file which can then be imported into another testbed instance or can just be used as data.
    * This new capability will export and import an experiment trial out of or into a testbed instance.
	* This service is started up along with the other containers when you use the Local/testbed_up script files
	* To use this service, start it up and go to http://\<your host\>:8082
	* To do an export you need to select the Elastic index which contains the trial and then the UUID of the trial.
	There are helpers for both of these by just clicking on those fields.  All of the messages for that trial will
	be written to a file with the trial UUID as the name.  You can then save this file to your local storage.
	The file is formatted as one line per message in json object format.
    * to do an import select the index in elastic you want to import into.  Then select the file which contains the trial information.
    At this time, no checking is done to warn or avoid duplicates or match with other trials of the same experiment.
  * Improvements to the message validator which will validate all messages on the message bus,
    if it is turned on in the control GUI
* Upgrade steps for the new ELK container.  You must take these steps if you are running
  on a system that you have previously built and run an earlier version of the testbed.
  * The metadata server has a new schema and hence the old database needs to be deleted.
    There is no upgrade path provided for the data.
    If you have any data that you want to keep, you should dump it out and save it outside of the testbed.
    This is the case for both the experiment data and the message data stored in elastic.
    To accomplish the upgrade, you must delete the docker volume for both elastic and metadata before you build the testbed.
    When the testbed is built, new databases will be created with the upgraded schemas
    * use `docker volume ls` to show a list of all of the volumes on your system (there may be a lot of them)
    * Look for the following volumes: elk-container_es_data, metadata-docker_metadata-app, metadata-docker_metadata-msg,
      metadata-docker_pgadmin and metadata-docker_postgres-data
    * you can delete a docker volume using the command `docker volume rm <volume name>`
    * Now buid and start up the testbed
* There is a new vesion of the asist Minecraft mod.  You should copy the file docs/asistmod-0.5.jar to the directory where your
    Minecraft client looks for mods.  Note that we have changed the version scheme of the mod (and the file).
    The older mod file said version 1.0, but the newer one says 0.5 to be consistent with the release number of the testbed.
* If you are running on Linux, you should go into Local directory and run `sudo ./permissions.sh &` before you run ./testbed_up.sh
* Also if you are not running on Windows, you need to edit the .ini file in the configurer directory and replace all of the
  "host.docker.internal" and "localhost" entries with the IP address of where you are running the testbed.
   Then you need to run the python script in that directory as: `python3 testbed_config.py -cf testbed_single_host.ini`
   you should see a list of all of the entries that were changed in the configuration files for the testbed.

## V 0.4 Field Test, 6-MAY-2020

* New features
  * Triage,Lever,Door, ItemPickUp, ItemEquipped Events now availabe on the observations/events/player/triage, observations/events/player/lever, observations/events/player/door, observations/events/player/itempickup and observations/events/player/itemequipped topics, respectively
  * Multiplayer Map no longer selectable from GUI, but archived in containers
  * Schemas added for Triage,Lever,Door, ItemPickUp, ItemEquipped Events
  * MapBlock functionality allows for adding blocks on map start via MapBlock.csv. Instructions @ Local/MinecraftServer/data/mods/MapBlocks.md
  * Configurer tool added which can figure all of the containers from one .ini properties file. See configurer/readme.md for details.

## V 0.3 Field Test, 6-APR-2020

* This release of the ASIST Testbed is being released via the source repository and the container registry.  The Source code repository is [here](https://source.cloud.google.com/asist-2130/ASIST) and the Container registry is [here](https://console.cloud.google.com/gcr/images/asist-2130/GLOBAL).
Both of these distribution mechanism are read-only and require permissions for access.  Please leave a note in Slack testbed_support channel if you need access.
* Instructions can be found in the various readme files.
* New features

    * Help and Help About information updated
    * Errors section has been added to Control GUI to capture messaging errors
    * Experiment and Trial Creation functionality added to Control GUI
    * Experiment Metadata Store DB has been added as a separate docker stack
    * A new core mod (asist mod) added to supplement and perhaps replace malmo mod in the future
    * MQTT Message Validation tool has been added and hooked up to the Control GUI for error validation
    * API Endpoint for agents to obtain an Experiment ID and Trial ID changed to @ http://malmocontrol/api/experiment/getIds from within the malmonet network, and https://localhost:9000/MalmoControl/api/experiment/getIds from outside the network.
    * New Map added with new gameplay including minecraft dog
    * Data replayer tool added.  The tool takes a trial_id and replays the data for that trial_id back onto the message bus.
    * MissionInfo Directory added

## V 0.2 Field Test, 3-MAR-2020

* This release of the ASIST Testbed is being released via the source repository and the container registry.  The Source code repository is [here](https://source.cloud.google.com/asist-2130/ASIST) and the Container registry is [here](https://console.cloud.google.com/gcr/images/asist-2130/GLOBAL).
Both of these distribution mechanism are read-only and require permissions for access.  Please leave a note in Slack testbed_support channel if you need access.
* Instructions can be found in the various readme files.
* New features
  * The malmo control GUI has been extensively reworked with new and enhanced features such as:
    * Help and Help About information
	* Status of various components of the testbed.  Indicators for the status of Malmo, Minecraft and the Reference agent. Other indicators will be added with future releases.
	* An Experiment Control widget to create and start an experiment with metadata.  This will generate a unique experiment id and attach that id to all observation messages from Minecraft/Malmo.
	* API Endpoint for agents to obtain an Experiment ID from within the MCR network @ http://malmocontrol/api/experiment/getId
  * documentation on how to pull pre-built containers from the container registry
  * Message format changes.  There is a new trial_id in most messages.  See the updated message documentation and message schema files
  * The control GUI sends an experiment message on the message bus than can be used by other agents.
  * Several containers now send heartbeat messages that are used by the experiment control for container monitoring, and can be seen on the mqtt network via the ELK stack or a debugging tool.
  * the message bus topic hierarchy has been changed to support additonal message types
* Fixes
  * fix for the Linux Java version problem

## V 0.1.1 Field Test, 30-JAN-2020

* This version of the testbed is being distributed via a Google code repository.  The repo is readable for only the testbed field test participants.  If necessary, the testbed development team will make critical updates to support the field test.

* This version of the testbed contains:
  * The Minecraft “server” ( root directory in ./MalmoContainer),
  * The Elastic-Logstash-Kibana Data Collector ( root directory in ./Elk-Container), along with the message bus broker (mqtt - mosquitto) in a container
  * A reference agent ( root directory in ./ReferenceAgents/MQTTPythonReferenceAgent) that you can run as an example and view the code to see how to connect from a python program onto the message bus
  * A data extraction tool ( root file in ./Tools/dumpElastic.py) for extracting data out of the Elasticsearch database.
  * An initial Experiment control program.  Follow the instructions to build and use this component of the testbed to start missions in Minecraft.

* Messages
  * The data generated from Minecraft, published on the message bus and collected in Elasticsearch contains avatar location and state information and chat events only.
  * The format of the messages are described in the MessageSpecs folder.  NOTE: the message formats have changed since the preliminary distribution earlier in January.
  * When you use the Minecraft control web site to start a mission, a “start” control message will be published on the message bus.  This starts the reference agent publishing and  can be used by other agents to start.
  * The message topics used are described in the MessageSpecs folder in message_topics.md

* This testbed was built and tested using Windows 10, with minor testing in the Linux CentOS environment. Accordingly, the docker-compose.yml files and dockerfiles included reference certain standards and syntaxes that are specific to Windows 10 and Linux. You may run into trouble when running on Mac and other Linux versions.

* Docker Volume and File mounting utilizes different filepath syntaxes for different OS platforms. For this reason the dockerfiles and docker-compose.yml files are readiy included in this testbed for alteration/customization. Each container folder has a dockerfile in its root directory that can be modified to make the volume and file mounting work for your specific OS environment. The main docker-compose file is available @ Local/docker-compose.v1_testbed.yml.

* When running a local experiment, you will have to change the host port in Local/MalmoContainer/ConfigFolder/config.json,
Local/MalmoControl/appsettings.json, and Local/ReferenceAgent/ConfigFolder/config.json to target the IP of the computer running the ELK stack. If you choose to run the ELK Stack on the same machine as the machine running the MCR stack (not recommended), you will have to enter your local machine's ip address in the ["mqtthost"] or ["host"] fields. "localhost" will not
work in these fields, as you will be referencing the inside of a docker container. You must enter the host machine's true IP address.
If you are attempting this feat on a Windows machine, you can enter "host.docker.internal" instead of the true IP. This will not work on a Mac or Linux system.

* Unless you have a large machine ( >32GB memory and > 6 cores), you should run the Data Collector (ELK-Stack) on a different machine than the MCR stack.  We have tested this two node configuration on developer level laptops with Intel i7-8850H CPU (6 cores) 2.6GHz and 32 GB memory. This HW configuration works well on Windows.

* Please use the testbed_support Slack channel for support and feedback on the testbed field test.

* For instructions on how to build and setup the testbed see the README.md file in the root directory


## Special Thanks

* Roger Carff of IHMC for his patience and assistance in pre-alpha debugging on both Windows and Ubuntu platforms

* Glenn Lematta and Chris Corral of ASU for help with Minecraft custom map construction

* The Microsoft/Malmo team




