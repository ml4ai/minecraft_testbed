# -*- coding: utf-8 -*-
"""
.. module:: agent_version_info
   :platform: Linux, Windows, OSX
   :synopsis: Parser for agent version information messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for agent version information messages
"""

from ...messages import AgentVersionInfo
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements

class AgentVersionInfoParser:
    """
    A class for parsing agent version information messages from MQTT bus.

    Attributes
    ----------
    topic : string
        MQTT topic used to publish / subscribe to
    MessageClass : MinecraftBridge.message class
        Message class associated with this parser

    Methods
    -------
    parse
        Converts a dictionary representation from MQTT bus message to 
        AventVersionInfo message object
    generate
        Convert AgentVersionInfo instance to JSON for publication
    """

    msg_type = MessageType.agent
    msg_subtype = MessageSubtype.versioninfo
    alternatives = []

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        agent_name : string
            Name of the agent for use in the topic
        """

        self._topic = "agent/{agent_name}/versioninfo"

        self._MessageClass = AgentVersionInfo

        self._agent_name = kwargs.get("agent_name", "AGENT_NAME_NOT_PROVIDED")


    @property
    def topic(self):
        """
        Get the message topic associated with this parser
        """

        return self._topic.format(agent_name=self._agent_name)


    @topic.setter
    def topic(self, _):
        
        pass


    @property
    def MessageClass(self):
        """
        Get the message class this parser is designed to handle
        """

        return self._MessageClass

    @topic.setter
    def MessageClass(self, _):

        pass


    def parse(json_message):
        """
        Convert the a JSON message to an instance of AgentVersionInfo.

        Arguments
        ---------
        json_message : dictionary
            Dictionary representation of the message received from the MQTT bus
        """

        # Make sure that there's a "header" and "msg" field in the message
        if not "header" in json_message.keys() or not "msg" in json_message.keys():
            raise MissingHeaderException(json_message) 

        # Parse the header and message header
        busHeader = BusHeaderParser.parse(json_message["header"])
        messageHeader = MessageHeaderParser.parse(json_message["msg"])

        # Check to see if this parser can handle this message type, if not, 
        # then return None
        if busHeader.message_type != MessageType.agent:
            return None
        if messageHeader.sub_type != MessageSubtype.versioninfo:
            return None

        # Parse the data
        data = json_message["data"]

        message = AgentVersionInfo(agent_name=data["agent_name"],
                                   version=data["version"],
                                   owner=data["owner"])

        for source in data.get("source", []):
            message.addSource(source)
        for dependency in data.get("dependencies", []):
            message.addDependency(dependency)
        for config in data.get("config", []):
            message.addConfig(config["name"], config["value"])
        for info in data.get("publishes", []):
            message.addPublishInfo(info["topic"], info["message_type"], info["sub_type"])
        for info in data.get("subscribes", []):
            message.addSubscribeInfo(info["topic"], info["message_type"], info["sub_type"])

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message


    def generate(self, message):
        """
        
        """

        return message.toJson()