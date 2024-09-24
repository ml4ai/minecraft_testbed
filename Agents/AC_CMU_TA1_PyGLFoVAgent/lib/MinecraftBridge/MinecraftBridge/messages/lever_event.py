# -*- coding: utf-8 -*-
"""
.. module:: lever_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Lever Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Lever Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class LeverEvent(BaseMessage):
    """
    A class encapsulating Lever Event messages.

    Note
    ----
    Constructing a LeverEvent message requires passing the following keyword
    arguments:

        `playername`
        `position`

    While aliases exist for these attributes, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    playername : string
        The name of the player that operated the lever
    position : tuple of ints
        Location of the lever
    location : tuple of ints
        Location of the lever; alias for `position`
    powered : boolean
        True if the lever was turned on, False otherwise
    lever_x : int
        The x location of the lever, alias of position[0]
    lever_y: int
        The y location of the lever, alias of position[1]
    lever_z: int
        The z location of the lever, alias of position[2]
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        playername : string
        participant_id : string
            Name or ID of the player that operated the lever
        position : tuple of ints
        location : tuple of ints
        lever_x : int
        lever_y : int
        lever_z : int
            (x,y,z) location of the lever
        powered : boolean
            Indication if the lever was turned on (True) or off (False)
        """

        BaseMessage.__init__(self, **kwargs)
        

        # Get the location of the lever: try `position` first, followed by
        # `location` and finally `lever_x`, `lever_y`, `lever_z`
        position = kwargs.get('position', kwargs.get('location', None))

        if position is None:
            try:
                position = (kwargs['lever_x'], 
                            kwargs['lever_y'], 
                            kwargs['lever_z'])
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


        self._playername = kwargs.get('playername',
                           kwargs.get('participant_id', None))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  "playername") from None

        try:
            self._powered = kwargs['powered']
        except KeyError:
            raise MissingMessageArgumentException(str(self),
                                                  'powered') from None

        # `powered` needs to be able to be coerced into a boolean 
        try:
            self._powered = bool(self._powered)
        except:
            raise MalformedMessageCreationException(str(self), 'powered',
                                                    self._powered) from None



    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'LeverEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player that operated the lever.  Attempting to set
        the value of the `playername` will result in an 
        `ImmutableAttributeException` being raised.        
        """        
        return self._playername

    @playername.setter
    def playername(self, playername):
        raise ImmutableAttributeException(str(self), "playername") from None


    @property
    def position(self):
        """
        Get the location of the lever.  Attempting to set the value of the
        `position` will result in an `ImmutableAttributeException` being raised.
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
    def powered(self):
        """
        Get whether the lever was turned on or off.  Attempting to set the 
        value of the `powered` will result in an `ImmutableAttributeException`
        being raised.

        Returns
        -------
            True if the lever was turned on, False if the lever was turned off
        """                
        return self._powered

    @powered.setter
    def powered(self, opened):
        raise ImmutableAttributeException(str(self), "powered") from None


    @property
    def lever_x(self):
        """
        Get the x-value of the location of the lever (i.e., `position[0]`).
        Attempting to set the x-value of the location will result in an
         `ImmutableAttributeException` being raised.
        """
        return self._position[0]

    @lever_x.setter
    def lever_x(self, x):
        raise ImmutableAttributeException(str(self), "lever_x") from None


    @property
    def lever_y(self):
        """
        Get the y-value of the location of the lever (i.e., `position[1]`).
        Attempting to set the y-value of the location will result in an
         `ImmutableAttributeException` being raised.
        """
        return self._position[1]

    @lever_y.setter
    def lever_y(self, y):
        raise ImmutableAttributeException(str(self), "lever_y") from None


    @property
    def lever_z(self):
        """
        Get the z-value of the location of the lever (i.e., `position[2]`).
        Attempting to set the z-value of the location will result in an
         `ImmutableAttributeException` being raised.        
        """
        return self._position[2]

    @lever_z.setter
    def lever_z(self, z):
        raise ImmutableAttributeException(str(self), "lever_z") from None
    

    def toDict(self):
        """
        Generates a dictionary representation of the LeverEvent message.  
        LeverEvent information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the LeverEvent.
        """

        jsonDict = BaseMessage.toDict(self)
    
        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        jsonDict['data']['playername'] = self.playername,
        jsonDict['data']['lever_x'] = self.lever_x,
        jsonDict['data']['lever_y'] = self.lever_y,
        jsonDict['data']['lever_z'] = self.lever_z,
        jsonDict['data']['powered'] = self.powered

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the LeverEvent message.  LeverEvent
        information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            LeverEvent message.
        """

        return json.dumps(self.toDict())
