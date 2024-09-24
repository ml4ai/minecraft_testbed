# -*- coding: utf-8 -*-
"""
.. module:: victim_evacuated
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating VictimEvacuated Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating VictimEvacuated messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class VictimEvacuated(BaseMessage):
    """
    A class encapsulating VictimEvacuated messages.

    Attributes
    ----------
    participant_id : string
        The id of the player being reported
    playername : string
        The name of the player
    victim_location : tuple of integers
        Location of the victim
    victim_x : integer
        Alias of `victim_location[0]`
    victim_y : integer
        Alias of `victim_location[1]`
    victim_z : integer
        Alias of `victim_location[2]`
    type : string
        Type of victim being evacuated
    victim_id : unique id identifying the victim
        Unique ID identifying the victim
    success : boolean
        whether or not the victim was evacuated to the area corresponding with
        its letter identifier (a,b,c)
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["type", "victim_id", "success"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._type = kwargs["type"]
        self._victim_id = kwargs["victim_id"]
        self._success = kwargs["success"]

        # Get the participant ID and playername.
        self._participant_id = kwargs.get('participant_id',
                               kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        self._playername = kwargs.get('playername', self._participant_id)

        # Try to get the victim_location property:  try `victim_location` first,
        # followed by `victim_x`, `victim_y`, and `victim_z`
        location = kwargs.get("victim_location", None)

        if location is None:
            try:
                location = (kwargs['victim_x'], 
                            kwargs['victim_y'], 
                            kwargs['victim_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'victim_location') from None

        # Try to coerce location into a tuple of ints
        try:
            self._victim_location = tuple([int(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'victim_location',
                                                    location) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentFeedback')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """


        Attempting to set `participant_id` raises an `ImmutableAttrubteException`
        """

        return self._participant_id

    @participant_id.setter
    def participant_id(self, _):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def playername(self):
        """


        Attempting to set `playername` raises an `ImmutableAttrubteException`
        """

        return self._playername

    @playername.setter
    def playername(self, _):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def victim_location(self):
        """


        Attempting to set `victim_location` raises an `ImmutableAttrubteException`
        """

        return self._victim_location

    @victim_location.setter
    def victim_location(self, _):
        raise ImmutableAttributeException(str(self), "victim_location")


    @property
    def victim_x(self):
        """


        Attempting to set `victim_x` raises an `ImmutableAttrubteException`
        """

        return self._victim_location[0]

    @victim_x.setter
    def victim_x(self, _):
        raise ImmutableAttributeException(str(self), "victim_x")


    @property
    def victim_y(self):
        """


        Attempting to set `victim_y` raises an `ImmutableAttrubteException`
        """

        return self._victim_location[1]

    @victim_y.setter
    def victim_y(self, _):
        raise ImmutableAttributeException(str(self), "victim_y")


    @property
    def victim_z(self):
        """


        Attempting to set `victim_z` raises an `ImmutableAttrubteException`
        """

        return self._victim_location[2]

    @victim_z.setter
    def victim_z(self, _):
        raise ImmutableAttributeException(str(self), "victim_z")


    @property
    def type(self):
        """


        Attempting to set `type` raises an `ImmutableAttrubteException`
        """

        return self._type

    @type.setter
    def type(self, _):
        raise ImmutableAttributeException(str(self), "type")


    @property
    def victim_id(self):
        """


        Attempting to set `victim_id` raises an `ImmutableAttrubteException`
        """

        return self._victim_id

    @victim_id.setter
    def victim_id(self, _):
        raise ImmutableAttributeException(str(self), "victim_id")


    @property
    def success(self):
        """


        Attempting to set `success` raises an `ImmutableAttrubteException`
        """

        return self._success

    @success.setter
    def success(self, _):
        raise ImmutableAttributeException(str(self), "success")


    def toDict(self):
        """
        Generates a dictionary representation of the VictimEvacuated message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimEvacuated message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the event data
        jsonDict["data"]["participant_id"] = self._participant_id
        jsonDict["data"]["playername"] = self._playername
        jsonDict["data"]["victim_x"] = self._victim_x
        jsonDict["data"]["victim_y"] = self._victim_y
        jsonDict["data"]["victim_z"] = self._victim_z
        jsonDict["data"]["type"] = self._type
        jsonDict["data"]["victim_id"] = self._victim_id
        jsonDict["data"]["success"] = self._success

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the VictimEvacuated message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            ##### message.
        """

        return json.dumps(self.toDict())
