# -*- coding: utf-8 -*-
"""
.. module:: fov_map_metadata
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating FoV map metadata messages.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Field of View Map Metadata messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class FoV_MapMetadata(BaseMessage):
    """
    A class encapsulating Field of View map metadata messages.

    Attributes
    ----------
    map_name : string
        name of the JSON file of the map
    world_name : string
        name of the Minecraft world used to generate the map
    map_url : string
        url of the JSON file of the map
    world_url : string
        url of the Minecraft world used to generate the map
    creation_time : string
        timestamp when the map was created
    lower_bound : tuple of floats
        (x,y,z) of the lower bound of the world from which the map was created
    upper_bound : tuple of floats
        (x,y,z) of the upper bound of the world from which the map was created       
    ignored_blocks : list
        list of ignored blocks when map was created
    parser_metadata : dictionary
        dictionary of additional metadata of the parser code
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)    

        # Check to see if the necessary arguments have been passed, raise an
        # exception if one is missing
        for arg_name in ['map_name', 'world_name', 'map_url', 'world_url',
                         'creation_time', 'lower_bound', 'upper_bound',
                         'ignored_blocks', 'parser_metadata']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(self.__class__.__name__, arg_name) from None

        # TODO: Validate the passed arguments
        self._map_name = str(kwargs.get('map_name'))
        self._world_name = str(kwargs.get('world_name'))
        self._map_url = str(kwargs.get('map_url'))
        self._world_url = str(kwargs.get('world_url'))
        self._creation_time = kwargs.get('creation_time')
        self._lower_bound = kwargs.get('lower_bound')
        self._upper_bound = kwargs.get('upper_bound')
        self._ignored_blocks = kwargs.get('ignored_blocks')
        self._parser_metadata = kwargs.get('parser_metadata')


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'FoV_MapMetadata')
        """

        return self.__class__.__name__


    @property
    def map_name(self):
        """
        Get the name of the JSON file of the map used.
        
        Attempting to set `nap_name` raises an `ImmutableAttributeException`.
        """

        return self._map_name

    @map_name.setter
    def map_name(self, name):
        raise ImmutableAttributeException(str(self), "map_name")


    @property
    def world_name(self):
        """
        Get the name of the world the map data was generated from.
        
        Attempting to set `world_name` raises an `ImmutableAttributeException`.
        """

        return self._world_name

    @world_name.setter
    def world_name(self, name):
        raise ImmutableAttributeException(str(self), "world_name")
    

    @property
    def map_url(self):
        """
        Get the URL where the map JSON datafile is located
        
        Attempting to set `map_url` raises an `ImmutableAttributeException`.
        """

        return self._map_url

    @map_url.setter
    def map_url(self, url):
        raise ImmutableAttributeException(str(self), "map_url")



    @property
    def world_url(self):
        """
        Get the URL where the Minecraft world is located
        
        Attempting to set `world_url` raises an `ImmutableAttributeException`.
        """

        return self._world_url

    @world_url.setter
    def world_url(self, url):
        raise ImmutableAttributeException(str(self), "world_url")


    @property
    def creation_time(self):
        """
        Get the creation time of the map data file
        
        Attempting to set `creation_time` raises an `ImmutableAttributeException`.
        """

        return self._creation_time

    @creation_time.setter
    def creation_time(self, time):
        raise ImmutableAttributeException(str(self), "creation_time")


    @property
    def lower_bound(self):
        """
        Get the lower bound of block locations, as a tuple, in the map.
        
        Attempting to set `lower_bound` raises an `ImmutableAttributeException`.
        """

        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, bound):
        raise ImmutableAttributeException(str(self), "lower_bound")


    @property
    def upper_bound(self):
        """
        Get the upper bound of block locations in the map, as a tuple.
        
        Attempting to set `upper_bound` raises an `ImmutableAttributeException`.
        """

        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, bound):
        raise ImmutableAttributeException(str(self), "upper_bound")


    @property
    def ignored_blocks(self):
        """
        Get the list of blocks ignored when generating the map file.
        
        Attempting to set `ignored_blocks` raises an `ImmutableAttributeException`.
        """

        return self._ignored_blocks

    @ignored_blocks.setter
    def ignored_blocks(self, blocks):
        raise ImmutableAttributeException(str(self), "ignored_blocks")
    

    @property
    def parser_metadata(self):
        """
        Get the metadata associated with the map parsing code.
        
        Attempting to set `parser_metadata` raises an `ImmutableAttributeException`.
        """

        return self._parser_metadata

    @parser_metadata.setter
    def parser_metadata(self, metadata):
        raise ImmutableAttributeException(str(self), "parser_metadata")



    def toDict(self):
        """
        Generates a dictionary representation of the FoV_MapMetadata message.  
        FoV_MapMetadata information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the FoV_MapMetadata.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}


        jsonDict['data'] = { 'map_name': self.map_name,
                             'world_name': self.world_name,
                             'map_url': self.map_url,
                             'world_url': self.world_url,
                             'creation_time': self.creation_time,
                             'lower_bound': self.lower_bound,
                             'upper_bound': self.upper_bound,
                             'ignored_blocks': self.ignored_blocks,
                             'parser_metadata': self.parser_metadata
                           }

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the FoV_MapMetadata message.  
        FoV_MapMetadata information is contained in a JSON object under the key
        "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            FoV_MapMetadata message.
        """

        return json.dumps(self.toDict())        
