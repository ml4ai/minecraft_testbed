# -*- coding: utf-8 -*-
"""
.. module:: .py
   :platform: Linux, Windows, OSX
   :synopsis: Parser for  messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a parser for  messages
"""

import ciso8601

from ...messages import TESTBED_VERSION
from ...messages import MessageHeader
from .message_types import MessageSubtype

class MessageHeaderParser:
    """
    A lightweight wrapper of a message header.  Message headers contain common
    information about the generation of the message:

    timestamp            - Timestamp of the creation of the data (ISO8601)
    experiment_id        - String identifier of an experiment
    trial_id             - String identifier of an experiment trial
    replay_id (optional) - UUID of a replay of original trial, if replayed
    source               - name of testbed component that generated the data
    sub_type             - Subtype of the data
    version              - Version of the subtype

    See the message specifications in the testbed

    TODO:  Implement message validation
    """

    @staticmethod
    def parse(json_message):
        """
        Create an instance of this class by parsing the provided JSON data.

        Args:
            json_message - a JSON representation of a message.  It is assumed
                           to have been validated.
        """

        # Convert the subtype to the enumerated value.  Note that the 
        # enumerated values use '_' in place of ':'
        sub_type = MessageSubtype[json_message["sub_type"].replace(':','_')]

        # String elements requiring no conversion
        experiment_id = json_message.get("experiment_id", "<NOT_PROVIDED>")
        trial_id = json_message.get("trial_id", "<NOT_PROVIDED>")
        replay_id = json_message.get("replay_id", None)
        source = json_message.get("source", "<NOT_PROVIDED>")

        # Convert the version to a float
        try:
            version = float(json_message["version"])
        except:
            version = 0.0

        # Convert timestamp to ISO8601
        # NOTE: Timezone information will be incorporated into the parsed
        #       timestamp if the 'Z' character is present at the end of the
        #       string; when converting back to an ISO8601 string, timezone
        #       will be rewritten as "+00:00", as opposed to "Z".  So, we drop
        #       the "Z" and will re-add if parsed back into JSON
        timestamp = ciso8601.parse_datetime(json_message["timestamp"][:-1])

        # Create and return an instance of the header
        return MessageHeader(sub_type, experiment_id, trial_id, source, timestamp, version, replay_id)


