# -*- coding: utf-8 -*-
"""
.. module:: threat_sign_list
   :platform: Linux, Windows, OSX
   :synopsis: Parser for threat sign list messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for threat sign list messages
"""

from ...messages import ThreatSignList, ThreatSign
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements

import logging


class ThreatSignListParser:
    """
    A class for parsing threat sign list messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "ground_truth/mission/threatsign_list"
    MessageClass = ThreatSignList

    msg_type = MessageType.groundtruth
    msg_subtype = MessageSubtype.Mission_ThreatSignList
    alternatives = []

    logger = logging.getLogger("ThreatSignListParser")


    @classmethod
    def parse(cls, json_message):
        """
        Convert the a JSON message to an instance of ThreatSignList.

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
        if messageHeader.sub_type != MessageSubtype.Mission_ThreatSignList:
            return None

        # Parse the data
        data = json_message["data"]

        mission = data["mission"]

        message = ThreatSignList(mission=mission)
        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the freeze blocks in the list
        for block in data["mission_threatsign_list"]:
            location = (block["x"], block["y"], block["z"])

            try:
                block_type = MinecraftElements.Block[block["block_type"]]
            except KeyError:
                cls.logger.warning("%s: Trying to parse unknown block type %s", cls.__name__, block["block_type"])
                block_type = MinecraftElements.Block["UNKNOWN"]
            
            room_name = block["room_name"]
            feature_type = block["feature_type"]

            message.add(ThreatSign(location=location, 
                                    block_type=block_type, 
                                    room_name=room_name, 
                                    feature_type=feature_type))

        return message