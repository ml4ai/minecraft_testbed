# -*- coding: utf-8 -*-
"""
.. module:: dispatchers
   :platform: Linux, Windows, OSX
   :synopsis: Library of message dispatchers to allow for variability in how
              messages are handled

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

The dispatchers modules provides a set of dispatchers to store and dispatch
messages as they become available.  The purpose is to allow for modifying the
way the agent handles backlogged messages, and to allow a simple means of
trading off between completeness and efficience.
"""

from .stack import Stack
from .queue import Queue
from .singleton import Singleton
from .latest_player_state import LatestPlayerStateDispatcher
from .ignore_multiple_player_state import IgnoreMultiplePlayerStateDispatcher

__all__ = ["Stack", "Queue", "Singleton", "LatestPlayerStateDispatcher", "IgnoreMultiplePlayerStateDispatcher"]