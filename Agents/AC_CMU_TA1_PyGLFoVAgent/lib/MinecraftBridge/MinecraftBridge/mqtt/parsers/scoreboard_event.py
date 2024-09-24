# -*- coding: utf-8 -*-
"""
.. module:: scoreboard_event
   :platform: Linux, Windows, OSX
   :synopsis: Parser for scoreboard event messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for scoreboard event messages
"""

from ...messages import ScoreboardEvent
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException


class ScoreboardEventParser:
    """
    A class for parsing scoreboard event messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "observations/events/scoreboard"
    MessageClass = ScoreboardEvent

    msg_type = MessageType.event
    msg_subtype = MessageSubtype.Event_Scoreboard
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
        if busHeader.message_type != MessageType.observation:
            return None
        if messageHeader.sub_type != MessageSubtype.Event_Scoreboard:
            return None

        # Parse the data
        data = json_message["data"]

        message = ScoreboardEvent(**data)
        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the scores in the list
        for player, score in data["scoreboard"].items():
            message.addScore(player, score)

        message.finalize()

        return message