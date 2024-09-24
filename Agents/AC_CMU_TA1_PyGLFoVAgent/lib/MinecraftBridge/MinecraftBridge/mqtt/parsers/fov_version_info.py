# -*- coding: utf-8 -*-
"""
.. module:: fov_version_info.py
   :platform: Linux, Windows, OSX
   :synopsis: Parser for FoV Summary messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for FoV Version Information messages
"""


from ...messages import FoV_VersionInfo, FoV_Dependency
from .message_types import MessageType, MessageSubtype
from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException

class FoV_VersionInfoParser:
    """
    A class for parsing FoV version information messages from the MQTT bus

    MQTT Message Fields
    -------------------
    version : string
        Version string of the PyGLFoVAgent
    url : string
        URL to tag / release of repo of PyGLFoVAgent
    dependencies : list
        List of Version Info Dependency Objects
    """

    topic = "agent/versioninfo/pygl_fov"
    MessageClass = FoV_VersionInfo

    msg_type = MessageType.agent
    msg_subtype = MessageSubtype.FoV_VersionInfo
    alternatives = []


    @staticmethod
    def parse(json_message):
        """
        Convert the json message to an instance of FoV_VersionInfo.

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
        if messageHeader.sub_type != MessageSubtype.FoV_VersionInfo:
            return None

        # Parse the data
        data = json_message["data"]

        message = FoV_VersionInfo(version=data["version"],
                                  url=data["url"])

        for dependency in data["dependencies"]:
            message.addDependency(FoV_Dependency(package=dependency["package"],
                                                 version=dependency["version"],
                                                 url=dependency["url"]))

        message.addHeader("header", busHeader)
        message.addHeader("msg", messageHeader)

        return message