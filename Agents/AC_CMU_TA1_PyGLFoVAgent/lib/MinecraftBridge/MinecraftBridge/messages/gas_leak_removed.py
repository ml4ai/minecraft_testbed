# -*- coding: utf-8 -*-
"""
.. module:: gas_leak_removed
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Gas Leak Removed Events.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Gas Leak Removed messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class GasLeakRemovedEvent(BaseMessage):
    """
    A class encapsulating Gas Leak Removed Event messages.

    Note
    ----
    Constructing a GasLeakRemovedEvent message requires passing the following 
    keyword arguments:

        `source`
        `location`

    While aliases exist for the `location` attribute, they are currently not
    accepted as constructor parameters.

    Attributes
    ----------
    source : string
        The name of the entity (playername / "system") that removed the gasleak
    location : tuple of ints
        The (x,y,z) location of the gas leak
    gasleak_x : int
        The x location of the gas leak, alias of location[0]
    gasleak_y : int
        The y location of the gas leak, alias of location[1]
    gasleak_z : int
        The z location of the gas leak, alias of location[2]
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        source : string
            The name of the entity that removed the gas leak
        location : tuple of ints
        gasleak_x : int
        gasleak_y : int
        gasleak_z : int
            The (x,y,z) location of the gas leak
        """        

        BaseMessage.__init__(self, **kwargs)

        # Get the location of the entity: try `location` first, followed by
        # `gasleak_x`, `gasleak_y`, `gasleak_z`
        location = kwargs.get('location', None)

        if location is None:
            try:
                location = (kwargs['gasleak_x'], 
                            kwargs['gasleak_y'], 
                            kwargs['gasleak_z'])
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

        try:
            self._source = kwargs["source"]
        except:
            raise MissingMessageArgumentException(str(self),
                                                  'source') from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'GasLeakRemovedEvent')
        """

        return self.__class__.__name__


    @property
    def location(self):
        """
        Get the location of the gas leak.  Attempting to set the value of
        `location` will result in an `ImmutableAttributeException` being 
        raised.
        """

        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location") from None


    @property
    def source(self):
        """
        Get the name of the entity (playername or "system") that removed the
        gasleak.  Attempting to set the value of `source` will result in an
        `ImmutableAttributeException` being raised.
        """
        return self._source

    @source.setter
    def source(self, source):
        raise ImmutableAttributeException(str(self), "source") from None
    

    @property
    def gasleak_x(self):
        """
        Get the x-value of the location of the gas leak (i.e., `location[0]`).
        Attempting to set the x-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[0]

    @gasleak_x.setter
    def gasleak_x(self, x):
        raise ImmutableAttributeException(str(self), "gasleak_x") from None
    

    @property
    def gasleak_y(self):
        """
        Get the y-value of the location of the gas leak (i.e., `location[1]`).
        Attempting to set the y-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[1]

    @gasleak_y.setter
    def gasleak_y(self, y):
        raise ImmutableAttributeException(str(self), "gasleak_y") from None


    @property
    def gasleak_z(self):
        """
        Get the z-value of the location of the gasleak (i.e., `location[2]`).
        Attempting to set the z-value of the location will result in an 
        `ImmutableAttributeException` being raised.
        """

        return self._location[2]

    @gasleak_z.setter
    def gasleak_z(self, z):
        raise ImmutableAttributeException(str(self), "gasleak_z") from None


    def toDict(self):
        """
        Convert the BeepEvent to a Python dictionary whose key / value pairs
        match those of the testbed message format
        """

        jsonDict = BaseMessage.toDict(self)

        # Add the beep event data
        jsonDict['data'] = { 'mission_timer': getMissionTimerString(self.missionTimer),
                             'source':        self.source,
                             'gasleak_x':     self.location[0],
                             'gasleak_y':     self.location[1],
                             'gasleak_z':     self.location[2]
                           }

        return jsonDict


    def toJson(self):
        """
        Convert the BeepEvent to a JSON message
        """

        return json.dumps(self.toDict())
