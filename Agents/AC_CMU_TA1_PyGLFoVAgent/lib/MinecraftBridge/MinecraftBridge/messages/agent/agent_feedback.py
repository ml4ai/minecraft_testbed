# -*- coding: utf-8 -*-
"""
.. module:: agent_feedback
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Feedback Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Feedback messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class AgentFeedback(BaseMessage):
    """
    A class encapsulating Agent Feedback messages.

    Attributes
    ----------
    participant_id : string
        The id of the participant providing the feedback
    feedback_type : string
        The type of feedback requested
    feedback_text : string
        The content of the feedback (if text)
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["participant_id", "feedback_type", "feedback_text"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._participant_id = kwargs["participant_id"]
        self._feedback_type = kwargs["feedback_type"]
        self._feedback_text = kwargs["feedback_text"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentFeedback')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        ID of the participant providing feedback.

        Attemting to set `participant_id` raises an `ImmutableAttributeException`.
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, _):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def feedback_type(self):
        """
        Type of feedback provided.

        Attemting to set `feedback_type` raises an `ImmutableAttributeException`.
        """
        return self._feedback_type

    @feedback_type.setter
    def feedback_type(self, _):
        raise ImmutableAttributeException(str(self), "feedback_type")


    @property
    def feedback_text(self):
        """
        Text of feedback provided.

        Attemting to set `feedback_text` raises an `ImmutableAttributeException`.
        """
        return self._feedback_text

    @feedback_text.setter
    def feedback_text(self, _):
        return self._feedback_text
    

    def toDict(self):
        """
        Generates a dictionary representation of the AgentFeedback message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentFeedback message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["participant_id"] = self.participant_id
        jsonDict["data"]["feedback_type"] = self.feedback_type
        jsonDict["data"]["feedback_text"] = self.feedback_text

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the AgentFeedback message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentFeedback message.
        """

        return json.dumps(self.toDict())
