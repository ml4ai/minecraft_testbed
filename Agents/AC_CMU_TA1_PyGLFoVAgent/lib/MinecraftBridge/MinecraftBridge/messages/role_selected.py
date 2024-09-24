# -*- coding: utf-8 -*-
"""
.. module:: role_selected
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Role Selection events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Role Selected messages.
"""

import json
import sys
from .message_exceptions import (
    MalformedMessageCreationException,
    MissingMessageArgumentException,
    ImmutableAttributeException
)
from .base_message import BaseMessage

class RoleSelectedEvent(BaseMessage):
    """
    A class encapsulating RoleSelectedEvent messages.

    Note
    ----
    Constructing a RoleSelectedEvent message requires passing the following keyword
    arguments:
        `participant_id`
        `new_role`
        `prev_role`

    While aliases exists for these attribute, they are currently not accepted
    as constructor parameters.

    Attributes
    ----------
    participant_id: string
        Unique identifier of participant (e.g. "P000420")
    playername : string
        Name of the player changing roles
    new_role : string
        New role the player is adopting
    newRole : string
        Alias of `new_role`
    prev_role : string
        Previous role of the player
    previousRole : string
        Alias of `prev_role`
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        participant_id : string
            Unique identifier of the participant; uses playername if not given
        playername : string
            Name of the player; uses participant_id if not supplied
        new_role : string
            New role the player is adopting
        prev_role : string
            Previous role the player is adopting
        """

        BaseMessage.__init__(self, **kwargs)

        self._participant_id = kwargs.get('participant_id',
                               kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        self._playername = kwargs.get('playername', self._participant_id)

        try:
            self._new_role = kwargs['new_role']
        except KeyError:
            raise MissingMessageArgumentException(str(self),
                                                  'new_role') from None

        try:
            self._prev_role = kwargs['prev_role']
        except KeyError:
            raise MissingMessageArgumentException(str(self),
                                                  'prev_role') from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'RoleSelectedEvent')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        Get the unique identifier for the participant changing role.  

        Attempting to set `participant_id` raises an `ImmutableAttributeException`.
        """

        return self._participant_id

    @participant_id.setter
    def participant_id(self, name):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def playername(self):
        """
        Get the name of the player changing role.  Attempting to set the value
        of `playername` will result in an `ImmutableAttributeException` being
        raised.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def new_role(self):
        """
        Get the new role adoped by the player.

        Attempting to set `new_role` raises an `ImmutableAttributeException`
        """

        return self._new_role

    @new_role.setter
    def new_role(self, role):
        raise ImmutableAttributeException(str(self), "new_role")


    @property
    def newRole(self):
        """
        Alias of `new_role`
        """

        return self._new_role

    @newRole.setter
    def newRole(self, role):
        raise ImmutableAttributeException(str(self), "newRole")

    @property
    def prev_role(self):
        """
        Get the previous role of the player.

        Attempting to set `prev_role` raises an `ImmutableAttributeException`.
        """

        return self._prev_role

    @prev_role.setter
    def prev_role(self, role):
        raise ImmutableAttributeException(str(self), "prev_role")


    @property
    def previousRole(self):
        """
        Alias of `prev_role`
        """

        return self._prev_role

    @previousRole.setter
    def previousRole(self, role):
        raise ImmutableAttributeException(str(self), "previousRole")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the RoleSelectedEvent message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["new_role"] = self.new_role
        jsonDict["data"]["prev_role"] = self.prev_role

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
            RoleSelectedEvent message.
        """

        return json.dumps(self.toDict())

