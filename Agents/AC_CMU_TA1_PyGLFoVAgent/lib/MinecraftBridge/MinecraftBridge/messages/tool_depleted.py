# -*- coding: utf-8 -*-
"""
.. module:: tool_depleted
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Tool Depleted Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Tool Depleted Event messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class ToolDepletedEvent(BaseMessage):
    """
    A class encapsulating ToolDepletedEvent messages.

    Attributes
    ----------
    playername : string
        The name of the player whose tool was depleted
    tool_type : string
        The type of tool depleted
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        playername : string
            The name of the player whose tool was depleted
        tool_type : string
            The type of tool depleted
        """

        BaseMessage.__init__(self, **kwargs)

        # Get the playername.  Note that this may have been renamed as
        # participant id, so try that if playername is not provided
        self._playername = kwargs.get('playername', 
                           kwargs.get('participant_id', None))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  'playername') from None

        try:
            self._tool_type = kwargs["tool_type"]
        except KeyError:
            raise MissingMessageArgumentException(str(self),
                                                  "tool_type") from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ToolDepletedEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player using the tool.  Attempting to set the value
        of `playername` will result in an `ImmutableAttributeException` being 
        raised.        
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def tool_type(self):
        """
        Get the type of tool used by the player.  Attempting to set the value
        of `tool_type` will result in an `ImmutableAttributeException` being 
        raised.        
        """

        return self._tool_type

    @tool_type.setter
    def tool_type(self, tool):
        raise ImmutableAttributeException(str(self), "tool_type")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ToolDepletedEvent message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["tool_type"] = self.tool_type


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
            ToolDepletedEvent message.
        """

        return json.dumps(self.toDict())
