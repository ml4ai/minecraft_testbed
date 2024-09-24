# -*- coding: utf-8 -*-
"""
.. module:: cmu_ta2_ted
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Team Effectiveness Diagnostic Messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Team Effectiveness Diagnostic messages.
"""

import json

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage


class CMU_TA2_TED(BaseMessage):
    """
    A class encapsulating Team Effectiveness Diagnostic messages.

    Attributes
    ----------
    delta_ms : float
        Time difference from previous message
    team_score : float
        Points scored in previous period
    team_score_agg : float
        Total score since mission start
    process_effort_s : float
        Player seconds spent taking action (effort) in previous period.
        Max = 30 seconds (3 players active for 10 seconds each)
    process_effort_agg : float
        Total effort since mission start.  Aggregated and divided by total
        player seconds elapsed
    process_skill_use_s : float
        Player seconds spent exerting role-congruent effort in previous period
    process_skill_use_rel : float
        Player seconds spent exerting role-congruent effort relative to effort
        exerted in previous period
    process_skill_use_agg : float
        Percentage of time spent exerting role-congruent effort since mission
        start
    process_workload_burnt : float
        Percentage of search and rescue workload executed in previous period
    process_workload_burnt_agg : float
        Percentage of search and rescue workload executed since mission start
    message_equity : float
        balance of conversation (chat variance across players) in this period
    message_consistency_agg : float
        balance of conversation since mission start
    action_explore_s : float
        Player seconds spent searching unexplored cells in previous period
    explore_count : float
        New cells explored in previous period (Not sure -- may be mislabeled in
        message specs)
    process_coverage : float
        New cells explored in previous period
    process_coverage_agg : float
        Percentage of cells explored since mission start
    triage_count : float
        New victims triaged in previous period
    action_triage_s : float
        Player seconds spent triaging victims in previous period
    process_triaging_agg : float
        Percentage of maximum possible triage time completed since mission 
        start
    dig_rubble_count : float
        New rubble destroyed in previous period
    action_dig_rubble_s : float
        Player seconds spent destrying rubble in previous period
    move_victim_count : float
        Number of victims moved in previous period
    action_move_rubble_s : float
        Player seconds spent moving victims in previous period
    inaction_stand_s : float
        Player seconds spent not engaged in any activity in previous period
    message_freq : float
        Number of messages sent in previous period
    """

    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["delta_ms", "process_coverage", "process_coverage_agg",
                         "inaction_stand_s", "action_triage_s", "triage_count",
                         "action_dig_rubble_s", "dig_rubble_count",
                         "action_move_rubble_s", "move_victim_count",
                         "action_explore_s", "explore_count", "process_triaging_agg",
                         "team_score", "team_score_agg", "message_freq", "message_equity",
                         "message_consistency_agg", "process_skill_use_s",
                         "process_effort_s", "process_skill_use_rel", 
                         "process_workload_burnt", "process_skill_use_agg",
                         "process_effort_agg", "process_workload_burnt_agg"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._delta_ms = kwargs["delta_ms"]
        self._process_coverage = kwargs["process_coverage"]
        self._process_coverage_agg = kwargs["process_coverage_agg"]
        self._inaction_stand_s = kwargs["inaction_stand_s"]
        self._action_triage_s = kwargs["action_triage_s"]
        self._triage_count = kwargs["triage_count"]
        self._action_dig_rubble_s = kwargs["action_dig_rubble_s"]
        self._dig_rubble_count = kwargs["dig_rubble_count"]
        self._action_move_rubble_s = kwargs["action_move_rubble_s"]
        self._move_victim_count = kwargs["move_victim_count"]
        self._action_explore_s = kwargs["action_explore_s"]
        self._explore_count = kwargs["explore_count"]
        self._process_triaging_agg = kwargs["process_triaging_agg"]
        self._team_score = kwargs["team_score"]
        self._team_score_agg = kwargs["team_score_agg"]
        self._message_freq = kwargs["message_freq"]
        self._message_equity = kwargs["message_equity"]
        self._message_consistency_agg = kwargs["message_consistency_agg"]
        self._process_skill_use_s = kwargs["process_skill_use_s"]
        self._process_effort_s = kwargs["process_effort_s"]
        self._process_skill_use_rel = kwargs["process_skill_use_rel"]
        self._process_workload_burnt = kwargs["process_workload_burnt"]
        self._process_skill_use_agg = kwargs["process_skill_use_agg"]
        self._process_effort_agg = kwargs["process_effort_agg"]
        self._process_workload_burnt_agg = kwargs["process_workload_burnt_agg"]
        


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'CMU_TA2_TED')
        """

        return self.__class__.__name__


    @property
    def delta_ms(self):
        """

        Attempting to set `delta_ms` raises an `ImmutableAttributeException`.
        """
        return self._delta_ms

    @delta_ms.setter
    def delta_ms(self, _):
        raise ImmutableAttributeException(str(self), "delta_ms")


    @property
    def process_coverage(self):
        """

        Attempting to set `process_coverage` raises an `ImmutableAttributeException`.
        """
        return self._process_coverage

    @process_coverage.setter
    def process_coverage(self, _):
        raise ImmutableAttributeException(str(self), "process_coverage")


    @property
    def process_coverage_agg(self):
        """

        Attempting to set `process_coverage_agg` raises an `ImmutableAttributeException`.
        """
        return self._process_coverage_agg

    @process_coverage_agg.setter
    def process_coverage_agg(self, _):
        raise ImmutableAttributeException(str(self), "process_coverage_agg")


    @property
    def inaction_stand_s(self):
        """

        Attempting to set `inaction_stand_s` raises an `ImmutableAttributeException`.
        """
        return self._inaction_stand_s

    @inaction_stand_s.setter
    def inaction_stand_s(self, _):
        raise ImmutableAttributeException(str(self), "inaction_stand_s")


    @property
    def action_triage_s(self):
        """
        Attempting to set `action_triage_s` raises an `ImmutableAttributeException`.
        """
        return self._action_triage_s

    @action_triage_s.setter
    def action_triage_s(self, _):
        raise ImmutableAttributeException(str(self), "action_triage_s")


###    @property
###    def action_stand_s(self):
###        """
###
###        Attempting to set `action_stand_s` raises an `ImmutableAttributeException`.
###        """
###        return self._action_stand_s
###
###    @action_stand_s.setter
###    def action_stand_s(self, _):
###        raise ImmutableAttributeException(str(self), "action_stand_s")


    @property
    def triage_count(self):
        """

        Attempting to set `triage_count` raises an `ImmutableAttributeException`.
        """
        return self._triage_count

    @triage_count.setter
    def triage_count(self, _):
        raise ImmutableAttributeException(str(self), "triage_count")


    @property
    def action_dig_rubble_s(self):
        """

        Attempting to set `action_dig_rubble_s` raises an `ImmutableAttributeException`.
        """
        return self._action_dig_rubble_s

    @action_dig_rubble_s.setter
    def action_dig_rubble_s(self, _):
        raise ImmutableAttributeException(str(self), "action_dig_rubble_s")


    @property
    def dig_rubble_count(self):
        """

        Attempting to set `dig_rubble_count` raises an `ImmutableAttributeException`.
        """
        return self._dig_rubble_count

    @dig_rubble_count.setter
    def dig_rubble_count(self, _):
        raise ImmutableAttributeException(str(self), "dig_rubble_count")


    @property
    def action_move_rubble_s(self):
        """

        Attempting to set `action_move_rubble_s` raises an `ImmutableAttributeException`.
        """
        return self._action_move_rubble_s

    @action_move_rubble_s.setter
    def action_move_rubble_s(self, _):
        raise ImmutableAttributeException(str(self), "action_move_rubble_s")


    @property
    def move_victim_count(self):
        """

        Attempting to set `move_victim_count` raises an `ImmutableAttributeException`.
        """
        return self._move_victim_count

    @move_victim_count.setter
    def move_victim_count(self, _):
        raise ImmutableAttributeException(str(self), "move_victim_count")


    @property
    def action_explore_s(self):
        """

        Attempting to set `action_explore_s` raises an `ImmutableAttributeException`.
        """
        return self._action_explore_s

    @action_explore_s.setter
    def action_explore_s(self, _):
        raise ImmutableAttributeException(str(self), "action_explore_s")


    @property
    def explore_count(self):
        """

        Attempting to set `explore_count` raises an `ImmutableAttributeException`.
        """
        return self._explore_count

    @explore_count.setter
    def explore_count(self, _):
        raise ImmutableAttributeException(str(self), "explore_count")


    @property
    def process_triaging_agg(self):
        """

        Attempting to set `process_triaging_agg` raises an `ImmutableAttributeException`.
        """
        return self._process_triaging_agg

    @process_triaging_agg.setter
    def process_triaging_agg(self, _):
        raise ImmutableAttributeException(str(self), "process_triaging_agg")


    @property
    def team_score(self):
        """

        Attempting to set `team_score` raises an `ImmutableAttributeException`.
        """
        return self._team_score

    @team_score.setter
    def team_score(self, _):
        raise ImmutableAttributeException(str(self), "team_score")


    @property
    def team_score_agg(self):
        """

        Attempting to set `team_score_agg` raises an `ImmutableAttributeException`.
        """
        return self._team_score_agg

    @team_score_agg.setter
    def team_score_agg(self, _):
        raise ImmutableAttributeException(str(self), "team_score_agg")


    @property
    def message_freq(self):
        """

        Attempting to set `message_freq` raises an `ImmutableAttributeException`.
        """
        return self._message_freq

    @message_freq.setter
    def message_freq(self, _):
        raise ImmutableAttributeException(str(self), "message_freq")


    @property
    def message_equity(self):
        """

        Attempting to set `message_equity` raises an `ImmutableAttributeException`.
        """
        return self._message_equity

    @message_equity.setter
    def message_equity(self, _):
        raise ImmutableAttributeException(str(self), "message_equity")


    @property
    def message_consistency_agg(self):
        """

        Attempting to set `message_consistency_agg` raises an `ImmutableAttributeException`.
        """
        return self._message_consistency_agg

    @message_consistency_agg.setter
    def message_consistency_agg(self, _):
        raise ImmutableAttributeException(str(self), "message_consistency_agg")


    @property
    def process_skill_use_s(self):
        """

        Attempting to set `process_skill_use_s` raises an `ImmutableAttributeException`.
        """
        return self._process_skill_use_s

    @process_skill_use_s.setter
    def process_skill_use_s(self, _):
        raise ImmutableAttributeException(str(self), "process_skill_use_s")


    @property
    def process_effort_s(self):
        """

        Attempting to set `process_effort_s` raises an `ImmutableAttributeException`.
        """
        return self._process_effort_s

    @process_effort_s.setter
    def process_effort_s(self, _):
        raise ImmutableAttributeException(str(self), "process_effort_s")


    @property
    def process_skill_use_rel(self):
        """

        Attempting to set `process_skill_use_rel` raises an `ImmutableAttributeException`.
        """
        return self._process_skill_use_rel

    @process_skill_use_rel.setter
    def process_skill_use_rel(self, _):
        raise ImmutableAttributeException(str(self), "process_skill_use_rel")


    @property
    def process_workload_burnt(self):
        """

        Attempting to set `process_workload_burnt` raises an `ImmutableAttributeException`.
        """
        return self._process_workload_burnt

    @process_workload_burnt.setter
    def process_workload_burnt(self, _):
        raise ImmutableAttributeException(str(self), "process_workload_burnt")


    @property
    def process_skill_use_agg(self):
        """

        Attempting to set `process_skill_use_agg` raises an `ImmutableAttributeException`.
        """
        return self._process_skill_use_agg

    @process_skill_use_agg.setter
    def process_skill_use_agg(self, _):
        raise ImmutableAttributeException(str(self), "process_skill_use_agg")


    @property
    def process_effort_agg(self):
        """

        Attempting to set `process_effort_agg` raises an `ImmutableAttributeException`.
        """
        return self._process_effort_agg

    @process_effort_agg.setter
    def process_effort_agg(self, _):
        raise ImmutableAttributeException(str(self), "process_effort_agg")


    @property
    def process_workload_burnt_agg(self):
        """

        Attempting to set `process_workload_burnt_agg` raises an `ImmutableAttributeException`.
        """
        return self._process_workload_burnt_agg


    @process_workload_burnt_agg.setter
    def process_workload_burnt_agg(self, _):
        raise ImmutableAttributeException(str(self), "process_workload_burnt_agg")


    def toDict(self):
        """
        Generates a dictionary representation of the ##### message.
        Message information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the Team Effectiveness Diagnostic message.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the TED data
        jsonDict["data"]["delta_ms"] = self.delta_ms
        jsonDict["data"]["process_coverage"] = self.process_coverage
        jsonDict["data"]["process_coverage_agg"] = self.process_coverage_agg
        jsonDict["data"]["inaction_stand_s"] = self.inaction_stand_s
        jsonDict["data"]["action_triage_s"] = self.action_triage_s
        jsonDict["data"]["triage_count"] = self.triage_count
        jsonDict["data"]["action_dig_rubble_s"] = self.action_dig_rubble_s
        jsonDict["data"]["dig_rubble_count"] = self.dig_rubble_count
        jsonDict["data"]["action_move_rubble_s"] = self.action_move_rubble_s
        jsonDict["data"]["move_victim_count"] = self.move_victim_count
        jsonDict["data"]["action_explore_s"] = self.action_explore_s
        jsonDict["data"]["explore_count"] = self.explore_count
        jsonDict["data"]["process_triaging_agg"] = self.process_triaging_agg
        jsonDict["data"]["team_score"] = self.team_score
        jsonDict["data"]["team_score_agg"] = self.team_score_agg
        jsonDict["data"]["message_freq"] = self.message_freq
        jsonDict["data"]["message_equity"] = self.message_equity
        jsonDict["data"]["message_consistency_agg"] = self.message_consistency_agg
        jsonDict["data"]["process_skill_use_s"] = self.process_skill_use_s
        jsonDict["data"]["process_effort_s"] = self.process_effort_s
        jsonDict["data"]["process_skill_use_rel"] = self.process_skill_use_rel
        jsonDict["data"]["process_workload_burnt"] = self.process_workload_burnt
        jsonDict["data"]["process_skill_use_agg"] = self.process_skill_use_agg
        jsonDict["data"]["process_effort_agg"] = self.process_effort_agg
        jsonDict["data"]["process_workload_burnt_agg"] = self.process_workload_burnt_agg

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the Team Effectiveness Diagnostic message.  
        Message information is contained in a JSON object under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            Team EffectivenessDiagnostic message.
        """

        return json.dumps(self.toDict())
