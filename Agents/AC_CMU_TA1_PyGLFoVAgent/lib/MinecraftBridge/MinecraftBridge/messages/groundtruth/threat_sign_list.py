# -*- coding: utf-8 -*-
"""
.. module:: threat_sign_list
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Threat Sign information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Threat Sign List messages.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class ThreatSign:
    """
    A class encapsulating individual threat signs.

    Note
    ----
    Constructing a ThreatSign message requires passing the following keyword
    arguments:

        `location`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    location : tuple of ints
        Location of the threat sign
    x : int
        x location of the threat sign (alias of `location[0]`)
    y : int
        y location of the threat sign (alias of `location[1]`)
    z : int
        z location of the threat sign (alias of `location[2]`)
    block_type : string
        Block type of the threat sign (i.e., redstone)
    room_name : string
        Name of the room the threat sign is in
    feature_type : string
        Type of map feature that this threat sign is associated with
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
        self._feature_type = kwargs.get('feature_type', "Threat Room")


    def __str__(self):
        """
        String representation of the ThreatSign.

        Returns
        -------
        string
            Class name of the message (i.e., 'ThreatSign')
        """

        return self.__class__.__name__


    @property
    def location(self):
        """
        Get the location of the threat sign.  

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
        Get the block type of the threat sign.  

        Attempting to set `block_type` raises an `ImmutableAttributeException`.
        """

        return self._block_type

    @block_type.setter
    def block_type(self, type):
        raise ImmutableAttributeException(str(self), "block_type")


    @property
    def room_name(self):
        """
        Get the name of the room the threat sign is in.  

        Attempting to set `room_name` raises an `ImmutableAttributeException`.
        """

        return self._room_name

    @room_name.setter
    def room_name(self, name):
        raise ImmutableAttributeException(str(self), "room_name")


    @property
    def feature_type(self):
        """
        Get the type of the threat sign.  

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
            A dictionary representation of the ThreatSign.
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
            Threat Sign.
        """

        return json.dumps(self.toDict())



class ThreatSignList(BaseMessage):
    """
    A class encapsulating BlockageList messages.

    Attributes
    ----------
    mission : string
        Name of the mission
    threat_signs : list of ThreatSign
        List of blockages 
    mission_threatsign_list : list of ThreatSign
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

        # If no threat_signs are provided, start with an empty list
        self._threat_signs = kwargs.get('threat_sign_list',[])

        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ThreatSignList')
        """

        return self.__class__.__name__


    def add(self, sign):
        """
        Add a threat sign to the list of threat signs

        Parameters
        ----------
        sign : ThreatSign
            Instance of a ThreatSign to add
        """

        # Check if the threat sign list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), 
                                              "threat_signs (from add)")

        self.threat_signs.append(sign)


    def finalize(self):
        """
        Indicate that all Threat Signs instances have been added to the list
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
    def threat_signs(self):
        """
        Get the list of threat_signs.  

        Attempting to set `threat_signs` raises an `ImmutableAttributeException`.
        """

        return self._threat_signs

    @threat_signs.setter
    def threat_signs(self, signs):
        raise ImmutableAttributeException(str(self), "threat_signs")


    @property
    def mission_threatsign_list(self):
        """
        Alias of `threat_signs`
        """

        return self._threat_signs

    @mission_threatsign_list.setter
    def mission_threatsign_list(self, signs):
        raise ImmutableAttributeException(str(self), "mission_threatsign_list")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ThreatSignList.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["mission"] = self.mission
        jsonDict["data"]["mission_threatsign_list"] = [ sign.toDict() for sign in self.mission_threatsign_list ]

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
            ThreatSignList message.
        """

        return json.dumps(self.toDict())        
