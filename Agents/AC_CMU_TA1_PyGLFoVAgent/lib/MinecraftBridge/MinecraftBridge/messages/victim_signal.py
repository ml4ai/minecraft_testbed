# -*- coding: utf-8 -*-
"""
.. module:: victim_signal
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating VictimSignal Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating VictimSignal messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class VictimSignal(BaseMessage):
    """
    A class encapsulating VictimSignal messages.

    Attributes
    ----------
    participant_id : string
        The ID of the participant that triggered the signal
    playername : string
        The name of the player triggering the signal
    message : string
        The message emitted by the signal device
    location : tuple of integers
        The (x,y,z) location of the signal
    x : integer
        The x locaiton of the entity (alias of `location[0]`)
    y : integer
        The y location of the entity (alias of `location[1]`)
    z : integer
        The z location of the entity (alias of `location[2]`)
    roomname : string
        The room name associated with the signal
    """

    def __init__(self, **kwargs):
        """
        """

        BaseMessage.__init__(self, **kwargs)

        # Get the participant ID and playername.
        self._participant_id = kwargs.get('participant_id',
                               kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        self._playername = kwargs.get('playername', self._participant_id)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["message", "roomname"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._message = kwargs["message"]
        self._roomname = kwargs["roomname"]

        # Try to get the location property:  try `location` furst, followed by 
        # `x`, `y`, and `z`
        location = kwargs.get("location", None)

        if location is None:
            try:
                location = (kwargs['x'], kwargs['y'], kwargs['z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'location') from None

        # Try to coerce location into a tuple of ints
        try:
            self._location = tuple([int(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'location',
                                                    location) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'VictimSignal')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        ID of the participant that generated the signal
    
        Attempting to set `participant_id` raises an `ImmutableAttributeException`.
        """
    
        return self._participant_id
    
    @participant_id.setter
    def participant_id(self, _):
    
        raise ImmutableAttributeException(str(self), "participant_id")
    

    @property
    def playername(self):
        """
        Name of the participant that generated the signal
    
        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """
    
        return self._playername
    
    @playername.setter
    def playername(self, _):
    
        raise ImmutableAttributeException(str(self), "playername")
    

    @property
    def message(self):
        """
        Message emitted by the signaling device
    
        Attempting to set `message` raises an `ImmutableAttributeException`.
        """
    
        return self._message
    
    @message.setter
    def message(self, _):
    
        raise ImmutableAttributeException(str(self), "message")
    

    @property
    def location(self):
        """
        Location (x,y,z) of where the signal was generated
    
        Attempting to set `location` raises an `ImmutableAttributeException`.
        """
    
        return self._location
    
    @location.setter
    def location(self, _):
    
        raise ImmutableAttributeException(str(self), "location")
    

    @property
    def x(self):
        """
        Alias of `location[0]` 
    
        Attempting to set `x` raises an `ImmutableAttributeException`.
        """
    
        return self._location[0]
    
    @x.setter
    def x(self, _):
    
        raise ImmutableAttributeException(str(self), "x")
    

    @property
    def y(self):
        """
        Alias of `location[1]`
    
        Attempting to set `y` raises an `ImmutableAttributeException`.
        """
    
        return self._location[1]
    
    @y.setter
    def y(self, _):
    
        raise ImmutableAttributeException(str(self), "y")
    

    @property
    def z(self):
        """
        Alias of `location[2]`
    
        Attempting to set `z` raises an `ImmutableAttributeException`.
        """
    
        return self._location[2]
    
    @z.setter
    def z(self, _):
    
        raise ImmutableAttributeException(str(self), "z")
    

    @property
    def roomname(self):
        """
        Name of the room associated with the signal
    
        Attempting to set `roomname` raises an `ImmutableAttributeException`.
        """
    
        return self._roomname
    
    @roomname.setter
    def roomname(self, _):
    
        raise ImmutableAttributeException(str(self), "roomname")


    def toDict(self):
        """
        Generates a dictionary representation of the VictimSignal message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimSignal message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["participant_id"] = self.participant_id
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["message"] = self.message
        jsonDict["data"]["x"] = self.x
        jsonDict["data"]["y"] = self.y
        jsonDict["data"]["z"] = self.z
        jsonDict["data"]["roomname"] = self.roomname

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the VictimSignal message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            VictimSignal message.
        """

        return json.dumps(self.toDict())
