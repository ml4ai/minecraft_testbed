# -*- coding: utf-8 -*-
"""
.. module:: freezeblock_list
   :platform: Linux, Windows, OSX
   :synopsis: Parser for Freezeblock List messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for Freezeblock List messages
"""

from ...messages import FreezeBlockList, FreezeBlock
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements

import logging


class FreezeBlockListParser:
    """
    A class for parsing freezeblock list messages from MQTT bus.

    MQTT Message Fields
    -------------------
    mission : string
        The name of the mission in progress
    mission_freezeblock_list : list of dictionaries
        The list of freezeblocks in the mission

    Freezeblock Fields
    ------------------
    x : float
        The current x location of the block
    y : float
        The current y location of the block
    z : float
        The current z location of the block
    block_type : string
        The block type
    room_name : string
        The room name the block is in
    feature_type : string
        The type of feature the block is
    """

    topic = "ground_truth/mission/freezeblock_list"
    MessageClass = FreezeBlockList

    msg_type = MessageType.groundtruth
    msg_subtype = MessageSubtype.Mission_FreezeBlockList
    alternatives = []

    logger = logging.getLogger("FreezeBlockListParser")


    @classmethod
    def parse(cls, json_message):
        """
        Convert the json message to an instance of FreezeBlockList.

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
        if messageHeader.sub_type != MessageSubtype.Mission_FreezeBlockList:
            return None

        # Parse the data
        data = json_message["data"]

        mission = data["mission"]

        message = FreezeBlockList(mission=mission)
        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the freeze blocks in the list
        for block in data["mission_freezeblock_list"]:
            location = (block["x"], block["y"], block["z"])

            try:
                block_type = MinecraftElements.Block[block["block_type"]]
            except KeyError:
                cls.logger.warning("%s: Trying to parse unknown block type %s", cls.__name__, block["block_type"])
                block_type = MinecraftElements.Block["UNKNOWN"]

            room_name = block["room_name"]
            feature_type = block["feature_type"]

            message.add(FreezeBlock(location=location, 
                                    block_type=block_type, 
                                    room_name=room_name, 
                                    feature_type=feature_type))

        return message