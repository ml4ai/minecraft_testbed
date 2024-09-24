# -*- coding: utf-8 -*-
"""
.. module:: ASIST_BaseAgent
   :platform: Linux, Windows, OSX
   :synopsis: ASIST_BaseAgent module

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Package containing a BaseAgent for use in ASIST.  The purpose of the BaseAgent
is to primarily maintain connection with the


"""

__author__ = "Dana Hughes"
__email__ = "danahugh@andrew.cmu.edu"
__url__ = "https://gitlab.com/cmu_asist/ASIST_BaseAgent"
__version__ = "0.1.3"

from .agent import BaseAgent, BootstrapAgent
from .context import MissionContext
from .components.participant import Participant, ParticipantCollection
from .components.semantic_map import SemanticMap

__all__ = [
   "BaseAgent", "BootstrapAgent", "MissionContext",
   "Participant", "ParticipantCollection", "SemanticMap"]
