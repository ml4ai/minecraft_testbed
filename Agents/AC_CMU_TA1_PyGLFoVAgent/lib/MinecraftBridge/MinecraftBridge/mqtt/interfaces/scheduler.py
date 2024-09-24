# -*- coding: utf-8 -*-
"""
.. module:: scheduler
   :platform: Linux, Windows, OSX
   :synopsis: A class for scheduling callbacks on Minecraft mission time.

.. moduleauthor:: Ini Oguntola <ioguntol@andrew.cmu.edu>

This file provides a class suitable for scheduling callbacks to
synchronize with the Minecraft mission timer.
"""

from .base import MinecraftInterface
from ...messages import PlayerState, Trial
from ...utils import BaseScheduler



class SchedulerInterface(BaseScheduler, MinecraftInterface):
    """
    A Scheduler that receives mission time by registering itself with a bridge
    interface, and receiving PlayerState messages through a registered 
    callback.

    Attributes
    ----------
    time : float
        Current mission time, in seconds
    time_remaining : float
        Number of seconds remaining in the mission

    Methods
    -------
    schedule(callback, time)
        Schedule a callback to be called at a particular timestamp
    countdown(callback, t_minus)
        Schedule a callback to be called with a specific amount of time remaining
    wait(callback, delay)
        Schedule a callback to be called after a specified delay
    repeat(callback, interval)
        Schedule a callback to be called at regular intervals
    pause()
        Pause the scheduler
    resume()
        Resume the scheduler
    reset()
        Reset the mission time and clear any pending events
    """

    # MinecraftBridge message types to register with
    MESSAGE_CLASSES = [PlayerState, Trial]


    def __init__(self, bridge, *args, **kwargs):
        """
        Arguments:
            - bridge: a MinecraftBridge or MinecraftInterface object
            - blocking: boolean indicating whether scheduled callbacks should block
                other callbacks, as opposed to executing in a background thread
        """
        BaseScheduler.__init__(self, *args, **kwargs)
        MinecraftInterface.__init__(self, bridge)

        # Register with the bridge
        for message_class in self.__class__.MESSAGE_CLASSES:
            self._unwrapped.register(self, message_class)
