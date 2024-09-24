# -*- coding: utf-8 -*-
"""
.. module:: blockage_list
   :platform: Linux, Windows, OSX
   :synopsis: Parser for Blockage List messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for Blockage List messages
"""

from ...messages import BlockageList, Blockage
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements

import logging


class BlockageListParser:
    """
    A class for parsing blockage list messages from MQTT bus.

    MQTT Message Fields
    -------------------
    mission : string
        the name of the mission in progress
    mission_blockage_list : list of Blockage messages
        the list of blockages in the mission

    MQTT Blockage Fields
    --------------------
    x : float
        The current x location of the blockage block
    y : float
        The current y location of the blockage block
    z : float
        The current z location of the blockage block
    block_type : string
        The blockage block type
    room_name : string
        The room name the blockage block is in
    feature_type : string
        The type of map feature this block is associated with
    """

    topic = "ground_truth/mission/blockages_list"
    MessageClass = BlockageList

    msg_type = MessageType.groundtruth
    msg_subtype = MessageSubtype.Mission_BlockageList
    alternatives = [MessageSubtype.stop]

    # Class-level logger
    logger = logging.getLogger("BlockageListParser")



    @classmethod
    def parse(cls, json_message):
        """
        Convert the a Python dictionary format of the message to a BlockageList
        instance.

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
        if messageHeader.sub_type != MessageSubtype.Mission_BlockageList:
            return None

        # Parse the data
        data = json_message["data"]

        mission = data["mission"]

        message = BlockageList(mission=mission)
        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the blockages in the list
        for blockage in data["mission_blockage_list"]:
            location = (blockage["x"], blockage["y"], blockage["z"])

            # The testbed is often changing---not guaranteed that the received
            # block type has made it to MinecraftElements
            try:
                block_type = MinecraftElements.Block[blockage["block_type"]]
            except KeyError:
                cls.logger.warning("%s: Trying to parse unknown block type %s", cls.__name__, blockage["block_type"])
                block_type = MinecraftElements.Block["UNKNOWN"]

            room_name = blockage["room_name"]
            feature_type = blockage["feature_type"]

            message.add(Blockage(location=location, 
                                 block_type=block_type, 
                                 room_name=room_name, 
                                 feature_type=feature_type))

        return message