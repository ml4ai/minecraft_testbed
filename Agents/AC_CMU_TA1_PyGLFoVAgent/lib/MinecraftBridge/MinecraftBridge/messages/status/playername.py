# -*- coding: utf-8 -*-
"""
.. module:: playername
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating PlayerName messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating PlayerName messages.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class PlayerName(BaseMessage):
    """
    A class encapsulating playername messages.

    Attributes
    ----------
    playername : string
        The player name
    """

    def __init__(self, **kwargs):
        """

        """

        BaseMessage.__init__(self, **kwargs)

        if not "playername" in kwargs:
            raise MissingMessageArgumentException(str(self), "playername")

        self._playername = kwargs["playername"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PlayerName')
        """

        return self.__class__.__name__



    @property
    def playername(self):
        """
        Get the name of the player

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, _):
        raise ImmutableAttributeException(str(self), "playername")


 

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PlayerName message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername


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
            PlayerName message.
        """

        return json.dumps(self.toDict())
