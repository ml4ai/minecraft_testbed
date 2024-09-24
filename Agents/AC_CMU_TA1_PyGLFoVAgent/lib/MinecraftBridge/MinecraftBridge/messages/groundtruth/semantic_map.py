# -*- coding: utf-8 -*-
"""
.. module:: semantic_map
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Semantic Map messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Semantic Map Initialization messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class Location:
    """
    Definition of a base location within the semantic map
    """

    def __init__(self, location_id, **kwargs):
        """
        """

        self.id = location_id
        self.name = kwargs.get("name", "UNKNOWN")
        self.type = kwargs.get("type", "UNKNOWN")


class ParentLocation(Location):
    """
    Definition of a composite of child locations
    """

    def __init__(self, location_id, **kwargs):
        """
        """

        Location.__init__(self, location_id, **kwargs)

        self.children = {}


    def add(self, child):
        """
        Add a child location to the set of children locations

        Arguments
        ---------
        child : Location
            Child Location to be added to this ParentLocation
        """

        # Check if the child exists, by it's id
        if child.id in self.children:
            # TODO:  raise a warning here...
            return

        self.children[child.id] = child



class SemanticMapInitialized(BaseMessage):
    """
    A class encapsulating Semantic Map Initialization messages.

    Attributes
    ----------
    semantic_map_name : string
        Filename of the semantic map
    semantic_map : dict
        Dictionary representation of the semantic map
    """


    def __init__(self, **kwargs):
        
        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["semantic_map_name", "semantic_map"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._semantic_map_name = kwargs["semantic_map_name"]
        self._semantic_map = kwargs["semantic_map"]


    @property
    def semantic_map_name(self):
        """
        Get the filename of the semantic map.  

        Attempting to set `semantic_map_name` raises an `ImmutableAttributeException`.
        """

        return self._semantic_map_name

    @semantic_map_name.setter
    def name(self, name):
        raise ImmutableAttributeException(str(self), "semantic_map_name")


    @property
    def semantic_map(self):
        """
        Get the dictionary defining the semantic map

        Attempting to set `semantic_map` raises an `ImmutableAttributeException`.
        """

        return self._semantic_map

    @semantic_map.setter
    def semantic_map(self, semantic_map):
        raise ImmutableAttributeException(str(self), "semantic_map")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the SemanticMapInitialized message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["semantic_map_name"] = self.semantic_map_name
        jsonDict["data"]["semantic_map"] = self.semantic_map
        
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
            SemanticMapInitialized message.
        """

        return json.dumps(self.toDict())       
        
