# -*- coding: utf-8 -*-
"""
.. module:: get_trial_info_response.py
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating GetTrialInfoResponse information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating GetTrialInfoResponse messages.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class GetTrialInfoResponse(BaseMessage):
    """
    A class encapsulating GetTrialInfoResponse messages.  This class contains
    the data published when a getTrialInfo request (control/request/getTrialInfo) 
    has been sent.

    Attributes
    ----------
    experiment_id : string
        UUID of the experiment being run
    trial_id : string
        UUID of the trial being run
    mission_name : string
        Name of the mission being run
    map_name : string
        Name of the map being used
    map_block_filename : string
        Name of the file containing victim / rubble blocks
    map_info_filename : string
        Not sure what this is
    observer_info : list of strings
        Not sure what this is either, see Trial messages
    callsigns : dictionary
        Mapping of player callsign (string) to playername (string)
    """

    def __init__(self, **kwargs):
        """

        """

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["experiment_id", "trial_id", "mission_name",
                         "map_name", "map_block_filename"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._experiment_id = kwargs["experiment_id"]
        self._trial_id = kwargs["trial_id"]
        self._mission_name = kwargs["mission_name"]
        self._map_block_filename = kwargs["map_block_filename"]
        self._map_name = kwargs["map_name"]
        self._map_info_filename = kwargs.get("map_info_filename", None)
        self._observer_info = kwargs.get("observer_info", [])
        self._callsigns = kwargs.get("callsigns", {})

        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PlayerState')
        """

        return self.__class__.__name__


    def finalize(self):
        """
        Indicate that all Observer Info and Callsigns have been added
        """

        self._finalized = True


    def addInfo(self, info):
        """
        Add an observer info message to the list of info

        Parameters
        ----------
        info : string
            Info to add to the list
        """

        # Check if the observer info list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "observer_info (from addInfo)")

        self._observer_info.append(info)


    def addCallsign(self, callsign, name):
        """
        Add a mapping from the callsign to the player name to the map of 
        callsigns.

        Parameters
        ----------
        callsign : string
            Callsign of the player
        name : string
            Name of the player
        """

        # Check if the callsign map is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "callsigns (from addCallsign)")

        self._callsigns[callsign] = name



    @property
    def experiment_id(self):
        """

        Attempting to set `experiment_id` raises an `ImmutableAttributeException`.
        """

        return self._experiment_id

    @experiment_id.setter
    def experiment_id(self, _):
        raise ImmutableAttributeException(str(self), "experiment_id")


    @property
    def trial_id(self):
        """

        Attempting to set `trial_id` raises an `ImmutableAttributeException`.
        """

        return self._trial_id

    @trial_id.setter
    def trial_id(self, _):
        raise ImmutableAttributeException(str(self), "trial_id")


    @property
    def mission_name(self):
        """

        Attempting to set `mission_name` raises an `ImmutableAttributeException`.
        """

        return self._mission_name

    @mission_name.setter
    def mission_name(self, _):
        raise ImmutableAttributeException(str(self), "mission_name")


    @property
    def map_block_filename(self):
        """

        Attempting to set `map_block_filename` raises an `ImmutableAttributeException`.
        """

        return self._map_block_filename

    @map_block_filename.setter
    def map_block_filename(self, _):
        raise ImmutableAttributeException(str(self), "map_block_filename")


    @property
    def map_name(self):
        """

        Attempting to set `map_name` raises an `ImmutableAttributeException`.
        """

        return self._map_name

    @map_name.setter
    def map_name(self, _):
        raise ImmutableAttributeException(str(self), "map_name")


    @property
    def map_info_filename(self):
        """

        Attempting to set `map_info_filename` raises an `ImmutableAttributeException`.
        """

        return self._map_info_filename

    @map_info_filename.setter
    def map_info_filename(self, _):
        raise ImmutableAttributeException(str(self), "map_info_filename")


    @property
    def observer_info(self):
        """

        Attempting to set `observer_info` raises an `ImmutableAttributeException`.
        """

        return self._observer_info

    @observer_info.setter
    def observer_info(self, _):
        raise ImmutableAttributeException(str(self), "observer_info")


    @property
    def callsigns(self):
        """

        Attempting to set `callsigns` raises an `ImmutableAttributeException`.
        """

        return self._callsigns

    @callsigns.setter
    def callsigns(self, _):
        raise ImmutableAttributeException(str(self), "callsigns")
 

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the GetTrialInfoResponse.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDist["data"]["experiment_id"] = self.experiment_id
        jsonDist["data"]["trial_id"] = self.trial_id
        jsonDist["data"]["mission_name"] = self.mission_name
        jsonDist["data"]["map_block_filename"] = self.map_block_filename
        jsonDist["data"]["map_name"] = self.map_name
        jsonDist["data"]["map_info_filename"] = self.map_info_filename
        jsonDist["data"]["observer_info"] = self.observer_info
        jsonDist["data"]["callsigns"] = self.callsigns


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
            GetTrialInfoResponse message.
        """

        return json.dumps(self.toDict())
