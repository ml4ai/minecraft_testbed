# -*- coding: utf-8 -*-
"""
.. module:: agent_intervention
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Intervention Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Intervention messages.
"""

import json
import uuid
from datetime import datetime

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class AgentIntervention(BaseMessage):
    """
    A class encapsulating Agent Intervention messages.

    Attributes
    ----------
    id : string
        A unique ID for the intervention
    source : string
        The name of the agent generating the intervention
    agent : string
        Alias of `source`
    created : string
        Timestamp (UCT) when the intervention was created
    start : tuple of ints
        Mission time (minutes, seconds) that the message is effective
    duration : double
        The length of time in seconds the intervention remains valid
    explanation : dictionary
        A dictionary with arbitrary entries for explanation
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["start", "duration"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._agent = kwargs.get("source", kwargs.get("agent", None))

        if self._agent is None:
            raise MissingMessageArgumentException(str(self),
                                                  "source") from None

        self._start = kwargs["start"]
        self._duration = kwargs["duration"]
        self._explanation = kwargs.get("explanation", {})
        self._id = kwargs.get("id", str(uuid.uuid4()))
        self._created = kwargs.get("created", datetime.utcnow().isoformat(timespec='milliseconds'))


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentIntervention')
        """

        return self.__class__.__name__


    @property
    def id(self):
        """
        Get the unique id of the intervention.  

        Attempting to set `id` raises an `ImmutableAttributeException`.
        """

        return self._id

    @id.setter
    def id(self, id):
        raise ImmutableAttributeException(str(self), "id")


    @property
    def source(self):
        """
        Get the name of the agent.  

        Attempting to set `source` raises an `ImmutableAttributeException`.
        """

        return self._agent

    @source.setter
    def source(self, name):
        raise ImmutableAttributeException(str(self), "source")


    @property
    def agent(self):
        """
        Alias of `source`
        """

        return self._agent

    @agent.setter
    def agent(self, name):
        raise ImmutableAttributeException(str(self), "agent")


    @property
    def created(self):
        """
        Get the creation time of the intervention.  

        Attempting to set `created` raises an `ImmutableAttributeException`.
        """

        return self._created

    @created.setter
    def created(self, time):
        raise ImmutableAttributeException(str(self), "created")


    @property
    def start(self):
        """
        Get the time the intervention is valid.  

        Attempting to set `start` raises an `ImmutableAttributeException`.
        """

        return self._start

    @start.setter
    def start(self, time):
        raise ImmutableAttributeException(str(self), "start")


    @property
    def duration(self):
        """
        Get the amount of time the intervention is valid.  

        Attempting to set `duration` raises an `ImmutableAttributeException`.
        """

        return self._duration

    @duration.setter
    def duration(self, time):
        raise ImmutableAttributeException(str(self), "duration")


    @property
    def explanation(self):
        """
        Get the explanation of the intervention.  

        Attempting to set `explanation` raises an `ImmutableAttributeException`.
        """

        return self._explanation

    @explanation.setter
    def explanation(self, explanation):
        raise ImmutableAttributeException(str(self), "explanation")


    def toDict(self):
        """
        Generates a dictionary representation of the AgentIntervention message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentIntervention message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the intervention data
        jsonDict["data"]["id"] = self.id
        jsonDict["data"]["source"] = self.source
        jsonDict["data"]["created"] = str(self.created) + "Z"
        jsonDict["data"]["start"] = self.start
        jsonDict["data"]["duration"] = self.duration
        jsonDict["data"]["explanation"] = self.explanation

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the AgentIntervention message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentIntervention message.
        """

        return json.dumps(self.toDict())






class AgentChatIntervention(AgentIntervention):
    """
    A class encapsulating Chat Intervention messages.  Chat Intervention
    messages inherit attributes of AgentIntervention messages.

    Attributes
    ----------
    content : string
        Message from the agent to display
    receiver : string, default="broadcast"
        Name of the participant id, or "broadcast" if the message should be
        sent to all participants
    type : enum ["json", "string", "HTML", "block"], default="string"
        Type of data to be displayed
    renderer : string ["Minecraft_Chat", "Minecraft_Block", "Client_Map"], default="Minecraft_Chat"
        Renderer used to display the content
    """

    def __init__(self, **kwargs):

        AgentIntervention.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["content"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._content = kwargs["content"]
        self._receiver = kwargs.get("receivers", kwargs.get("receiver", []))
        self._type = kwargs.get("type", "string")
        self._renderer = kwargs.get("renderers", kwargs.get("renderer", ["Minecraft_Chat"]))


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentChatIntervention')
        """

        return self.__class__.__name__


    @property
    def content(self):
        """
        Get the content of the intervention.  

        Attempting to set `content` raises an `ImmutableAttributeException`.
        """

        return self._content

    @content.setter
    def content(self, text):
        raise ImmutableAttributeException(str(self), "content")


    @property
    def receiver(self):
        """
        Get the receiver of the intervention.  

        Attempting to set `receiver` raises an `ImmutableAttributeException`.
        """

        return self._receiver

    @receiver.setter
    def receiver(self, participant):
        raise ImmutableAttributeException(str(self), "receiver")


    @property
    def type(self):
        """
        Get the type of the intervention.  

        Attempting to set `type` raises an `ImmutableAttributeException`.
        """

        return self._type

    @type.setter
    def type(self, type):
        raise ImmutableAttributeException(str(self), "type")


    @property
    def renderer(self):
        """
        Get the renderer to display the content

        Attempting to set `renderer` raises an `ImmutableAttributeException`.
        """

        return self._renderer

    @renderer.setter
    def renderer(self, renderer):
        raise ImmutableAttributeException(str(self), "renderer")


    def toDict(self):
        """
        Generates a dictionary representation of the AgentChatIntervention message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ChatIntervention message.
        """

        jsonDict = AgentIntervention.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the intervention data
        jsonDict["data"]["content"] = self.content
        jsonDict["data"]["receivers"] = self.receiver
        jsonDict["data"]["type"] = self.type
        jsonDict["data"]["renderers"] = self.renderer

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the AgentChatIntervention message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentChatIntervention message.
        """

        return json.dumps(self.toDict())


