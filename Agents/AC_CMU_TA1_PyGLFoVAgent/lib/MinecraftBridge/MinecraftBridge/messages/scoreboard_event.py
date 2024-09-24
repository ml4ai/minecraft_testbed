# -*- coding: utf-8 -*-
"""
.. module:: scoreboard_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Scoreboard Events

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Scoreboard Event messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class ScoreboardEvent(BaseMessage):
    """
    A class encapsulating ScoreboardEvent messages.


    Notes
    -----
    Creating the ScoreboardEvent requires no parameters to be given.  Rather,
    the `addScore` method should be used to add scores to the scoreboard, and
    once all scores are added, the `finalize` method should be used to make the
    scoreboard immutable.


    Examples
    --------
    Adding scoreboard events involves the following steps:

    1.  Creating a new instance of a ScoreboardEvent

        >>> scoreboard = ScoreboardEvent()

    2.  Adding scores of individual players

        >>> scoreboard.addScore("ArthurDent", 100)
        >>> scoreboard.addScore("ZaphodBeeblebrox", 80)
        >>> scoreboard.addScore("FordPrefect", 200)

    3.  Finalizing the message, to disallow any further adding of scores

        >>> scoreboard.finalize()


    Attributes
    ----------
    scoreboard : dict of ints
        Dictionary mapping playernames to current scores.
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)
                
        self._scoreboard = {}

        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ScoreboardEvent')
        """

        return self.__class__.__name__


    @property
    def scoreboard(self):
        """
        Get the scoreboard dictionary.  While attempting to set the value of
        `scoreboard` will result in an `ImmutableAttributeException` being 
        raised, it is still possible to modify the *contents* of the scoreboard
        dictionary (which should not be done).
        """
        return self._scoreboard

    @scoreboard.setter
    def scoreboard(self, scoreboard):
        raise ImmutableAttributeException(str(self), "scoreboard") from None
    

#    @property
#    def mission_timer(self):
#        """
#        Get the value of the mission timer.  
#
#        Attempting to set `mission_timer` raises an `ImmutableAttributeException`.
#        """
#        return BaseMessage.mission_timer(self)
#
#        return self._mission_timer

#    @mission_timer.setter
#    def mission_timer(self, timer):
#        return BaseMessage.mission_timer(self, timer)
#
#        raise ImmutableAttributeException(self.__class__.__name__, 
#                                          "mission_timer") from None
    

#    @property
#    def elaped_milliseconds(self):
#        """
#        Get the number of elapsed milliseconds since the beginning of the mission.  
#
#        Attempting to set `elaped_milliseconds` raises an `ImmutableAttributeException`.
#        """
#        return BaseMessage.elapsed_milliseconds(self)
#        return self._elaped_milliseconds

#    @elaped_milliseconds.setter
#    def elaped_milliseconds(self, time):
#        return BaseMessage.elapsed_milliseconds(self, time)
#
#        raise ImmutableAttributeException(self.__class__.__name__,
#                                          "elapsed_milliseconds") from None


    def addScore(self, name, score):
        """
        Add a score to the scoreboard, overwritting the score if it exists

        Parameters
        ----------
        name : string
            Name of the player to add the score to
        score : int
            score of the added player
        """

        # Check if the scoreboard is finalized, and if so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "scoreboard (via addScore)") from None

        # Otherwise, feel free to add scores
        self.scoreboard[name] = score


    def finalize(self):
        """
        Finalize the message instance, so no new scores can be added.
        """

        self._finalized = True


    def toDict(self):
        """
        Generates a dictionary representation of the ScoreboardEvent message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ScoreboardEvent message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the gas leak event data
        jsonDict["data"]["scoreboard"] = self.scoreboard

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the ScoreboardEvent message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            ScoreboardEvent message.
        """

        return json.dumps(self.toDict())
