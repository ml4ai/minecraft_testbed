# -*- coding: utf-8 -*-
"""
.. module:: rubble_destroyed
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Rubble Destroyed Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Rubble Destroyed Event messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class RubbleDestroyedEvent(BaseMessage):
    """
    A class encapsulating Rubble Destroyed Event messages.

    Note
    ----
    Constructing a RubbleDestroyedEvent message requires passing the following 
    keyword arguments:

        `location`

    While aliases exist for this attribute, they are currently not accepted as
    constructor parameters.

    Attributes
    ----------
    participant_id: string
        Unique identifier of participant that destroyed the rubble (e.g. "P000420")
    playername : string
        The name of the player that destroyed the rubble
    name : string
        Alias of `playername`
    location : tuple of ints
        The (x,y,z) location of the rubble
    rubble_x : int
        The x location of the rubble, alias of location[0]
    rubble_y: int
        The y location of the rubble, alias of location[1]
    rubble_z : int
        The z location of the rubble, alias of location[2]
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        participant_id : string
            Unique identifier of the participant; uses playername if not given
        playername : string
            Name of the player; uses participant_id if not supplied
        location : tuple of ints
        rubble_x : int
        rubble_y : int
        rubble_z : int
            The (x,y,z) location of the rubble
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


        # Get the location of the entity: try `location` first, followed by
        # `rubble_x`, `rubble_y`, `rubble_z`
        location = kwargs.get('location', None)

        if location is None:
            try:
                location = (kwargs['rubble_x'], 
                            kwargs['rubble_y'], 
                            kwargs['rubble_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'location') from None        

        # Location needs to be able to be coerced into a tuple of ints.  Raise 
        # an exception if not possible
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
            Class name of the message (i.e., 'RubbleDestroyedEvent')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        Get the unique identifier of the participant who destroyed the rubble.  
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
        Get the name of the player who destroyed the rubble.  Attempting to set
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
    def location(self):
        """
        Get the location of the rubble.  Attempting to set the value of
        `location` will result in an `ImmutableAttributeException` being 
        raised.
        """
        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location") from None


    @property
    def rubble_x(self):
        """
        Get the x-value of the location of the rubble (i.e., `location[0]`).
        Attempting to set the x-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[0]

    @rubble_x.setter
    def rubble_x(self, x):
        raise ImmutableAttributeException(str(self), "rubble_x") from None
    

    @property
    def rubble_y(self):
        """
        Get the y-value of the location of the rubble (i.e., `location[1]`).
        Attempting to set the y-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[1]

    @rubble_y.setter
    def rubble_y(self, y):
        raise ImmutableAttributeException(str(self), "rubble_y") from None


    @property
    def rubble_z(self):
        """
        Get the z-value of the location of the rubble (i.e., `location[2]`).
        Attempting to set the z-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[2]

    @rubble_z.setter
    def rubble_z(self, z):
        raise ImmutableAttributeException(str(self), "rubble_z") from None


    def toDict(self):
        """
        Generates a dictionary representation of the RubbleDestroyedEvent message.
        RubbleDestroyed information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the RubbleDestroyedEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["rubble_x"] = self.rubble_x
        jsonDict["data"]["rubble_y"] = self.rubble_y
        jsonDict["data"]["rubble_z"] = self.rubble_z

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the RubbleDestroyedEvent message.  
        RubbleDestoryedEvent information is contained in a JSON object under the
        key "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            RubbleDestroyedEvent message.
        """

        return json.dumps(self.toDict())
