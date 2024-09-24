# -*- coding: utf-8 -*-
"""
.. module:: victim_no_longer_safe
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Victim No Longer Safe events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Victim No Longer Safe messages.
"""

import json
import enum

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class VictimNoLongerSafe(BaseMessage):
    """
    A class encapsulating VictimNoLongerSafe messages.

    Note
    ----
    Constructing a VictimPickedUp message requires passing the following 
    keyword arguments:

        `location`

    While aliases exist for these attributes, they are currently not accepted as
    constructor parameters.

    Attributes
    ----------
    location : tuple of ints
        The (x,y,z) location of the victim
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
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'VictimNoLongerSafe')
        """

        return self.__class__.__name__


    @property
    def type(self):
        """
        Get the type of victim.  Attempting to set the value of `type` will
        result in an `ImmutableAttributeException` being raised.
        """    
        return self._type

    @type.setter
    def type(self, type):
        raise ImmutableAttributeException(str(self), "type") from None


    @property
    def color(self):
        """
        Alias of `type`
        """
        return self._type

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



    def toDict(self):
        """
        Generates a dictionary representation of the VictimNoLongerSafe message.
        Message information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimNoLongerSafe message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["color"] = self.color
        jsonDict["data"]["victim_x"] = self.victim_x
        jsonDict["data"]["victim_y"] = self.victim_y
        jsonDict["data"]["victim_z"] = self.victim_z

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the VictimNoLongerSafe message.  
        VictimNoLongerSafe information is contained in a JSON object under the
        key "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            VictimNoLongerSafe message.
        """

        return json.dumps(self.toDict())