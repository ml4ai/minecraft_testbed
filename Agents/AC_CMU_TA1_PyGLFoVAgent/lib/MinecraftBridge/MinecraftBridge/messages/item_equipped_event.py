# -*- coding: utf-8 -*-
"""
.. module:: item_equipped_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Item Equipped Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Item Equipped Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class ItemEquippedEvent(BaseMessage):
    """
    A class encapsulating ItemDropEvent messages.

    Attributes
    ----------
    playername : string
        Name of the player who dropped the item
    itemName : string
        Name of the item dropped
    equippeditemname : string
        Alias of `itemName`
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
        """


        BaseMessage.__init__(self, **kwargs)

        self._playername = kwargs.get('playername',
                           kwargs.get('participant_id',
                           None))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  'playername') from None

        self._itemname = kwargs.get('equippeditemname',
                         kwargs.get('itemName',
                         None))
        if self._itemname is None:
            raise MissingMessageArgumentException(str(self),
                                                  'equippeditemname') from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ItemEquippedEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player who equipped the item.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def itemName(self):
        """
        Get the name of the item equipped.  

        Attempting to set `itemName` raises an `ImmutableAttributeException`.
        """

        return self._itemname

    @itemName.setter
    def itemName(self, name):
        raise ImmutableAttributeException(str(self), "itemName")


    @property
    def equippeditemname(self):
        """
        Alias of `itemName`
        """

        return self._itemname

    @equippeditemname.setter
    def equippeditemname(self, name):
        raise ImmutableAttributeException(str(self), "eqippeditemname")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ItemEquippedEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["equippeditemname"] = self.equippeditemname

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
            ItemEquippedEvent message.
        """

        return json.dumps(self.toDict())

