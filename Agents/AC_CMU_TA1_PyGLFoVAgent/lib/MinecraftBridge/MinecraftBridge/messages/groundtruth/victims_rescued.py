# -*- coding: utf-8 -*-
"""
.. module:: victims_rescued
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Victims Rescued Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Victims Rescued Event messages.
"""

import json
import enum

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class VictimsRescued(BaseMessage):
    """
    A class encapsulating VictimsRescued messages.

    Attributes
    ----------
    message : string
        Message content indicating victims that have been rescued
    rescued_message : string
        Alias of `message`
    """



    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        self._message = kwargs.get('rescued_message',
                        kwargs.get('message', None))
        if self._message is None:
            raise MissingMessageArgumentException(str(self),
                                                  'rescued_message') from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'VictimRescued')
        """

        return self.__class__.__name__


    @property
    def message(self):
        """
        Get the message indicating the victims were rescued.  Attempting to set
        the value of `message` will result in an `ImmutableAttributeException` 
        being raised.
        """    
        return self._message

    @message.setter
    def message(self, message):
        raise ImmutableAttributeException(str(self), "message") from None


    @property
    def rescued_message(self):
        """
        Alias of `message`
        """    
        return self._message

    @rescued_message.setter
    def expired_message(self, message):
        raise ImmutableAttributeException(str(self), "rescued_message") from None


    def toJson(self):
        """
        Generates a dictionary representation of the VictimsRescued message.
        Message information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the VictimsRescued message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["rescued_message"] = self.rescued_message

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the VictimsRescued message.  
        VictimsRescued information is contained in a JSON object under the key
        "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            VictimsRescued message.
        """

        return json.dumps(self.toDict())