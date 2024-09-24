# -*- coding: utf-8 -*-
"""
.. module:: #####
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating ##### Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating ##### messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class #####(BaseMessage):
    """
    A class encapsulating ##### messages.

    Attributes
    ----------

    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in []:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., '#####')
        """

        return self.__class__.__name__


    @property
    def (self):
        """
        

        Attemting to set `#####` raises an `ImmutableAttributeException`.
        """
        return self._

    @.setter
    def (self, _):
        raise ImmutableAttributeException(str(self), "")



    def toDict(self):
        """
        Generates a dictionary representation of the ##### message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ##### message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"][] = 

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the ##### message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            ##### message.
        """

        return json.dumps(self.toDict())
