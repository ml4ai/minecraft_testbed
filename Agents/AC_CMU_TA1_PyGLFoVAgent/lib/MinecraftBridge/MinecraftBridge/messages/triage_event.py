# -*- coding: utf-8 -*-
"""
.. module:: triage_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Triage Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Triage Event messages.
"""

import enum
import json

from .message_exceptions import (
    MalformedMessageCreationException,
    MissingMessageArgumentException,
    ImmutableAttributeException
)
from .base_message import BaseMessage


class TriageEvent(BaseMessage):
    """
    A class encapsulating TriageEvent messages.

    Note
    ----
    Constructing a Triage message requires passing the following keyword
    arguments:

        `participant_id`
        `color`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    participant_id: string
        Unique identifier of participant performing the triage (e.g. "P000420")
    player_name : string
        Name of the player performing the triage
    playername : string
        Alias of `player_name`
    victim_location : tuple of ints
        Location of the victim being triaged
    victim_x : int
        x location of the victim being triaged (i.e., alias of victim_location[0])
    victim_y : int
        y location of the victim being triaged (i.e., alias of victim_location[1])
    victim_z : int
        z location of the victim being triaged (i.e., alias of victim_location[2])
    triage_state : string
        State of the triage (e.g., IN_PROGRESS)
    color : string
        The color of the victim being triaged
    type : string
        The type of the victim being triaged (pseudo-alias of `color`)
    victim_id : int
        Unique identifier for the victim being triaged
    """

    class TriageState(str, enum.Enum):
        """
        An enumeration of possible triage states
        """

        IN_PROGRESS = "IN_PROGRESS"
        UNSUCCESSFUL = "UNSUCCESSFUL"
        SUCCESSFUL = "SUCCESSFUL"

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        participant_id : string
            ID of the player placing the victim
        playername : string
            Name of the player placing the victim
        victim_location : tuple of ints
        victim_x : int
        victim_y : int
        victim_z : int
            (x,y,z) location of where the victim was placed
        triage_state : string
            State of the triage attempt [IN_PROGRESS, UNSUCCESSFUL, SUCCESSFUL]
        color : string
            Color fo the victim being placed [GREEN, YELLOW].  Will convert
            from `type` if not provided
        type : string
            Type of victim being triaged [REGULAR, CRITICAL].  Will convert 
            from `color` if not provided
        victim_id : int
            ID of the placed victim
        """

        BaseMessage.__init__(self, **kwargs)

        # Get the participant ID and playername.  Note that, depending on the
        # provided keyword arguments, these may be one and the same.
        self._participant_id = kwargs.get('participant_id',
                               kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        self._playername = kwargs.get('playername', self._participant_id)

        # Get the position of the victim: try `location` first, followed by
        # `victim_x`, `victim_y`, and `victim_z`
        location = kwargs.get('location', None)

        if location is None:
            try:
                location = (kwargs['victim_x'], 
                            kwargs['victim_y'], 
                            kwargs['victim_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'location') from None

        # Location needs to be able to be coerced into a tuple of ints. Raise
        # an exception if not possible
        try:
            self._victim_location = tuple([int(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'location',
                                                    location) from None


        try:
            self._triage_state = TriageEvent.TriageState[kwargs['triage_state']]
        except KeyError:
            if not 'triage_state' in kwargs:
                raise MissingMessageArgumentException(str(self),
                                                      'triage_state') from None
            else:
                raise MalformedMessageCreationException(str(self), 'triage_state',
                                                        kwargs['triage_state']) from None

        # At the moment, some messages use "color", while others use "type".
        # Try to check "type" first, and fall back on "color".  If one is not
        # provided, use the other to assign the equivalent value.
        # If neither are present, then raise a MissingMessageArgumentException
        if not "type" in kwargs and not "color" in kwargs:
            raise MissingMessageArgumentException(str(self),
                                                  "type") from None

        self._type = kwargs.get('type', None)
        self._color = kwargs.get('color', None)

        if self._type is None:
            self._type = 'CRITICAL' if self._color == 'YELLOW' else 'REGULAR'
        if self._color is None:
            self._color = 'YELLOW' if self._type == 'CRITICAL' else 'GREEN'

        self._victim_id = kwargs.get("victim_id", -1)


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'TriageEvent')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        Get the unique identifier for the participant who performed the triage.

        Attempting to set `participant_id` raises an `ImmutableAttributeException`.
        """

        return self._participant_id

    @participant_id.setter
    def participant_id(self, name):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def player_name(self):
        """
        Get the name of the player who performed the triage.

        Attempting to set `player_name` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @player_name.setter
    def player_name(self, name):
        raise ImmutableAttributeException(str(self), "player_name")


    @property
    def playername(self):
        """
        Alias of `playername`
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def victim_location(self):
        """
        Get the location of the victim being triaged.

        Attempting to set `victim_location` raises an `ImmutableAttributeException`.
        """

        return self._victim_location

    @victim_location.setter
    def victim_location(self, location):
        raise ImmutableAttributeException(str(self), "victim_location")


    @property
    def victim_x(self):
        """
        Alias of `victim_location[0]`
        """

        return self._victim_location[0]

    @victim_x.setter
    def vicitm_x(self, x):
        raise ImmutableAttributeException(str(self), "victim_x")


    @property
    def victim_y(self):
        """
        Alias of `victim_location[1]`
        """

        return self._victim_location[1]

    @victim_y.setter
    def vicitm_y(self, y):
        raise ImmutableAttributeException(str(self), "victim_y")


    @property
    def victim_z(self):
        """
        Alias of `victim_location[2]`
        """

        return self._victim_location[2]

    @victim_z.setter
    def vicitm_z(self, z):
        raise ImmutableAttributeException(str(self), "victim_z")


    @property
    def triage_state(self):
        """
        Get the state of the triage attemp (e.g., IN_PROGRESS).

        Attempting to set `triage_state` raises an `ImmutableAttributeException`.
        """

        return self._triage_state

    @triage_state.setter
    def triage_state(self, state):
        raise ImmutableAttributeException(str(self), "triage_state")


    @property
    def color(self):
        """
        Get the type / color of the victim being triaged.

        Attempting to set `color` raises an `ImmutableAttributeException`.
        """

        return self._color

    @color.setter
    def color(self, color):
        raise ImmutableAttributeException(str(self), "color")


    @property
    def type(self):
        """
        Alias of `color`.
        """

        return self._type

    @type.setter
    def type(self, _type):
        raise ImmutableAttributeException(str(self), "type")


    @property
    def victim_id(self):
        """
        Get the victim's unique ID.

        Attempting to set `victim_id` raises an `ImmutableAttributeException`.
        """

        return self._victim_id

    @victim_id.setter
    def victim_id(self, _id):
        raise ImmutableAttributeException(str(self), "victim_id")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the TriageEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["victim_x"] = self.victim_x
        jsonDict["data"]["victim_y"] = self.victim_y
        jsonDict["data"]["victim_z"] = self.victim_z
        jsonDict["data"]["type"] = self.type
        jsonDict["data"]["triage_state"] = self.triage_state.value
        jsonDict["data"]["victim_id"] = self.victim_id          

        return jsonDict        


    def toJson(self):
        """
        Generates a JSON representation of the message.  Message information is
        contained in a JSON object under the key "data".  Additional named
        headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            TriageEvent message.
        """

        return json.dumps(self.toDict())
