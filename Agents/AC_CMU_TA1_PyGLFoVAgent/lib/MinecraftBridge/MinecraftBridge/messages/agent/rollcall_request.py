# -*- coding: utf-8 -*-
"""
.. module:: rollcall_request
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Rollcall Requests

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Rollcall Request messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class RollcallRequest(BaseMessage):
    """
    A class encapsulating Rollcall Request messages.

    Attributes
    ----------
    rollcall_id : string
        The ID of teh rollcall request
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        if not "rollcall_id" in kwargs:
            raise MissingMessageArgumentException(str(self), 
                                                  "rollcall_id") from None

        self._rollcall_id = kwargs["rollcall_id"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentVersionInfo')
        """

        return self.__class__.__name__


    @property
    def rollcall_id(self):
        """
        Get the ID of the rollcall request

        Attempting to set `rollcall_id` raises an `ImmutableAttributeException`.
        """

        return self._rollcall_id

    @rollcall_id.setter
    def rollcall_id(self, name):
        raise ImmutableAttributeException(str(self), "rollcall_id")


    def toDict(self):
        """
        Generates a dictionary representation of the Rollcall Request message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Rollcall Request message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the rollcall id to data
        jsonDict["data"]["rollcall_id"] = self.rollcall_id

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the Rollcall Request message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Rollcall Request message.
        """

        return json.dumps(self.toDict())
