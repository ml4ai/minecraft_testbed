# -*- coding: utf-8 -*-
"""
.. module:: perturbation_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating PerturbationEvent Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating PerturbationEvent messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class PerturbationEvent(BaseMessage):
    """
    A class encapsulating ##### messages.

    Attributes
    ----------
    type : string
        Name of perturbation type ["blackout", "rubble"]
    state : string
        state of the perturbation ["start", "stop"]
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_group in [{"type"}, {"state", "mission_state"}]:
            if not any(arg_name in kwargs for arg_name in arg_group):
                raise MissingMessageArgumentException(str(self), arg_group) from None

        self._type = kwargs["type"]
        self._state = kwargs.get("mission_state", kwargs.get("state"))


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PerturbationEvent')
        """

        return self.__class__.__name__


    @property
    def type(self):
        """
        Tpe of perturbation (blackout / rubble)

        Attemting to set `type` raises an `ImmutableAttributeException`.
        """
        return self._type

    @type.setter
    def type(self, _):
        raise ImmutableAttributeException(str(self), "type")


    @property
    def state(self):
        """
        State of the perturbation (start / stop)        

        Attemting to set `state` raises an `ImmutableAttributeException`.
        """
        return self._state

    @state.setter
    def state(self, _):
        raise ImmutableAttributeException(str(self), "state")


    def toDict(self):
        """
        Generates a dictionary representation of the PerturbationEvent message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PerturbationEvent message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the event data
        jsonDict["data"]["type"] = self.type
        jsonDict["data"]["state"] = self.state

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the PerturbationEvent message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            ##### message.
        """

        return json.dumps(self.toDict())
