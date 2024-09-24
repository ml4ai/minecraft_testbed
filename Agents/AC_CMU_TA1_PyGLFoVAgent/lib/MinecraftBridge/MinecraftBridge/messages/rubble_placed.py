# -*- coding: utf-8 -*-
"""
.. module:: rubble_placed
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Rubble Placed Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Rubble Placed Event messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class RubblePlacedEvent(BaseMessage):
    """
    A class encapsulating Rubble Placed Event messages.

    Attributes
    ----------
    from_location : tuple of ints
        The original (x,y,z) location of the rubble
    to_location : tuple of ints
        The new (x,y,z) location of the rubble
    from_x : int
        The original x location of the rubble, alias of from_location[0]
    from_y: int
        The original y location of the rubble, alias of from_location[1]
    from_z : int
        The original z location of the rubble, alias of from_location[2]
    to_x : int
        The new x location of the rubble, alias of to_location[0]
    to_y: int
        The new y location of the rubble, alias of to_location[1]
    to_z : int
        The new z location of the rubble, alias of to_location[2]        
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        from_location : tuple of ints
        from_x : int
        from_y : int
        from_z : int
            Location the rubble came from
        to_location : tuple of ints
        to_x : int
        to_y : int
        to_z : int
            Location the rubble was moved to
        """

        BaseMessage.__init__(self, **kwargs)


        # Get the location where the rubble came from: try `from_location` 
        # first, followed by `from_x`, `from_y`, `from_z`
        from_location = kwargs.get('from_location', None)

        if from_location is None:
            try:
                from_location = (kwargs['from_x'], 
                                 kwargs['from_y'], 
                                 kwargs['from_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'from_location') from None        

        # Location needs to be able to be coerced into a tuple of ints.  Raise 
        # an exception if not possible
        try:
            self._from_location = tuple([int(x) for x in from_location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'from_location',
                                                    from_location) from None


        # Get the location where the rubble is placed: try `to_location` 
        # first, followed by `to_x`, `to_y`, `to_z`
        to_location = kwargs.get('to_location', None)

        if to_location is None:
            try:
                to_location = (kwargs['to_x'], 
                               kwargs['to_y'], 
                               kwargs['to_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'to_location') from None

        # Location needs to be able to be coerced into a tuple of ints.  Raise 
        # an exception if not possible
        try:
            self._to_location = tuple([int(x) for x in to_location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'to_location',
                                                    to_location) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'RubblePlacedEvent')
        """

        return self.__class__.__name__


    @property
    def from_location(self):
        """
        Get the original location of the rubble.  Attempting to set the value of
        `from_location` will result in an `ImmutableAttributeException` being 
        raised.
        """
        return self._from_location

    @from_location.setter
    def from_location(self, location):
        raise ImmutableAttributeException(str(self), "from_location") from None


    @property
    def from_x(self):
        """
        Get the x-value of the original location of the rubble (i.e., 
        `from_location[0]`).  Attempting to set the x-value of the location 
        will result in an `ImmutableAttributeException` being raised.
        """

        return self._from_location[0]

    @from_x.setter
    def from_x(self, x):
        raise ImmutableAttributeException(str(self), "from_x") from None
    

    @property
    def from_y(self):
        """
        Get the y-value of the original location of the rubble (i.e., 
        `from_location[1]`).  Attempting to set the y-value of the location 
        will result in an `ImmutableAttributeException` being raised.
        """

        return self._from_location[1]

    @from_y.setter
    def from_y(self, y):
        raise ImmutableAttributeException(str(self), "from_y") from None


    @property
    def from_z(self):
        """
        Get the z-value of the original location of the rubble (i.e., 
        `from_location[2]`). Attempting to set the z-value of the location will
        result in an `ImmutableAttributeException` being raised.
        """

        return self._from_location[2]

    @from_z.setter
    def from_z(self, z):
        raise ImmutableAttributeException(str(self), "from_z") from None


    @property
    def to_location(self):
        """
        Get the new location of the rubble.  Attempting to set the value of
        `to_location` will result in an `ImmutableAttributeException` being 
        raised.
        """
        return self._to_location

    @to_location.setter
    def to_location(self, location):
        raise ImmutableAttributeException(str(self), "to_location") from None


    @property
    def to_x(self):
        """
        Get the x-value of the new location of the rubble (i.e., 
        `to_location[0]`).  Attempting to set the x-value of the location 
        will result in an `ImmutableAttributeException` being raised.
        """

        return self._to_location[0]

    @to_x.setter
    def to_x(self, x):
        raise ImmutableAttributeException(str(self), "to_x") from None
    

    @property
    def to_y(self):
        """
        Get the y-value of the new location of the rubble (i.e., 
        `to_location[1]`).  Attempting to set the y-value of the location 
        will result in an `ImmutableAttributeException` being raised.
        """

        return self._to_location[1]

    @to_y.setter
    def to_y(self, y):
        raise ImmutableAttributeException(str(self), "to_y") from None


    @property
    def to_z(self):
        """
        Get the z-value of the new location of the rubble (i.e., 
        `to_location[2]`). Attempting to set the z-value of the location will
        result in an `ImmutableAttributeException` being raised.
        """

        return self._to_location[2]

    @to_z.setter
    def to_z(self, z):
        raise ImmutableAttributeException(str(self), "to_z") from None



    def toDict(self):
        """
        Generates a dictionary representation of the RubblePlacedEvent message.
        RubblePlaced information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the RubblePlacedEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["from_x"] = self.from_x
        jsonDict["data"]["from_y"] = self.from_y
        jsonDict["data"]["from_z"] = self.from_z
        jsonDict["data"]["to_x"] = self.to_x
        jsonDict["data"]["to_y"] = self.to_y
        jsonDict["data"]["to_z"] = self.to_z

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the RubblePlacedEvent message.  
        RubblePlacedEvent information is contained in a JSON object under the
        key "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            RubblePlacedEvent message.
        """

        return json.dumps(self.toDict())

