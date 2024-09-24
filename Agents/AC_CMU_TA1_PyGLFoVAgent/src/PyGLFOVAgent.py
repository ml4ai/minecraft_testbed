# -*- coding: utf-8 -*-
"""
.. module:: PyGLFoVAgent
   :platform: Linux, Windows, OSX
   :synopsis: An agent used to produce messages regarding blocks in players'
              field of view

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""


from BaseAgent import BaseAgent
from BaseAgent.utils import parseCommandLineArguments

from MinecraftBridge.utils import Loggable
from MinecraftBridge.mqtt.parsers import MessageSubtype
from MinecraftBridge.mqtt import CallbackDecorator

from MinecraftBridge.messages import (
    PlayerState, 
    DoorEvent, 
    LeverEvent, 
    FreezeBlockList, 
    MissionStateEvent, 
    VictimList, 
    BlockageList, 
    VictimsExpired, 
    TriageEvent, 
    Trial, 
    MarkerDestroyedEvent, 
    MarkerPlacedEvent, 
    MarkerRemovedEvent,
    PerturbationRubbleLocations,
    RubbleDestroyedEvent, 
    RubblePlacedEvent, 
    RubbleCollapse,
    ThreatSignList, 
    VictimNoLongerSafe, 
    VictimPickedUp, 
    VictimPlaced,
    Status
)

from fovWorker import FoVWorker

from profile_reporter import ProfileReporter

import time
import numpy as np


__author__ = 'danahugh'
__version__ = '2.1.4'
__url__ = 'https://gitlab.com/cmu_asist/PyGLFoVAgent/-/tree/v2.1.4'



class PyGLFoVAgent(BaseAgent,Loggable):
    """
    A top-level agent for generating messages for player FoV content.
    PyGLFoVAgent observes player state, door event, and lever event messages,
    and generates a message summarizing the blocks in the player's field of
    view.

    For each trial, the agent creates an FoVWorker instance, which executes on
    its own thread.  The agent will stop the worker, join the thread, and delete
    the instance when the trial ends.  Workers are referenced by the experiment,
    trial, and replay id of the trial.

    Attributes
    ----------
    config : dictionary
        Configuration of the agent provided at startup.
    """

    def __init__(self, bridge, config, run_heartbeats=True):
        """
        Initialize a new PyGLFoVAgent.  

        Arguments
        ---------
        bridge : MinecraftBridge
            Instance of a MinecraftBridge
        config : dictionary
            Configuration loaded from external config file.
        """

        BaseAgent.__init__(self, bridge, config, run_heartbeats=run_heartbeats)

        self.__string_name = '[PyGLFoVAgent]'

        self.logger.info("%s: ", self.__string_name)
        self.logger.info("%s:                                                         --== DARPA ASIST ==-- ", self.__string_name)
        self.logger.info("%s:    ____           __    __     _____      __   _  ___   --== CMU-RI  TA1 ==-- ", self.__string_name)
        self.logger.info("%s:    //  ))       //  ))  //     //   '     ||  //  //||                        ", self.__string_name)
        self.logger.info("%s:   //__//       //      //     //__   ___  || //  //_||   ___   ___   ___  _//_", self.__string_name)
        self.logger.info("%s:  //    //  // // ==)) //     //    //  )) ||//  //  || //  ))//__))//  )) //  ", self.__string_name)
        self.logger.info("%s: //    ((__// ((___// //__// //    ((__//  |//  //   ||((__//((___ //  // ((_  ", self.__string_name)
        self.logger.info("%s:          //                                              //                   ", self.__string_name)
        self.logger.info("%s:      ((_//                                           ((_//  version: %s       ", self.__string_name, __version__)


        # Create an interface to simplify registering callbacks to the agent
        self.minecraft_interface = CallbackDecorator(self.minecraft_bridge)

        # The PyGLFoV agent needs to listen for Trial messages, to know when to
        # construct FoVWorkers, and MissionState messages, to know when to start
        # a worker
        self.minecraft_interface.register_callback(Trial,                self.onTrialMessage)
        self.minecraft_interface.register_callback(MissionStateEvent,    self.onMissionState)

        # All remaining callbacks can be to delegate messages
        self.minecraft_interface.register_callback(PlayerState,          self.delegateMessage)
        self.minecraft_interface.register_callback(DoorEvent,            self.delegateMessage)
        self.minecraft_interface.register_callback(VictimList,           self.delegateMessage)
        self.minecraft_interface.register_callback(BlockageList,         self.delegateMessage)
        self.minecraft_interface.register_callback(VictimsExpired,       self.delegateMessage)
        self.minecraft_interface.register_callback(TriageEvent,          self.delegateMessage)
        self.minecraft_interface.register_callback(MarkerDestroyedEvent, self.delegateMessage)
        self.minecraft_interface.register_callback(MarkerPlacedEvent,    self.delegateMessage)
        self.minecraft_interface.register_callback(MarkerRemovedEvent,   self.delegateMessage)
        self.minecraft_interface.register_callback(PerturbationRubbleLocations, self.delegateMessage)
        self.minecraft_interface.register_callback(RubbleCollapse,       self.delegateMessage)
        self.minecraft_interface.register_callback(RubbleDestroyedEvent, self.delegateMessage)
        self.minecraft_interface.register_callback(RubblePlacedEvent,    self.delegateMessage)
        self.minecraft_interface.register_callback(ThreatSignList,       self.delegateMessage)
        self.minecraft_interface.register_callback(VictimNoLongerSafe,   self.delegateMessage)
        self.minecraft_interface.register_callback(VictimPickedUp,       self.delegateMessage)
        self.minecraft_interface.register_callback(VictimPlaced,         self.delegateMessage)
        self.minecraft_interface.register_callback(FreezeBlockList,      self.delegateMessage)        


        # Workers will be created and destroyed as MessageState events are received
        # Some workers may still be working when MessageStates are recieved.  
        self.fovWorkers = {}



    def __str__(self):
        """
        String representation of the PyGLFoVAgent
        """

        return self.__string_name



    def __getWorkerKey(self, message):
        """
        Get a unique key for the message based on the message header.

        Current key is extractly from the message header:
        (experiment_id, trial_id, replay_id)

        If a message header is not present, then simply return None
        
        Returns
        -------
        tuple consisting of (experiment_id, trial_id, replay_id)
        """

        if message.headers["msg"] is None:
            return None

        # Construct the key
        key = (message.headers["msg"].experiment_id,
               message.headers["msg"].trial_id,
               message.headers["msg"].replay_id)

        return key



    def delegateMessage(self, message):
        """
        Callback function for most messages. Determines which worker the message
        should be sent to, and delegates to the worker.

        Arguments
        ---------
        message : MinecraftBridge.message
            Message to send
        """

        self.logger.debug("%s:  Processing %s Message", self, message)
    
        key = self.__getWorkerKey(message)
        worker = self.fovWorkers.get(key, None)

        if worker is None:
            self.logger.debug("%s:  No worker with given key:  %s", self, key)
            return

        worker.addMessage(message)

        time.sleep(0)



    def onMissionState(self, message):
        """
        Callback function when a MissionState message is received.  If the
        MissionState is a "start", then start the worker.  Otherwise, stop
        the worker.

        Arguments
        ---------
        message : MinecraftBridge.messages.MissionState
            Received Mission State message
        """

        self.logger.debug("%s:  Processing %s Message", self, message)

        # Get the worker that should handle this message.  If it doesn't exist,
        # send out a warning and do nothing
        key = self.__getWorkerKey(message)
        worker = self.fovWorkers.get(key, None)

        if worker is None:
            self.logger.debug("%s:  No worker with given key:  %s", self, key)
            return


        # Is this a START or STOP message?
        if message.state == MissionStateEvent.MissionState.START or message.state == MissionStateEvent.MissionState.Start:
            
            self.logger.info("%s:  MissionState START", self)
            self.logger.info("%s:  Worker State: %s", self, str(worker.state))

            if not worker.is_alive():
                worker.start()

            # Wait until the worker is running before attempting to modify the block feeder
            while worker.state is not FoVWorker.State.RUNNING:
                time.sleep(0)

            self.logger.debug("%s:    FoV worker %s running.", self, key)


        elif message.state == MissionStateEvent.MissionState.STOP or message.state == MissionStateEvent.MissionState.Stop:
            
            self.logger.debug("%s:    Stopping FoV worker %s", self, key)
            worker.stop()

            if worker.is_alive():
                worker.join()

            self.logger.debug("%s:    FoV worker %s deleted", self, key)


        else:
            self.logger.warning("%s:  Unknown MissionState state: %s", self, message.state)



    def onTrialMessage(self, message):
        """
        Callback function when Trial message is received.  If the trial is a
        "start", then creates and starts a new FoVWorker.  Otherwise, stops 
        and deletes the worker.

        Arguments
        ---------
        message : MinecraftBridge.messages.Trial
            Received Trial message        
        """

        self.logger.debug("%s:  Processing %s Message", self, message)

        key = self.__getWorkerKey(message)

        # If the trial is starting, then inform the FoV worker of the names of
        # the participants to generate FoV messages for.
        if message.headers["msg"].sub_type == MessageSubtype.start:

            self.logger.info("%s:  Starting Trial with Map: %s", self, message.map_name)

            # Create and store the new FoV worker
            map_path = self.config["maps"][message.map_name]
            worker = FoVWorker(self, self.config, key, map_path)
            self.fovWorkers[key] = worker


        elif message.headers["msg"].sub_type == MessageSubtype.stop:

            self.logger.info("%s:  Stopping Trial", self)

            worker = self.fovWorkers.get(key, None)

            if worker is not None:

                self.logger.debug("%s:    Stopping FoV worker %s", self, key)

                worker.stop()

                if worker.is_alive():
                    worker.join()
    
            else:
                self.logger.warning("%s:  Received STOP for non-existent FoV worker with key: %s", self, key)
        
        else:
            self.logger.warning("%s:  Unknown Trial Subtype: %s", self, message.headers["msg"].sub_type)


    def get_status(self):
        """
        Return the status of the agent, which will be dependent upon the state
        of the currently running FoV agent (if running).

        Returns
        -------
        state : MinecraftBridge.messages.Status.State
        status : string
        active : boolean
            True if there is an FoVWorker that is active
        """

        # See if there's an FoVWorker currently
        worker_key = (self.trial_info["experiment_id"],
                      self.trial_info["trial_id"],
                      self.trial_info["replay_id"])
        worker = self.fovWorkers.get(worker_key, None)

        # Log the statistics, if provided, and reset
        if worker is not None:
            profile_stats = worker.get_profile_stats()

            self.logger.info("%s: Profile Statistics:", self)
            self.logger.info("%s:   Total PlayerState messages processed: %d", self, profile_stats.get("counts",0))
            self.logger.info("%s:   Average Process Time (seconds):       %f", self, profile_stats.get("average_time", 0.0))
            self.logger.info("%s:   Std Dev Process Time (seconds):       %f", self, profile_stats.get("stdev_time", 0.0))
            self.logger.info("%s:   Minimum Process Time (seconds):       %f", self, profile_stats.get("min_time", 0.0))
            self.logger.info("%s:   Maximum Process Time (seconds):       %f", self, profile_stats.get("max_time", 0.0))

            worker.reset_profile_stats()

        # TODO:  Come up with some set of basis for the state of the agent
        state = Status.State.OK

        if worker is not None and worker.state in {FoVWorker.State.RUNNING, FoVWorker.State.STOPPING}:
            active = True
        else:
            active = False

        return state, "", active




    def publish(self, message):
        """
        Publish a message to the bus / bridge
        """

        self.logger.debug("%s:  Publishing %s message", self, message)
        self.minecraft_interface.publish(message)


    def stop(self):
        """
        Stop the fovThreads
        """

        BaseAgent.stop(self)

        self.logger.info("%s:  Stopping all FoV worker threads", self)

        for worker in self.fovWorkers.values():
            worker.stop()

            if worker.is_alive():
                worker.join()
                

        self.logger.info("%s:  FoV worker threads stopped", self)



    def run(self):
        """
        Run the agent, and call `stop` when the agent has completed to ensure
        that workers are cleaned up.
        """

        self.logger.debug("%s: Running...", self)
        BaseAgent.run(self)

        self.stop()


  
if __name__ == '__main__':
    """
    Parse command line and config file arguments, create an instance of the 
    PyGLFoVAgent, and run it.    
    """

    args, config, bridge = parseCommandLineArguments()

    agent = PyGLFoVAgent(bridge, config)
    agent.run()

