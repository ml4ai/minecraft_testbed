# -*- coding: utf-8 -*-
"""
.. module:: mission_state
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Mission State information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Mission State messages.
"""

import json
import enum

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class MissionStateEvent(BaseMessage):
    """
    A class encapsulating Mission State Event messages.

    Note
    ----
    Constructing a MissionStateEvent message requires passing the following keyword
    argument:

        `state`

    While an alias exists for this attribute, it is currently not accepted
    as constructor parameters.

    Attributes
    ----------
    mission : string
        The name of the mission, referencing the map name and variant
    state : instance of MissionState
        State of the mission ("Start / Stop")
    mission_state : instance of MissionState
        Alias of `state`
    """

    class MissionState(enum.Enum):
        """
        Enumeration of possible mission states.
        """

        START = "START",
        STOP = "STOP",
        Start = "Start",
        Stop = "Stop"

        def is_start_state(self):
            return self in {
                MissionStateEvent.MissionState.START,
                MissionStateEvent.MissionState.Start,
            }

        def is_stop_state(self):
            return self in {
                MissionStateEvent.MissionState.STOP,
                MissionStateEvent.MissionState.Stop,
            }



    def __init__(self, **kwargs):
        """
        Construction of a MessageState instance can be done either using 
        `mission_state` or `state` as keyword arguments to indicate whether the
        mission starts or stops.  `state` will only be used if `mission_state`
        is not provided.

        Keyword Arguments
        -----------------
        mission : string
            Name of the mission, generally referring to the map name and
            variant
        mission_state : MissionState
        state : MissionState
            State of the mission ('Start' / 'Stop')
        """

        BaseMessage.__init__(self, **kwargs)

        # Set the mission state, using `mission_state` if available, `state`
        # otherwise.  If neither are present, throw an exception
        state = kwargs.get('mission_state', kwargs.get('state', None))
        if state is None:
            raise MissingMessageArgumentException(str(self),
                                                  'mission_state') from None

        # Try to coerce the provided state into the enumeration, raising an 
        # exception if not possible
        try:
            self._state = MissionStateEvent.MissionState[state]
        except KeyError:
            raise MalformedMessageCreationException(str(self), 'mission_state',
                                                    state) from None

        try:
            self._mission = kwargs["mission"]
        except KeyError:
            raise MissingMessageArgumentException(str(self),
                                                  "misison") from None


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
    def mission(self):
        """
        Get the name of the mission.  Attempting to set the value of `mission`
        will result in an `ImmutableAttributeException` being raised.        
        """

        return self._mission

    @mission.setter
    def mission(self, mission):
        raise ImmutableAttributeException(str(self), "mission")


    @property
    def state(self):
        """
        Get the state of the mission (START / STOP).  Attempting to set the
        value of `state` will result in an `ImmutableAttributeException` 
        being raised.        
        """

        return self._state

    @state.setter
    def state(self, state):
        raise ImmutableAttributeException(str(self), "state")


    @property
    def mission_state(self):
        """
        Alias of `state`
        """
        return self._state

    @mission_state.setter
    def mission_state(self, state):
        raise ImmutableAttributeException(str(self), "mission_state")
       

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the MissionStateEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the mission state event data
        jsonDict["data"]["mission"] = self.mission
        jsonDict["data"]["mission_state"] = self.mission_state.value

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
            MissionStateEvent message.
        """

        return json.dumps(self.toDict())
