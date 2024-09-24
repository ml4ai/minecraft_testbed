# -*- coding: utf-8 -*-
"""
.. module:: user_speech
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating UserSpeech information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating UserSpeech messages.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class UserSpeech(BaseMessage):
    """
    A class encapsulating UserSpeech messages.

    Attributes
    ----------
    playername : string
        Name of the player who spoke
    text : string
        Text of the player speech

    """

    def __init__(self, **kwargs):
        """

        """

        BaseMessage.__init__(self, **kwargs)

        # Check that the needed arguments were provided
        if not "playername" in kwargs:
            raise MissingMessageArgumentException(str(self), "playername") from None

        if not "text" in kwargs:
            raise MissingMessageArgumentException(str(self), "text") from None

        self._playername = kwargs["playername"]
        self._text = kwargs["text"]



    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PlayerState')
        """

        return self.__class__.__name__



    @property
    def playername(self):
        """
        Get the name of the player.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def (self, _):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def text(self):
        """
        Get the text of the speech.  

        Attempting to set `text` raises an `ImmutableAttributeException`.
        """

        return self._text

    @text.setter
    def (self, _):
        raise ImmutableAttributeException(str(self), "text")

 

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the UserSpeech.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["text"] = self.text


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
            UserSpeech message.
        """

        return json.dumps(self.toDict())
