# -*- coding: utf-8 -*-
"""
.. module:: asr_message
   :platform: Linux, Windows, OSX
   :synopsis: Parser for ASR_Message messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for ASR_Message messages
"""

from ...messages import ASR_Message, ASR_Alternative
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

import MinecraftElements



class ASR_MessageParser:
    """
    A class for parsing ASR_Message messages from MQTT bus.

    MQTT ASR_Message Fields
    -----------------------
    text : string
        The transcription returned from the ASR system
    alternatives : object array
        A list of alternative transcription objects returned from the ASR system
    is_final : boolean
        Indicates whether the transcription is an intermediate or final 
        transcription
    asr_system : string
        The system used by the agent for automatic speech recognition
    id : string
        A version 4 UUID associated with this message
    participant_id : string
        The participant id this data is associated with

    MQTT ASR_Alternative Fields
    ---------------------------
    text : string
        The text of the alternative transcription
    confidence : float
        Confidence of the ASR system in the alternative transcription
    """

    MessageClass = ASR_Message

    topic = "agent/asr/final"

    msg_type = MessageType.observation
    msg_subtype = MessageSubtype.asr
    alternatives = []


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
        if busHeader.message_type != MessageType.observation:
            return None
        if messageHeader.sub_type != MessageSubtype.asr and messageHeader.sub_type != MessageSubtype.asr_transcription:
            return None

        # Parse the data
        data = json_message["data"]
        data["alternatives"] = [ ASR_Alternative(alternative["text"], 
                                                 alternative["confidence"])
                                 for alternative in data["alternatives"] ]

        message = ASR_Message(**data)
        message.finalize()

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message


###class ASR_MessageParserIntermediate(ASR_MessageParserBase):
###    """
###    Parser for intermediate ASR messages
###    """
###    topic = "agent/asr/intermediate"
###
###class ASR_MessageParserFinal(ASR_MessageParserBase):
###    """
###    Parser for final ASR messages
###    """
###    topic = "agent/asr/final"
###
