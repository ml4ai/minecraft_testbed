# -*- coding: utf-8 -*-
"""
.. module:: cmu_ta2_ted
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating IHMC Cognitive Load measures

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating IHMC Cognitive Load measures.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

from collections import namedtuple


class IHMC_CognitiveLoad(BaseMessage):
    """
    A class encapsulating Cognitive Load measure messages.

    Attributes
    ----------
    id : string
        UUID of the event
    agent : string
        Name of the agent who sent the message
    created : string
        Timestamp of when the data was generated
    cognitive_load : IHMC_CognitiveLoad.Measure
        Measure (value + confidence) of the cognitive load
    probability_of_forgetting : IHMC_CognitiveLoad.Measure
        Measure (value + confidence) of the probability of forgetting
    """

    Measure = namedtuple("Measure", ["value", "confidence"])

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["id", "agent", "created", "cognitive_load", 
                         "probability_of_forgetting"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        # Make sure that `cognitive_load` and `probability_of_forgetting` have
        # `value` and `confidence` subfields
        for arg_name in ["cognitive_load", "probability_of_forgetting"]:
            if not "value" in kwargs[arg_name] or not "confidence" in kwargs[arg_name]:
                raise MalformedMessageCreationException(str(self), arg_name,
                                                        kwargs[arg_name]) from None

        # Populate the fields
        self._id = kwargs["id"]
        self._agent = kwargs["agent"]
        self._created = kwargs["created"]
        self._cognitive_load = IHMC_CognitiveLoad.Measure(kwargs["cognitive_load"]["value"],
                                                          kwargs["cognitive_load"]["confidence"])
        self._probability_of_forgetting = IHMC_CognitiveLoad.Measure(kwargs["probability_of_forgetting"]["value"],
                                                                     kwargs["probability_of_forgetting"]["confidence"])



    @property
    def id(self):
        """

        Attempting to set `id` raises an `ImmutableAttributeException`
        """

        return self._id

    @id.setter
    def id(self, _):

        raise ImmutableAttributeException(self, "id")


    @property
    def agent(self):
        """

        Attempting to set `agent` raises an `ImmutableAttributeException`
        """

        return self._agent

    @agent.setter
    def agent(self, _):

        raise ImmutableAttributeException(self, "agent")


    @property
    def created(self):
        """

        Attempting to set `created` raises an `ImmutableAttributeException`
        """

        return self._created

    @created.setter
    def created(self, _):

        raise ImmutableAttributeException(self, "created")


    @property
    def cognitive_load(self):
        """

        Attempting to set `cognitive_load` raises an `ImmutableAttributeException`
        """

        return self._cognitive_load

    @cognitive_load.setter
    def cognitive_load(self, _):

        raise ImmutableAttributeException(self, "cognitive_load")


    @property
    def probability_of_forgetting(self):
        """

        Attempting to set `probability_of_forgetting` raises an `ImmutableAttributeException`
        """

        return self._probability_of_forgetting

    @probability_of_forgetting.setter
    def probability_of_forgetting(self, _):

        raise ImmutableAttributeException(self, "probability_of_forgetting")


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'IHMC_CognitiveLoad')
        """

        return self.__class__.__name__


    def toDict(self):
        """
        Generates a dictionary representation of the Cognitive Load message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Cognitive Load message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the Cognitive Load data
        jsonDict["data"]["id"] = self.id
        jsonDict["data"]["agent"] = self.agent
        jsonDict["data"]["created"] = self.created
        jsonDict["data"]["cognitive_load"] = { "value" : self.cognitive_load.value,
                                               "confidence": self.cognitive_load.confidence }
        jsonDict["data"]["probability_of_forgetting"] = { "value": self.probability_of_forgetting.value, 
                                                          "confidence": self.probability_of_forgetting.confidence }

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the Cognitive Load message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Cognitive Load message.
        """

        return json.dumps(self.toDict())
