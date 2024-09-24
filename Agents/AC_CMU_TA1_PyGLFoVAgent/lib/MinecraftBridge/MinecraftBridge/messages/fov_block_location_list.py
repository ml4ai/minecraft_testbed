# -*- coding: utf-8 -*-
"""
.. module:: fov_block_location_list
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating FoV block location messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Field of View block location list essages.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class FoV_BlockLocationList(BaseMessage):
    """
    A class encapsulating Field of View block location list messages.

    Attributes
    ----------
    playername : string
        The player whose FoV is being summarized
    observationNumber : string
        The observation number (from PlayerState) associated with the FoV summary
    locations : list of tuples
        List of block locations (x,y,z).
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)    

        # Check to see if the necessary arguments have been passed, raise an exception if one is missing
        for arg_name in ['playername', 'locations']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), arg_name) from None

        # TODO: Validate the passed arguments
        self._playername = kwargs['playername']

        self._observationNumber = kwargs.get('observation',
                                  kwargs.get('observationNumber', None))
        if self._observationNumber is None:
            raise MissingMessageArgumentException(str(self),
                                                  'observation') from None

        self._locations = kwargs['locations']


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'FovSummary')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player whose FoV is summarized.

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def observationNumber(self):
        """
        Get the observation number (from the PlayerState message) associated
        with this FoV message.

        Attempting to set `observationNumber` raises an `ImmutableAttributeException`.
        """

        return self._observationNumber

    @observationNumber.setter
    def observationNumber(self, number):
        raise ImmutableAttributeException(str(self), "observationNumber")


    @property
    def observation(self):
        """
        Alias of `observationNumber`
        """

        return self._obserationNumber

    @observation.setter
    def observation(Self, number):
        raise ImmutableAttributeException(str(self), "observation") 


    @property
    def locations(self):
        """
        Get the list of block locations

        Attempting to set `locations` raises an `ImmutableAttributeException`.
        """

        return self._locations

    @locations.setter
    def locations(self, location_list):
        raise ImmutableAttributeException(str(self), "locations")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the FoV_BlockLocationList message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        jsonDict['data'] = {  'playername': self.playername,
                              'observation': self.observationNumber,
                              'locations': self.locations 
                            }

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
            FoV_BlockLocationList message.
        """

        return json.dumps(self.toDict())
