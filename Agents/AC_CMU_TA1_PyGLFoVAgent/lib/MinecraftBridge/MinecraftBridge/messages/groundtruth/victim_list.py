# -*- coding: utf-8 -*-
"""
.. module:: victim_list
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Victim List information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Victim List messages.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class Victim:
    """
    A class encapsulating individual victims.

    Note
    ----
    Constructing a Victim message requires passing the following keyword
    arguments:

        `location`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    location : tuple of ints
        Location of the victim
    x : int
        x location of the victim (alias of `location[0]`)
    y : int
        y location of the victim (alias of `location[1]`)
    z : int
        z location of the victim (alias of `location[2]`)
    block_type : string
        Block type of the victim
    room_name : string
        Name of the room the victim is in
    unique_id : int
        Unique identifier of the victim
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

        # Check if the id is provided, and default to -1 if not
        self._unique_id = kwargs.get('unique_id', -1)


    def __str__(self):
        """
        String representation of the Victim.

        Returns
        -------
        string
            Class name of the message (i.e., 'Victim')
        """

        return self.__class__.__name__


    @property
    def location(self):
        """
        Get the location of the victim.  

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
        Get the block type of the victim.

        Attempting to set `block_type` raises an `ImmutableAttributeException`.
        """

        return self._block_type

    @block_type.setter
    def block_type(self, type):
        raise ImmutableAttributeException(str(self), "block_type")


    @property
    def room_name(self):
        """
        Get the name of the room the victim is in.  

        Attempting to set `room_name` raises an `ImmutableAttributeException`.
        """

        return self._room_name

    @room_name.setter
    def room_name(self, name):
        raise ImmutableAttributeException(str(self), "room_name")


    @property
    def unique_id(self):
        """
        Get the id of the victim.

        Attempting to set `unique_id` raises an `ImmutableAttributeException`.
        """
        return self._unique_id

    @unique_id.setter
    def unique_id(self, _id):
        raise ImmutableAttributeException(str(self), "unique_id")
    

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Victim.
        """

        jsonDict = {}

        # Add the message data
        jsonDict["x"] = self.x
        jsonDict["y"] = self.y
        jsonDict["z"] = self.z
        jsonDict["block_type"] = self.block_type
        jsonDict["room_name"] = self.room_name
        jsonDict["unique_id"] = self.unique_id

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
            Victim.
        """

        return json.dumps(self.toDict())






class VictimList(BaseMessage):
    """
    A class encapsulating FreezeBlockList messages.

    Attributes
    ----------
    mission : string
        Name of the mission
    victims : list of Victim
        List of victims 
    mission_victim_list : list of Victim
        Alias of `victims`
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

        # If no victims are provided, start with an empty list
        self._victims = kwargs.get('victims',[])

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
        Add a victim to the list of victims

        Parameters
        ----------
        victim : Victim
            Instance of a Victim to add
        """


        # Check if the victims list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "victims (from add)")

        self._victims.append(block)


    def finalize(self):
        """
        Indicate that all Victim instances have been added to the list
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
    def victims(self):
        """
        Get the list of victims.  

        Attempting to set `victims` raises an `ImmutableAttributeException`.
        """

        return self._victims

    @victims.setter
    def victims(self, blocks):
        raise ImmutableAttributeException(str(self), "victims")


    @property
    def mission_victim_list(self):
        """
        Alias of `victims`
        """

        return self._victims

    @mission_victim_list.setter
    def mission_victim_list(self, blocks):
        raise ImmutableAttributeException(str(self), "mission_victim_list")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimList.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["mission"] = self.mission
        jsonDict["data"]["mission_victim_list"] = [ victim.toDict() for victim in self.victims ]

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
            VictimList message.
        """

        return json.dumps(self.toDict())        

