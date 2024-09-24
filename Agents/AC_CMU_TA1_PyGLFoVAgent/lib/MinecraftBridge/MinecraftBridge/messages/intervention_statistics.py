# -*- coding: utf-8 -*-
"""
.. module:: intervention_statistics
   :platform: Linux, Windows, OSX
   :synopsis: Class to encapsulate statistics about issued and discarded interventions

.. moduleauthor:: Simon Stepputts <sstepput@andrew.cmu.edu>

"""

from .base_message import BaseMessage
from .message_exceptions import MissingMessageArgumentException
from .message_exceptions import ImmutableAttributeException

import json

class InterventionStatistics(BaseMessage):
    """
    This class encapsualtes intervention statistics. 
    Fundamentally, this message reports the number of issued, resolved and discarded interventions.

    Attributes
    ----------
    issued : int
        Total number of issued interventions
    resolved : int
        Number of interventions that have been qued for resolution
    discarded : int
        Number of interventions that have been discarded and never needed to be resolved
    """
    def __init__(self, **kwargs):
        super(InterventionStatistics, self).__init__()
        
        # Grab the total number of interventions issued
        self._active = kwargs.get("active", None)
        if self._active is None:
            raise MissingMessageArgumentException(str(self), 'active') from None

        # Grab the number of resolved interventions
        self._resolved = kwargs.get("resolved", None)
        if self._resolved is None:
            raise MissingMessageArgumentException(str(self), 'resolved') from None

        # Grab the number of interventions that didn't need to be resolved
        self._discarded = kwargs.get("discarded", None)
        if self._discarded is None:
            raise MissingMessageArgumentException(str(self), 'discarded') from None

    @property
    def active(self):
        """
        Get the total number of created interventions

        Attempting to set `actuve` raises an `ImmutableAttributeException`.
        """

        return self._active

    @active.setter
    def active(self, val):
        raise ImmutableAttributeException(str(self), "active")

    @property
    def resolved(self):
        """
        Get the total number of interventions that were resolved

        Attempting to set `resolved` raises an `ImmutableAttributeException`.
        """

        return self._resolved

    @resolved.setter
    def resolved(self, val):
        raise ImmutableAttributeException(str(self), "resolved")

    @property
    def discarded(self):
        """
        Get the total number of interventions that have been discarded before needing to be resolved

        Attempting to set `discarded` raises an `ImmutableAttributeException`.
        """

        return self._discarded

    @discarded.setter
    def discarded(self, val):
        raise ImmutableAttributeException(str(self), "discarded")
    
    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ItemPickupEvent.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["issued"] = self._active
        jsonDict["data"]["resolved"] = self._resolved
        jsonDict["data"]["discarded"] = self._discarded

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
            ItemPickupEvent message.
        """

        return json.dumps(self.toDict())