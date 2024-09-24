# -*- coding: utf-8 -*-
"""
.. module:: role_text
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating RoleText Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating RoleText messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class RoleText(BaseMessage):
    """
    A class encapsulating RoleText messages.

    Attributes
    ----------
    missionName : string
        Name of the mission
    transport_specialist_text : list of strings
        Text provided to the Transport Specialist
    medical_specialist_text : list of strings
        Text provided to the Medical Specialist
    engineering_specialist_text : list of strings
        Text provided to the Engineering Specialist
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["missionName", "transport_specialist_text",
                         "medical_specialist_text", "engineering_specialist_text"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._missionName = kwargs["missionName"]
        self._transport_specialist_text = kwargs["transport_specialist_text"]
        self._medical_specialist_text = kwargs["medical_specialist_text"]
        self._engineering_specialist_text = kwargs["engineering_specialist_text"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'RoleText')
        """

        return self.__class__.__name__


    @property
    def missionName(self):
        """
        Name of the mission

        Attemting to set `missionName` raises an `ImmutableAttributeException`.
        """
        return self._missionName

    @missionName.setter
    def missionName(self, _):
        raise ImmutableAttributeException(str(self), "missionName")


    @property
    def transport_specialist_text(self):
        """
        List of messages given to the transport specialist        

        Attemting to set `transport_specialist_text` raises an `ImmutableAttributeException`.
        """
        return self._transport_specialist_text

    @transport_specialist_text.setter
    def transport_specialist_text(self, _):
        raise ImmutableAttributeException(str(self), "transport_specialist_text")


    @property
    def medical_specialist_text(self):
        """
        List of messages given to the medical specialist

        Attemting to set `medical_specialist_text` raises an `ImmutableAttributeException`.
        """
        return self._medical_specialist_text

    @medical_specialist_text.setter
    def medical_specialist_text(self, _):
        raise ImmutableAttributeException(str(self), "medical_specialist_text")


    @property
    def engineering_specialist_text(self):
        """
        List of messages given to the engineering specialist

        Attemting to set `engineering_specialist_text` raises an `ImmutableAttributeException`.
        """
        return self._engineering_specialist_text

    @engineering_specialist_text.setter
    def engineering_specialist_text(self, _):
        raise ImmutableAttributeException(str(self), "engineering_specialist_text")


    def toDict(self):
        """
        Generates a dictionary representation of the RoleText message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the RoleText message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the role text data
        jsonDict["data"]["missionName"] = self.missionName
        jsonDict["data"]["transport_specialist_text"] = self.transport_specialist_text
        jsonDict["data"]["medical_specialist_text"] = self.medical_specialist_text
        jsonDict["data"]["engineering_specialist_text"] = self.engineering_specialist_text

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the RoleText message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            RoleText message.
        """

        return json.dumps(self.toDict())
