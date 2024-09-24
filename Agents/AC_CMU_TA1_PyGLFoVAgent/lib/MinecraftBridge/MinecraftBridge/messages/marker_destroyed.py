# -*- coding: utf-8 -*-
"""
.. module:: marker_destroyed_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Marker Destroyed Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Marker Destroyed Event messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

import MinecraftElements


class MarkerDestroyedEvent(BaseMessage):
    """
    A class encapsulating Marker Destroyed Event messages.

    Note
    ----
    Constructing a MarkerDestroyedEvent message requires passing the following 
    keyword arguments:

        `location`

    While aliases exist for this attribute, they are currently not accepted as
    constructor parameters.

    Attributes
    ----------
    type : string
        The type of marker placed
    marker_type : string
        Alias of `type`
    location : tuple of ints
        The (x,y,z) location of the marker
    marker_x : int
        The x location of the marker, alias of location[0]
    marker_y: int
        The y location of the marker, alias of location[1]
    marker_z : int
        The z location of the marker, alias of location[2]
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        type : string
        marker_type : string
            The type of marker block destroyed
        location : tuple of ints
        marker_x : int
        marker_y : int
        marker_z : int
            The (x,y,z) location of the marker
        """

        BaseMessage.__init__(self, **kwargs)


        # Get the location of the entity: try `location` first, followed by
        # `marker_x`, `marker_y`, `marker_z`
        location = kwargs.get('location', None)

        if location is None:
            try:
                location = (kwargs['marker_x'], 
                            kwargs['marker_y'], 
                            kwargs['marker_z'])
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

        self._marker_type = kwargs.get('type',
                            kwargs.get('marker_type', None))
        if self._marker_type is None:
            raise MissingMessageArgumentException(str(self),
                                                  'type') from None

        # Marker type needs to be coerced to a MinecraftElements.MarkerBlock
        # instance.  Set to "UNKNOWN" if it's not a valid block
        try:
            self._marker_type = MinecraftElements.MarkerBlock[self._marker_type.replace(' ','')]
        except KeyError:
            self.logger.warning("%s: Trying to parse unknown block type %s", self, self._marker_type)
            self._marker_type = MinecraftElements.MarkerBlock["UNKNOWN"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'MarkerDestoyedEvent')
        """

        return self.__class__.__name__
        

    @property
    def marker_type(self):
        """
        Get the type of marker destroyed.  Attempting to set the value of 
        `marker_type` will result in an `ImmutableAttributeException` being 
        raised.
        """    
        return self._marker_type

    @marker_type.setter
    def marker_type(self, type):
        raise ImmutableAttributeException(str(self), "marker_type") from None


    @property
    def type(self):
        """
        Alias of `marker_type`
        """
        return self._marker_type

    @type.setter
    def type(self, type):
        raise ImmutableAttributeException(str(self), "type") from None
        

    @property
    def location(self):
        """
        Get the location of the marker.  Attempting to set the value of
        `location` will result in an `ImmutableAttributeException` being 
        raised.
        """
        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location") from None


    @property
    def marker_x(self):
        """
        Get the x-value of the location of the marker (i.e., `location[0]`).
        Attempting to set the x-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[0]

    @marker_x.setter
    def marker_x(self, x):
        raise ImmutableAttributeException(str(self), "marker_x") from None
    

    @property
    def marker_y(self):
        """
        Get the y-value of the location of the marker (i.e., `location[1]`).
        Attempting to set the y-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[1]

    @marker_y.setter
    def marker_y(self, y):
        raise ImmutableAttributeException(str(self), "marker_y") from None


    @property
    def marker_z(self):
        """
        Get the z-value of the location of the marker (i.e., `location[2]`).
        Attempting to set the z-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[2]

    @marker_z.setter
    def marker_z(self, z):
        raise ImmutableAttributeException(str(self), "marker_z") from None


    def toDict(self):
        """
        Generates a dictionary representation of the MarkerDestroyedEvent message.
        MarkerDestroyed information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the MarkerDestroyedEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the marker destroyed event data
        jsonDict["data"]["type"] = self.type
        jsonDict["data"]["marker_x"] = self.marker_x
        jsonDict["data"]["marker_y"] = self.marker_y
        jsonDict["data"]["marker_z"] = self.marker_z

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the MarkerDestroyedEvent message.  
        MarkerDestroyedEvent information is contained in a JSON object under the
        key "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            MarkerDestroyededEvent message.
        """

        return json.dumps(self.toDict())
