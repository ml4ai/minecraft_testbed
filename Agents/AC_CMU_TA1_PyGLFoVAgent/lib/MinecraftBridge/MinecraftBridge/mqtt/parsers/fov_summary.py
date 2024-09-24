# -*- coding: utf-8 -*-
"""
.. module:: fov_summary.py
   :platform: Linux, Windows, OSX
   :synopsis: Parser for FoV Summary messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for FoV Summary messages
"""


from ...messages import FoVSummary
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

class FoVSummaryParser:
    """
    A class for parsing FoV Summary messages from MQTT bus.

    MQTT Message Fields
    -------------------
    observation : int
        An observation number that corresponds to that in a PlayerState message
    playername : string
        The name of the entity whose FoV is summarized
    blocks : list of dictionaries
        A list consisting of summary information for each block in the Field of View
    """

    topic = "agent/pygl_fov/player/3d/summary"
    MessageClass = FoVSummary

    msg_type = MessageType.observation
    msg_subtype = MessageSubtype.FoV
    alternatives = []

    @staticmethod
    def parse(json_message):
        """
        Convert the json message to an instance of FoVSummary.

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
        if messageHeader.sub_type != MessageSubtype.FoV:
            return None

        # Parse the data
        data = json_message["data"]

        message = FoVSummary(playername=data.get("participant_id", data.get("playername", "<UNKNOWN>")),
                            observationNumber=data["observation"])

        for summary in data["blocks"]:
            message.addBlock(summary)

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message        

