# -*- coding: utf-8 -*-
"""
.. module:: item_pickup_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Item Pickup Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Item Pickup Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class ItemPickupEvent(BaseMessage):
    """
    A class encapsulating ItemPickupEvent messages.

    Note
    ----
    Constructing an ItemPickupEvent message requires passing the following keyword
    arguments:

        `itemName`
        `location`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    playername : string
        Name of the player who dropped the item
    itemName : string
        Name of the item dropped
    itemname : string
        Alias of `itemName`
    location : tuple of floats
        Location where the item was dropped
    item_x : float
        x location of the dropped item
    item_y : float
        y location of the dropped item
    item_z : float
        z location of the dropped item
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        playername : string
        participant_id : string
            Name (or id) of the player who dropped the item
        itemname : string
        itemName : string
            Name of the dropped item
        location : tuple of floats
        item_x : float
        item_y : float
        item_z : float
            Location of the dropped item
        """


        BaseMessage.__init__(self, **kwargs)

        self._playername = kwargs.get('playername',
                           kwargs.get('participant_id',
                           None))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  'playername') from None

        self._itemName = kwargs.get('itemname',
                         kwargs.get('itemName',
                         None))
        if self._itemName is None:
            raise MissingMessageArgumentException(str(self),
                                                  'itemname') from None

        location = kwargs.get('location', None)
        if location is None:
            try:
                location = (kwargs['item_x'],
                            kwargs['item_y'],
                            kwargs['item_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'location') from None

        # Location needs to be able to be coerced into a tuple of ints.  Raise 
        # an exception if not possible
        try:
            self._location = tuple([float(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'location', 
                                                    kwargs['location']) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ItemPickupEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player who picked up the item.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def location(self):
        """
        Get the location where the item was picked up.  

        Attempting to set `location` raises an `ImmutableAttributeException`.
        """

        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location")


    @property
    def item_x(self):
        """
        x location of the picked up item (i.e., alias of `location[0]`)
        """

        return self._location[0]

    @location.setter
    def item_x(self, location):
        raise ImmutableAttributeException(str(self), "item_x")


    @property
    def item_y(self):
        """
        y location of the picked up item (i.e., alias of `location[1]`)
        """

        return self._location[1]

    @location.setter
    def item_y(self, location):
        raise ImmutableAttributeException(str(self), "item_y")


    @property
    def item_z(self):
        """
        x location of the picked up item (i.e., alias of `location[2]`)
        """

        return self._location[2]

    @item_z.setter
    def item_z(self, location):
        raise ImmutableAttributeException(str(self), "item_z")


    @property
    def itemName(self):
        """
        Get the name of the item picked up.  

        Attempting to set `itemName` raises an `ImmutableAttributeException`.
        """

        return self._itemName

    @itemName.setter
    def itemName(self, name):
        raise ImmutableAttributeException(str(self), "itemName")


    @property
    def itemname(self):
        """
        Alias of `itemName`
        """

        return self._itemName

    @itemname.setter
    def itemname(self, name):
        raise ImmutableAttributeException(str(self), "itemname")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ItemPickupEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["itemname"] = self.itemname
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
            ItemPickupEvent message.
        """

        return json.dumps(self.toDict())
