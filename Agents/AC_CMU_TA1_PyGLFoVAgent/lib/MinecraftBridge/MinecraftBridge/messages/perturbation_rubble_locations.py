# -*- coding: utf-8 -*-
"""
.. module:: perturbation_rubble_locations
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating PerturbationEvent Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating PerturbationRubbleLocation messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage
from . import Blockage

class PerturbationRubbleLocations(BaseMessage):
    """
    A class encapsulating Perturbation Rubble Location messages.

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