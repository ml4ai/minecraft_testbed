# -*- coding: utf-8 -*-
"""
.. module:: competency_task_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Competency Task Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Competency Task Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class CompetencyTaskEvent(BaseMessage):
    """
    A class encapsulating Competency Task Event messages.

    Note
    ----
    Constructing a CompetencyTaskEvent message requires passing the following 
    keyword argument:

        `taskMessage`

    While an alias exist for this attribute, it is currently not accepted as a 
    constructor parameter.

    Study 2 includes `playerName` and `callSign` in the messages; these are not
    included in the testbed repository MessageSpecs, so are included as
    optional.

    Attributes
    ----------
    taskMessage : string
        The message indicating the competency task status
    task_message : string
        Alias of `taskMessage`
    playerName : string, optional, default=None
        Name of the player performing the competency task
    callSign : string, optional, default=None
        Callsign of the player performing the competency task
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        task_message : string
        taskMessage : string
            Message indicating the competency task status
        playerName : string, optional, default=None
        playername : string, optional, default=None
        participant_id : string, optional, default=None
            Name of the player performing the competency task
        callSign : string, optional, default=None
        callsign : string, optional, default=None
            Callsign of the player performing the competency task
        """

        BaseMessage.__init__(self, **kwargs)

        self._taskMessage = kwargs.get('task_message', 
                            kwargs.get('taskMessage', None))

        if self._taskMessage is None:
            raise MissingMessageArgumentException(str(self), 
                                                  "task_message") from None

        self._playerName = kwargs.get('playerName', 
                           kwargs.get('playername',
                           kwargs.get('participant_id', None)))

        self._callSign = kwargs.get('callSign', 
                         kwargs.get('callsign', None))


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'CompetencyTaskEvent')
        """

        return self.__class__.__name__


    @property
    def taskMessage(self):
        """
        Get the task message.  Attempting to set the value of `taskMessage`
        will result in an `ImmutableAttributeException` being raised.
        """

        return self._taskMessage

    @taskMessage.setter
    def taskMessage(self, location):
        raise ImmutableAttributeException(str(self), "taskMessage") from None


    @property
    def task_message(self):
        """
        Alias for 'taskMessage'.
        """

        return self._taskMessage

    @task_message.setter
    def task_message(self, location):
        raise ImmutableAttributeException(str(self), "task_message") from None


    @property
    def playerName(self):
        """
        Get the name of the player.

        Attempting to set `playerName` raises an `ImmutableAttributeException`.
        """

        return self._playerName

    @playerName.setter
    def playerName(self, name):
        raise ImmutableAttributeException(str(self), "playerName") from None


    @property
    def callSign(self):
        """
        Get the call sign of the player.  

        Attempting to set `callSign` raises an `ImmutableAttributeException`.
        """

        return self._callSign

    @callSign.setter
    def callSign(self, name):
        raise ImmutableAttributeException(str(self), "callSign") from None


    def toDict(self):
        """
        Generates a dictionary representation of the CompetencyTaskEvent 
        message.  Competency Task information is contained in a dictionary
        under the key "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Competency Task Event.
        """


        # The CompetencyTaskEvent message does not contain mission_timer or 
        # elapsed_millisecond data, so should be omitted
        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the beep event data
        jsonDict["data"]["task_message"] = self.taskMessage
        if self.playerName is not None:
            jsonDict["data"]["playerName"] = self.playerName
        if self.callSign is not None:
            jsonDict["data"]["callSign"] = self.callSign

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the CompetencyTaskEvent message.  
        Comtetency Task information is contained in a JSON object under the key
        "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Competency Task Event message.
        """

        return json.dumps(self.toDict())
