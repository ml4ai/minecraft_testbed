# -*- coding: utf-8 -*-
"""
.. module:: cmu_ta2_beard
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating CMU TA2 BEARD AC output

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Background of Experience, Affect, and
Resources Diagnostic (BEARD) analytic component.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class ParticipantProfile:
    """
    Profile information for a single participant.

    Attributes
    ----------
    anger : float
    anxiety : float
    rmie : float
    mission_knowledge : float
    sbsod : float
    gaming_experience : float
    walking_skill : float
    victim_moving_skill : float
    role : string
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        anger : float
        anxiety : float
        rmie : float
        mission_knowledge : float
        sbsod : float
        gaming_experience : float
        walking_skill : float
        victim_moving_skill : float
        role : string
        """

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["anger", "anxiety", "rmie", "mission_knowledge",
                         "sbsod", "gaming_experience", "walking_skill",
                         "victim_moving_skill", "role"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._anger = float(kwargs["anger"])
        self._anxiety = float(kwargs["anxiety"])
        self._rmie = float(kwargs["rmie"])
        self._mission_knowledge = float(kwargs["mission_knowledge"])
        self._sbsod = float(kwargs["sbsod"])
        self._gaming_experience = float(kwargs["gaming_experience"])
        self._walking_skill = float(kwargs["walking_skill"])
        self._victim_moving_skill = float(kwargs["victim_moving_skill"])
        self._role = kwargs["role"]


    @property
    def anger(self):
        """

        Attempting to set `anger` raises an `ImmutableAttributeException`.
        """
        return self._anger

    @anger.setter
    def anger(self, _):
        raise ImmutableAttributeException(str(self), "anger")


    @property
    def anxiety(self):
        """

        Attempting to set `anxiety` raises an `ImmutableAttributeException`.
        """
        return self._anxiety

    @anxiety.setter
    def anxiety(self, _):
        raise ImmutableAttributeException(str(self), "anxiety")


    @property
    def rmie(self):
        """

        Attempting to set `rmie` raises an `ImmutableAttributeException`.
        """
        return self._rmie

    @rmie.setter
    def rmie(self, _):
        raise ImmutableAttributeException(str(self), "rmie")


    @property
    def mission_knowledge(self):
        """

        Attempting to set `mission_knowledge` raises an `ImmutableAttributeException`.
        """
        return self._mission_knowledge

    @mission_knowledge.setter
    def mission_knowledge(self, _):
        raise ImmutableAttributeException(str(self), "mission_knowledge")


    @property
    def sbsod(self):
        """

        Attempting to set `sbsod` raises an `ImmutableAttributeException`.
        """
        return self._sbsod

    @sbsod.setter
    def sbsod(self, _):
        raise ImmutableAttributeException(str(self), "sbsod")


    @property
    def gaming_experience(self):
        """

        Attempting to set `gaming_experience` raises an `ImmutableAttributeException`.
        """
        return self._gaming_experience

    @gaming_experience.setter
    def gaming_experience(self, _):
        raise ImmutableAttributeException(str(self), "gaming_experience")


    @property
    def walking_skill(self):
        """

        Attempting to set `walking_skill` raises an `ImmutableAttributeException`.
        """
        return self._walking_skill

    @walking_skill.setter
    def walking_skill(self, _):
        raise ImmutableAttributeException(str(self), "walking_skill")


    @property
    def victim_moving_skill(self):
        """

        Attempting to set `victim_moving_skill` raises an `ImmutableAttributeException`.
        """
        return self._victim_moving_skill

    @victim_moving_skill.setter
    def victim_moving_skill(self, _):
        raise ImmutableAttributeException(str(self), "victim_moving_skill")


    @property
    def role(self):
        """

        Attempting to set `role` raises an `ImmutableAttributeException`.
        """
        return self._role

    @role.setter
    def role(self, _):
        raise ImmutableAttributeException(str(self), "role")


    def toDict(self):
        """
        Create a dictionary representation of the message
        """

        return { "anger": self.anger,
                 "anxiety": self.anxiety,
                 "rmie": self.rmie,
                 "mission_knowledge": self.mission_knowledge,
                 "sbsod": self.sbsod,
                 "gaming_experience": self.gaming_experience,
                 "walking_skill": self.walking_skill,
                 "victim_moving_skill": self.victim_moving_skill,
                 "role": self.role
               }






class TeamProfile:
    """
    Profile information for the team.

    Attributes
    ----------
    anger_mean : float
    anger_sd : float
    anxiety_mean : float
    anxiety_sd : float
    rmie_mean : float
    rmie_sd : float
    mission_knowledge_mean : float
    mission_knowledge_sd : float
    sbsod_mean : float
    sbsod_sd : float
    gaming_experience_mean : float
    gaming_experience_sd : float
    walking_skill_mean : float
    walking_skill_sd : float
    victim_moving_skill_mean : float
    victim_moving_skill_sd : float
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        anger_mean : float
        anger_sd : float
        anxiety_mean : float
        anxiety_sd : float
        rmie_mean : float
        rmie_sd : float
        mission_knowledge_mean : float
        mission_knowledge_sd : float
        sbsod_mean : float
        sbsod_sd : float
        gaming_experience_mean : float
        gaming_experience_sd : float
        walking_skill_mean : float
        walking_skill_sd : float
        victim_moving_skill_mean : float
        victim_moving_skill_sd : float
        """

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["anger_mean", "anger_sd", "anxiety_mean", "anxiety_sd",
                         "rmie_mean", "rmie_sd", "mission_knowledge_mean",
                         "mission_knowledge_sd", "sbsod_mean", "sbsod_sd",
                         "gaming_experience_mean", "gaming_experience_sd",
                         "walking_skill_mean", "walking_skill_sd",
                         "victim_moving_skill_mean", "victim_moving_skill_sd"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None


        self._anger_mean = float(kwargs["anger_mean"])
        self._anger_sd = float(kwargs["anger_sd"])
        self._anxiety_mean = float(kwargs["anxiety_mean"])
        self._anxiety_sd = float(kwargs["anxiety_sd"])
        self._rmie_mean = float(kwargs["rmie_mean"])
        self._rmie_sd = float(kwargs["rmie_sd"])
        self._mission_knowledge_mean = float(kwargs["mission_knowledge_mean"])
        self._mission_knowledge_sd = float(kwargs["mission_knowledge_sd"])
        self._sbsod_mean = float(kwargs["sbsod_mean"])
        self._sbsod_sd = float(kwargs["sbsod_sd"])
        self._gaming_experience_mean = float(kwargs["gaming_experience_mean"])
        self._gaming_experience_sd = float(kwargs["gaming_experience_sd"])
        self._walking_skill_mean = float(kwargs["walking_skill_mean"])
        self._walking_skill_sd = float(kwargs["walking_skill_sd"])
        self._victim_moving_skill_mean = float(kwargs["victim_moving_skill_mean"])
        self._victim_moving_skill_sd = float(kwargs["victim_moving_skill_sd"])


    @property
    def anger_mean(self):
        """

        Attempting to set `anger_mean` raises an `ImmutableAttributeException`
        """

        return self._anger_mean

    @anger_mean.setter
    def anger_mean(self, _):
        raise ImmutableAttributeException(str(self), "anger_mean")


    @property
    def anger_sd(self):
        """

        Attempting to set `anger_sd` raises an `ImmutableAttributeException`
        """

        return self._anger_sd

    @anger_sd.setter
    def anger_sd(self, _):
        raise ImmutableAttributeException(str(self), "anger_sd")


    @property
    def anxiety_mean(self):
        """

        Attempting to set `anxiety_mean` raises an `ImmutableAttributeException`
        """

        return self._anxiety_mean

    @anxiety_mean.setter
    def anxiety_mean(self, _):
        raise ImmutableAttributeException(str(self), "anxiety_mean")


    @property
    def anxiety_sd(self):
        """

        Attempting to set `anxiety_sd` raises an `ImmutableAttributeException`
        """

        return self._anxiety_sd

    @anxiety_sd.setter
    def anxiety_sd(self, _):
        raise ImmutableAttributeException(str(self), "anxiety_sd")


    @property
    def rmie_mean(self):
        """

        Attempting to set `rmie_mean` raises an `ImmutableAttributeException`
        """

        return self._rmie_mean

    @rmie_mean.setter
    def rmie_mean(self, _):
        raise ImmutableAttributeException(str(self), "rmie_mean")


    @property
    def rmie_sd(self):
        """

        Attempting to set `rmie_sd` raises an `ImmutableAttributeException`
        """

        return self._rmie_sd

    @rmie_sd.setter
    def rmie_sd(self, _):
        raise ImmutableAttributeException(str(self), "rmie_sd")


    @property
    def mission_knowledge_mean(self):
        """

        Attempting to set `mission_knowledge_mean` raises an `ImmutableAttributeException`
        """

        return self._mission_knowledge_mean

    @mission_knowledge_mean.setter
    def mission_knowledge_mean(self, _):
        raise ImmutableAttributeException(str(self), "mission_knowledge_mean")


    @property
    def mission_knowledge_sd(self):
        """

        Attempting to set `mission_knowledge_sd` raises an `ImmutableAttributeException`
        """

        return self._mission_knowledge_sd

    @mission_knowledge_sd.setter
    def mission_knowledge_sd(self, _):
        raise ImmutableAttributeException(str(self), "mission_knowledge_sd")


    @property
    def sbsod_mean(self):
        """

        Attempting to set `sbsod_mean` raises an `ImmutableAttributeException`
        """

        return self._sbsod_mean

    @sbsod_mean.setter
    def sbsod_mean(self, _):
        raise ImmutableAttributeException(str(self), "sbsod_mean")


    @property
    def sbsod_sd(self):
        """

        Attempting to set `sbsod_sd` raises an `ImmutableAttributeException`
        """

        return self._sbsod_sd

    @sbsod_sd.setter
    def sbsod_sd(self, _):
        raise ImmutableAttributeException(str(self), "sbsod_sd")


    @property
    def gaming_experience_mean(self):
        """

        Attempting to set `gaming_experience_mean` raises an `ImmutableAttributeException`
        """

        return self._gaming_experience_mean

    @gaming_experience_mean.setter
    def gaming_experience_mean(self, _):
        raise ImmutableAttributeException(str(self), "gaming_experience_mean")


    @property
    def gaming_experience_sd(self):
        """

        Attempting to set `gaming_experience_sd` raises an `ImmutableAttributeException`
        """

        return self._gaming_experience_sd

    @gaming_experience_sd.setter
    def gaming_experience_sd(self, _):
        raise ImmutableAttributeException(str(self), "gaming_experience_sd")


    @property
    def walking_skill_mean(self):
        """

        Attempting to set `walking_skill_mean` raises an `ImmutableAttributeException`
        """

        return self._walking_skill_mean

    @walking_skill_mean.setter
    def walking_skill_mean(self, _):
        raise ImmutableAttributeException(str(self), "walking_skill_mean")


    @property
    def walking_skill_sd(self):
        """

        Attempting to set `walking_skill_sd` raises an `ImmutableAttributeException`
        """

        return self._walking_skill_sd

    @walking_skill_sd.setter
    def walking_skill_sd(self, _):
        raise ImmutableAttributeException(str(self), "walking_skill_sd")


    @property
    def victim_moving_skill_mean(self):
        """

        Attempting to set `victim_moving_skill_mean` raises an `ImmutableAttributeException`
        """

        return self._victim_moving_skill_mean

    @victim_moving_skill_mean.setter
    def victim_moving_skill_mean(self, _):
        raise ImmutableAttributeException(str(self), "victim_moving_skill_mean")


    @property
    def victim_moving_skill_sd(self):
        """

        Attempting to set `victim_moving_skill_sd` raises an `ImmutableAttributeException`
        """

        return self._victim_moving_skill_sd

    @victim_moving_skill_sd.setter
    def victim_moving_skill_sd(self, _):
        raise ImmutableAttributeException(str(self), "victim_moving_skill_sd")


    def toDict(self):
        """
        """

        return { "anger_mean": self.anger_mean,
                 "anger_sd": self.anger_sd,
                 "anxiety_mean": self.anxiety_mean,
                 "anxiety_sd": self.anxiety_sd,
                 "rmie_mean": self.rmie_mean,
                 "rmie_sd": self.rmie_sd,
                 "mission_knowledge_mean": self.mission_knowledge_mean,
                 "mission_knowledge_sd": self.mission_knowledge_sd,
                 "sbsod_mean": self.sbsod_mean,
                 "sbsod_sd": self.sbsod_sd,
                 "gaming_experience_mean": self.gaming_experience_mean,
                 "gaming_experience_sd": self.gaming_experience_sd,
                 "walking_skill_mean": self.walking_skill_mean,
                 "walking_skill_sd": self.walking_skill_sd,
                 "victim_moving_skill_mean": self.victim_moving_skill_mean,
                 "victim_moving_skill_sd": self.victim_moving_skill_sd
               }






class CMU_TA2_BEARD(BaseMessage):
    """
    A class encapsulating BEARD messages.


    Attributes
    ----------
    team : TeamProfile
        The team profile
    BLUE_ASIST1 : PlayerProfile
        The profile for the BLUE_ASIST1 player
    GREEN_ASIST1 : PlayerProfile
        The profile for the GREEN_ASIST1 player
    RED_ASIST1 : PlayerProfile
        The profile for the RED_ASIST1 player
    """


    def __init__(self, **kwargs):
        
        BaseMessage.__init__(self, **kwargs)

        for arg_name in ["team", "BLUE_ASIST1", "GREEN_ASIST1", "RED_ASIST1"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._team = TeamProfile(**kwargs["team"])
        self._BLUE_ASIST1 = ParticipantProfile(**kwargs["BLUE_ASIST1"])
        self._GREEN_ASIST1 = ParticipantProfile(**kwargs["GREEN_ASIST1"])
        self._RED_ASIST1 = ParticipantProfile(**kwargs["RED_ASIST1"])

    

    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'CMU_TA2_BEARD')
        """

        return self.__class__.__name__


    @property
    def team(self):
        """

        Attempting to set `team` raises an `ImmutableAttributeException`
        """

        return self._team

    @team.setter
    def team(self, _):
        raise ImmutableAttributeException(str(self), "team")


    @property
    def BLUE_ASIST1(self):
        """

        Attempting to set `BLUE_ASIST1` raises an `ImmutableAttributeException`
        """

        return self._BLUE_ASIST1

    @BLUE_ASIST1.setter
    def BLUE_ASIST1(self, _):
        raise ImmutableAttributeException(str(self), "BLUE_ASIST1")


    @property
    def GREEN_ASIST1(self):
        """

        Attempting to set `GREEN_ASIST1` raises an `ImmutableAttributeException`
        """

        return self._GREEN_ASIST1

    @GREEN_ASIST1.setter
    def GREEN_ASIST1(self, _):
        raise ImmutableAttributeException(str(self), "GREEN_ASIST1")


    @property
    def RED_ASIST1(self):
        """

        Attempting to set `RED_ASIST1` raises an `ImmutableAttributeException`
        """

        return self._RED_ASIST1

    @RED_ASIST1.setter
    def RED_ASIST1(self, _):
        raise ImmutableAttributeException(str(self), "RED_ASIST1")


    def toDict(self):
        """
        Generates a dictionary representation of the CMU_TA2_BEARD message.  
        CMU_TA2_BEARD information is contained in a dictionary under the key
        "data".  Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the CMU_TA2_BEARD.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the beep event data
        jsonDict["data"]["team"] = self.team.toDict()
        jsonDict["data"]["BLUE_ASIST1"] = self.BLUE_ASIST1.toDict()
        jsonDict["data"]["GREEN_ASIST1"] = self.GREEN_ASIST1.toDict()
        jsonDict["data"]["RED_ASIST1"] = self.RED_ASIST1.toDict()
        
        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the CMU_TA2_BEARD message.  
        CMU_TA2_BEARD information is contained in a JSON object under the key
        "data".  Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            CMU_TA2_BEARD message.
        """

        return json.dumps(self.toDict())
