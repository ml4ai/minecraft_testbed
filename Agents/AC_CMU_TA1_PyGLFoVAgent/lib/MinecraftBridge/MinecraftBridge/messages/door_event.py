# -*- coding: utf-8 -*-
"""
.. module:: door_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Door Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Door Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class DoorEvent(BaseMessage):
    """
    A class encapsulating Door Event messages.

    Attributes
    ----------
    participant_id: string
        Unique identifier of participant (e.g. "P000420")
    playername : string
        The name of the player that opened / closed the door.  If not supplied,
        then used as an alias for participant_id
    position : tuple of ints
        Location of the door
    location : tuple of ints
        Location of the door; alias for `position`
    opened : boolean
        True if the door was opened, False otherwise
    open : boolean
        True if the door was opened, False if closed; alias for `opened`
    door_x : int
        The x location of the opened / closed door, alias of position[0]
    door_y: int
        The y location of the opened / closed door, alias of position[1]
    door_z: int
        The z location of the opened / closed door, alias of position[2]
    """


    def __init__(self, **kwargs):
        """
        DoorEvent messages are constructed from the listed keyword arguments.
        Multiple keywords can be used to define the message attributes; 
        keywords are listed in the order that they are checked

        Keyword Arguments
        -----------------
        participant_id : string
        playername : string
            Unique identifier of the participant
        playername : string, optional
            Name of the player.  If not supplied, uses `participant_id`
        position : tuple of ints
        location : tuple of ints
        door_x : int
        door_y : int
        door_z : int
            Location (x,y,z) of the door.  If `position` and `location` are not
            provided, uses (`door_x`, `door_y`, `door_z`)
        opened : boolean
        open : boolean
            True if the door was opened, False otherwise
        """
        

        BaseMessage.__init__(self, **kwargs)

        # Try to get the participant_id first, and fall back on the playername
        # if it's not present.  If neither are present, throw an exception
        self._participant_id = kwargs.get('participant_id', 
                                          kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        # If present in the keyword arguments, set the playername; otherwise, 
        # use participaint_id
        self._playername = kwargs.get('playername', self._participant_id)

        # Get the opened property; try `opened` first, then `open`
        self._opened = kwargs.get('opened', kwargs.get('open', None))
        if self._opened is None:
            raise MissingMessageArgumentException(str(self), 
                                                  'opened') from None
        self._opened = bool(self._opened)

        # Get the location of the door: try `position` first, followed by
        # `location` and finally `door_x`, `door_y`, `door_z`
        position = kwargs.get('position', kwargs.get('location', None))

        if position is None:
            try:
                position = (kwargs['door_x'], kwargs['door_y'], kwargs['door_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'position') from None


        # Position needs to be able to be coerced into a tuple of ints.  Raise
        # an exception if not possible
        try:
            self._position = tuple([int(x) for x in position][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'position', 
                                                    position) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'DoorEvent')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        Get the unique identifier of the player that opened or closed the door.  
        Attempting to set the value of the `participant_id` will result in an 
        `ImmutableAttributeException` being raised.        
        """        
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        raise ImmutableAttributeException(str(self), "participant_id") from None


    @property
    def playername(self):
        """
        Get the name of the player that opened or closed the door.  Attempting
        to set the value of the `playername` will result in an 
        `ImmutableAttributeException` being raised.        
        """        
        return self._playername

    @playername.setter
    def playername(self, playername):
        raise ImmutableAttributeException(str(self), "playername") from None


    @property
    def position(self):
        """
        Get the location of the door opened or closed the door.  Attempting
        to set the value of the `position` will result in an 
        `ImmutableAttributeException` being raised.        
        """                
        return self._position


    @position.setter
    def position(self, position):
        raise ImmutableAttributeException(str(self), "position") from None


    @property
    def location(self):
        """
        Alias for `position`.
        """
        return self._position

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location") from None


    @property
    def opened(self):
        """
        Get whether the door was opened or closed.  Attempting to set the value
        of the `playername` will result in an `ImmutableAttributeException` 
        being raised.

        Returns
        -------
            True if the door was opened, False if the door was closed
        """                
        return self._opened

    @opened.setter
    def opened(self, opened):
        raise ImmutableAttributeException(str(self), "opened") from None


    @property
    def open(self):
        """
        Alias for `opened`.
        """
        return self._opened

    @open.setter
    def open(self, opened):
        raise ImmutableAttributeException(str(self), "open") from None


    @property
    def door_x(self):
        """
        Get the x-value of the location of the door (i.e., `position[0]`).
        Attempting to set the x-value of the location will result in an
         `ImmutableAttributeException` being raised.
        """
        return self._position[0]

    @door_x.setter
    def door_x(self, x):
        raise ImmutableAttributeException(str(self), "door_x") from None


    @property
    def door_y(self):
        """
        Get the y-value of the location of the door (i.e., `position[1]`).
        Attempting to set the y-value of the location will result in an
         `ImmutableAttributeException` being raised.
        """
        return self._position[1]

    @door_y.setter
    def door_y(self, y):
        raise ImmutableAttributeException(str(self), "door_y") from None


    @property
    def door_z(self):
        """
        Get the z-value of the location of the door (i.e., `position[2]`).
        Attempting to set the z-value of the location will result in an
         `ImmutableAttributeException` being raised.        
        """
        return self._position[2]

    @door_z.setter
    def door_z(self, z):
        raise ImmutableAttributeException(str(self), "door_z") from None
    

    def toDict(self):
        """
        Generates a dictionary representation of the DoorEvent message.  
        DoorEvent information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the DoorEvent.
        """

        jsonDict = BaseMessage.toDict(self)
    
        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        jsonDict['data']['participant_id'] = self.participant_id,
        jsonDict['data']['playername'] = self.playername,
        jsonDict['data']['door_x'] = self.door_x,
        jsonDict['data']['door_y'] = self.door_y,
        jsonDict['data']['door_z'] = self.door_z,
        jsonDict['data']['opened'] = self.opened

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the DoorEvent message.  DoorEvent
        information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            DoorEvent message.
        """

        return json.dumps(self.toDict())
