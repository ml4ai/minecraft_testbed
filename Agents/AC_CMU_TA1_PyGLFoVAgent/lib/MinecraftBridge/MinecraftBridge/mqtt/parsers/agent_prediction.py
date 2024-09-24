# -*- coding: utf-8 -*-
"""
.. module:: agent_prediction
   :platform: Linux, Windows, OSX
   :synopsis: Parser for agent action and state prediciton messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for agent action and state prediction messages
"""

from ...messages import (
    AgentPredictionGroupProperty,
    AgentActionPrediction,
    AgentStatePrediction,
    AgentActionPredictionMessage,
    AgentStatePredictionMessage
)
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements

class AgentActionPredictionMessageParser:
    """
    A class for parsing agent action prediction messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "agent/prediction/action/CMU-RI_ASIST_Agent"
    MessageClass = AgentActionPredictionMessage

    msg_type = MessageType.agent
    msg_subtype = MessageSubtype.Prediction_Action
    alternatives = []

    @staticmethod
    def parse(json_message):
        """
        Convert the a JSON message to an instance of AgentActionPredictionMessage.

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
        if messageHeader.sub_type != MessageSubtype.Prediction_Action:
            return None

        # Parse the data
        data = json_message["data"]
        group_data = AgentPredictionGroupProperty(data["group"]["start"],
                                                  data["group"]["duration"],
                                                  data["group"]["explanation"])

        message = AgentActionPredictionMessage(created=data["created"],
                                               group=group_data)

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the predictions
        for prediction in data["predictions"]:
            message.add(AgentActionPrediction(**prediction))

        message.finalize()            

        return message


class AgentStatePredictionMessageParser:
    """
    A class for parsing agent state prediction messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "agent/prediction/state/CMU-RI_ASIST_Agent"
    MessageClass = AgentStatePredictionMessage

    msg_type = MessageType.agent
    msg_subtype = MessageSubtype.Prediction_State
    alternatives = []

    @staticmethod
    def parse(json_message):
        """
        Convert the a JSON message to an instance of AgentStatePredictionMessage.

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
        if messageHeader.sub_type != MessageSubtype.Prediction_State:
            return None

        # Parse the data
        data = json_message["data"]
        group_data = AgentPredictionGroupProperty(data["group"]["start"],
                                                  data["group"]["duration"],
                                                  data["group"]["explanation"])

        message = AgentStatePredictionMessage(created=data["created"],
                                              group=group_data)

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the predictions
        for prediction in data["predictions"]:
            message.add(AgentStatePrediction(**prediction))

        message.finalize()

        return message        