# -*- coding: utf-8 -*-
"""
.. module:: heartbeat
   :platform: Linux, Windows, OSX
   :synopsis: Definition of a class that runs a thread for generating heartbeat
              messages.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""

import threading
import time

from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype

from MinecraftBridge.messages import (
    BusHeader,
    MessageHeader,
    Status
)

from MinecraftBridge.utils import Loggable



class HeartbeatThread(threading.Thread, Loggable):
    """
    Class to maintain a thread for handling heartbeat generation messages.
    Heartbeat messages need to be generated while trials are active, and should
    produce a message every few (e.g., 20) seconds to inform the testbed that 
    it is alive.

    Attributes
    ----------

    Methods
    -------
    send_heartbeats(send)
        Indicate whether heartbeat messages should be sent or not
    """

    def __init__(self, minecraft_bridge, trial_info, parent, 
                       heartbeat_rate = 10, **kwargs):
        """
        Arguments
        ---------
        minecraft_bridge : MinecraftBridge interface
            Interface to the bridge to publish and subscribe to
        trial_info : dictionary
            Dictionary of trial information maintained by the BaseAgent
        parent : BaseAgent
            Instance of the agent associated with the heartbeat, used to elicit
            status information
        heartbeat_rate : float
            Number of seconds between heartbeat messages
        """

        threading.Thread.__init__(self)

        self._minecraft_bridge = minecraft_bridge
        self._trial_info = trial_info

        self.heartbeat_rate = heartbeat_rate

        self.__next_heartbeat_time = time.time()
        self.__run_heartbeats = False
        self.__send_heartbeats = False

        self._agent = parent

        # Get the agent's name from the parent, if provided.  Otherwise, see
        # if it was provided by the keyword arguments.
        if self._agent is not None:
            self._agent_name = self._agent.agent_name
        else:
            if not "agent_name" in kwargs:
                self.logger.warning("%s:  agent_name not provided in keyword arguments", self)
            self._agent_name = kwargs.get("agent_name", "ASI_CMU_TA1_ATLAS")


    def send_heartbeats(self, send=True):
        """
        Indicate that the thread should produce heartbeats or not.

        Arguments
        ---------
        send : boolean, default=True
            Indicate if heartbeat messages should be generated (true) or not
        """

        self.__send_heartbeats = send



    def __publish_heartbeat(self):
        """
        Helper function that creates and publishes the heartbeat message.
        """

        self.logger.debug("%s:  Publishing heartbeat message", self)

        # Get the status of the agent.
        try:
            state, status, active = self._agent.get_status()
        except Exception as e:
            # Somehow, statis information is unavailable.  Send a warning, and
            # provide the exception message as status info
            state = Status.State.WARN
            status = f"Exception when querying status: {str(e)}"
            active = self.__send_heartbeats

        # Construct the message to publish
        message = Status(state=state, status=status, active=active)

        # Add header with trial information
        bus_header = BusHeader(MessageType.status)
        msg_header = MessageHeader(MessageSubtype.heartbeat,
                                   self._trial_info["experiment_id"],
                                   self._trial_info["trial_id"],
                                   self._agent_name,
                                   replay_id = self._trial_info["replay_id"])

        message.addHeader("header", bus_header)
        message.addHeader("msg", msg_header)

        self._minecraft_bridge.send(message)



    def run(self):
        """
        Callback when the thread is started.  Starts a loop that sends
        heartbeats at the given rate
        """

        self.logger.debug("%s:  Starting Heartbeat Thread", self)

        self.__run_heartbeats = True

        # Sit in an infinite loop while the heartbeat thread runs
        while self.__run_heartbeats:

            if self.__send_heartbeats:

                if time.time() > self.__next_heartbeat_time:

                    # Set up the next heartbeat timing and send the heartbeat
                    # message
                    self.__next_heartbeat_time = time.time() + self.heartbeat_rate
                    self.__publish_heartbeat()

                    self.logger.debug("%s: Next heartbeat time: %d", self, self.__next_heartbeat_time)

                # Yield the thread -- is this needed?
            time.sleep(0)



    def stop(self):
        """
        Indicate that the heartbeat thread should stop so that it can be joined
        """

        self.__run_heartbeats = False
