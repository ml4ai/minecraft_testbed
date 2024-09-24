# -*- coding: utf-8 -*-
"""
.. module:: agent_version_info
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Version Information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Version Info messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class AgentVersionInfo(BaseMessage):
    """
    A class encapsulating Agent Version Info messages.

    Attributes
    ----------
    agent_name : string
        The name of the agent
    agent_type : string
        The type of the agent
    version : string
        The version number of the agent
    owner : string
        The name of the person / organization that supports the agent
    source : list of strings
        A list of URLs where the agent was obtained from
    dependences : list of strings
        A list of the dependent components of the agent
    config : dictionary of configuration values
        A list of configuration parameters
    publishes : list of (topic, message_type, message_subtype) tuple
        A list of messages the agent publishes
    subscribes : list of (topic, message_type, message_subtype) tuple
        A list of messages the agent subscribes to
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["agent_name", "version", "owner"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._agent_name = kwargs["agent_name"]
        self._agent_type = kwargs.get("agent_type", "other")
        self._version = kwargs["version"]
        self._owner = kwargs["owner"]
        self._source = kwargs.get("source", [])
        self._dependencies = kwargs.get("dependencies", [])
        self._config = kwargs.get("config", {})
        self._publishes = kwargs.get("publishes", [])
        self._subscribes = kwargs.get("subscribes", [])

        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentVersionInfo')
        """

        return self.__class__.__name__


    @property
    def agent_name(self):
        """
        Get the name of the agent.  

        Attempting to set `agent_name` raises an `ImmutableAttributeException`.
        """

        return self._agent_name

    @agent_name.setter
    def agent_name(self, name):
        raise ImmutableAttributeException(str(self), "agent_name")


    @property
    def agent_type(self):
        """
        Get the type of the agent.

        Attempting to set `agent_type` raises an `ImmutableAttributeException`.
        """

        return self._agent_type

    @agent_type.setter
    def agent_type(self, _):
        raise ImmutableAttributeException(str(self), "agent_type")
    

    @property
    def version(self):
        """
        Get the version string of the agent.  

        Attempting to set `version` raises an `ImmutableAttributeException`.
        """

        return self._version

    @version.setter
    def version(self, version):
        raise ImmutableAttributeException(str(self), "version")


    @property
    def source(self):
        """
        Get the list of URLs where the agent can be obtained.  

        Attempting to set `source` raises an `ImmutableAttributeException`.
        """

        return self._source

    @source.setter
    def source(self, urls):
        raise ImmutableAttributeException(str(self), "source")


    @property
    def dependencies(self):
        """
        Get the list of dependencies of the agent.  

        Attempting to set `dependencies` raises an `ImmutableAttributeException`.
        """

        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        raise ImmutableAttributeException(str(self), "dependencies")


    @property
    def config(self):
        """
        Get the dictionary of configuration values.  

        Attempting to set `config` raises an `ImmutableAttributeException`.
        """

        return self._config

    @config.setter
    def config(self, config):
        raise ImmutableAttributeException(str(self), "config")


    @property
    def publishes(self):
        """
        Get the list of messages that the agent publishes.  

        Attempting to set `publishes` raises an `ImmutableAttributeException`.
        """

        return self._publishes

    @publishes.setter
    def publishes(self, publishes):
        raise ImmutableAttributeException(str(self), "publishes")


    @property
    def subscribes(self):
        """
        Get the list of messages that the agent subscribes to.  

        Attempting to set `subscribes` raises an `ImmutableAttributeException`.
        """

        return self._subscribes

    @subscribes.setter
    def subscribes(self, subscribes):
        raise ImmutableAttributeException(str(self), "subscribes")


    @property
    def owner(self):
        """
        Get the person / organization that supports this agent.  

        Attempting to set `owner` raises an `ImmutableAttributeException`.
        """

        return self._owner

    @owner.setter
    def owner(self, owner):
        raise ImmutableAttributeException(str(self), "owner")


    def addConfig(self, name, value):
        """
        Add a configuration value to the message

        Parameters
        ----------
        name : string
            Name of the configuration parameter
        value
            value of the configuration parameter (will be cast as a string)
        """

        # Check if the message is finalized, and if so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "config (via addConfig)") from None

        # Otherwise, feel free to add scores
        self._config[name] = str(value)


    def addSource(self, url):
        """
        Add a URL where the agent can be obtained

        Parameters
        ----------
        url : string
            URL where the agent can be obtained
        """

        # Check if the message is finalized, and if so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "source (via addSource)") from None

        self._source.append(url)


    def addDependency(self, url):
        """
        Add a URL of a dependency of the agent

        Parameters
        ----------
        url : string
            URL of the dependency
        """

        # Check if the message is finalized, and if so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "dependencies (via addDependency)") from None

        self._dependencies.append(url)


    def addPublishInfo(self, topic, message_type, message_subtype):
        """
        Add message info for a message type that the agent publishes.

        Parameters
        ----------
        topic : string
            Topic the agent publishes to
        message_type : string
            message type of the published message
        message_subtype : string
            subtype of the published message
        """

         # Check if the message is finalized, and if so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "publishes (via addPublishInfo)") from None

        self._publishes.append((topic, message_type, message_subtype))


    def addSubscribeInfo(self, topic, message_type, message_subtype):
        """
        Add message info for a message type that the agent subscribes.

        Parameters
        ----------
        topic : string
            Topic the agent publishes to
        message_type : string
            message type of the published message
        message_subtype : string
            subtype of the published message
        """

         # Check if the message is finalized, and if so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "subscribes (via addSubscribesInfo)") from None

        self._subscribes.append((topic, message_type, message_subtype))


    def finalize(self):
        """
        Finalize the message instance, so no new scores can be added.
        """

        self._finalized = True


    def toDict(self):
        """
        Generates a dictionary representation of the AgentVersionInfo message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentVersionInfo message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["agent_name"] = self.agent_name
        jsonDict["data"]["version"] = self.version
        jsonDict["data"]["owner"] = self.owner
        jsonDict["data"]["source"] = self.source
        jsonDict["data"]["dependencies"] = self.dependencies
        jsonDict["data"]["config"] = [{"name": name, "value": value} for name,value in self.config.items()]
        jsonDict["data"]["publishes"] = [{"topic": info[0], "message_type": info[1], "sub_type": info[2]} for info in self.publishes]
        jsonDict["data"]["subscribes"] = [{"topic": info[0], "message_type": info[1], "sub_type": info[2]} for info in self.subscribes]

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the AgentVersionInfo message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentVersionInfo message.
        """

        return json.dumps(self.toDict())
