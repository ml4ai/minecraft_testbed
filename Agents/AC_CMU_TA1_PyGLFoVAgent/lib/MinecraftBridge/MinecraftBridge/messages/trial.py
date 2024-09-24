# -*- coding: utf-8 -*-
"""
.. module:: trial
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Trial information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Trial messages.
"""

import json
import enum

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class ClientInfo:
    """
    A class encapsulating ClientInfo messages.

    Note
    ----
    ClientInfo message contents are all optional (as per the message specs),
    and are all strings.  If no value is provided, a value of `<NOT_PROVIDED>`
    will be assigned.

    Attributes
    ----------
    playername : string, optional
        Name of the player
    callsign : string, optional
        Callsign of the player
    participantid : string, optional
        Unique ID of the participant
    staticmapversion : string, optional
        Static map version provided the player
    markerblocklegend : string, optional
        The marker block legend version provided to the player
    uniqueid : string, optional
        Unique identifier of the player
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Arguments are optional, assign `<NOT_PROVIDED>` if not given

        self._playername = kwargs.get("playername", 
                           kwargs.get("participant_id",
                           kwargs.get("particpantid", "<NOT_PROVIDED>")))
        self._callsign = kwargs.get("callsign", "<NOT_PROVIDED>")
        self._participant_id = kwargs.get("participant_id", 
                               kwargs.get("participantid", "<NOT_PROVIDED>"))
        self._static_map_version = kwargs.get("staticmapversion", "<NOT_PROVIDED>")
        self._marker_block_legend = kwargs.get("markerblocklegend", "<NOT_PROVIDED>")
        self._unique_id = kwargs.get("uniqueid", "<NOT_PROVIDED>")


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'ClientInfo')
        """

        return self.__class__.__name__


    @property
    def playername(self):
        """
        Get the name of the player.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def callsign(self):
        """
        Get the callsign of the player.  

        Attempting to set `callsign` raises an `ImmutableAttributeException`.
        """

        return self._callsign

    @callsign.setter
    def callsign(self, callsign):
        raise ImmutableAttributeException(str(self), "callsign")


    @property
    def participantid(self):
        """
        Get the participant ID of the player.  

        Attempting to set `participantid` raises an `ImmutableAttributeException`.
        """

        return self._participant_id

    @participantid.setter
    def participantid(self, _id):
        raise ImmutableAttributeException(str(self), "participantid")


    @property
    def staticmapversion(self):
        """
        Get the version of the static map provided to the player.  

        Attempting to set `staticmapversion` raises an `ImmutableAttributeException`.
        """

        return self._static_map_version

    @staticmapversion.setter
    def staticmapversion(self, version):
        raise ImmutableAttributeException(str(self), "staticmapversion")


    @property
    def markerblocklegend(self):
        """
        Get the version of the marker block legend provided to the player.  

        Attempting to set `markerblocklegend` raises an `ImmutableAttributeException`.
        """

        return self._marker_block_legend

    @markerblocklegend.setter
    def markerblocklegend(self, version):
        raise ImmutableAttributeException(str(self), "markerblocklegend")


    @property
    def uniqueid(self):
        """
        Get the unique id of the player.  

        Attempting to set `uniqueid` raises an `ImmutableAttributeException`.
        """

        return self._unique_id

    @uniqueid.setter
    def uniqueid(self, _id):
        raise ImmutableAttributeException(str(self), "uniqueid")

       

    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the ClientInfo.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["playername"] = self.playername
        jsonDict["data"]["callsign"] = self.callsign
        jsonDict["data"]["participantid"] = self.participantid
        jsonDict["data"]["staticmapversion"] = self.staticmapversion
        jsonDict["data"]["markerblocklegend"] = self. markerblocklegend
        jsonDict["data"]["uniqueid"] = self.uniqueid

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
            ClientInfo message.
        """

        return json.dumps(self.toDict())





class Trial(BaseMessage):
    """
    A class encapsulating Trial messages.


    Attributes
    ----------
    name : string
        Human-readable name for the trial
    date : string
        Date and time when the trial was run
    experimenter : string
        Name of the experimenter performing the trial
    subjects : list of strings
        List of the names or ids of the subjects in the trial
    trial_number : string
        Sequentially numbered trial
    group_number : string
        Data organization identifier
    study_number : string
        Study identifier
    condition : string
        Experimental condition used for the trial
    notes : list of strings
        List of experimenter notes for the trial
    testbed_version : string
        Testbed version used for the trial
    experiment_name : string
        Human-readable name of the experiment
    experiment_date : string
        The date and time the experiment was created
    experiment_author : string
        The name of the author of the experiment
    experiment_mission : string
        The mission associated with the experiment
    map_name : string
        The name of the map used
    map_block_filename : string
        The map block filename used during the trial
    client_info : List of ClientInfo
        Client info parameters assigned by the epxerimenter
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["name", "date", "experimenter", "subjects",
                         "trial_number", "group_number", "study_number",
                         "condition", "notes", "testbed_version",
                         "experiment_name", "experiment_date", 
                         "experiment_author", "experiment_mission",
                         "map_name", "map_block_filename"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._name = kwargs["name"]
        self._date = kwargs["date"]
        self._experimenter = kwargs["experimenter"]
        self._subjects = kwargs["subjects"]
        self._trial_number = kwargs["trial_number"]
        self._group_number = kwargs["group_number"]
        self._study_number = kwargs["study_number"]
        self._condition = kwargs["condition"]
        self._notes = kwargs["notes"]
        self._testbed_version = kwargs["testbed_version"]
        self._experiment_name = kwargs["experiment_name"]
        self._experiment_date = kwargs["experiment_date"]
        self._experiment_author = kwargs["experiment_author"]
        self._experiment_mission = kwargs["experiment_mission"]
        self._map_name = kwargs["map_name"]
        self._map_block_filename = kwargs["map_block_filename"]
        self._client_info = kwargs.get("client_info", [])


    class TrialState(enum.Enum):
        """
        Enumeration of possible trial states
        """

        start = "start",
        stop = "stop"


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'Trial')
        """

        return self.__class__.__name__


    @property
    def name(self):
        """
        Get the human-readable name for the trial.  

        Attempting to set `name` raises an `ImmutableAttributeException`.
        """

        return self._name

    @name.setter
    def name(self, name):
        raise ImmutableAttributeException(str(self), "name")


    @property
    def date(self):
        """
        Get the date the trial was run  

        Attempting to set `date` raises an `ImmutableAttributeException`.
        """

        return self._date

    @date.setter
    def date(self, date):
        raise ImmutableAttributeException(str(self), "date")


    @property
    def experimenter(self):
        """
        Get the name of the experimenter performing the trial.  

        Attempting to set `experimenter` raises an `ImmutableAttributeException`.
        """

        return self._experimenter

    @experimenter.setter
    def experimenter(self, name):
        raise ImmutableAttributeException(str(self), "experimenter")


    @property
    def subjects(self):
        """
        Get the list of names or ids of the subjects of the trial.  

        Attempting to set `subjects` raises an `ImmutableAttributeException`.
        """

        return self._subjects

    @subjects.setter
    def subjects(self, subjects):
        raise ImmutableAttributeException(str(self), "subjects")


    @property
    def trial_number(self):
        """
        Get the sequence number of the trial.  

        Attempting to set `trial_number` raises an `ImmutableAttributeException`.
        """

        return self._trial_number

    @trial_number.setter
    def trial_number(self, number):
        raise ImmutableAttributeException(str(self), "trial_number")


    @property
    def group_number(self):
        """
        Get the group number data organization identifier.  

        Attempting to set `group_number` raises an `ImmutableAttributeException`.
        """

        return self._group_number

    @group_number.setter
    def group_number(self, number):
        raise ImmutableAttributeException(str(self), "group_number")


    @property
    def study_number(self):
        """
        Get the study identifier.  

        Attempting to set `study_number` raises an `ImmutableAttributeException`.
        """

        return self._study_number

    @study_number.setter
    def study_number(self, number):
        raise ImmutableAttributeException(str(self), "study_number")


    @property
    def condition(self):
        """
        Get the experimental condition used for the trial.  

        Attempting to set `condition` raises an `ImmutableAttributeException`.
        """

        return self._condition

    @condition.setter
    def condition(self, condition):
        raise ImmutableAttributeException(str(self), "condition")


    @property
    def notes(self):
        """
        Get the list of notes for the trial.  

        Attempting to set `notes` raises an `ImmutableAttributeException`.
        """

        return self._notes

    @notes.setter
    def notes(self, notes):
        raise ImmutableAttributeException(str(self), "notes")


    @property
    def testbed_version(self):
        """
        Get the version of the testbed used for the trial.  

        Attempting to set `testbed_version` raises an `ImmutableAttributeException`.
        """

        return self._testbed_version

    @testbed_version.setter
    def testbed_version(self, version):
        raise ImmutableAttributeException(str(self), "testbed_version")


    @property
    def experiment_name(self):
        """
        Get the human-readable name of the experiment.  

        Attempting to set `experiment_name` raises an `ImmutableAttributeException`.
        """

        return self._experiment_name

    @experiment_name.setter
    def experiment_name(self, name):
        raise ImmutableAttributeException(str(self), "experiment_name")



    @property
    def experiment_date(self):
        """
        Get the date and time the experiment was created.  

        Attempting to set `experiment_date` raises an `ImmutableAttributeException`.
        """

        return self._experiment_date

    @experiment_date.setter
    def experiment_date(self, date):
        raise ImmutableAttributeException(str(self), "experiment_date")


    @property
    def experiment_author(self):
        """
        Get the name of the author of the experiment.  

        Attempting to set `experiment_author` raises an `ImmutableAttributeException`.
        """

        return self._experiment_author

    @experiment_author.setter
    def experiment_author(self, author):
        raise ImmutableAttributeException(str(self), "experiment_author")


    @property
    def experiment_mission(self):
        """
        Get the mission associated with the experiment.  

        Attempting to set `experiment_mission` raises an `ImmutableAttributeException`.
        """

        return self._experiment_mission

    @experiment_mission.setter
    def experiment_mission(self, misison):
        raise ImmutableAttributeException(str(self), "experiment_mission")


    @property
    def map_name(self):
        """
        Get the name of the map used for the mission.  

        Attempting to set `map_name` raises an `ImmutableAttributeException`.
        """

        return self._map_name

    @map_name.setter
    def map_name(self, name):
        raise ImmutableAttributeException(str(self), "map_name")


    @property
    def map_block_filename(self):
        """
        Get the name of the map block file used during the trial.  

        Attempting to set `map_block_filename` raises an `ImmutableAttributeException`.
        """

        return self._map_block_filename

    @map_block_filename.setter
    def map_block_filename(self, filename):
        raise ImmutableAttributeException(str(self), "map_block_filename")


    @property
    def client_info(self):
        """
        Get the list of client info parameters assigned by the experimenter.  

        Attempting to set `client_info` raises an `ImmutableAttributeException`.
        """

        return self._client_info

    @client_info.setter
    def client_info(self, info):
        raise ImmutableAttributeException(str(self), "client_info")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Trial.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["name"] = self.name
        jsonDict["data"]["date"] = self.date
        jsonDict["data"]["experimenter"] = self.experimenter
        jsonDict["data"]["subjects"] = self.subjects
        jsonDict["data"]["trial_number"] = self.trial_number
        jsonDict["data"]["group_number"] = self.group_number
        jsonDict["data"]["study_number"] = self.study_number
        jsonDict["data"]["condition"] = self.condition
        jsonDict["data"]["notes"] = self.notes
        jsonDict["data"]["testbed_version"] = self.testbed_version
        jsonDict["data"]["experiment_name"] = self.experiment_name
        jsonDict["data"]["experiment_date"] = self.experiment_date
        jsonDict["data"]["experiment_author"] = self.experiment_author
        jsonDict["data"]["experiment_mission"] = self.experiment_mission
        jsonDict["data"]["map_name"] = self.map_name
        jsonDict["data"]["map_block_filename"] = self.map_block_filename
        jsonDict["data"]["client_info"] = [info.toDict() for info in self.client_info]

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
            Trial message.
        """

        return json.dumps(self.toDict())