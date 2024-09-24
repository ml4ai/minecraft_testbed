# -*- coding: utf-8 -*-
"""
.. module:: blockage_list
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Beep Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Blockage List messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException
)
from ..base_message import BaseMessage

class Blockage:
    """
    A class encapsulating individual blockages.

    Note
    ----
    Constructing a Blockage message requires passing the following keyword
    arguments:

        `location`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    location : tuple of ints
        Location of the blockage
    x : int
        x location of the blockage (alias of `location[0]`)
    y : int
        y location of the blockage (alias of `location[1]`)
    z : int
        z location of the blockage (alias of `location[2]`)
    block_type : string
        Block type of the blockage
    room_name : string
        Name of the room the blockage is in
    feature_type : string
        type of map feature that this blockage is associated with
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
        self._feature_type = kwargs.get('feature_type', "Blockage")


    def __str__(self):
        """
        String representation of the Blockage.

        Returns
        -------
        string
            Class name of the message (i.e., 'Blockage')
        """

        return self.__class__.__name__


    @property
    def location(self):
        """
        Get the location of the blockage.  

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
        Get the block type of the blockage.  

        Attempting to set `block_type` raises an `ImmutableAttributeException`.
        """

        return self._block_type

    @block_type.setter
    def block_type(self, type):
        raise ImmutableAttributeException(str(self), "block_type")


    @property
    def room_name(self):
        """
        Get the name of the room the blockage is in.  

        Attempting to set `room_name` raises an `ImmutableAttributeException`.
        """

        return self._room_name

    @room_name.setter
    def room_name(self, name):
        raise ImmutableAttributeException(str(self), "room_name")


    @property
    def feature_type(self):
        """
        Get the type of the blockage.  

        Attempting to set `feature_type` raises an `ImmutableAttributeException`.
        """

        return self._feature_type

    @feature_type.setter
    def feature_type(self, type):
        raise ImmutableAttributeException(str(self), "feature_type")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Blockage.
        """

        jsonDict = {}

        # Add the message data
        jsonDict["x"] = self.x
        jsonDict["y"] = self.y
        jsonDict["z"] = self.z
        jsonDict["block_type"] = self.block_type
        jsonDict["room_name"] = self.room_name
        jsonDict["feature_type"] = self.feature_type

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
            Blockage.
        """

        return json.dumps(self.toDict())




class BlockageList(BaseMessage):
    """
    A class encapsulating BlockageList messages.

    Attributes
    ----------
    mission : string
        Name of the mission
    blockages : list of Blockage
        List of blockages 
    mission_blockage_list : list of Blockage
        Alias of `blockages`
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

        # If no blockages are provided, start with an empty list
        self._blockages = kwargs.get('blockages',[])

        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'BlockageList')
        """

        return self.__class__.__name__


    def add(self, blockage):
        """
        Add a blockage to the list of blockages

        Parameters
        ----------
        blockage : Blockage
            Instance of a Blockage to add
        """


        # Check if the blockage list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "blockages (from add)")

        self.blockages.append(blockage)


    def finalize(self):
        """
        Indicate that all Blockage instances have been added to the list
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
    def blockages(self):
        """
        Get the list of blockages.  

        Attempting to set `blockages` raises an `ImmutableAttributeException`.
        """

        return self._blockages

    @blockages.setter
    def blockages(self, blockages):
        raise ImmutableAttributeException(str(self), "blockages")


    @property
    def mission_blockage_list(self):
        """
        Alias of `blockages`
        """

        return self._blockages

    @mission_blockage_list.setter
    def mission_blockage_list(self, blockages):
        raise ImmutableAttributeException(str(self), "mission_blockage_list")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the BlockageList.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["mission"] = self.mission
        jsonDict["data"]["mission_blockage_list"] = [ blockage.toDict() for blockage in self.blockages ]

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
            BlockageList message.
        """

        return json.dumps(self.toDict())        