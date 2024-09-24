# -*- coding: utf-8 -*-
"""
.. module:: victim_placed
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Victim Placed Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Victim Placed Event messages.
"""

import json
import enum

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class VictimPlaced(BaseMessage):
    """
    A class encapsulating VictimPlaced messages.

    Attributes
    ----------
    location : tuple of ints
        The (x,y,z) location of the victim
    participant_id: string
        Unique identifier of participant who placed the victim (e.g. "P000420")
    playername : string
        Name of the player who placed the victim
    name : string
        Alias of `playername`
    victim_id : int
        Unique identifier of the victim
    type : string
        Type of victim being triaged [REGULAR, CRITICAL]
    color : string
        Color of the victim being triaged [GREEN, YELLOW].  This should be
        considered a (pseudo-)alias of `type`
    victim_x : int
        The x location of the victim, alias of from_location[0]
    victim_y: int
        The y location of the victim, alias of from_location[1]
    victim_z : int
        The z location of the victim, alias of from_location[2]
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        participant_id : string
            ID of the player placing the victim
        playername : string
            Name of the player placing the victim
        location : tuple of ints
        victim_x : int
        victim_y : int
        victim_z : int
            (x,y,z) location of where the victim was placed
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
            self._location = tuple([int(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'location',
                                                    location) from None


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
        String representation of the message
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        Get the unique identifier for the participant who placed the victim.  
        Attempting to set the value of `participant_id` will result in an 
        `ImmutableAttributeException` being raised.
        """        
        return self._participant_id

    @participant_id.setter
    def participant_id(self, name):
        raise ImmutableAttributeException(str(self), "participant_id") from None


    @property
    def playername(self):
        """
        Get the name of the player who placed the victim.  Attempting to set
        the value of `playername` will result in an 
        `ImmutableAttributeException` being raised.
        """        
        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername") from None


    @property
    def name(self):
        """
        Alias for `playername`
        """
        return self._playername

    @name.setter
    def name(self, name):
        raise ImmutableAttributeException(str(self), "name") from None


    @property
    def type(self):
        """
        Get the type of victim placed.  Attempting to set the value of `type`
        will result in an `ImmutableAttributeException` being raised.
        """    
        return self._type

    @type.setter
    def type(self, type):
        raise ImmutableAttributeException(str(self), "type") from None


    @property
    def color(self):
        """
        Psuedo-alias of `type`; REGULAR is replaced with GREEN, CRITICAL is
        replaced with YELLOW.
        """
        return self._color

    @color.setter
    def color(self, color):
        raise ImmutableAttributeException(str(self), "color") from None
        

    @property
    def location(self):
        """
        Get the location of the victim.  Attempting to set the value of
        `location` will result in an `ImmutableAttributeException` being 
        raised.
        """
        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location") from None


    @property
    def victim_x(self):
        """
        Get the x-value of the location of the victim (i.e., `location[0]`).
        Attempting to set the x-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[0]

    @victim_x.setter
    def victim_x(self, x):
        raise ImmutableAttributeException(str(self), "victim_x") from None
    

    @property
    def victim_y(self):
        """
        Get the y-value of the location of the victim (i.e., `location[1]`).
        Attempting to set the y-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[1]

    @victim_y.setter
    def victim_y(self, y):
        raise ImmutableAttributeException(str(self), "victim_y") from None


    @property
    def victim_z(self):
        """
        Get the z-value of the location of the victim (i.e., `location[2]`).
        Attempting to set the z-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[2]

    @victim_z.setter
    def victim_z(self, z):
        raise ImmutableAttributeException(str(self), "victim_z") from None


    @property
    def victim_id(self):
        """
        Get the id of victim placed.  Attempting to set the value of `victim_id`
        will result in an `ImmutableAttributeException` being raised.
        """
        return self._victim_id

    @victim_id.setter
    def victim_id(self, _id):
        raise ImmutableAttributeException(str(self), "victim_id") from None 


    def toJson(self):
        """
        Generates a dictionary representation of the VictimPlaced message.
        VictimPlaced information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimPlaced.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["type"] = self.type
        jsonDict["data"]["victim_x"] = self.victim_x
        jsonDict["data"]["victim_y"] = self.victim_y
        jsonDict["data"]["victim_z"] = self.victim_z
        jsonDict["data"]["victim_id"] = self.victim_id

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the VictimPlaced message.  
        VictimPlaced information is contained in a JSON object under the
        key "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            VictimPlaced message.
        """


        return json.dumps(self.toDict())