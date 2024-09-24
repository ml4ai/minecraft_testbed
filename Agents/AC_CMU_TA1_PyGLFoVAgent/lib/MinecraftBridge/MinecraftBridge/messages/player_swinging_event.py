# -*- coding: utf-8 -*-
"""
.. module:: player_swinging_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Player Swinging Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Player Swinging Event messages.
"""
import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class PlayerSwingingEvent(BaseMessage):
    """
    A class encapsulating PlayerSwingingEvent messages.

    Attributes
    ----------
    playername : string
        Name of the player who jumped
    swinging : boolean
        Indicate if the player is swinging (True if swinging, False if not)      
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        playername : string
        participant_id : string
        name : string
            Name of the player who jumped
        swinging : boolean
            Indicate if the player is swinging (True) or not (False)
        """
        BaseMessage.__init__(self, **kwargs)

        self._playername = kwargs.get("playername",
                           kwargs.get("participant_id", 
                           kwargs.get("name", None)))
        if self._playername is None:
            raise MissingMessageArgumentException(str(self),
                                                  'playername') from None

        try:
            self._swinging = bool(kwargs["swinging"])
        except KeyError:
            raise MissingMessageArgumentException(str(self),
                                                  'swinging') from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PlayerSwingingEvent')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player who swinged.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def swinging(self):
        """
        Get whether the player is swinging (True) or stopped (False)

        Attempting to set `sprinting` raises an `ImmutableAttributeException`.
        """

        return self._swinging

    @swinging.setter
    def swinging(self, swinging):
        raise ImmutableAttributeException(str(self), "swinging")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PlayerSwingingEvent message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["swinging"] = self.swinging

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
            PlayerSwingingEvent message.
        """

        return json.dumps(self.toDict())
