# -*- coding: utf-8 -*-
"""
.. module:: experiment
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Experiment messages.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Experiment messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class Experiment(BaseMessage):
    """
    A class encapsulating Experiment messages.

    Attributes
    ----------
    name : string
        A user friendly name for the experiment
    date : string
        The date and time that the experiment was created
    author : string
        Name of the author of the experiment
    mission : string
        Name of the mission associated with the experiment
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an exception if one is missing
        for arg_name in ['name', 'date', 'author', 'mission']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self),
                                                      arg_name) from None

        self._name = kwargs['name']
        self._date = kwargs['date']
        self._author = kwargs['author']
        self._mission = kwargs['mission']


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'Experiment')        
        """

        return self.__class__.__name__


    @property
    def name(self):
        """
        Get the name of the experiment.  Attempting to set the value of `name`
        will result in an `ImmutableAttributeException` being raised.
        """
        return self._name

    @name.setter
    def name(self, name):
        raise ImmutableAttributeException(str(self), "name") from None


    @property
    def date(self):
        """
        Get the date the experiment was created.  Attempting to set the value
        of `date` will result in an `ImmutableAttributeException` being raised.
        """
        return self._date

    @date.setter
    def date(self, date):
        raise ImmutableAttributeException(str(self), "date") from None


    @property
    def author(self):
        """
        Get the author of the experiment.  Attempting to set the value of 
        `author` will result in an `ImmutableAttributeException` being raised.
        """        
        return self._author

    @author.setter
    def author(self, author):
        raise ImmutableAttributeException(str(self), "author") from None


    @property
    def mission(self):
        return self._mission

    @mission.setter
    def mission(self, mission):
        """
        Get the mission associated with the experiment.  Attempting to set the 
        value of `mission` will result in an `ImmutableAttributeException` 
        being raised.
        """        
        raise ImmutableAttributeException(str(self), "mission") from None
        

    def toDict(self):
        """
        Generates a dictionary representation of the Experiment message.  
        Experiment information is contained in a dictionary under the key 
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Experiment.
        """

        jsonDict = BaseMessage.toDict(self)
    
        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the beep event data
        jsonDict["data"]["name"] = self.name
        jsonDict["data"]["date"] = self.date
        jsonDict["data"]["author"] = self.author
        jsonDict["data"]["mission"] = self.mission

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the Experiment message.  Experiment
        information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Experiment message.
        """

        return json.dumps(self.toDict())
