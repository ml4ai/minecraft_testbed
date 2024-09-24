# -*- coding: utf-8 -*-
"""
.. module:: tool_used
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Tool Used Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Tool Used Event messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class ToolUsedEvent(BaseMessage):
    """
    A class encapsulating ToolUsedEvent messages.

    Attributes
    ----------
    playername : string
        The name of the entity that used the tool
    tool_type : string
        The type of tool being used
    durability : int
        The number of uses left in the tool
    count : int
        The number of tools of this type in the player's inventory
    block_location : tuple of ints
        The location of the block being hit
    target_block_x : int
        The x location of the block being hit (i.e., alias of block_location[0])
    target_block_y : int
        The y location of the block being hit (i.e., alias of block_location[1])
    target_block_z : int
        The z location of the block being hit (i.e., alias of block_location[2])
    block_type : string
        Block type of the block being hit
    target_block_type : string
        Alias of block_type
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        playername : string
            Name of the player who used the tool
        tool_type : string
            Type of tool used
        durability : int
            Remaining number of tool usages left
        count : int
            Number of tools of this type in player's inventory
        block_location : tuple of int
        target_block_x : int
        target_block_y : int
        target_block_z : int
            Location of the block the tool was used on
        target_block_type : string
        block_type : string
            Type of block that the tool was used on
        """

        BaseMessage.__init__(self, **kwargs)

        # Get the playername.  Note that this may have been renamed as
        # participant id, so try that if playername is not provided
        self._playername = kwargs.get('playername', 
                           kwargs.get('participant_id', None))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  'playername') from None

        # Get the location of the target block: try `block_location` first, 
        # followed by `target_block_x`, `target_block_y`, `target_block_z`
        location = kwargs.get('block_location', None)

        if location is None:
            try:
                location = (kwargs['target_block_x'], 
                            kwargs['target_block_y'], 
                            kwargs['target_block_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'block_location') from None

        # Location needs to be able to be coerced into a tuple of ints.  Raise 
        # an exception if not possible
        try:
            self._block_location = tuple([int(x) for x in location][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'block_location', 
                                                    location) from None

        self._target_block_type = kwargs.get("target_block_type",
                                  kwargs.get("block_type", None))
        if self._target_block_type is None:
            raise MissingMessageArgumentException(str(self),
                                                  'target_block_type') from None

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["tool_type", "durability", "count"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self),
                                                      arg_name) from None

        self._tool_type = kwargs["tool_type"]
        self._durability = int(kwargs["durability"])
        self._count = int(kwargs["count"])


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ToolUsedEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player using the tool.  Attempting to set the value
        of `playername` will result in an `ImmutableAttributeException` being 
        raised.        
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def tool_type(self):
        """
        Get the type of tool used by the player.  Attempting to set the value
        of `tool_type` will result in an `ImmutableAttributeException` being 
        raised.        
        """

        return self._tool_type

    @tool_type.setter
    def tool_type(self, tool):
        raise ImmutableAttributeException(str(self), "tool_type")


    @property
    def durability(self):
        """
        Get the remaining durability of the tool.  Attempting to set the value 
        of `durability` will result in an `ImmutableAttributeException` being 
        raised.        
        """

        return self._durability

    @durability.setter
    def durability(self, durability):
        raise ImmutableAttributeException(str(self), "durability")


    @property
    def count(self):
        """
        Get the number of tools of the given type in the player's inventory.  
        Attempting to set the value of `count` will result in an 
        `ImmutableAttributeException` being raised.        
        """

        return self._count

    @count.setter
    def count(self, count):
        raise ImmutableAttributeException(str(self), "count")


    @property
    def block_location(self):
        """
        Get the location of the block the tool was used on.  Attempting to set
        the value of `block_location` will result in an
        `ImmutableAttributeException` being raised.        
        """

        return self._block_location

    @block_location.setter
    def block_location(self, location):
        raise ImmutableAttributeException(str(self), "block_location")


    @property
    def target_block_x(self):
        """
        Alias of `block_location[0]`
        """

        return self._block_location[0]

    @target_block_x.setter
    def target_block_x(self, x):
        raise ImmutableAttributeException(str(self), "target_block_x")


    @property
    def target_block_y(self):
        """
        Alias of `block_location[1]`
        """

        return self._block_location[1]

    @target_block_y.setter
    def target_block_y(self, y):
        raise ImmutableAttributeException(str(self), "target_block_y")


    @property
    def target_block_z(self):
        """
        Alias of `block_location[2]`
        """

        return self._block_location[2]

    @target_block_z.setter
    def  target_block_z(self, _z):
        raise ImmutableAttributeException(str(self), "target_block_z")


    @property
    def block_type(self):
        """
        Get the type of block the tool was used on.  Attempting to set the 
        value of `block_type` will result in an `ImmutableAttributeException`
        being raised.        
        """

        return self._block_type

    @block_type.setter
    def block_type(self, type):
        raise ImmutableAttributeException(str(self), "block_type")


    @property
    def target_block_type(self):
        """
        Alias of `block_type`
        """

        return self._target_block_type

    @target_block_type.setter
    def target_block_type(self, type):
        raise ImmutableAttributeException(str(self), "target_block_type")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ToolUsedEvent message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["tool_type"] = self.tool_type
        jsonDict["data"]["durability"] = self.durability
        jsonDict["data"]["count"] = self.count
        jsonDict["data"]["target_block_x"] = self.target_block_x
        jsonDict["data"]["target_block_y"] = self.target_block_y
        jsonDict["data"]["target_block_z"] = self.target_block_z
        jsonDict["data"]["target_block_type"] = self.target_block_type

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
            ToolUsedEvent message.
        """

        return json.dumps(self.toDict())
