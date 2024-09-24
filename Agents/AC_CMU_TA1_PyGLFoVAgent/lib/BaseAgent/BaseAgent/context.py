# -*- coding: utf-8 -*-
"""
.. module:: observer
   :platform: Linux, Windows, OSX
   :synopsis: A context class that acts as a wrapper around
              a MinecraftBridge and a RedisBridge.

.. moduleauthor:: Ini Oguntola <ioguntol@andrew.cmu.edu>
"""

from .components import (
    Participant, 
    ParticipantCollection, 
    SemanticMap, 
    MissionClock
)
from MinecraftBridge.messages import (
    SemanticMapInitialized, 
    Trial,
    MissionStateEvent,
    PlayerState
)
from MinecraftBridge.mqtt import (
    Bridge as MQTTBridge, 
    FileBridge,
    CallbackDecorator
)
from MinecraftBridge.mqtt.parsers import MessageSubtype
from MinecraftBridge.utils import Loggable

import os
import RedisBridge



class MissionContext(Loggable):
    """
    Wrapper around a MinecraftBridge and RedisBridge that 
    acts as the context for an ASIST mission trial.

    Attributes
    ----------
    minecraft_bridge : MinecraftBridge.mqtt.CallbackDecorator
        Callback decorator / interface for Minecraft bridge to the external bus
    redis_bridge : RedisBridge.CallbackDecorator
        Callback decorator for Redis bridge to the internal bus
    participants : ParticipantCollection
        Collection of participants for the current trial
    semantic_map : SemanticMap
        Representation of the map semantics
    trial_info : dict
        Dictionary of info for the current trial
    mission_clock : MissionClock


    NOTE:  run, stop, and creation / maintainance of components was moved to 
           the BaseAgent, as 1) subcomponents should not be allowed to start or
           stop the bus, and 2) there are future plans from TA3 to require 
           agents to interface with the testbed through a more complex protocol
           (i.e., agent should be able to receive information through request/
           response)
    """

    def __init__(self, minecraft_interface, redis_interface, participants, 
                       semantic_map, trial_info, mission_clock, name=None):
        """
        Arguments:
        ----------
        minecraft_interface : MinecraftBridge.bridge interface / decorator
            Interface to Minecraft bridge to the external bus
        redis_interface : RedisBridge.bridge interface / decorator
            Interface to Redis bridge to the internal bus
        name : str
            The name for this context
        """

        self.__name = name

        self._minecraft_interface = minecraft_interface
        self._redis_interface = redis_interface
        self._participants = participants
        self._semantic_map = semantic_map
        self._trial_info = trial_info
        self._mission_clock = mission_clock



    def __str__(self):
        """
        String representation of this object.
        """
        if self.__name:
            return f'[{self.__class__.__name__} - {self.__name}]'

        return f'[{self.__class__.__name__}]'


    @property
    def minecraft_bridge(self):
        """
        The Minecraft bridge for this context.
        """
        return self._minecraft_interface


    @property
    def minecraft_interface(self):
        return self._minecraft_interface
    


    @property
    def redis_bridge(self):
        """
        The Redis bridge for this context.
        """
        return self._redis_interface


    @property
    def redis_interface(self):
        return self._redis_interface
    


    @property
    def participants(self):
        """
        The ParticipantCollection for the current trial.
        """
        return self._participants


    @property
    def semantic_map(self):
        """
        The SemanticMap for the current trial.
        """
        return self._semantic_map


    @property
    def trial_info(self):
        """
        A dictionary of info for the current trial.
        Has keys for 'experiment_id', 'trial_id', and 'replay_id'.
        """
        return self._trial_info


    @property
    def mission_clock(self):
        return self._mission_clock
    


















class BootstrapMissionContext(Loggable):
    """
    Wrapper around a MinecraftBridge and RedisBridge that 
    acts as the context for an ASIST mission trial.

    Attributes
    ----------
    minecraft_bridge : MinecraftBridge.mqtt.CallbackDecorator
        Callback decorator / interface for Minecraft bridge to the external bus
    redis_bridge : RedisBridge.CallbackDecorator
        Callback decorator for Redis bridge to the internal bus
    participants : ParticipantCollection
        Collection of participants for the current trial
    semantic_map : SemanticMap
        Representation of the map semantics
    trial_info : dict
        Dictionary of info for the current trial


    Methods
    -------
    run()
        Run the Minecraft and Redis bridges simultaneously
    stop()
        Stop the Minecraft and Redis bridges

    Static Methods
    --------------
    from_metadata(input_path, output_path=None)
        Return MissionContext instance for a saved metadata file
    """

    def __init__(self, minecraft_interface, redis_interface, participants, 
                       semantic_map, trial_info, name=None):
        """
        Arguments:
        ----------
        minecraft_interface : MinecraftBridge.bridge interface / decorator
            Interface to Minecraft bridge to the external bus
        redis_interface : RedisBridge.bridge interface / decorator
            Interface to Redis bridge to the internal bus
        name : str
            The name for this context
        """

        self.__name = name


        # If not provided, spin up our own RedisBridge
        if redis_bridge is None:
            redis_host = config.get('redis_host', 'localhost')
            redis_port = config.get('redis_port', 6379)
            try:
                redis_bridge = RedisBridge.RedisBridge(host=redis_host, port=redis_port)
            except:
                redis_bridge = RedisBridge.RedisBridge(dummy_redis_server=True)

        self.logger.info(
            f"{self}:  Initializing with Minecraft bridge {minecraft_bridge} and Redis bridge {redis_bridge}")

        # Wrap the bridges with callback interfaces to provide clients
        # with a simple means of registring a callback, without needing
        # to maintain lookup maps.
        self._minecraft_bridge = CallbackDecorator(minecraft_bridge)
        self._redis_bridge = redis_bridge.callback_decorator()

        # Register internal callbacks for this Context
        self._minecraft_bridge.register_callback(Trial, self.__onTrial, priority=-1)
        self._minecraft_bridge.register_callback(
            SemanticMapInitialized, self.__onSemanticMapInitialized, priority=-1)

        # Initialize components
        self._participants = ParticipantCollection()
        self._semantic_map = SemanticMap()
        self._default_trial_info = config.get('default_trial_info', {
            'experiment_id': None,
            'trial_id': None,
            'replay_id': None,
        })
        self._trial_info = self._default_trial_info.copy()

        self._mission_clock = MissionClock()
        self._minecraft_bridge.register_callback(MissionStateEvent, self._mission_clock._onMissionState)
        self._minecraft_bridge.register_callback(PlayerState, self._mission_clock._onPlayerState)



    def __str__(self):
        """
        String representation of this object.
        """
        if self.__name:
            return f'[{self.__class__.__name__} - {self.__name}]'

        return f'[{self.__class__.__name__}]'


    @property
    def minecraft_bridge(self):
        """
        The Minecraft bridge for this context.
        """
        return self._minecraft_bridge


    @property
    def minecraft_interface(self):
        return self._minecraft_bridge
    

    @property
    def mission_clock(self):
        return self._mission_clock


    @property
    def redis_bridge(self):
        """
        The Redis bridge for this context.
        """
        return self._redis_bridge


    @property
    def redis_interface(self):
        return self._redis_bridge
    


    @property
    def participants(self):
        """
        The ParticipantCollection for the current trial.
        """
        return self._participants


    @property
    def semantic_map(self):
        """
        The SemanticMap for the current trial.
        """
        return self._semantic_map


    @property
    def trial_info(self):
        """
        A dictionary of info for the current trial.
        Has keys for 'experiment_id', 'trial_id', and 'replay_id'.
        """
        return self._trial_info


    def run(self):
        """
        Run the Minecraft and Redis bridges simultaneously.
        """
        self.logger.debug(f"{self}:  Running context ...")
        self.redis_bridge.start()
        self.minecraft_bridge.connect()

        # The Minecraft bridge instance maintains control of execution
        # at this point. Once finished, stop the context.
        self.stop()


    def stop(self):
        """
        Stop the Minecraft and Redis bridges.
        """
        self.logger.debug(f"{self}:  Stopping context ...")
        if self.minecraft_bridge:
            self.minecraft_bridge.disconnect()
        if self.redis_bridge:
            self.redis_bridge.stop()


    @staticmethod
    def from_metadata(input_path, output_path=None):
        """
        Return a new MissionContext instance for a saved metadata file.

        Arguments
        ---------
        input_path : string
            path of the file to read messages in from
        output_path : string
            path of the file to write messages to

        Returns
        -------
        context : MissionContext
            A MissionContext instance for the saved metadata
        """
        output_path = os.devnull if output_path is None else output_path
        minecraft_bridge = FileBridge(None, input_path, output_path)
        return MissionContext(minecraft_bridge)


    def __onSemanticMapInitialized(self, msg):
        """
        Initialize the semantic map.
        """
        self.logger.debug(f"{self}:  Initializing Semantic Map")
        self._semantic_map.init_from_message(msg)


    def __onTrial(self, msg):
        """
        Process the start or stop of a trial.
        """
        if msg.headers['msg'].sub_type == MessageSubtype.start:
            # Populate trial info
            self._trial_info['experiment_id'] = msg.headers['msg'].experiment_id
            self._trial_info['trial_id'] = msg.headers['msg'].trial_id
            self._trial_info['replay_id'] = msg.headers['msg'].replay_id

            # Populate the participants based on the message's ClientInfo
            for client in msg.client_info:
                participant = Participant(
                    client.participantid, client.playername, client.callsign)
                self._participants.add(participant)

        elif msg.headers['msg'].sub_type == MessageSubtype.stop:
            # Reset our trial info and participant collection
###            self._trial_info = self._default_trial_info.copy()
            # DANA: A client may end up keeping a local variable mapping to 
            #       _trial_info, if _trial_info is reassigned to a new 
            #       dictionary, then the client will be using the original
            #       values, and would end up publishing to a stale
            #       experiment_id and trial_id.  Need to keep the _trial_info
            #       pointer consistent to avoid this.
            self._trial_info["experiment_id"] = self._default_trial_info["experiment_id"]
            self._trial_info["trial_id"] = self._default_trial_info["trial_id"]
            self._trial_info["replay_id"] = self._default_trial_info["replay_id"]
            self._participants.clear()

        else:
            self.logger.warning(f"{self}:  Unrecognized Trial message type - {msg.headers['msg'].sub_type}")

