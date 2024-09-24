# -*- coding: utf-8 -*-
"""
.. module:: ihmc_ta2_dyad
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating IHMC Dyad measures

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating IHMC Dyad measures.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

from collections import namedtuple


class IHMC_Dyad(BaseMessage):
    """
    A class encapsulating dyad messages.

    Attributes
    ----------
    id : string
        UUID of the event
    event_type : IHMC_Dyad.EventType
        Ofe of the enumerated events ["start","update","end"]
    participants : list of DyadParticipant
        List of participants in the dyad
    in_dyad_probability : float
        Probability that the participants are in a dyad
    duration : double
        Amount of time that the dyad lasted in milliseconds.  Returns `None` if
        the event type is not `end`
    """

    class EventType(enum.Enum):
        """
        Enumeration of possible Dyad event types
        """

        start = "start"
        update = "update"
        end = "end"

    # Definition of lightweight class to store participant information
    DyadParticipant = namedtuple("DyadParticipant", ["participant_id", "callsign", "role"])


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["id", "event_type", "participants", 
                         "in-dyad-probability"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        # Make sure that `participants` are correctly formatted
        for participant in kwargs.get("participants", []):
            for arg_name in ["participant_id", "callsign", "role"]:
                if not arg_name in participant:
                    raise MalformedMessageCreationException(str(self), "participants",
                                                            kwargs["participants"]) from None


        # Populate the fields
        self._id = kwargs["id"]
        self._event_type = IHMC_Dyad.EventType[kwargs["event_type"]]
        self._participants = [ IHMC_Dyad.DyadParticipant(p["participant_id"],
                                                         p["callsign"],
                                                         p["role"]) 
                               for p in kwargs.get("participants", []) ]
        self._in_dyad_probability = kwargs.get("in-dyad-probability", 0.0)
        self._duration = kwargs.get("duration", None)


    @property
    def id(self):
        """

        Attempting to set `id` raises an `ImmutableAttributeException`
        """

        return self._id

    @id.setter
    def id(self, _):

        raise ImmutableAttributeException(self, "id")


    @property
    def event_type(self):
        """

        Attempting to set `event_type` raises an `ImmutableAttributeException`
        """

        return self._event_type

    @event_type.setter
    def event_type(self, _):

        raise ImmutableAttributeException(self, "event_type")


    @property
    def participants(self):
        """

        Attempting to set `participants` raises an `ImmutableAttributeException`
        """

        return self._participants

    @participants.setter
    def participants(self, _):

        raise ImmutableAttributeException(self, "participants")


    @property
    def in_dyad_probability(self):
        """

        Attempting to set `in_dyad_probability` raises an `ImmutableAttributeException`
        """

        return self._in_dyad_probability

    @in_dyad_probability.setter
    def in_dyad_probability(self, _):

        raise ImmutableAttributeException(self, "in_dyad_probability")


    @property
    def duration(self):
        """

        Attempting to set `duration` raises an `ImmutableAttributeException`
        """

        return self._duration

    @duration.setter
    def duration(self, _):

        raise ImmutableAttributeException(self, "duration")


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'IHMC_Dyad')
        """

        return self.__class__.__name__


    def toDict(self):
        """
        Generates a dictionary representation of the Dyad message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Dyad message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the Cognitive Load data
        jsonDict["data"]["id"] = self.id
        jsonDict["data"]["event_type"] = self.event_type.value
        jsonDict["data"]["in-dyad-probability"] = self.in_dyad_probability
        jsonDict["data"]["participants"] = [ { "participant_id": p.participant_id,
                                               "callsign": p.callsign,
                                               "role": p.role }
                                              for p in self.participants ]

        if self.duration is not None:
            jsonDict["data"]["duration"] = self.duration

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the Dyad message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Dyad message.
        """

        return json.dumps(self.toDict())
