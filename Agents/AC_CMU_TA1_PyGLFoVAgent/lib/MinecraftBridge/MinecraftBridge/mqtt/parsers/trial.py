# -*- coding: utf-8 -*-
"""
.. module:: trial
   :platform: Linux, Windows, OSX
   :synopsis: Parser for trial messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for trial messages
"""

from ...messages import Trial, ClientInfo
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

class TrialParser:
    """
    A class for parsing trial messages from MQTT bus.

    MQTT Message Fields
    -------------------

    """

    topic = "trial"
    MessageClass = Trial

    msg_type = MessageType.trial
    msg_subtype = MessageSubtype.start
    alternatives = [MessageSubtype.stop]


    @staticmethod
    def parse(json_message):
        """
        Convert the a JSON message to an instance of Trial.

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
        if busHeader.message_type != MessageType.trial:
            return None
        if messageHeader.sub_type not in [MessageSubtype.start, MessageSubtype.stop]:
            return None

        # Parse the data
        data = json_message["data"]

        client_info = [ClientInfo(**info) for info in data["client_info"]]

        message = Trial( state=Trial.TrialState[messageHeader.sub_type.name.lower()],
                         name=data["name"],
                         date=data["date"],
                         experimenter=data["experimenter"],
                         subjects=data["subjects"],
                         trial_number=data["trial_number"],
                         group_number=data["group_number"],
                         study_number=data["study_number"],
                         condition=data["condition"],
                         notes=data["notes"],
                         testbed_version=data["testbed_version"],
                         experiment_name=data["experiment_name"],
                         experiment_date=data["experiment_date"],
                         experiment_author=data["experiment_author"],
                         experiment_mission=data["experiment_mission"],
                         map_name=data["map_name"],
                         map_block_filename=data["map_block_filename"],
                         client_info=client_info
                       )

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message