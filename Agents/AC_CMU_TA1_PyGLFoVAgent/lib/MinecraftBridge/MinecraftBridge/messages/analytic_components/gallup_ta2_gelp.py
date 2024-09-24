# -*- coding: utf-8 -*-
"""
.. module:: gallup_ta2_gelp
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Emergent Leadership Prediction Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Emergent Leadership Prediction messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class GELP(BaseMessage):
    """
    A class encapsulating emergent leadership prediction messages.

    Attributes
    ----------
    version
    owner
    config
    source
    dependencies
    publishes
    subscribes
    event_ts
    participant_id
    callsign
    elapsed_milliseconds
    gelp_overall
    gelp_lower_bound
    gelp_upper_bound
    gelp_components
    gelp_components_lower_bound
    gelp_components_upper_bound    
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["version", "owner", "config", "source", "dependencies",
                         "publishes", "subscribes", "event_ts", "participant_id", 
                         "callsign", "elapsed_milliseconds", "gelp_overall", 
                         "gelp_lower_bound", "gelp_upper_bound", "gelp_components", 
                         "gelp_components_lower_bound", "gelp_components_upper_bound"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        ## TODO: Not certain how Gallup actually structured their data, so will
        ##       need to be careful when developing the parser for this thing

        self._version = kwargs["version"]
        self._owner = kwargs["owner"]
        self._config = kwargs["config"]
        self._source = kwargs["source"]
        self._dependencies = kwargs["dependencies"]
        self._publishes = kwargs["publishes"]
        self._subscribes = kwargs["subscribes"]

        self._event_ts = kwargs["event_ts"]
        self._participant_id = kwargs["participant_id"]
        self._callsign = kwargs["callsign"]
        self._elapsed_milliseconds = kwargs["elapsed_milliseconds"]
        self._gelp_overall = kwargs["gelp_overall"]
        self._gelp_lower_bound = kwargs["gelp_lower_bound"]
        self._gelp_upper_bound = kwargs["gelp_upper_bound"]
        self._gelp_components = kwargs["gelp_components"]
        self._gelp_components_lower_bound = kwargs["gelp_components_lower_bound"]
        self._gelp_components_upper_bound = kwargs["gelp_components_upper_bound"]


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentFeedback')
        """
    
        return self.__class__.__name__
    

    @property
    def version(self):
        """"
    
        Attempting to set `version` raises an `ImmutableAttributeException`.
        """
        return self._version
    
    @version.setter
    def version(self, _):
        raise ImmutableAttributeException(str(self), "version")
    
        
    @property
    def owner(self):
        """"
    
        Attempting to set `owner` raises an `ImmutableAttributeException`.
        """
        return self._owner
    
    @owner.setter
    def owner(self, _):
        raise ImmutableAttributeException(str(self), "owner")
    
        
    @property
    def config(self):
        """"
    
        Attempting to set `config` raises an `ImmutableAttributeException`.
        """
        return self._config
    
    @config.setter
    def config(self, _):
        raise ImmutableAttributeException(str(self), "config")
    
        
    @property
    def source(self):
        """"
    
        Attempting to set `source` raises an `ImmutableAttributeException`.
        """
        return self._source
    
    @source.setter
    def source(self, _):
        raise ImmutableAttributeException(str(self), "source")
    
        
    @property
    def dependencies(self):
        """"
    
        Attempting to set `dependencies` raises an `ImmutableAttributeException`.
        """
        return self._dependencies
    
    @dependencies.setter
    def dependencies(self, _):
        raise ImmutableAttributeException(str(self), "dependencies")
    
        
    @property
    def publishes(self):
        """"
    
        Attempting to set `publishes` raises an `ImmutableAttributeException`.
        """
        return self._publishes
    
    @publishes.setter
    def publishes(self, _):
        raise ImmutableAttributeException(str(self), "publishes")
    
        
    @property
    def subscribes(self):
        """"
    
        Attempting to set `subscribes` raises an `ImmutableAttributeException`.
        """
        return self._subscribes
    
    @subscribes.setter
    def subscribes(self, _):
        raise ImmutableAttributeException(str(self), "subscribes")

    
    @property
    def event_ts(self):
        """
    
        Attempting to set `event_ts` raises an `ImmutableAttributeException`
        """
        return self._event_ts
    
    @event_ts.setter
    def event_ts(self, _):
        raise ImmutableAttributeException(str(self), "event_ts")
    
        
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
    def callsign(self):
        """
    
        Attempting to set `callsign` raises an `ImmutableAttributeException`
        """
        return self._callsign
    
    @callsign.setter
    def callsign(self, _):
        raise ImmutableAttributeException(str(self), "callsign")
    
        
    @property
    def elapsed_milliseconds(self):
        """
    
        Attempting to set `elapsed_milliseconds` raises an `ImmutableAttributeException`
        """
        return self._elapsed_milliseconds
    
    @elapsed_milliseconds.setter
    def elapsed_milliseconds(self, _):
        raise ImmutableAttributeException(str(self), "elapsed_milliseconds")
    
        
    @property
    def gelp_overall(self):
        """
    
        Attempting to set `gelp_overall` raises an `ImmutableAttributeException`
        """
        return self._gelp_overall
    
    @gelp_overall.setter
    def gelp_overall(self, _):
        raise ImmutableAttributeException(str(self), "gelp_overall")
    
        
    @property
    def gelp_lower_bound(self):
        """
    
        Attempting to set `gelp_lower_bound` raises an `ImmutableAttributeException`
        """
        return self._gelp_lower_bound
    
    @gelp_lower_bound.setter
    def gelp_lower_bound(self, _):
        raise ImmutableAttributeException(str(self), "gelp_lower_bound")
    
        
    @property
    def gelp_upper_bound(self):
        """
    
        Attempting to set `gelp_upper_bound` raises an `ImmutableAttributeException`
        """
        return self._gelp_upper_bound
    
    @gelp_upper_bound.setter
    def gelp_upper_bound(self, _):
        raise ImmutableAttributeException(str(self), "gelp_upper_bound")
    
        
    @property
    def gelp_components(self):
        """
    
        Attempting to set `gelp_components` raises an `ImmutableAttributeException`
        """
        return self._gelp_components
    
    @gelp_components.setter
    def gelp_components(self, _):
        raise ImmutableAttributeException(str(self), "gelp_components")
    
        
    @property
    def gelp_components_lower_bound(self):
        """
    
        Attempting to set `gelp_components_lower_bound` raises an `ImmutableAttributeException`
        """
        return self._gelp_components_lower_bound
    
    @gelp_components_lower_bound.setter
    def gelp_components_lower_bound(self, _):
        raise ImmutableAttributeException(str(self), "gelp_components_lower_bound")
    
        
    @property
    def gelp_components_upper_bound(self):
        """
    
        Attempting to set `gelp_components_upper_bound` raises an `ImmutableAttributeException`
        """
        return self._gelp_components_upper_bound
    
    @gelp_components_upper_bound.setter
    def gelp_components_upper_bound(self, _):
        raise ImmutableAttributeException(str(self), "gelp_components_upper_bound")
    
        
    def toDict(self):
        """
        Generates a dictionary representation of the GELP message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.
    
        Returns
        -------
        dict
            A dictionary representation of the ##### message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the GELP results data
        jsonDict["data"]["version"] = self.version
        jsonDict["data"]["owner"] = self.owner
        jsonDict["data"]["config"] = self.config
        jsonDict["data"]["source"] = self.source
        jsonDict["data"]["dependencies"] = self.dependencies
        jsonDict["data"]["publishes"] = self.publishes
        jsonDict["data"]["subscribes"] = self.subscribes

        jsonDict["data"]["gelp_results"]["event_ts"] = self.event_ts
        jsonDict["data"]["gelp_results"]["participant_id"] = self.participant_id
        jsonDict["data"]["gelp_results"]["callsign"] = self.callsign
        jsonDict["data"]["gelp_results"]["elapsed_milliseconds"] = self.elapsed_milliseconds
        jsonDict["data"]["gelp_results"]["gelp_overall"] = self.gelp_overall
        jsonDict["data"]["gelp_results"]["gelp_lower_bound"] = self.gelp_lower_bound
        jsonDict["data"]["gelp_results"]["gelp_upper_bound"] = self.gelp_upper_bound
        jsonDict["data"]["gelp_results"]["gelp_components"] = self.gelp_components
        jsonDict["data"]["gelp_results"]["gelp_components_lower_bound"] = self.gelp_components_lower_bound
        jsonDict["data"]["gelp_results"]["gelp_components_upper_bound"] = self.gelp_components_upper_bound

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the GELP message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            GELP message.
        """

        return json.dumps(self.toDict())
