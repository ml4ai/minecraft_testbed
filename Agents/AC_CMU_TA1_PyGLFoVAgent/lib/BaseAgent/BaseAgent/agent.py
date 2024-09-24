# -*- coding: utf-8 -*-
"""
.. module:: agent
   :platform: Linux, Windows, OSX
   :synopsis: A base class building an ASIST agent.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

This file provides a base agent class suitable for integrating into the ASIST
testbed, or through reading input messages from a metadata file and generating
output messages to a separate file.

Boilerplate functionality includes the following:

1.  Connecting the agent to the message buses,

2.  Connecting the agent to input / output metadata files,

3.  Generating agent_version_info messages,

4.  Set up basic logging,

5.  Injest a configuration file with minimally required properties
"""

import os

from MinecraftBridge.messages import (
    MissionStateEvent,
    PlayerState,
    RoleSelectedEvent,
    RollcallRequest,
    SemanticMapInitialized,
    Status,
    Trial,

)
from MinecraftBridge.mqtt import FileBridge
from MinecraftBridge.mqtt.interfaces import CallbackInterface
from MinecraftBridge.mqtt.parsers import MessageSubtype, MessageType
from MinecraftBridge.utils import Loggable
from RedisBridge import RedisBridge
from RedisBridge.interfaces import CallbackInterface as CallbackInterfaceRB

from .components import (
    HeartbeatThread,
    Participant,
    ParticipantCollection,
    RollcallResponder,
    SemanticMap,
    VersionInfoPublisher,
    MissionClock
)
from .context import MissionContext
from .utils import DependencyInjection


class BaseAgent(Loggable):
    """
    A base agent class suitable for integrating with the ASIST testbed

    Properties
    ----------
    minecraft_bridge : MinecraftBridge instance
        Bridge connection to Minecraft (e.g. MQTT Message Bus)
    mission_clock : MissionClock
        MissionClock instance used to maintain an estimate of the current 
        mission time
    participants : ParticipantCollection
        Collection of participants in current trial
    semantic_map : SemanticMap
        Representation of the semantic map for the current trial
    trial_id : dictionary
        Dictionary with Experiment, Trial, and Replay IDs

    Methods
    -------
    get_status()
        Returns status information about the agent, used by the heartbeat
        thread during generation of heartbeat messages.
    run()
        Create buses for the agent, if necessary, and connect the agent to
        the bridges
    stop()
        Stop the agent's execution, and clean up the connection with the bridges
    """

    # The agent will need to interact with the testbed both during trial runs,
    # and between trials.  When trials are not running, Experiment, Trial, and
    # Replay IDs should be a UUID of all zeros, or None
    __DEFAULT_EXPERIMENT_ID = '00000000-0000-0000-0000-000000000000'
    __DEFAULT_TRIAL_ID = '00000000-0000-0000-0000-000000000000'
    __DEFAULT_REPLAY_ID = None

    def __init__(self, minecraft_bridge, config, **kwargs):
        """
        Arguments
        ---------
        name : string
            Name of the agent
        minecraft_bridge : MinecraftBridge instance
            Bridge connection to Minecraft (e.g. MQTT Message Bus)
        config : dictionary
            Configuration dictionary
        """

        # Store the configuration file
        self.config = config

        # The agent_name is used for publication purposes, while the name is
        # used for logging purposes.  NOTE:  Need to decide if this should be
        # two values, or simply remain consistent.
        # Check to see if an agent_name is provided, and raise a warning if not
        if not "agent_name" in config:
            self.logger.warning(
                "%s:  Agent name not provided in config file", self.__class__.__name__)
            if not "agent_name" in kwargs:
                self.logger.warning(
                    "%s:  Agent name also not provided in keyword arguments", self.__class__.__name__)

        self.agent_name = self.config.get('agent_name',
                                          kwargs.get('agent_name', 'ASI_CMU_TA1_ATLAS'))
        self.name = '[%s]' % self.agent_name

        # Wrap the MinecraftBridge with a callback interfaces to provide clients
        # with a simple means of registering a callback, without needing
        # to maintain lookup maps.
        self._minecraft_bridge = minecraft_bridge
        self._callback_interface = CallbackInterface(
            minecraft_bridge, registration_priority=-1)

        # Setup components that store data retrieved during the agent-to-testbed
        # protocols.  This data will be available (but not assignable) to
        # subclasses of the BaseAgent
        self._trial_info = {'experiment_id': BaseAgent.__DEFAULT_EXPERIMENT_ID,
                            'trial_id': BaseAgent.__DEFAULT_TRIAL_ID,
                            'replay_id': BaseAgent.__DEFAULT_REPLAY_ID
                            }
        self._participants = ParticipantCollection()
        self._semantic_map = SemanticMap()

        # Setup and start components to handle necessary protocols between the
        # agent and the testbed.  To avoid needless heartbeat messages, it's
        # possible to have this component not start.  However, the default
        # behavior should be to start
        self._heartbeat = HeartbeatThread(self._minecraft_bridge,
                                          self._trial_info, self,
                                          self.config.get(
                                              "heartbeat_rate", 20),
                                          agent_name=self.agent_name)

        if kwargs.get("run_heartbeats", True):
            self._heartbeat.start()
        self._active = False

        # Setup a MissionClock instance to provide _approximate_ mission time 
        # to interested components
        self._mission_clock = MissionClock(fidelity=self.config.get("mission_clock_fidelity", 0))

        self.version = kwargs.get("version", "UNKNOWN")
        self._rollcall_responder = RollcallResponder(self._minecraft_bridge,
                                                     self._trial_info,
                                                     agent_name=self.agent_name,
                                                     version=self.version)

        self._version_info_publisher = VersionInfoPublisher(self._minecraft_bridge,
                                                            self._trial_info,
                                                            self.config,
                                                            agent_name=self.agent_name)

        # Register the callbacks needed to handle agent-testbed interaction
        self._callback_interface.register_callback(Trial, self.__onTrial)
        self._callback_interface.register_callback(
            RoleSelectedEvent, self.__onRoleSelected)
        self._callback_interface.register_callback(
            RollcallRequest, self.__onRollcallRequest)
        self._callback_interface.register_callback(
            SemanticMapInitialized, self.__onSemanticMapInitialized)
        self._callback_interface.register_callback(
            MissionStateEvent, self._mission_clock._onMissionState)
        self._callback_interface.register_callback(
            PlayerState, self._mission_clock._onPlayerState)


    def __str__(self):
        """
        String representation of the agent
        """
        return self.name


    @property
    def minecraft_bridge(self):
        """
        Interface to the Minecraft message bus, which provides functionality
        defined below.

        Methods
        -------
        register_callback(MessageClass, callback_method)
            Indicate to call the provided callback method when a message with
            the type of the MessageClass is received
        deregister_callback(callback_method)
            Indicate that callbacks should no longer be made to the given
            callback method
        publish(message)
            Publish the message to the bus
        """
        return self._minecraft_bridge


    @property
    def trial_info(self):
        """
        Returns the UUIDs of the Experiment ID, Trial ID, and Replay ID of the
        current trial.  If a trial is not running, these are set to default
        values consisting of all zeros.  If the trial is not a replay, the
        Replay ID is set to `None`.

        Returns
        -------
        Dictionary with the following keyed properties:

        experiment_id : string
            Experiment ID, as UUID
        trial_id : string
            Trial ID, as UUID
        replay_id : string or None
            Replay ID, as UUID, or None if not a replay
        """
        return self._trial_info

    @trial_info.setter
    def trial_info(self, _):
        pass


    @property
    def participants(self):
        """
        Return the collection of participants in the current trial.  If a trial is not
        running, then the collection is empty.

        Returns
        -------
        Instance of ParticipantCollection
        """
        return self._participants

    @participants.setter
    def participants(self, _):
        pass


    @property
    def semantic_map(self):
        """
        Return the representation of the semantic map for the current trial.

        Returns
        -------
        Instance of SemanticMap
        """

        return self._semantic_map

    @semantic_map.setter
    def semantic_map(self, _):
        pass


    @property
    def mission_clock(self):
        return self._mission_clock


    def get_status(self):
        """
        Return status information of the agent.  This will typically be
        overridden by subclasses of BaseAgent.

        Returns
        -------
        state : MinecraftBridge.messages.Status.State
            State of the agent
        status : string
            Message giving detail on the status of the component
        active : boolean
            Indication of whether the agent is active
        """

        return Status.State.OK, "", self._active

    ### CALLBACK METHODS TO HANDLE AGENT-TO-TESTBED PROTOCOL ###

    def __onTrial(self, message):
        """
        Process the start or stop of a trial.
        """

        if message.headers['msg'].sub_type == MessageSubtype.start:

            self.logger.info("%s:  Starting Trial", self)

            # Populate the participants based on the message's ClientInfo,
            # after clearing out the current clients
            self._participants.clear()

            for client in message.client_info:
                self._participants.add(Participant(client.participantid,
                                                   client.playername,
                                                   client.callsign))

            # Set the trial, experiment, and replay ids
            self._trial_info['experiment_id'] = message.headers['msg'].experiment_id
            self._trial_info['trial_id'] = message.headers['msg'].trial_id
            self._trial_info['replay_id'] = message.headers['msg'].replay_id

            # Start the hearbeat thread
            self.logger.debug("%s:  Starting Heartbeat Messages", self)
            self._heartbeat.send_heartbeats(True)

            # Publish the version information of the agent
            self._version_info_publisher.publish_version_info()

            self._active = True

        elif message.headers['msg'].sub_type == MessageSubtype.stop:

            self.logger.info("%s:  Stopping Trial", self)

            # Reset our participant collection?
            # Actually, only need to reset this before the start of new trials
            # Persisting the participant collection until then could be useful
            # (e.g. for dashboard)
            # self._participants.clear()

            # Set the trial info to the default values
            self._trial_info['experiment_id'] = BaseAgent.__DEFAULT_EXPERIMENT_ID
            self._trial_info['trial_id'] = BaseAgent.__DEFAULT_TRIAL_ID
            self._trial_info['replay_id'] = BaseAgent.__DEFAULT_REPLAY_ID

            # Stop the hearbeat thread
            self.logger.debug("%s:  Stopping Heartbeat Messages", self)
            self._heartbeat.send_heartbeats(False)

            self._active = False

        else:
            self.logger.warning(
                f"{self}:  Unrecognized Trial message type - {message.headers['msg'].sub_type}")

    def __onRoleSelected(self, message):
        """
        Update participant roles.

        Arguments
        ---------
        message : MinecraftBridge.message.RoleSelectedEvent
            RoleSelectedEvent instance
        """
        self.participants[message.participant_id].role = message.newRole

    def __onRollcallRequest(self, message):
        """
        Have the Rollcall Responder publish a response message

        Arguments
        ---------
        request : MinecraftBridge.message.RollcallRequest
            Rollcall request message to respond to
        """

        self.logger.debug("%s:  Received Rollcall Request Message", self)

        self._rollcall_responder.respond(message)

    def __onSemanticMapInitialized(self, message):
        """
        Initialize the Semantic Map from the message contents

        Arguments
        ---------
            message : MinecraftBridge.messages.SemanticMapInitialized
        """

        self.logger.debug(
            "%s:  Received Semantic Map Initialized Message", self)

        self._semantic_map.init_from_message(message)

    def run(self, auto_stop=True):
        """
        Create a bus for the agent, if necessary, and connect the agent to the
        bridge.  Maintains the connection and cleans up once complete.

        Arguments
        ---------
        args : argparse Namespace
            Command line arguments
        auto_stop: whether to stop the bus automatically after processing.
        """
        self.logger.debug(f"{self}:  Running agent ...")
        self.minecraft_bridge.connect()

        # The Minecraft bridge instance maintains control of execution
        # at this point. Once finished, stop the context if ``auto_stop=True``.
        if auto_stop:
            self.stop()

    def stop(self):
        """
        Stop the agent's execution, and clean up the connection with the bridge
        """

        # Stop the bridges
        self.logger.debug(f"{self}:  Stopping agent ...")
        if self.minecraft_bridge:
            self.minecraft_bridge.disconnect()

        # Stop any threads the BaseAgent is responsible for
        self._heartbeat.stop()

    #################################################
    ### Legacy Methods (to be eventually removed) ###
    #################################################

    @property
    def bridge(self):
        """
        Temporary while refactoring
        """
        return self.minecraft_bridge

    def register_callback(self, message_class, callback):
        """
        Temporary while refactoring
        """
        self.minecraft_bridge.register_callback(message_class, callback)


class BootstrapAgent(BaseAgent):
    """
    Minimal agent bootstrapped from a metadata file.
    """

    def __init__(self, metadata_path, config={}, **kwargs):
        # Create Minecraft bridge
        config.setdefault('agent_name', self.__class__.__name__)
        minecraft_bridge = FileBridge(
            config['agent_name'], metadata_path, os.devnull)
        super().__init__(minecraft_bridge, config, **kwargs)

        # Create Redis bridge
        redis_host = config.get('redis_host', 'localhost')
        redis_port = config.get('redis_port', 6379)
        try:
            self.redis_bridge = RedisBridge(host=redis_host, port=redis_port)
        except:
            self.redis_bridge = RedisBridge(dummy_redis_server=True)

        # Create context
        self.context = MissionContext(
            CallbackInterface(self.minecraft_bridge),
            CallbackInterfaceRB(self.redis_bridge),
            self.participants,
            self.semantic_map,
            self.trial_info,
        )

    def stop(self):
        super().stop()
        self.redis_bridge.stop()

    def run(self, auto_stop=True):
        self.redis_bridge.start()
        super().run(auto_stop=auto_stop)
        if auto_stop:
            self.stop()
