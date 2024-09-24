# -*- coding: utf-8 -*-
"""
.. module:: agent_measure
   :platform: Linux, Windows, OSX
   :synopsis: Parser for Agent Measure messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for agent measure messages
"""

from ...messages import AgentMeasure
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException


class AgentMeasureParser:
    """
    A class for parsing agent measure messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "agent/measures/{agent_name}"
    MessageClass = AgentMeasure

    msg_type = MessageType.agent
    msg_subtype = MessageSubtype.measures
    alternatives = []

    @staticmethod
    def parse(json_message):
        """
        Convert the a JSON message to an instance of ScoreboardEvent.

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
        if messageHeader.sub_type != MessageSubtype.measures:
            return None

        # Create keyword arguments from the contents of the message
        message_items = list(json_message["data"].get("event_properties",{}).items()) + \
                        list(json_message["data"].get("measure_data",{}).items())
        data = { key: value for key,value in message_items }
        data["study_version"] = json_message["data"]["study_version"]
        data["elapsed_milliseconds"] = json_message["data"]["elapsed_milliseconds"]

        message = AgentMeasure(**data)
        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message