# -*- coding: utf-8 -*-
"""
.. module:: status
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Heartbeat messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Heartbeat messages.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class Status(BaseMessage):
    """
    A class encapsulating status (heartbeat) messages.


    Attributes
    ----------
    state : Status.State
        state of the agent
    status : string, optional
        message providing detail about the status of the component
    active : boolean, optional
        message indicating if the component is actively functioning
    """


    class State(enum.Enum):
        """
        Enumeration of Status.State
        """

        OK = "ok"
        INFO = "info"
        WARN = "warn"
        ERROR = "error"
        FAIL = "fail"


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the "state" arguments have been passed, raise an 
        # exception if one is missing
        if not 'state' in kwargs:
            raise MissingMessageArgumentException(str(self), 
                                                  'state') from None

        # The 'state' argument must conform to one of the enumerated types
        try:
            self._state = Status.State(kwargs["state"])
        except:
            raise MalformedMessageCreationException(str(self), "state", 
                                                    kwargs["state"]) from None

        self._status = kwargs.get("status", "")
        self._active = kwargs.get("active", True)


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'WoofEvent')
        """

        return self.__class__.__name__


    @property
    def state(self):
        """
        Get the name of the state of the status.  Attempting to set the value 
        of `state` will raise an `ImmutableAttributeException`.
        """

        return self._state

    @state.setter
    def state(self, _):
        raise ImmutableAttributeException(str(self), "state") from None


    @property
    def status(self):
        """
        Get the status message.  Attempting to set `status` will raise an 
        `ImmutableAttributeException`.
        """

        return self._status

    @status.setter
    def status(self, _):
        raise ImmutableAttributeException(str(self), "status") from None


    @property
    def active(self):
        """
        Get whether the status is active.  Attempting to set `active` will 
        raise an `ImmutableAttributeException`.
        """

        return self._active

    @active.setter
    def active(self, _):
        raise ImmutableAttributeException(str(self), "active") from None


    def toDict(self):
        """
        Generates a dictionary representation of the Status message.  
        Status information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Status.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the status data
        jsonDict["data"]["state"] = self.state.value
        jsonDict["data"]["status"] = self.status
        jsonDict["data"]["active"] = self.active
        
        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the Status message.  Status
        information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Status message.
        """

        return json.dumps(self.toDict())
