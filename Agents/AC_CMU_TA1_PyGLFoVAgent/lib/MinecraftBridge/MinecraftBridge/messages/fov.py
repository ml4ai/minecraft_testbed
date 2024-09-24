# -*- coding: utf-8 -*-
"""
.. module:: fov
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating FoV messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Field of View messages.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class FoVSummary(BaseMessage):
    """
    A class encapsulating Field of View messages.

    Attributes
    ----------
    playername : string
        The player whose FoV is being summarized
    observationNumber : string
        The observation number (from PlayerState) associated with the FoV summary
    blocks : list of dictionaries
        List of block summary information, consisting of a dictionary for each
        block summarized.
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)    

        # Check to see if the necessary arguments have been passed, raise an exception if one is missing
        for arg_name in ['playername', 'observationNumber']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(self.__class__.__name__, arg_name) from None

        # TODO: Validate the passed arguments
        self._playername = kwargs['playername']
        self._participant_id = kwargs.get('participant_id', self._playername)
        self._observationNumber = kwargs['observationNumber']
        self._blocks = kwargs.get('blocks',[])

        ## TEMPORARY HACK SINCE FOV HAS CHANGED!
        ## TODO:  Need to fix the mixins so that id is correct!
        for block in self._blocks:
            if not 'id' in block:
                block['id'] = -1


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'FovSummary')
        """

        return self.__class__.__name__


#    def addHeader(self, name, data):
#        """
#        Add a header to the message.
#
#        Args
#            name - name of the header.  Must be a string
#            data - object containing the header data
#        """
#
#        # Don't bother if the header is None
#        if data is not None:
#            self.headers[name] = data

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
    def participant_id(self):
        """
        Get the participant_id whose FoV is summarized.

        Attempting to set `participant_id` raises an `ImmutableAttributeException`.
        """

        return self._participant_id

    @participant_id.setter
    def participant_id(self, _):
        raise ImmutableAttributeException(str(self), "participant_id")
   




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
    def blocks(self):
        """
        Get the list of block summaries

        Attempting to set `blocks` raises an `ImmutableAttributeException`.
        """

        return self._blocks

    @blocks.setter
    def blocks(self, block_list):
        raise ImmutableAttributeException(str(self), "blocks")



    def addBlock(self, summary):
        """
        Add a block to the list of blocks.

        Arguments
        ---------
        summary : dictionary
            key-value mapping of the name and value of the block summary
        """

        self._blocks.append(summary)


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the FoVSummary.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        jsonDict['data'] = {  'playername': self.playername,
                              'observation': self.observationNumber,
                              'blocks': self.blocks 
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
            FoVSummary message.
        """

        return json.dumps(self.toDict())        
