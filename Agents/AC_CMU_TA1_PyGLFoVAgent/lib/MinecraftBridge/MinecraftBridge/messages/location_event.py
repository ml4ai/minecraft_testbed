# -*- coding: utf-8 -*-
"""
.. module:: location_event
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Location Monitor messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Location Monitor messages.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class LocationEvent(BaseMessage):
    """
    A class encapsulating LocationEvent messages.

    Note
    ----
    Future iterations will need to objectify the sub-attributes

    Attributes
    ----------
    participant_id : string
        ID of the participant whose location changed
    playername : string (optional)
        Name of the player
    callsign : string (optional)
        Callsign of the player
    corresponding_observation_number : int
        observation number from PlayerState message
    locations : list
        A list of locations the player is currently in
    connections : list
        A list of connections the player is currently in
    exited_locations : list
        A list of locations the player just left
    exited_connections : list
        A list of connections the player just left
    """


    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        participant_id : string
            ID of the participant whose location has changed
        playername : string, optional
            name of the player, adopts participant_id if not supplied
        callsign : string, optional
            callsign of the player
        corresponding_observation_number : int
            observation number from the PlayerState message
        locations : list, optional, default=[]
            List of locations the player is currently in
        connections : list, optional, default=[]
            List of connections the player is currently in
        exited_locations : list
            List of locations the player just left
        exited_connections : list
            List of connections the player just left
        """
        
        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["participant_id", "corresponding_observation_number"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self.participant_id = kwargs["participant_id"]
        self.corresponding_observation_number = kwargs["corresponding_observation_number"]

        # Optional arguments
        self.playername = kwargs.get("playername", self.participant_id)
        self.callsign = kwargs.get("callsign", None)
        self.locations = kwargs.get("locations", [])
        self.connections = kwargs.get("connections", [])
        self.exited_locations = kwargs.get("exited_locations", [])
        self.exited_connections = kwargs.get("exited_connections", [])



    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the SemanticMapInitialized message.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        ## TODO!!!

        
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
            SemanticMapInitialized message.
        """

        return json.dumps(self.toDict())       
        
