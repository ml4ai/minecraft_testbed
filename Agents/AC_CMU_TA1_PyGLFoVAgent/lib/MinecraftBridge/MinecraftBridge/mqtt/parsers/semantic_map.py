# -*- coding: utf-8 -*-
"""
.. module:: semantic_map
   :platform: Linux, Windows, OSX
   :synopsis: Parser for semantic map ground truth messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for semantic map ground truth messages
"""

from ...messages import SemanticMapInitialized
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

class SemanticMapInitializedParser:
    """
    A class for parsing semantic map ground truth messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "ground_truth/semantic_map/initialized"
    MessageClass = SemanticMapInitialized

    msg_type = MessageType.groundtruth
    msg_subtype = MessageSubtype.SemanticMap_Initialized
    alternatives = []

    @staticmethod
    def parse(json_message):
        """
        Convert the a JSON message to an instance of SemanticMapInitialized.

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
        if busHeader.message_type != MessageType.groundtruth:
            return None
        if messageHeader.sub_type != MessageSubtype.SemanticMap_Initialized:
            return None

        # Parse the data
        data = json_message["data"]

        message = SemanticMapInitialized(semantic_map_name=data["semantic_map_name"],
                                         semantic_map=data["semantic_map"]
                       )

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message