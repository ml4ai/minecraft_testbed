# -*- coding: utf-8 -*-
"""
.. module:: bus_header
   :platform: Linux, Windows, OSX
   :synopsis: Parser for bus headers for the MQTT bus

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of parers for MQTT bus headers
"""

import ciso8601

from ...messages import TESTBED_VERSION
from ...messages import BusHeader
from .message_types import MessageType


class BusHeaderParser:
    """
    A class for parsing an MQTT message bus header.

    MQTT Bus Header Fields
    ----------------------
    timestamp : string
        Timestamp of the message publication (ISO8601 format)
    message_type : string
        One of the defined message types
    version : string
        The version of the message type object
    """

    @staticmethod
    def parse(json_header):
        """
        Convert the header information to an instance of BusHeader

        Arguments
        ---------
        json_header : dictionary
            Dictionary representation of the message header recieved ffrom the MQTT bus
        """

        # Convert the topic to the enumerated value
        message_type = MessageType[json_header["message_type"]]

        # Convert the version to a float
        try:
            version = float(json_header["version"])
        except:
            version = 0.0

        # Convert timestamp to ISO8601
        # NOTE: Timezone information will be incorporated into the parsed
        #       timestamp if the 'Z' character is present at the end of the
        #       string; when converting back to an ISO8601 string, timezone
        #       will be rewritten as "+00:00", as opposed to "Z".  So, we drop
        #       the "Z" and will re-add if parsed back into JSON
        timestamp = ciso8601.parse_datetime(json_header["timestamp"][:-1])

        # Create and return an instance of the header
        return BusHeader(message_type, timestamp, version)
