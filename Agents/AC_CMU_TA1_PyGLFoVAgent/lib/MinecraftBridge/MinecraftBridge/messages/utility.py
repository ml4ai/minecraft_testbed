# -*- coding: utf-8 -*-
"""
.. module:: utility
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating PlayerUtility Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating PlayerUtility messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class PlayerUtility(BaseMessage):
    """
    A class encapsulating PlayerUtility messages.

    Attributes
    ----------
    participant_id : string
        ID of the participant whose utility is being reported
    utility : string
        Utility of the participant
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["utility"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        # NOTE: participant_id is not in the Spiral 2 metadata files, so assign
        #       "<UNKNOWN>" if it's missing

        self._participant_id = kwargs.get("participant_id", "<UNKNOWN>")
        self._utility = kwargs["utility"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentFeedback')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        ID of the participant whose utility is being reported

        Attemting to set `participant_id` raises an `ImmutableAttributeException`.
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, _):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def utility(self):
        """
        Utility of the participant

        Attemting to set `utility` raises an `ImmutableAttributeException`.
        """
        return self._utility

    @utility.setter
    def utility(self, _):
        raise ImmutableAttributeException(str(self), "utility")


    def toDict(self):
        """
        Generates a dictionary representation of the PlayerUtility message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PlayerUtility message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the utility data
        jsonDict["data"]["participant_id"] = self.participant_id
        jsonDict["data"]["utility"] = self.utility

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the PlayerUtility message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            PlayerUtility message.
        """

        return json.dumps(self.toDict())
