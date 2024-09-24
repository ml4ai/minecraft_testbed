# -*- coding: utf-8 -*-
"""
.. module:: rollcall_responder
   :platform: Linux, Windows, OSX
   :synopsis: Definition of a class to handle rollcall request messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""

import time

from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype

from MinecraftBridge.messages import (
    BusHeader,
    MessageHeader,
    RollcallRequest,
    RollcallResponse
)

from MinecraftBridge.utils import Loggable



class RollcallResponder(Loggable):
    """
    Class used to handle rollcall request messages, and ensure the protocol
    between the agent and the testbed is properly maintained
    """

    def __init__(self, minecraft_bridge, trial_info, **kwargs):
        """
        Arguments
        ---------
        minecraft_bridge : MinecraftBridge interface
            Interface to the bridge to publish and subscribe to
        """

        # Bridge reference to publish to, and trial info
        self._minecraft_bridge = minecraft_bridge
        self._trial_info = trial_info

        if not "agent_name" in kwargs:
            self.logger.warning("%s:  agent_name not provided in keyword arguments", self)
        if not "version" in kwargs:
            self.logger.warning("%s:  Version number not provided in keyword arguments", self)

        self._version = kwargs.get("version", "UNKNOWN")
        self._agent_name = kwargs.get("agent_name", "ASI_CMU_TA1_ATLAS")

        # Maintain the time that the agent was started
        self.__start_time = time.time()


    def respond(self, request):
        """
        Create and publish a rollcall response message.

        Arguments
        ---------
        request : MinecraftBridge.message.RollcallRequest
            Rollcall request message to respond to
        """

        self.logger.debug("%s:  Publishing Rollcall Response", self)

        response = RollcallResponse(rollcall_id=request.rollcall_id,
                                    version=self._version,
                                    status="up",
                                    uptime = int(time.time() - self.__start_time))

        # Add headers with the key info
        bus_header = BusHeader(MessageType.agent)
        msg_header = MessageHeader(MessageSubtype.rollcall_response,
                                   request.headers["msg"].experiment_id,
                                   request.headers["msg"].trial_id,
                                   self._agent_name,
                                   replay_id = request.headers["msg"].replay_id)

        response.addHeader("header", bus_header)
        response.addHeader("msg", msg_header)

        self.logger.debug("%s:  %s", self, response.toJson())

        self._minecraft_bridge.send(response)
