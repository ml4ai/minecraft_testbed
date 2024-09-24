# -*- coding: utf-8 -*-
"""
.. module:: fov_profile
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating FoV messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating profile messages sent by the PyGLFoVAgent.
"""


import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class FoVProfile(BaseMessage):
    """
    A class encapsulating PyGLFoVAgent profile messages.

    Attributes
    ----------
    backend : string
        GL backend used (GLFW, GLUT, etc)
    vendor : string
        Graphics card / library vendor
    renderer : string
        Graphics card model / library
    sl_version : string
        Shading language vendor
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)    

        self._backend = kwargs.get("backend", "UNKNOWN")
        self._vendor = kwargs.get("vendor", "UNKNOWN")
        self._renderer = kwargs.get("renderer", "UNKNOWN")
        self._version = kwargs.get("version", "UNKNOWN")
        self._sl_version = kwargs.get("sl_version", "UNKNOWN")

        self._process_statistics = {} 


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'FoVProfile')
        """

        return self.__class__.__name__


    def add_processing_statistics(self, name, mean_time, std_time, min_time, max_time, count):
        """
        Add statistics for a given compute acction

        Arguments
        ---------
        name : string
            Name of the compute / processing action performed
        mean_time : double
            Average time to perform the action
        std_time : double
            Standard deviation of the time to perform the action
        min_time : double
            Minimum amount of the time action took to perform
        max_time : double
            Maximum amount of time the action took to perform
        count : int
            Number of times the process was called
        """

        self._process_statistics[name] = { 'name': name,
                                           'mean': mean_time,
                                           'std': std_time,
                                           'min': min_time,
                                           'max': max_time,
                                           'count': count
                                         }


    @property
    def backend(self):
        """
        GL Backend used

        Attempting to set `backend` raises an `ImmutableAttributeException`.
        """

        return self._backend

    @backend.setter
    def backend(self, _):
        raise ImmutableAttributeException(str(self), "backend")


    @property
    def vendor(self):
        """
        

        Attempting to set `vendor` raises an `ImmutableAttributeException`.
        """

        return self._vendor

    @vendor.setter
    def vendor(self, _):
        raise ImmutableAttributeException(str(self), "vendor")


    @property
    def renderer(self):
        """
        

        Attempting to set `renderer` raises an `ImmutableAttributeException`.
        """

        return self._renderer

    @renderer.setter
    def renderer(self, _):
        raise ImmutableAttributeException(str(self), "renderer")


    @property
    def version(self):
        """
        

        Attempting to set `version` raises an `ImmutableAttributeException`.
        """

        return self._version

    @version.setter
    def version(self, _):
        raise ImmutableAttributeException(str(self), "version")


    @property
    def sl_version(self):
        """
        

        Attempting to set `sl_version` raises an `ImmutableAttributeException`.
        """

        return self._sl_version

    @sl_version.setter
    def sl_version(self, _):
        raise ImmutableAttributeException(str(self), "sl_version")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the FoVProfile.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}


        jsonDict['data'] = { 'backend': str(self.backend),
                             'vendor': str(self.vendor),
                             'renderer': str(self.renderer),
                             'version': str(self.version),
                             'sl_version': str(self.sl_version),
                             'processing_times': list(self._process_statistics.values())
                           }

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the message.  Message information is
        contained in a JSON object under the key "data".  Additional named
        headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            FoVProfile message.
        """

        print(self.toDict())

        return json.dumps(self.toDict())        
