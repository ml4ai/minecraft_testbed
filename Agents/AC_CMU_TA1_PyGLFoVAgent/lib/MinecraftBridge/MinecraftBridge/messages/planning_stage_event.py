# -*- coding: utf-8 -*-
"""
.. module:: planning_stage_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating messages related to the start and
              stop of a planning phase

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Message class encapsulating messages related to the start and stop of a 
planning phase.
"""

import json
import enum

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class PlanningStageEvent(BaseMessage):
    """
    A class encapsulating Planning Stage Event messages.

    Attributes
    ----------
    state : instance of PlanningState
        State of the planning stage ("Start / Stop")
    """

    class PlanningState(enum.Enum):
        """
        Enumeration of possible planning stage states.
        """

        Start = "Start",
        Stop = "Stop"



    def __init__(self, **kwargs):
        """
        """

        BaseMessage.__init__(self, **kwargs)

        # Set the planning stage state
        state = kwargs.get('state', None)
        if state is None:
            raise MissingMessageArgumentException(str(self), 'state') from None

        # Try to coerce the provided state into the enumeration, raising an 
        # exception if not possible
        try:
            self._state = PlanningStageEvent.PlanningState[state]
        except KeyError:
            raise MalformedMessageCreationException(str(self), 'state',
                                                    state) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'MissionStateEvent')
        """

        return self.__class__.__name__


    @property
    def state(self):
        """
        Get the state of the planning phase (Start / Stop).  Attempting to set 
        the value of `state` will result in an `ImmutableAttributeException` 
        being raised.        
        """

        return self._state

    @state.setter
    def state(self, state):
        raise ImmutableAttributeException(str(self), "state")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PlanningStageEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the state event data
        jsonDict["data"]["state"] = self.state.value

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
            PlanningStageEvent message.
        """

        return json.dumps(self.toDict())
