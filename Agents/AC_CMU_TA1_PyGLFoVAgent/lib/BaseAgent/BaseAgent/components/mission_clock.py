# -*- coding: utf-8 -*-
"""
.. module:: mission_clock
   :platform: Linux, Windows, OSX
   :synopsis: Definition of a component for maintaining mission time information
              and alerting listeners to updates to time.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

This component is used to expose mission time information to interested 
parties, and accept callbacks for when the mission timer is updated.
"""

from MinecraftBridge.utils import Loggable



class MissionClock(Loggable):
    """
    Lightweight class for providing access to mission time.  Mission time is
    extracted from PlayerState messages, which are published at a rate of 
    roughly 10 Hz.



    Attributes
    ----------
    mission_timer : tuple or None
        A tuple of ints indicating the minutes and seconds remaining
    elapsed_milliseconds : int or None
        Number of seconds since mission start
    """

    def __init__(self, **kwargs):
        """
        Keyword Arguments
        -----------------
        fidelity : int, default=0
            Minimal amount of time to pass between informing observers with
            `on_tick` callbacks.  Used to minimize unnecessary updates from 
            closely timed PlayerState events.
        """

        self._fidelity = kwargs.get("fidelity", 0)

        self._mission_timer = None
        self._elapsed_milliseconds = None

        self._observers = set()


    def __str__(self):
        """
        String representation of the MissionTime
        """

        if self._mission_timer is None:
            mission_time_string = "Timer Not Running"
        else:
            mission_time_string = f'{self._mission_timer[0]:02d}:{self._mission_timer[1]:02d}'

        return f'{self.__class__.__name__} [{mission_time_string}]'


    @property
    def mission_timer(self):
        """
        The current mission timer, as a tuple (minutes,seconds)
        """

        return self._mission_timer

    @property
    def elapsed_milliseconds(self):
        """
        Milliseconds elapsed since the start of the mission
        """

        return self._elapsed_milliseconds


    def register_observer(self, observer):
        """
        Add a component to be informed whenever time changes

        Arguments
        ---------
        observer
            Component to call when the time is updated.  The component must 
            implement `on_tick`
        """

        self._observers.add(observer)


    def deregister_observer(self, observer):
        """
        Remove an observing component

        Arguments
        ---------
        observer
            Component to remove from receiving update callbacks
        """

        if not observer in self._observers:
            self.logger.debug(f'{self}: Attempting to remove an unregistered observer: {observer}')

        self._observers.remove(observer)


    def __notify_observers(self):
        """
        Notify Mission Time observers that the time has been updated
        """

        for observer in self._observers:
            observer.on_tick()


    def _onPlayerState(self, message):
        """
        Callback when a PlayerState message is received.

        message : MinecraftBridge.messages.PlayerState
        """

        # Do we have a valid mission timer?  If not, then write this one down
        if self._elapsed_milliseconds is None:
            self._elapsed_milliseconds = message.elapsed_milliseconds
            self._mission_timer = message.mission_timer
            self.__notify_observers()
            return

        # Don't bother updating if not enough milliseconds have passed
        if (message.elapsed_milliseconds - self._elapsed_milliseconds) < self._fidelity:
            return

        self._elapsed_milliseconds = message.elapsed_milliseconds
        self._mission_timer = message.mission_timer
        self.__notify_observers()


    def _onMissionState(self, message):
        """
        Callback when a MissionState message is received.

        message : MinecraftBridge.messages.MissionState
        """

        if message.state.is_start_state():
            self._elapsed_milliseconds = message.elapsed_milliseconds
            self._mission_timer = message.mission_timer
        else:
            self._elapsed_milliseconds = None
            self._mission_timer = None

        self.__notify_observers()
