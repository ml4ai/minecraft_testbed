# -*- coding: utf-8 -*-
"""
.. module:: profile_reporter.py
   :platform: Linux, Windows, OSX
   :synopsis: Threaded class for periodically generating profile reports

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""

import time
import threading
###import logging
import numpy as np

from MinecraftBridge.messages import FoVProfile, BusHeader, MessageHeader
from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype
from MinecraftBridge.utils import Loggable

__author__ = 'danahugh'


class ProfileReporter(threading.Thread, Loggable):
    """
    """

    def __init__(self, parent, reporting_period = 60, **kwargs):
        """
        Arguments
        ---------
        reporting_period : double
            Duration (in seconds) to generate reports
        """

        threading.Thread.__init__(self)

        self.parent = parent
        self.reporting_period = reporting_period

###        # Grab a handle to logger for the class, if provided.  If not, then
###        # check if it exists in the loggerDict, or use the default
###        self._logger = kwargs.get("logger", None)
###
###        if self._logger is None:
###            if self.__class__.__name__ in logging.Logger.manager.loggerDict:
###                self._logger = logging.getLogger(self.__class__.__name__)
###            else:
###                self._logger = logging.getLogger(__name__)


        self.processing_times = {}

        self.__run_reporter = False
        self.__send_reports = False
        self.__next_report_time = time.time()

        self.context = {'backend': 'UNKNOWN',
                        'vendor': 'UNKNOWN',
                        'renderer': 'UNKNOWN',
                        'version': 'UNKNOWN',
                        'sl_version': 'UNKNOWN'}


    def add_compute_time(self, function_name, processing_time):
        """
        Arguments
        ---------
        function_name : string
            Name of the function or method that was timed
        processing_time : double
            Time (in seconds) needed to perform the calculation
        """

        if not function_name in self.processing_times:
            self.processing_times[function_name] = [processing_time]
        else:
            self.processing_times[function_name].append(processing_time)


    def reset(self):
        """
        Reset the processing time dictionary in preparation for a new set of 
        times.
        """

        self.processing_times = {}


    def send_reports(self, send=True):
        """
        Indicate that the thread should send reports or not

        Arguments
        ---------
        send : boolean, default = True
            Indicate if report messages should be generated or not
        """

        self.__send_reports = True


    def set_context(self, context):
        """
        """

        self.context = context


    def publishReport(self):
        """
        Construct and publish an FoVProfile message, based on current data
        """

        profile_message = FoVProfile(backend=self.context['backend'],
                                     vendor=self.context['vendor'],
                                     renderer=self.context['renderer'],
                                     version=self.context['version'],
                                     sl_version=self.context['sl_version'])

        for name, times in self.processing_times.items():
            profile_message.add_processing_statistics(name, 
                                                      np.mean(times),
                                                      np.std(times),
                                                      np.min(times),
                                                      np.max(times),
                                                      len(times))

        header = BusHeader(MessageType.agent)
        msg_header = MessageHeader(MessageSubtype.FoV_Profile, 
                                   self.parent.trial_info["experiment_id"],
                                   self.parent.trial_info["trial_id"],
                                   self.parent.agent_name,
                                   replay_id=self.parent.trial_info["replay_id"])

        profile_message.addHeader("header", header)
        profile_message.addHeader("msg", msg_header)

        # Reset the statistics
        self.reset()

        print(profile_message.toDict())

        self.parent.publish(profile_message)



    def run(self):
        """
        Callback when the thread is started.  Starts a loop that generates a
        message publishing processing times at the rate given by the reporting
        time.
        """

        self.logger.debug("%s:  Starting Profile Reporting Thread", self)

        self.__run_reporter = True

        # Don't want to immediately send a report---this allows time for data 
        # to be collected
        self.__next_report_time = time.time() + self.reporting_period

        while self.__run_reporter:

            if self.__send_reports:

                if time.time() > self.__next_report_time:

                    self.publishReport()

                    self.__next_report_time = time.time() + self.reporting_period

                    self.logger.debug("%s:  Next Report time: %d", self, self.__next_report_time)

#            time.sleep(0)


    def stop(self):
        """
        """

        self.__run_reporter = False





