# -*- coding: utf-8 -*-
"""
.. module:: rubble_collapse
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating RubbleCollapse Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating RubbleCollapse messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class RubbleCollapse(BaseMessage):
    """
    A class encapsulating RubbleCollapse messages.

    Attributes
    ----------
    participant_id : string
        The id of the player being reported
    playername : string
        The name of the player
    triggerLocation : tuple of integers
        The location of the trigger block
    triggerLocation_x : integer
        Alias of `triggerLocation[0]`
    triggerLocation_y : integer
        Alias of `triggerLocation[1]`
    triggerLocation_z : integer
        Alias of `triggerLocation[2]`
    fromBlock : tuple of integers
        the corner defining a rectangle of rubble
    fromBlock_x : integer
        Alias of `fromBlock[0]`
    fromBlock_y : integer
        Alias of `fromBlock[1]`
    fromBlock_z : integer
        Alias of `fromBlock[2]`
    toBlock : tuple of integers
        other corner defining a rectangle of rubble
    toBlock_x : integer
        Alias of `toBlock[0]`
    toBlock_y : integer
        Alias of `toBlock[1]`
    toBlock_z : integer
        Alias of `toBlock[2]`
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Get the participant ID and playername.
        self._participant_id = kwargs.get('participant_id',
                               kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        self._playername = kwargs.get('playername', self._participant_id)

        # Try to get the triggerLocation property:  try `triggerLocation` first,
        # followed by `triggerLocation_x`, `triggerLocation_y`, and 
        # `triggerLocation_z`
        triggerLocation = kwargs.get("triggerLocation", None)

        if triggerLocation is None:
            try:
                triggerLocation = (kwargs['triggerLocation_x'], 
                                   kwargs['triggerLocation_y'], 
                                   kwargs['triggerLocation_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'triggerLocation') from None

        # Try to coerce triggerLocation into a tuple of ints
        try:
            self._triggerLocation = tuple([int(x) for x in triggerLocation][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'triggerLocation',
                                                    triggerLocation) from None


        # Try to get the fromBlock property:  try `fromBlock` first, followed
        # by `fromBlock_x`, `fromBlock_y`, and `fromBlock_z`
        fromBlock = kwargs.get("fromBlock", None)

        if fromBlock is None:
            try:
                fromBlock = (kwargs['fromBlock_x'], 
                             kwargs['fromBlock_y'], 
                             kwargs['fromBlock_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'fromBlock') from None

        # Try to coerce fromBlock into a tuple of ints
        try:
            self._fromBlock = tuple([int(x) for x in fromBlock][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'toBlock',
                                                    fromBlock) from None

        # Try to get the toBlock property:  try `toBlock` first, followed
        # by `toBlock_x`, `toBlock_y`, and `toBlock_z`
        toBlock = kwargs.get("toBlock", None)

        if toBlock is None:
            try:
                toBlock = (kwargs['toBlock_x'], 
                           kwargs['toBlock_y'], 
                           kwargs['toBlock_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'toBlock') from None

        # Try to coerce toBlock into a tuple of ints
        try:
            self._toBlock = tuple([int(x) for x in toBlock][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'toBlock',
                                                    toBlock) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'RubbleCollapse')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """

        Attempting to set `participant_id` raises an `ImmutableAttributeException`
        """

        return self._participant_id

    @participant_id.setter
    def participant_id(self, _):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def playername(self):
        """

        Attempting to set `playername` raises an `ImmutableAttributeException`
        """

        return self._playername

    @playername.setter
    def playername(self, _):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def triggerLocation(self):
        """

        Attempting to set `triggerLocation` raises an `ImmutableAttributeException`
        """

        return self._triggerLocation

    @triggerLocation.setter
    def triggerLocation(self, _):
        raise ImmutableAttributeException(str(self), "triggerLocation")


    @property
    def triggerLocation_x(self):
        """

        Attempting to set `triggerLocation_x` raises an `ImmutableAttributeException`
        """

        return self._triggerLocation_x

    @triggerLocation_x.setter
    def triggerLocation_x(self, _):
        raise ImmutableAttributeException(str(self), "triggerLocation_x")


    @property
    def triggerLocation_y(self):
        """

        Attempting to set `triggerLocation_y` raises an `ImmutableAttributeException`
        """

        return self._triggerLocation_y

    @triggerLocation_y.setter
    def triggerLocation_y(self, _):
        raise ImmutableAttributeException(str(self), "triggerLocation_y")


    @property
    def triggerLocation_z(self):
        """

        Attempting to set `triggerLocation_z` raises an `ImmutableAttributeException`
        """

        return self._triggerLocation_z

    @triggerLocation_z.setter
    def triggerLocation_z(self, _):
        raise ImmutableAttributeException(str(self), "triggerLocation_z")


    @property
    def fromBlock(self):
        """

        Attempting to set `fromBlock` raises an `ImmutableAttributeException`
        """

        return self._fromBlock

    @fromBlock.setter
    def fromBlock(self, _):
        raise ImmutableAttributeException(str(self), "fromBlock")


    @property
    def fromBlock_x(self):
        """

        Attempting to set `fromBlock_x` raises an `ImmutableAttributeException`
        """

        return self._fromBlock[0]

    @fromBlock_x.setter
    def fromBlock_x(self, _):
        raise ImmutableAttributeException(str(self), "fromBlock_x")


    @property
    def fromBlock_y(self):
        """

        Attempting to set `fromBlock_y` raises an `ImmutableAttributeException`
        """

        return self._fromBlock[1]

    @fromBlock_y.setter
    def fromBlock_y(self, _):
        raise ImmutableAttributeException(str(self), "fromBlock_y")


    @property
    def fromBlock_z(self):
        """

        Attempting to set `fromBlock_z` raises an `ImmutableAttributeException`
        """

        return self._fromBlock[2]

    @fromBlock_z.setter
    def fromBlock_z(self, _):
        raise ImmutableAttributeException(str(self), "fromBlock_z")


    @property
    def toBlock(self):
        """

        Attempting to set `toBlock` raises an `ImmutableAttributeException`
        """

        return self._toBlock

    @toBlock.setter
    def toBlock(self, _):
        raise ImmutableAttributeException(str(self), "toBlock")


    @property
    def toBlock_x(self):
        """

        Attempting to set `toBlock_x` raises an `ImmutableAttributeException`
        """

        return self._toBlock[0]

    @toBlock_x.setter
    def toBlock_x(self, _):
        raise ImmutableAttributeException(str(self), "toBlock_x")


    @property
    def toBlock_y(self):
        """

        Attempting to set `toBlock_y` raises an `ImmutableAttributeException`
        """

        return self._toBlock[1]

    @toBlock_y.setter
    def toBlock_y(self, _):
        raise ImmutableAttributeException(str(self), "toBlock_y")


    @property
    def toBlock_z(self):
        """

        Attempting to set `toBlock_z` raises an `ImmutableAttributeException`
        """

        return self._toBlock[2]

    @toBlock_z.setter
    def toBlock_z(self, _):
        raise ImmutableAttributeException(str(self), "toBlock_z")



    def toDict(self):
        """
        Generates a dictionary representation of the RubbleCollapse message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the RubbleCollapse message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the event data
        jsonDict["data"]["participant_id"] = self.participant_id
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["triggerLocation_x"] = self.triggerLocation_x
        jsonDict["data"]["triggerLocation_y"] = self.triggerLocation_y
        jsonDict["data"]["triggerLocation_z"] = self.triggerLocation_z
        jsonDict["data"]["fromBlock_x"] = self.fromBlock_x
        jsonDict["data"]["fromBlock_y"] = self.fromBlock_y
        jsonDict["data"]["fromBlock_z"] = self.fromBlock_z
        jsonDict["data"]["toBlock_x"] = self.toBlock_x
        jsonDict["data"]["toBlock_y"] = self.toBlock_y
        jsonDict["data"]["toBlock_z"] = self.toBlock_z

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the RubbleCollapse message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            ##### message.
        """

        return json.dumps(self.toDict())
