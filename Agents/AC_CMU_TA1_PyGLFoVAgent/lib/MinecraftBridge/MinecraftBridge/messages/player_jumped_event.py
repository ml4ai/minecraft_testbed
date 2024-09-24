# -*- coding: utf-8 -*-
"""
.. module:: player_jumped_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Player Jumped Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Player Jumped Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class PlayerJumpedEvent(BaseMessage):
    """
    A class encapsulating PlayerJumpedEvent messages.

    Note
    ----
    Constructing a PlayerJumpedEvent message requires passing the following 
    keyword arguments:

        `location`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    PlayerJumpedEvent messages contain attributes `item_x`, `item_y`, and 
    `item_z`.  While the semantics of these are unusual, they are included to
    conform to the ASIST testbed MessageSpecs.

    Attributes
    ----------
    playername : string
        Name of the player who jumped
    location : tuple of floats
        Location where the player jumped
    item_x : float
        x position of the location of the player (alias of `location[0]`)
    item_y : float
        y position of the location of the player (alias of `location[1]`)
    item_z : float
        z position of the location of the player (alias of `location[2]`)        
    """


    def __init__(self, **kwargs):
        """
        Construction of a PlayerJumpedEvent message requires two pieces of
        information -- the name of the player, and the location of the player.
        The name of the player can be passed as `playername`, `participant_id`,
        or `name`; player location is given either by the tuple `location`, or
        with individual (x,y,z) components passed as `player_{x,y,z}` or 
        `item_{x,y,z}`.  Keyword arguments below are listed in the order they
        are checked for.

        Keyword Arguments
        -----------------
        playername : string
        participant_id : string
        name : string
            Name of the player who jumped
        location : tuple of floats
        player_x : float
        player_y : float
        player_z : float
        item_x : float
        item_y : float
        item_z : float
            (x,y,z) position of the player
        """

        BaseMessage.__init__(self, **kwargs)

        self._playername = kwargs.get("playername",
                           kwargs.get("participant_id", 
                           kwargs.get("name", None)))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  'playername') from None

        # Attempt to get the location of the event, first checking for the 
        # `location` keyword, followed by `player` or `item` x,y,z components.
        try:
            location = kwargs['location']
        except KeyError:
            try:
                location = (kwargs['player_x'],
                            kwargs['player_y'],
                            kwargs['player_z'])
            except KeyError:
                try:
                    location = (kwargs['item_x'],
                                kwargs['item_y'],
                                kwargs['item_z'])
                except KeyError:
                    raise MissingMessageArgumentException(str(self),
                                                          'location') from None

 
        # Location needs to be able to be coerced into a tuple of floats.
        # Raise an exception if not possible
        try:
            self._location = tuple([float(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'location',
                                                    location) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PlayerJumpedEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player who jumped.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def location(self):
        """
        Get the location where the player jumped.  

        Attempting to set `location` raises an `ImmutableAttributeException`.
        """

        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location")


    @property
    def item_x(self):
        """
        Alias of `location[0]`
        """

        return self._location[0]

    @item_x.setter
    def item_x(self, x):
        raise ImmutableAttributeException(str(self), "item_x")


    @property
    def item_y(self):
        """
        Alias of `location[1]`
        """

        return self._location[1]

    @item_y.setter
    def item_y(self, y):
        raise ImmutableAttributeException(str(self), "item_y")


    @property
    def item_z(self):
        """
        Alias of `location[2]`
        """

        return self._location[2]

    @item_z.setter
    def item_z(self, z):
        raise ImmutableAttributeException(str(self), "item_z")
       

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PlayerJumpedEvent message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = playername
        jsonDict["data"]["item_x"] = self.item_x
        jsonDict["data"]["item_y"] = self.item_y
        jsonDict["data"]["item_z"] = self.item_z

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
            PlayerJumpedEvent message.
        """

        return json.dumps(self.toDict())

