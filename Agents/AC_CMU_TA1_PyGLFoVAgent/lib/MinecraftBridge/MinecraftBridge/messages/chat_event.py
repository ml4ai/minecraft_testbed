# -*- coding: utf-8 -*-
"""
.. module:: chat_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Chat Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Chat Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class ChatEvent(BaseMessage):
    """
    A class encapsulating Chat Event messages.

    Attributes
    ----------
    sender : string
        The name of the sender
    addressees : tuple of strings
        The list of addressee names
    text : string
        The text of the chat message
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        sender : string
            The name of the sender
        addressees : tuple of strings
            The list of addressee names
        text : string
            The text of the chat message
        """

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ['sender', 'addressees', 'text']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                    arg_name) from None

        self._sender = kwargs['sender']

        # Cast the addressees as a tuple, so that client code cannot modify the
        # list of attendees.  Also, make sure that the addressees isn't passed
        # as a string
        if isinstance(kwargs['addressees'], str):
            raise MalformedMessageCreationException(str(self), 'addressees',
                                                    kwargs['addressees']) from None
        try:
            self._addressees = tuple(kwargs['addressees'])
        except:
            raise MalformedMessageCreationException(str(self), 'addressees',
                                                    kwargs['addressees']) from None

        self._text = kwargs['text']


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ChatEvent')        
        """

        return self.__class__.__name__


    @property
    def sender(self):
        """
        Get the name of the sender of the chat.  Attempting to set the value of
        the `sender` will result in an `ImmutableAttributeException` being
        raised.
        """
        return self._sender

    @sender.setter
    def sender(self, sender):
        raise ImmutableAttributeException(str(self), "sender") from None


    @property
    def addressees(self):
        """
        Get the list of addressee names of the chat.  Attempting to set the 
        value of the `addressees` will result in an 
        `ImmutableAttributeException` being raised.
        """
        return self._addressees

    @addressees.setter
    def addressees(self, addressees):
        raise ImmutableAttributeException(str(self), "addressees") from None
    

    @property
    def text(self):
        """
        Get the text of the chat.  Attempting to set the value of the `text`
        will result in an `ImmutableAttributeException` being raised.
        """
        return self._text

    @text.setter
    def text(self, sender):
        raise ImmutableAttributeException(str(self), "text") from None


    def toDict(self):
        """
        Generates a dictionary representation of the ChatEvent message.  
        ChatEvent information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ChatEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the beep event data
        jsonDict["data"]["sender"] = self.sender
        jsonDict["data"]["addressees"] = self.addressees
        jsonDict["data"]["text"] = self.text

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the ChatEvent message.  ChatEvent
        information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            BeepEvent message.
        """

        return json.dumps(self.toDict())
