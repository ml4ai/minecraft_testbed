# -*- coding: utf-8 -*-
"""
.. module:: freezeblock_list
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Freezeblock List messages.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Freezeblock List messages.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class FreezeBlock:
    """
    A class encapsulating individual blockages.

    Note
    ----
    Constructing a FreezeBlock message requires passing the following keyword
    arguments:

        `location`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    location : tuple of ints
        Location of the freeze block
    x : int
        x location of the blockage (alias of `location[0]`)
    y : int
        y location of the blockage (alias of `location[1]`)
    z : int
        z location of the blockage (alias of `location[2]`)
    block_type : string
        Block type of the freeze block
    room_name : string
        Name of the room the freeze block is in
    """    

    def __init__(self, **kwargs):

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ['location', 'block_type', 'room_name']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self),
                                                      arg_name) from None

        # Location needs to be able to be coerced into a tuple of ints.  Raise 
        # an exception if not possible
        try:
            self._location = tuple([int(x) for x in kwargs['location']][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'location',
                                                    kwargs['location']) from None

        self._block_type = kwargs['block_type']
        self._room_name = kwargs['room_name']


    def __str__(self):
        """
        String representation of the Blockage.

        Returns
        -------
        string
            Class name of the message (i.e., 'FreezeBlock')
        """

        return self.__class__.__name__


    @property
    def location(self):
        """
        Get the location of the freeze block.  

        Attempting to set `location` raises an `ImmutableAttributeException`.
        """

        return self._location

    @location.setter
    def location(self, location):
        raise ImmutableAttributeException(str(self), "location")


    @property
    def x(self):
        """
        Alias of `location[0]`
        """

        return self._location[0]

    @x.setter
    def x(self, x):
        raise ImmutableAttributeException(str(self), "x")


    @property
    def y(self):
        """
        Alias of `location[1]`
        """

        return self._location[1]

    @y.setter
    def y(self, y):
        raise ImmutableAttributeException(str(self), "y")


    @property
    def z(self):
        """
        Alias of `location[2]`
        """

        return self._location[2]

    @z.setter
    def z(self, z):
        raise ImmutableAttributeException(str(self), "z")


    @property
    def block_type(self):
        """
        Get the block type of the freeze block.

        Attempting to set `block_type` raises an `ImmutableAttributeException`.
        """

        return self._block_type

    @block_type.setter
    def block_type(self, type):
        raise ImmutableAttributeException(str(self), "block_type")


    @property
    def room_name(self):
        """
        Get the name of the room the freeze block is in.  

        Attempting to set `room_name` raises an `ImmutableAttributeException`.
        """

        return self._room_name

    @room_name.setter
    def room_name(self, name):
        raise ImmutableAttributeException(str(self), "room_name")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the FreezeBlock.
        """

        jsonDict = {}

        # Add the message data
        jsonDict["x"] = self.x
        jsonDict["y"] = self.y
        jsonDict["z"] = self.z
        jsonDict["block_type"] = self.block_type
        jsonDict["room_name"] = self.room_name

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
            FreezeBlock.
        """

        return json.dumps(self.toDict())



class FreezeBlockList(BaseMessage):
    """
    A class encapsulating FreezeBlockList messages.

    Attributes
    ----------
    mission : string
        Name of the mission
    freezeblocks : list of FreezeBlock
        List of blockages 
    mission_freezeblock_list : list of FreezeBlock
        Alias of `freezeblocks`
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an
        # exception if one is missing
        for arg_name in ['mission']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self),
                                                      arg_name) from None

        self._mission = kwargs['mission']

        # If no freezeblocks are provided, start with an empty list
        self._freezeblocks = kwargs.get('freezeblocks',[])

        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'FreezeBlockList')
        """

        return self.__class__.__name__


    def add(self, block):
        """
        Add a freeze block to the list of blockages

        Parameters
        ----------
        block : FreezeBlock
            Instance of a FreezeBlock to add
        """


        # Check if the freezeblocks list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "freezeblocks (from add)")

        self._freezeblocks.append(block)


    def finalize(self):
        """
        Indicate that all FreezeBlock instances have been added to the list
        """

        self._finalized = True


    @property
    def mission(self):
        """
        Get the mission name.  

        Attempting to set `mission` raises an `ImmutableAttributeException`.
        """

        return self._mission

    @mission.setter
    def mission(self, name):
        raise ImmutableAttributeException(str(self), "mission")


    @property
    def freezeblocks(self):
        """
        Get the list of freezeblocks.  

        Attempting to set `freezeblocks` raises an `ImmutableAttributeException`.
        """

        return self._freezeblocks

    @freezeblocks.setter
    def freezeblocks(self, blocks):
        raise ImmutableAttributeException(str(self), "freezeblocks")


    @property
    def mission_freezeblock_list(self):
        """
        Alias of `freezeblocks`
        """

        return self._freezeblocks

    @mission_freezeblock_list.setter
    def mission_freezeblock_list(self, blocks):
        raise ImmutableAttributeException(str(self), "mission_freezeblock_list")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the FreezeBlockList.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["mission"] = self.mission
        jsonDict["data"]["mission_freezeblock_list"] = [ block.toDict() for block in self.freezeblocks ]

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
            FreezeBlockList message.
        """

        return json.dumps(self.toDict())        
