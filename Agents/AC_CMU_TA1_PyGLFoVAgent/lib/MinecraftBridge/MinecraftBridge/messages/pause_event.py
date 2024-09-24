# -*- coding: utf-8 -*-
"""
.. module:: pause_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Pause Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Pause Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class PauseEvent(BaseMessage):
    """
    A class encapsulating PauseEvent messages.

    Attributes
    ----------
    paused : boolean
        Indicate if the game is paused (True) or unpaused (False)
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        paused : boolean
            Indicate if the message is for a pause (True) or unpause (False)
        """

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the `paused` argument is passed, raise an exception
        # if not
        try:
            self._paused = bool(kwargs["paused"])
        except KeyError:
            raise MissingMessageArgumentException(str(self), 
                                                  "paused") from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PauseEvent')
        """


        return self.__class__.__name__


    @property
    def paused(self):
        """
        Get whether the message is referring to a pause or unpause event.  
        Attempting to set the value of the `paused` will result in an 
        `ImmutableAttributeException` being raised.        
        """
        return self._paused

    @paused.setter
    def paused(self, paused):
        raise ImmutableAttributeException(str(self), "paused") from None
    


    def toDict(self):
        """
        Generates a dictionary representation of the PauseEvent message.  
        PauseEvent information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PauseEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the beep event data
        jsonDict["data"]["paused"] = self.paused

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the PauseEvent message.  PauseEvent
        information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            PauseEvent message.
        """

        return json.dumps(self.toDict())
