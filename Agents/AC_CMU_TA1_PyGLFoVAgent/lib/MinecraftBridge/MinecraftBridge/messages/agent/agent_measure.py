# -*- coding: utf-8 -*-
"""
.. module:: agent_measure
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Measure Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Measure messages.
"""

import json
import uuid
from datetime import datetime

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class AgentMeasure(BaseMessage):
    """
    A class encapsulating Agent Measure messages.

    Attributes
    ----------
    study_version : int
        the version of the study this measure is being reported on
    elapsed_milliseconds : int
        the current elapsed milliseconds
    qualifying_event_type : string ("event", "timedEvent", or "time")
        which type of event triggered the measure
    qualifying_event_message_type : MessageType or None, default=None
        message type, if applicable
    qualifying_event_sub_type : MessageSubtype or None, default=None
        message subtype, if applicable
    time_delta : int or None, default=None
        the time delta applicable since event in elapsed milliseconds
    event_mission_time : int or None, default=None
        the time of an event which occurs at a specific mission time in
        elapsed milliseconds, if applicable
    measure_id : string
        the id of the current measure
    datatype : string
        the datatype of the measure
    measure_value : any
        the value of the measure
    description : string
        a description of the measure
    additional_data : dictionary
        any additional user-defined data needed
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["study_version", "qualifying_event_type",
                         "measure_id", "datatype", "measure_value",
                         "description"]:

            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._study_version = kwargs["study_version"]
###        self._elapsed_milliseconds = kwargs["_elapsed_milliseconds"]
        self._qualifying_event_type = kwargs["qualifying_event_type"]
        self._qualifying_event_message_type = kwargs.get("qualifying_event_message_type","")
        self._qualifying_event_sub_type = kwargs.get("qualifying_event_sub_type","")
        self._time_delta = kwargs.get("time_delta", None)
        self._mission_time = kwargs.get("mission_time", self.elapsed_milliseconds)
        self._measure_id  = kwargs["measure_id"]
        self._datatype = kwargs["datatype"]
        self._measure_value = kwargs["measure_value"]
        self._description = kwargs["description"]
        self._additional_data = kwargs.get("additional_data", {})



    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentIntervention')
        """

        return self.__class__.__name__


    @property
    def study_version(self):
        """

        Attempting to set `study_version` will raise an `ImmutableAttributeException`
        """

        return self._study_version

    @study_version.setter
    def study_version(self, _):
        raise ImmutableAttributeException(str(self), "study_version")


    @property
    def qualifying_event_type(self):
        """

        Attempting to set `qualifying_event_type` will raise an `ImmutableAttributeException`
        """

        return self._qualifying_event_type

    @qualifying_event_type.setter
    def qualifying_event_type(self, _):
        raise ImmutableAttributeException(str(self), "qualifying_event_type")


    @property
    def qualifying_event_message_type(self):
        """

        Attempting to set `qualifying_event_message_type` will raise an `ImmutableAttributeException`
        """

        return self._qualifying_event_message_type

    @qualifying_event_message_type.setter
    def qualifying_event_message_type(self, _):
        raise ImmutableAttributeException(str(self), "qualifying_event_message_type")


    @property
    def qualifying_event_sub_type(self):
        """

        Attempting to set `qualifying_event_sub_type` will raise an `ImmutableAttributeException`
        """

        return self._qualifying_event_sub_type

    @qualifying_event_sub_type.setter
    def qualifying_event_sub_type(self, _):
        raise ImmutableAttributeException(str(self), "qualifying_event_sub_type")


    @property
    def time_delta(self):
        """

        Attempting to set `time_delta` will raise an `ImmutableAttributeException`
        """

        return self._time_delta

    @time_delta.setter
    def time_delta(self, _):
        raise ImmutableAttributeException(str(self), "time_delta")


    @property
    def mission_time(self):
        """

        Attempting to set `mission_time` will raise an `ImmutableAttributeException`
        """

        return self._mission_time

    @mission_time.setter
    def mission_time(self, _):
        raise ImmutableAttributeException(str(self), "mission_time")


    @property
    def measure_id(self):
        """

        Attempting to set `measure_id` will raise an `ImmutableAttributeException`
        """

        return self._measure_id

    @measure_id.setter
    def measure_id(self, _):
        raise ImmutableAttributeException(str(self), "measure_id ")


    @property
    def datatype(self):
        """

        Attempting to set `datatype` will raise an `ImmutableAttributeException`
        """

        return self._datatype

    @datatype.setter
    def datatype(self, _):
        raise ImmutableAttributeException(str(self), "datatype")


    @property
    def measure_value(self):
        """

        Attempting to set `measure_value` will raise an `ImmutableAttributeException`
        """

        return self._measure_value

    @measure_value.setter
    def measure_value(self, _):
        raise ImmutableAttributeException(str(self), "measure_value")


    @property
    def description(self):
        """

        Attempting to set `description` will raise an `ImmutableAttributeException`
        """

        return self._description

    @description.setter
    def description(self, _):
        raise ImmutableAttributeException(str(self), "description")


    @property
    def additional_data(self):
        """

        Attempting to set `additional_data` will raise an `ImmutableAttributeException`
        """

        return self._additional_data

    @additional_data.setter
    def additional_data(self, _):
        raise ImmutableAttributeException(str(self), "additional_data")


    def toDict(self):
        """
        Generates a dictionary representation of the AgentIntervention message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentIntervention message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.  Also, add the event_properties and measure_data
        # fields with empty dicitonaries
        if not "data" in jsonDict:
            jsonDict["data"] = {}
        jsonDict["data"]["event_properties"] = {}
        jsonDict["data"]["measure_data"] = {}

        # Add the intervention data
        jsonDict["data"]["study_version"] = self.study_version
        jsonDict["data"]["elapsed_milliseconds"] = self.elapsed_milliseconds

        jsonDict["data"]["event_properties"]["qualifying_event_type"] = self.qualifying_event_type
        jsonDict["data"]["event_properties"]["qualifying_event_message_type"] = str(self.qualifying_event_message_type)
        jsonDict["data"]["event_properties"]["qualifying_event_sub_type"] = str(self.qualifying_event_sub_type)
        jsonDict["data"]["event_properties"]["time_delta"] = self.time_delta
        jsonDict["data"]["event_properties"]["mission_time"] = self.mission_time

        jsonDict["data"]["measure_data"]["datatype"] = self.datatype
        jsonDict["data"]["measure_data"]["measure_id"] = self.measure_id 
        jsonDict["data"]["measure_data"]["measure_value"] = self.measure_value 
        jsonDict["data"]["measure_data"]["description"] = self.description
        jsonDict["data"]["measure_data"]["additional_data"] = self.additional_data


        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the AgentIntervention message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentIntervention message.
        """

        return json.dumps(self.toDict())

