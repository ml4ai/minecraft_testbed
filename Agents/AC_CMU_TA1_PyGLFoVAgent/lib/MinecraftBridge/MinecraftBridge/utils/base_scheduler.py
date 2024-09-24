# -*- coding: utf-8 -*-
"""
.. module:: scheduler
   :platform: Linux, Windows, OSX
   :synopsis: A class for scheduling callbacks on Minecraft mission time.

.. moduleauthor:: Ini Oguntola <ioguntol@andrew.cmu.edu>

This file provides a class suitable for scheduling callbacks to
synchronize with the Minecraft mission timer.
"""
import concurrent.futures
import queue



class _Event:

    def __init__(self, callback, interval=None, args=(), kwargs={}):
        self.callback, self.interval = callback, interval
        self.args, self.kwargs = args, kwargs

    def __call__(self):
        self.callback(*self.args, **self.kwargs)

    def __lt__(self, _):
        return False



class BaseScheduler:
    """
    A scheduler based only on the Minecraft mission timer,
    that determines the current time from messages received via a MinecraftBridge.

    Allows for scheduling callbacks that are synchronized with mission time.

    Usage
    -----
    ```
    scheduler = BaseScheduler()
    bridge.register(PlayerState, scheduler)
    ```

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
    receive(message)
        Update the scheduler from a MinecraftBridge message
    """

    def __init__(self, blocking=True):
        """
        Arguments:
            - blocking: boolean indicating whether scheduled callbacks should block
                other callbacks, as opposed to executing in a background thread
        """
        self._time = None
        self._mission_length = None

        self._events = queue.PriorityQueue()
        self._executor = concurrent.futures.ThreadPoolExecutor()
        self._blocking = blocking
        self._paused = False # indicate if pending events should be executed

        # For countdown events scheduled before `self._mission_length` is set
        self._countdown_buffer = []

        # For delayed events scheduled before `self.time` is set
        self._delay_buffer = []

        # Reset on Trial messages
        from ..messages import Trial
        self._reset_message_types = (Trial,)


    @property
    def time(self):
        """
        Returns the current mission time (in seconds).
        """
        return self._time


    @property
    def time_remaining(self):
        """
        Returns the number of seconds remaining in the mission.
        """
        if self._mission_length is not None and self._time is not None:
            return self._mission_length - self._time


    def schedule(self, callback, time, args=(), kwargs={}):
        """
        Schedule a callback to be called at a particular timestamp.

        Arguments:
            - callback: the function to be called
            - time: mission time (in seconds) at which to trigger the callback
            - args: list of arguments to the callback
            - kwargs: dictionary of keyword arguments to the callback
        """
        event = _Event(callback, args=args, kwargs=kwargs)
        self._events.put((time, event))


    def countdown(self, callback, t_minus, args=(), kwargs={}):
        """
        Schedule a callback to be called when there is a given amount of
        time remaining in the mission.

        Arguments:
            - callback: the function to be called
            - t_minus: number of remaining seconds at which to trigger the callback
            - args: list of arguments to the callback
            - kwargs: dictionary of keyword arguments to the callback
        """
        event = _Event(callback, args=args, kwargs=kwargs)

        if self._mission_length is None:
            self._countdown_buffer.append((t_minus, event))
        else:
            self._events.put((self._mission_length - t_minus, event))


    def wait(self, callback, delay, args=(), kwargs={}):
        """
        Schedule a callback to be called after a specified delay.

        Arguments:
            - callback: the function to be called
            - delay: number of seconds (in mission time) after the current
                mission time to wait before triggering the callback
            - args: list of arguments to the callback
            - kwargs: dictionary of keyword arguments to the callback
        """
        event = _Event(callback, args=args, kwargs=kwargs)

        if self.time is None:
            self._delay_buffer.append((delay, event))
        else:
            self._events.put((self.time + delay, event))


    def repeat(self, callback, interval, args=(), kwargs={}):
        """
        Schedule a callback to be called at regular intervals.

        Arguments:
            - callback: a function to be called
            - interval: regular interval of mission time (in seconds)
                at which to trigger the callback
            - args: list of arguments to the callback
            - kwargs: dictionary of keyword arguments to the callback
        """
        event = _Event(callback, interval=interval, args=args, kwargs=kwargs)

        if self.time is None:
            self._delay_buffer.append((0, event))
        else:
            self._events.put((self.time, event))


    def pause(self):
        """
        Pause the scheduler.
        """
        self._paused = True


    def resume(self):
        """
        Resume the scheduler.
        """
        self._paused = False
        self._execute_pending_events()


    def reset(self):
        """
        Reset the mission time and clear any pending events.
        """
        self._clear_event_queue()
        self._executor.shutdown()
        self._time = None
        self._mission_length = None
        self._executor = concurrent.futures.ThreadPoolExecutor()


    def receive(self, msg):
        """
        Callback upon receiving a message from a MinecraftBridge.
        """
        if isinstance(msg, self._reset_message_types):
            self.reset()

        if msg.elapsed_milliseconds < 0:
            return

        # Update mission time
        if self.time is None:
            self._time = msg.elapsed_milliseconds / 1000
        else:
            self._time = max(self._time, msg.elapsed_milliseconds / 1000)

        # Add any delayed events to the event queue
        self._add_delayed_events()

        # Update mission length and add countdown events to the event queue
        if self._mission_length is None and msg.mission_timer != (-1, -1):
            self._mission_length = self._time + 60 * msg.mission_timer[0] + msg.mission_timer[1]
            self._add_countdown_events()

        # Execute any pending events
        self._execute_pending_events()


    def _add_countdown_events(self):
        """
        Move events from the countdown buffer to the event queue.
        """
        if self._mission_length is None:
            return

        for t_minus, event in self._countdown_buffer:
            self._events.put((self._mission_length - t_minus, event))

        self._countdown_buffer.clear()


    def _add_delayed_events(self):
        """
        Move events from the delay buffer to the event queue.
        """
        if self.time is None:
            return

        for delay, event in self._delay_buffer:
            self._events.put((self.time + delay, event))

        self._delay_buffer.clear()


    def _clear_event_queue(self):
        """
        Clear the event queue (except repeating events).
        """
        repeating_events = []
        while not self._events.empty():
            _, event = self._events.get()
            if event.interval is not None:
                repeating_events.append(event)

        # Put repeating events back onto the event queue
        for event in repeating_events:
            self._events.put((0, event))


    def _execute_pending_events(self):
        """
        Execute any pending events.
        """
        while self.time is not None and self._time >= self._next_event_time() and not self._paused:
            # Pop the next event off the queue and execute it
            time, event = self._events.get()
            if self._blocking:
                event()
            else:
                self._executor.submit(event)

            # If this is a repeating event, schedule it again
            if event.interval is not None:
                self._events.put((time + event.interval, event))


    def _next_event_time(self):
        """
        Time of the next event (mission time, in seconds).
        """
        if len(self._events.queue) > 0:
            time, event = self._events.queue[0]
            return time

        return float('inf')

