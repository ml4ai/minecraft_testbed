# -*- coding: utf-8 -*-
"""
.. module:: agent chat intervention
   :platform: Linux, Windows, OSX
   :synopsis: Parser for agent chat intervention messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a dictionary of arguments needed to build each specific 
MessageParser instance to connect to the MQTT bridge.  The dictionary maps the
MessageClass to a dictionary that contains, at a minimum, the following fields:

    * topic - the message topic
    * type - the message type (MinecraftBridge.mqtt.parsers.MessageType)
    * subtype - the message subtype (MinecraftBridge.mqtt.parsers.MessageSubtype)

topics can have named substitutions, identified by braces.  Common substitution
names include

    * agent_name - name of the agent (as part of a topic string) that is
                   producing the message
"""

from ... import messages
from .message_types import MessageType, MessageSubtype

from .agent_measure import AgentMeasureParser

from .agent_prediction import (
    AgentActionPredictionMessageParser,
    AgentStatePredictionMessageParser
)

from .agent_version_info import AgentVersionInfoParser
from .asr_message import ASR_MessageParser
#from .asr_message import ASR_MessageParserFinal
from .blockage_list import BlockageListParser
from .fov_summary import FoVSummaryParser
from .fov_version_info import FoV_VersionInfoParser
from .freezeblock_list import FreezeBlockListParser
from .perturbation_rubble_location import PerturbationRubbleLocationsParser
from .scoreboard_event import ScoreboardEventParser
from .semantic_map import SemanticMapInitializedParser
from .threat_sign_list import ThreatSignListParser
from .trial import TrialParser
from .victim_list import VictimListParser



MQTT_PARSERS = {
    messages.AgentChatIntervention: {
        "topic": "agent/intervention/{agent_name}/chat",
        "type": MessageType.agent,
        "subtype": MessageSubtype.Intervention_Chat
    },
    messages.BeepEvent: {
        "topic": "observations/events/player/beep",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Beep
    },
    messages.ChatEvent: {
        "topic": "minecraft/chat",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Chat
    },
    messages.CompetencyTaskEvent: {
        "topic": "observations/events/competency/task",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_CompetencyTask
    }, 
    messages.DoorEvent: {
        "topic": "observations/events/player/door",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Door
    },
    messages.Experiment: {
        "topic": "experiment",
        "type": MessageType.experiment,
        "subtype": MessageSubtype.create
    },
    messages.FoV_BlockLocationList: {
        "topic": "agent/pygl_fov/player/3d/block_locations",
        "type": MessageType.observation,
        "subtype": MessageSubtype.FoV_BlockLocationList
    },
    messages.FoV_MapMetadata: {
        "topic": "agent/versioninfo/pygl_fov/map_metadata",
        "type": MessageType.agent,
        "subtype": MessageSubtype.FoV_MapMetadata
    },
    messages.FoVProfile: {
        "topic": "agent/pygl_fov/profile",
        "type": MessageType.agent,
        "subtype": MessageSubtype.FoV_Profile
    },    
    messages.GasLeakPlacedEvent: {
        "topic": "observations/events/server/gasleak_placed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_GasLeakPlaced
    },
    messages.GasLeakRemovedEvent: {
        "topic": "observations/events/server/gasleak_removed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_GasLeakRemoved
    },
    messages.IHMC_CognitiveLoad: {
        "topic": "agent/measure/AC_CMUFMS_TA2_Cognitive/load",
        "type": MessageType.agent,
        "subtype": MessageSubtype.Measure_cognitive_load 
    },
    messages.IHMC_Dyad: {
        "topic": "observations/events/player/dyad",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_dyad
    },
    messages.InterventionStatistics: {
        "topic": "agent/{agent_name}/intervention/statistics",
        "type": MessageType.agent,
        "subtype": MessageSubtype.Status_InterventionStatistics
    },
    messages.ItemDropEvent: {
        "topic": "observations/events/player/itemdrop",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_ItemDrop
    },
    messages.ItemEquippedEvent: {
        "topic": "observations/events/player/itemequipped",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_ItemEquipped
    },
    messages.ItemPickupEvent: {
        "topic": "observations/events/player/itempickup",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_ItemPickup
    },
    messages.ItemUsedEvent: {
        "topic": "observations/events/player/itemused",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_ItemUsed
    },
    messages.LeverEvent: {
        "topic": "observations/events/player/lever",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Lever
    }, 
    messages.LocationEvent: {
        "topic": "observations/events/player/location",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_location
    },
    messages.MarkerDestroyedEvent: {
        "topic": "observations/events/perturbation/marker_destroyed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_MarkerDestroyed
    }, 
    messages.MarkerPlacedEvent: {
        "topic": "observations/events/player/marker_placed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_MarkerPlaced
    }, 
    messages.MarkerRemovedEvent: {
        "topic": "observations/events/player/marker_removed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_MarkerRemoved
    },
    messages.MissionStateEvent: {
        "topic": "observations/events/mission",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_MissionState
    }, 
    messages.PauseEvent: {
        "topic": "observations/events/pause",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Pause
    },
    messages.PerturbationEvent: {
        "topic": "observations/events/mission/perturbation",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Perturbation
    },
    messages.PlanningStageEvent: {
        "topic": "observations/events/mission/planning",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_PlanningStage
    },     
    messages.PlayerJumpedEvent: {
        "topic": "observations/events/player/jumped",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_PlayerJumped
    },
    messages.PlayerSprintingEvent: {
        "topic": "observations/events/player/sprinting",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_PlayerSprinting
    },
    messages.PlayerState: {
        "topic": "observations/state",
        "type": MessageType.observation,
        "subtype": MessageSubtype.state
    }, 
    messages.PlayerSwingingEvent: {
        "topic": "observations/events/player/swinging",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_PlayerSwinging
    },
    messages.PlayerUtility: {
        "topic": "observations/events/player/utility",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Utility
    },
    messages.RoleSelectedEvent: {
        "topic": "observations/events/player/role_selected",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_RoleSelected
    },
    messages.RollcallRequest: {
        "topic": "agent/control/rollcall/request",
        "type": MessageType.agent,
        "subtype": MessageSubtype.rollcall_request
    },
    messages.RollcallResponse: {
        "topic": "agent/control/rollcall/response",
        "type": MessageType.agent,
        "subtype": MessageSubtype.rollcall_response
    },
    messages.RoleText: {
        "topic": "groundtruth/mission/role_text",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Mission_RoleText
    },
    messages.RubbleCollapse: {
        "topic": "observations/events/player/rubble_collapse",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_RubbleCollapse
    },
    messages.RubbleDestroyedEvent: {
        "topic": "observations/events/player/rubble_destroyed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_RubbleDestroyed
    },
    messages.RubblePlacedEvent: {
        "topic": "observations/events/server/rubble_placed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_RubblePlaced
    },
    messages.Status: {
        "topic": "status/{agent_name}/heartbeats",
        "type": MessageType.status,
        "subtype": MessageSubtype.heartbeat
    },
    messages.ToolDepletedEvent: {
        "topic": "observations/events/player/tool_depleted",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_ToolDepleted
    },
    messages.ToolUsedEvent: {
        "topic": "observations/events/player/tool_used",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_ToolUsed
    },
    messages.TriageEvent: {
        "topic": "observations/events/player/triage",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Triage
    },
    messages.VictimEvacuated: {
        "topic": "observations/events/player/victim_evacuation",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_VictimEvacuated
    },
    messages.VictimsExpired: {
        "topic": "ground_truth/mission/victims_expired",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Event_VictimsExpired
    }, 
    messages.VictimsRescued: {
        "topic": "ground_truth/mission/victims_rescued",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Event_VictimsRescued
    },
    messages.VictimNoLongerSafe: {
        "topic": "observations/events/perturbation/victim_no_longer_safe",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_VictimNoLongerSafe
    },
    messages.VictimPickedUp: {
        "topic": "observations/events/player/victim_picked_up",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_VictimPickedUp
    },
    messages.VictimPlaced: {
        "topic": "observations/events/player/victim_placed",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_VictimPlaced
    },
    messages.VictimSignal: {
        "topic": "observations/events/player/signal",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Signal
    },    
    messages.WoofEvent: {
        "topic": "observations/events/player/woof",
        "type": MessageType.event,
        "subtype": MessageSubtype.Event_Woof
    }
}


UNIQUE_MQTT_PARSER_CLASSES = {
    messages.AgentVersionInfo: AgentVersionInfoParser
}


UNIQUE_MQTT_PARSER_STATIC_CLASSES = {
    messages.AgentActionPredictionMessage: AgentActionPredictionMessageParser,
    messages.AgentStatePredictionMessage: AgentStatePredictionMessageParser,
    messages.AgentMeasure: AgentMeasureParser,
    messages.AgentVersionInfo: AgentVersionInfoParser,
    messages.BlockageList: BlockageListParser,
    messages.FoV_VersionInfo: FoV_VersionInfoParser,
    messages.FoVSummary: FoVSummaryParser,    
    messages.FreezeBlockList: FreezeBlockListParser,
    messages.PerturbationRubbleLocations: PerturbationRubbleLocationsParser,
    messages.ScoreboardEvent: ScoreboardEventParser,
    messages.SemanticMapInitialized: SemanticMapInitializedParser,
    messages.ThreatSignList: ThreatSignListParser,    
    messages.Trial: TrialParser, 
    messages.VictimList: VictimListParser,
    messages.ASR_Message: ASR_MessageParser
#    messages.ASR_Message: ASR_MessageParserFinal
}



NOT_IMPLEMENTED_MQTT_PARSERS = {
    messages.AgentActionPredictionMessage: {
        "topic": "agent/prediction/action/{agent_name}",
        "type": MessageType.agent,
        "subtype": MessageSubtype.Prediction_Action
    },
    messages.AgentStatePredictionMessage: {
        "topic": "agent/prediction/state/{agent_name}",
        "type": MessageType.agent,
        "subtype": MessageSubtype.Prediction_State
    },
    messages.AgentVersionInfo: {
        "topic": "agent/{agent_name}/versioninfo",
        "type": MessageType.agent,
        "subtype": MessageSubtype.versioninfo
    },
    messages.BlockageList: {
        "topic": "ground_truth/mission/blockages_list",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Mission_BlockageList
    }, 
    messages.FoV_VersionInfo: {
        "topic": "agent/versioninfo/pygl_fov",
        "type": MessageType.agent,
        "subtype": MessageSubtype.FoV_VersionInfo
    },
    messages.FoVSummary: {
        "topic": "agent/pygl_fov/player/3d/summary",
        "type": MessageType.observation,
        "subtype": MessageSubtype.FoV
    },    
    messages.FreezeBlockList: {
        "topic": "ground_truth/mission/freezeblock_list",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Mission_FreezeBlockList
    },
    messages.ScoreboardEvent: {
        "topic": "observations/events/scoreboard",
        "type": MessageType.observation,
        "subtype": MessageSubtype.Event_Scoreboard
    },
    messages.SemanticMapInitialized: {
        "topic": "ground_truth/semantic_map/initialized",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.SemanticMap_Initialized
    },
    messages.ThreatSignList: {
        "topic": "ground_truth/mission/threatsign_list",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Mission_ThreatSignList
    },    
    messages.Trial: {
        "topic": "trial",
        "type": MessageType.trial,
        "subtype": MessageSubtype.start
    }, 
    messages.VictimList: {
        "topic": "ground_truth/mission/victims_list",
        "type": MessageType.groundtruth,
        "subtype": MessageSubtype.Mission_VictimList
    }
}