# -*- coding: utf-8 -*-
"""
.. module:: base_message
   :platform: Linux, Windows, OSX
   :synopsis: Base Class of Minecraft Messages and associated helper functions

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Base class defining common structure and functionality of all message classes,
and additional parsing functionality commonly used by several message types.
"""


import json
import sys

from ..utils import Loggable

from .message_exceptions import ImmutableAttributeException


def parseMissionTimer(missionTimerString):
    """
    Convert a mission timer string to a tuple consisting of the (minute,second)
    of the mission timer.  Only the first two entries delimited by a colon are
    parsed, additional entries are truncated.  If the string cannot be parsed,
    then the function returns (-1,-1).


    Examples
    --------
    Standard usage accepts strings in the format "mm : ss".  Whitespace is 
    ignored, and leading zeros are not necessary.

    >>> parseMissionTimer("8 : 36")
    (8, 36)
    >>> parseMissionTimer("08:36")
    (8, 36)

    No effort is made to ensure that the number of seconds is bound to the 
    range [0,60).  Similarly, negative values are accepted without issue.

    >>> parseMissionTimer("8 : 102")
    (8, 102)
    >>> parseMissionTimer("-5 : 36")
    (-5, 36)
    >>> parseMissionTimer("5 : -36")
    (5, -36)

    Extra entries dilimited by a colon are truncated during parsing.  _Only_
    the first two values are parsed.

    >>> parseMissionTimer("8 : 36 : 52")
    (8, 36)

    Strings without at least two entries separated by a colon are not parsed.
    Additionally, only valid integers can be parsed, floats will not be
    converted.  Strings that don't look anything like a timer will certainly
    not be parsed.

    >>> parseMissionTimer("8")
    (-1, -1)
    >>> parseMissionTimer("8 : Beeblebrox")
    (-1, -1)
    >>> parseMissionTimer("8 : 2.4")
    (-1, -1)
    >>> parseMissionTimer("pan galactic gargle blaster")
    (-1, -1)


    Parameters
    ----------
    missionTimerString : string
        String representation of the mission timer, in "mm:ss" format.


    Returns
    -------
    tuple of ints
        Tuple representation of the mission timer, in the form 
        (minutes:seconds).  If the missionTimerString cannot be parsed, returns
        (-1,-1)
    """

    try:
        missionTimer = tuple([int(x) for x in missionTimerString.split(":")][:2])
    except:
        missionTimer = (-1,-1)

    # If the parsed timer doesn't have at least two elements, assume that it is
    # incorrectly parsed
    if len(missionTimer) != 2:
        missionTimer = (-1,-1)

    return missionTimer



def getMissionTimerString(missionTimer):
    """
    Return a string representation of the provided mission timer.  If a mission
    timer of (-1,-1) is provided, returns the string "Mission Timer not 
    Initialized".


    Examples
    --------
    Standard usage accepts a tuple of integers, representing the minutes and
    seconds of the mission time.

    >>> getMissionTimerString((8, 36))
    "8 : 36"

    The function will gladly accept negative values without issue, as well as 
    values outside of the range of [0,60) for seconds.

    >>> getMissionTimerString((8, 102))
    "8 : 102"
    >>> getMissionTimerString((-5, 36))
    "-5 : 36"
    >>> getMissionTimerString((5, -36))
    "5 : -36"

    The function will only accept a 2-tuple of numbers.  Floats are truncated
    when cast to integers.

    >>> getMissionTimerString((8,))
    "Mission Timer not Initialized"
    >>> getMissionTimerString((8, 36, 52))
    "Mission Timer not Initialized"
    >>> getMissionTimerString(("Zaphod", "Beeblebrox"))
    "Mission Timer not Initialized"
    >>> getMissionTimerString((8, "Beeblebrox"))
    "Mission Timer not Initialized"
    >>> getMissionTimerString((8, 36.2))
    "8 : 36"

    (-1, -1) is a special case which is considered as not initialized.  This 
    goes for floating point representations of -1 as well.
    >>> getMissionTimerString((-1, -1))
    "Mission Timer not Initialized"
    >>> getMissionTimerString((-1.0, -1.0))
    "Mission Timer not Initialized"


    Parameters
    ----------
    missionTimer : tuple of ints
        Tuple representation of the mission timer, in the form 
        (minutes, seconds).


    Return
    ------
    string
        String representation of the mission time, "minutes : seconds", or
        "Mission Timer not Initialized" if the passed timer is (-1,-1)
    """

    if missionTimer == (-1,-1):
        return "Mission Timer not Initialized"

    # Not everything passed will match the format of a tuple of integers.  If
    # the parameter cannot be parsed, then simply indicate that the Mission
    # Timer not Initialized
    try:
        missionTimerString = "%d : %d" % missionTimer
    except:
        missionTimerString = "Mission Timer not Initialized"

    return missionTimerString



class BaseMessage(Loggable):
    """
    A base class for all Message types, containing attributes and 
    functionality common to all messages.

    Note
    ----
    The `mission_timer` and `elapsed_milliseconds` attributes are immutable.
    Attempting to assign values to these attributes will raise an exception.

    Attributes
    ----------
    headers : dict
        A map of named headers for the message.  Named headers can be used for
        encoding data used by a specific implementation of a bridge (e.g., the 
        "header" and "msg" headers used by the ASIST MQTT bus).  Headers are
        assumed to implement a `toDict` method to serialize the data.

    Other Parameters
    ----------------
    mission_timer : string, optional
        String representation of the mission timer when the message was
        generated, which is internally converted to a tuple of integers for
        convenience.  If not provided, sets the `mission_timer` attribute to 
        (-1,-1).
    missionTimer : string, optional
        An alternative parameter name for `mission_timer`.  If `mission_timer`
        is not present, attempts to use the `missionTimer` parameter.  Included
        for backwards compatibility.
    elapsed_milliseconds : integer, optional
        Number of milliseconds elapsed from the start of the mission to when
        the message was generated.  If not provided, or unable to cast to an
        int, sets the `elapsed_milliseconds` attribute to -1.
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        mission_timer : string
        missionTimer : string
            String representation of the current mission time, "mm : ss"
        elapsed_milliseconds : int
            Number of milliseconds elapsed since mission started
        """

        # Placeholder for any headers
        self.headers = {}

        # Parse the keyword arguments, if they exist.  Make sure that the 
        # elapsed_milliseconds is cast as an int, and set it to -1 if that is
        # not possible
        mission_timer = kwargs.get("mission_timer", kwargs.get("missionTimer", ""))
        self._mission_timer = parseMissionTimer(mission_timer)

        try:
            self._elapsed_milliseconds = int(kwargs.get("elapsed_milliseconds", -1))
        except:
            self._elapsed_milliseconds = -1


    @property
    def mission_timer(self):
        """
        Get the value of the mission timer, as a tuple of ints representing the
        (minute, second) of the timer.  Attempting to set the value of the 
        mission_timer will result in an `ImmutableAttributeException` being
        raised.
        """
        return self._mission_timer

    @mission_timer.setter
    def mission_timer(self, timer):
        raise ImmutableAttributeException(self.__class__.__name__, 
                                          "mission_timer") from None
    

    @property
    def missionTimer(self):
        """
        Alias of `mission_timer`

        Attempting to set `mission_timer` raises an ImmutableAttributeException
        """

        return self._mission_timer

    @missionTimer.setter
    def missionTimer(self, timer):
        raise ImmutableAttributeException(self.__class__.__name__,
                                          "missionTimer") from None


    @property
    def elapsed_milliseconds(self):
        """
        Get the number of milliseconds that have elapsed from the start of the
        mission to when then message was generated.  Attempting to set the 
        value will result in an `ImmutableAttributeException` being raised.
        """
        return self._elapsed_milliseconds

    @elapsed_milliseconds.setter
    def elapsed_milliseconds(self, time):
        raise ImmutableAttributeException(self.__class__.__name__,
                                          "elapsed_milliseconds") from None


    def addHeader(self, name, header):
        """
        Adds a named header to the message.

        Parameters
        ----------
        name : string
            Name used to refer to the header.  A string type is assumed, but
            not enforced.  If `None` is passed, then the header isn't added.
        header : object
            Object containing the header data.
        """

        # Don't bother if the header is None
        if header is not None:
            self.headers[name] = header


    def toDict(self, include_data=True):
        """
        Generates a dictionary representation of the BaseMessage, which maps
        header names to dictionary representations of the corresponding header
        objects.

        Parameters
        ----------
        include_data : boolean, default=True
            If set to True, the returned dictionary contains a "data" key
            mapping to a dictionary containing entries for "mission_timer" and
            "elapsed_milliseconds".

        Returns
        -------
        dict
            A dictionary mapping header names to dictionary representations of
            the header objects.
        """

        jsonDict = {}

        # Add dictonary representation of headers
        for name, header in self.headers.items():
            jsonDict[name] = header.toDict()

        # Add an entry for data, if requested, otherwise, leave a mapping from
        # the "data" key to a blank dictionary
        if include_data:
            jsonDict["data"] = {
                "elapsed_milliseconds": self._elapsed_milliseconds,
                "mission_timer": getMissionTimerString(self._mission_timer)
            }
        else:
            jsonDict["data"] = { }

        return jsonDict


    def toJson(self, include_data=True):
        """
        Generates a JSON string representation of the BaseMessage.  The JSON 
        representation consists of a single JSON object mapping header names to
        JSON representations of the corresponding header objects.

        Parameters
        ----------
        include_data : boolean, default=True
            If set to True, the returned JSON string contains a "data" key
            mapping to a JSON object containing entries for "mission_timer" and
            "elapsed_milliseconds".

        Returns
        -------
        string
            A JSON string mapping header names to JSON representations of the
            header objects.        
        """

        return json.dumps(self.toDict(include_data))
