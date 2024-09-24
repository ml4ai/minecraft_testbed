# -*- coding: utf-8 -*-
"""
.. module:: version_info_publisher
   :platform: Linux, Windows, OSX
   :synopsis: Definition of a class to publish version info messages at the
              start of Trial messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""

import time

from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype

from MinecraftBridge.messages import (
    BusHeader,
    MessageHeader,
    AgentVersionInfo,
    Trial
)

from MinecraftBridge.utils import Loggable



class VersionInfoPublisher(Loggable):
    """
    Class used to handle version information messages, and ensure the protocol
    between the agent and the testbed is properly maintained
    """

    def __init__(self, minecraft_bridge, trial_info, config, **kwargs):
        """
        Arguments
        ---------
        minecraft_bridge : MinecraftBridge

        trial_info : dictionary

        config : dictionary
        """

        # Store the minecraft_bridge instance for publishing purposes
        self._minecraft_bridge = minecraft_bridge
        self._config = config
        self._trial_info = trial_info
        if not "agent_name" in kwargs:
            self.logger.warning("%s: agent_name not provided in keyword arguments", self)
        self._agent_name = kwargs.get("agent_name", "ASI_CMU_TA1_ATLAS")


    def publish_version_info(self):
        """
        Create and publish a Version Info message.
        """

        self.logger.debug("%s:  Publishing Version Info", self)

        # Create the message
        versionInfo_message = AgentVersionInfo(version=self._config.get('version', 'UNKNOWN'), 
                                               url=self._config.get('url', 'UNKNOWN'), 
                                               agent_name=self._agent_name,
                                               owner=self._config.get('author', 'UNKNOWN'))

        # Add headers with the key info
        bus_header = BusHeader(MessageType.agent)
        msg_header = MessageHeader(MessageSubtype.versioninfo,
                                   self._trial_info["experiment_id"],
                                   self._trial_info["trial_id"],
                                   self._agent_name,
                                   replay_id = self._trial_info["replay_id"])

        # Add additional dependency info from the config file
        for dependency in self._config.get('dependencies', []):
            versionInfo_message.addDependency(dependency)

        # Add the URL where the agent can be obtained
        versionInfo_message.addSource(self._config.get('url', 'UNKNOWN'))

        for publish_info in self._config.get('publishes', []):
            versionInfo_message.addPublishInfo(publish_info['topic'],
                                               publish_info['type'].format(agent_name=self._agent_name),
                                               publish_info['subtype'])

        for subscribe_info in self._config.get('subscribes', []):
            versionInfo_message.addSubscribeInfo(subscribe_info['topic'],
                                                 subscribe_info['type'],
                                                 subscribe_info['subtype'])

        versionInfo_message.addHeader("header", bus_header)
        versionInfo_message.addHeader("msg", msg_header)

        # Publish the agent version info message
        versionInfo_message.finalize()

        self._minecraft_bridge.send(versionInfo_message)

