# -*- coding: utf-8 -*-
"""
.. module:: victim_expired
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Victim Expired Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Victim Expired Event messages.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class VictimsExpired(BaseMessage):
    """
    A class encapsulating VictimExpired messages.

    Attributes
    ----------
    message : string
        Message content indicating victims that have expired
    expired_message : string
        Alias of `message`
    """



    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        expired_message : string
        message : string
            Message content indicating victims that have expired
        """

        BaseMessage.__init__(self, **kwargs)

        self._message = kwargs.get("expired_message",
                        kwargs.get("message", None))
        if self._message is None:
            raise MissingMessageArgumentException(str(self),
                                                  "expired_message") from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'VictimExpired')
        """

        return self.__class__.__name__


    @property
    def message(self):
        """
        Get the message indicating the victims expired.  Attempting to set the
        value of `message` will result in an `ImmutableAttributeException` 
        being raised.
        """    
        return self._message

    @message.setter
    def message(self, message):
        raise ImmutableAttributeException(str(self), "message") from None


    @property
    def expired_message(self):
        """
        Alias of `message`
        """    
        return self._message

    @expired_message.setter
    def expired_message(self, message):
        raise ImmutableAttributeException(str(self), "expired_message") from None


    def toJson(self):
        """
        Generates a dictionary representation of the VictimsExpired message.
        Message information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimsExpired message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["expired_message"] = self.expired_message

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the VictimsExpired message.  
        VictimsExpired information is contained in a JSON object under the key
        "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            VictimsExpired message.
        """

        return json.dumps(self.toDict())