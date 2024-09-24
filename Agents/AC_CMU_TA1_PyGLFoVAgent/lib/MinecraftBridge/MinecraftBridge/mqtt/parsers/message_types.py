"""
message_types.py

This file contains enumerations of the message types received from Minecraft.  
Message types follow the convention established by the ASISTMod / MQTT Bus.
Additional message types and subtypes may be incorporated.

Author: Dana Hughes
email:  danahugh@andrew.cmu.edu
"""

import enum

# TODO: Double check these!
class MessageType(enum.Enum):
    """
    Enumeration of main type of messages.  These enumerations reflect the 
    message types available from the MQTT bus in the ASIST Testbed, see message
    specs for more details.
    """

    agent = "agent"
    chat = "chat"
    control = "control"
    event = "event"
    export = "export"
    experiment = "experiment"
    groundtruth = "groundtruth"
    measures = "measures"
    observation = "observation"
    physiological = "physiological"
    status = "status"
    trial = "trial"



class MessageSubtype(enum.Enum):
    """
    Enumeration of subtypes of messages.  These enumerations reflect the 
    message types available from the MQTT bus in the ASIST Testbed, see message
    specs for more details.
    """

    AC_TED = "AC:TED"
    AC_BEARD = "AC:BEARD"
    asr = "asr"
    asr_transcription = "asr:transcription"
    create = "create"
    Event_Beep = "Event:Beep"
    Event_chat = "Event:chat"
    Event_Chat = "Event:Chat"
    Event_cognitive_load = "Event:cognitive_load"
    Event_CompetencyTask = "Event:CompetencyTask"
    Event_Door = "Event:Door"
    Event_dyad = "Event:dyad"
    Event_GasLeakPlaced = "Event:GasLeakPlaced"
    Event_GasLeakRemoved = "Event:GasLeakRemoved"
    Event_ItemDrop = "Event:ItemDrop"
    Event_ItemEquipped = "Event:ItemEquipped"
    Event_ItemPickup = "Event:ItemPickup"
    Event_ItemUsed = "Event:ItemUsed"
    Event_Lever = "Event:Lever"
    Event_location = "Event:location"
    Event_MarkerDestroyed = "Event:MarkerDestroyed"
    Event_MarkerPlaced = "Event:MarkerPlaced"
    Event_MarkerRemoved = "Event:MarkerRemoved"
    Event_Mission = "Event:Mission"
    Event_MissionState = "Event:MissionState"
    Event_Pause = "Event:Pause"
    Event_Perturbation = "Event:Perturbation"
    Event_PerturbationRubbleLocations = "Event:PerturbationRubbleLocations"
    Event_PlanningStage = "Event:PlanningStage"
    Event_PlayerJumped = "Event:PlayerJumped"
    Event_PlayerSprinting = "Event:PlayerSprinting"
    Event_PlayerSwinging = "Event:PlayerSwinging"
    Event_proximity = "Event:proximity"
    Event_RoleSelected = "Event:RoleSelected"
    Event_RubbleCollapse = "Event:RubbleCollapse"
    Event_RubbleDestroyed = "Event:RubbleDestroyed"
    Event_RubblePlaced = "Event:RubblePlaced"
    Event_Scoreboard = "Event:Scoreboard"
    Event_Triage = "Event:Triage"
    Event_Woof = "Event:Woof"
    Event_woof = "Event:woof"
    Event_ToolUsed = "Event:ToolUsed"
    Event_ToolDepleted = "Event:ToolDepleted"
    Event_TrialState = "Event:TrialState"
    Event_TriageCount = "Event:TriageCount"
    Event_VictimNoLongerSafe = "Event:VictimNoLongerSafe"
    Event_VictimEvacuated = "Event:VictimEvacuated"
    Event_VictimsExpired = "Event:VictimsExpired"
    Event_VictimsRescued = "Event:VictimsRescued"
    Event_VictimPickedUp = "Event:VictimPickedUp"
    Event_VictimPlaced = "Event:VictimPlaced"
    Event_Signal = "Event:Signal"
    Event_Utility = "Event:Utility"
    FoV = "FoV"
    FoV_VersionInfo = "FoV:VersionInfo"
    FoV_Profile = "FoV:Profile"
    FoV_MapMetadata = "FoV:MapMetadata"
    FoV_BlockLocationList = "FoV:BlockLocationList"
    heartbeat = "heartbeat"
    Intervention_Chat = "Intervention:Chat"
    Intervention_Block = "Intervention:Block"
    Intervention_Map = "Intervention:Map"
    measures = "measures"
    Measure_cognitive_load = "Measure:cognitive_load"
    Mission_BlockageList = "Mission:BlockageList"
    Mission_FreezeBlockList = "Mission:FreezeBlockList"
    Mission_RoleText = "Mission:RoleText"
    Mission_ThreatSignList = "Mission:ThreatSignList"
    Mission_VictimList = "Mission:VictimList"
    Prediction_Action = "Prediction:Action"
    Prediction_State = "Prediction:State"
    rollcall_request = "rollcall:request"
    rollcall_response = "rollcall:response"
    SemanticMap_All_Updates = "SemanticMap:All_Updates"
    SemanticMap_Initialized = "SemanticMap:Initialized"
    Status_Heartbeat = "Status:Heartbeat"
    Status_SurveyResponse = "Status:SurveyResponse"
    Status_InterventionStatistics = "Status:InterventionStatistics"
    state = "state"
    start = "start"
    stop = "stop"
    trial = "trial"
    versioninfo = "versioninfo"
    
