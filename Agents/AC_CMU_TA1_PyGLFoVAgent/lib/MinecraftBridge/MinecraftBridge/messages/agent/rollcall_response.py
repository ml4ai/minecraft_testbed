# -*- coding: utf-8 -*-
"""
.. module:: rollcall_response
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Rollcall Responses

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Rollcall Response messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class RollcallResponse(BaseMessage):
    """
    A class encapsulating Rollcall Response messages.

    Attributes
    ----------
    rollcall_id : string
        The ID of the rollcall request
    version : string
        The version of the responding component
    status : enum
        Status of the component
    uptime : int
        number of seconds that the component has been up
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["rollcall_id", "version", "status", "uptime"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._rollcall_id = kwargs["rollcall_id"]
        self._version = kwargs["version"]
        self._status = kwargs["status"]
        self._agent_type = kwargs.get("agent_type", "ASI")

        # Try to coerce the uptime into an integer
        try:
            self._uptime = int(kwargs["uptime"])
        except:
            raise MalformedMessageCreationException(str(self),
                                                    "uptime",
                                                    kwargs["uptime"]) from None


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
        Get the ID of the rollcall response

        Attempting to set `rollcall_id` raises an `ImmutableAttributeException`.
        """

        return self._rollcall_id

    @rollcall_id.setter
    def rollcall_id(self, name):
        raise ImmutableAttributeException(str(self), "rollcall_id")


    @property
    def version(self):
        """
        Get the version of the component generating the response

        Attempting to set `version` raises an `ImmutableAttributeException`.
        """

        return self._version

    @version.setter
    def version(self, _):
        raise ImmutableAttributeException(str(self), "version")


    @property
    def status(self):
        """
        Get the status of the component generating the response

        Attempting to set `status` raises an `ImmutableAttributeException`.
        """

        return self._status

    @status.setter
    def status(self, _):
        raise ImmutableAttributeException(str(self), "status")


    @property
    def uptime(self):
        """
        Get the number of seconds the component has been running

        Attempting to set `uptime` raises an `ImmutableAttributeException`.
        """
        return self._uptime

    @uptime.setter
    def uptime(self, _):
        raise ImmutableAttributeException(str(self), "uptime")


    @property
    def agent_type(self):
        """
        Get the type of agent generating this response

        Attempting to set `agent_type` raises and `ImmutableAttributeException`.
        """
        return self._agent_type

    @agent_type.setter
    def agent_type(self, _):
        raise ImmutableAttributeException(str(self), "agent_type")
    


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
        jsonDict["data"]["status"] = self.status
        jsonDict["data"]["uptime"] = self.uptime
        jsonDict["data"]["version"] = self.version
        jsonDict["data"]["agent_type"] = self.agent_type


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
