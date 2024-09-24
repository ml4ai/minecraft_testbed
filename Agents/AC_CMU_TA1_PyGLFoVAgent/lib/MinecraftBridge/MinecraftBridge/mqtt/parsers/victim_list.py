# -*- coding: utf-8 -*-
"""
.. module:: victim_list
   :platform: Linux, Windows, OSX
   :synopsis: Parser for victim list messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for victim list messages
"""

from ...messages import VictimList, Victim
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements

import logging



class VictimListParser:
    """
    A class for parsing victim list messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "ground_truth/mission/victims_list"
    MessageClass = VictimList

    msg_type = MessageType.groundtruth
    msg_subtype = MessageSubtype.Mission_VictimList
    alternatives = []

    logger = logging.getLogger("VictimListParser")

    @classmethod
    def parse(cls, json_message):
        """
        Convert the a JSON message to an instance of VictimList.

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
        if messageHeader.sub_type != MessageSubtype.Mission_VictimList:
            return None

        # Parse the data
        data = json_message["data"]

        message = VictimList(**data)
        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        # Parse all the victims in the list
        for victim in data["mission_victim_list"]:
            location = (victim["x"], victim["y"], victim["z"])
            unique_id = victim.get("unique_id", -1)

            try:
                block_type = MinecraftElements.Block[victim["block_type"]]
            except KeyError:
                cls.logger.warning("%s: Trying to parse unknown block type %s", cls.__name__, victim["block_type"])
                block_type = MinecraftElements.Block["UNKNOWN"]

            room_name = victim["room_name"]
            unique_id = victim.get("unique_id", -1)

            message.add(Victim(location=location, 
                               block_type=block_type, 
                               room_name=room_name,
                               unique_id=unique_id))

        return message
