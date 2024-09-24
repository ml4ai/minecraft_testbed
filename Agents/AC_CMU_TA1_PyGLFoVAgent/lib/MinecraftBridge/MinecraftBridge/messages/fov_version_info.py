# -*- coding: utf-8 -*-
"""
.. module:: fov_version_info
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating FoV Version Info messages.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Field of View Version Information messages.
"""

import json

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage


class FoV_Dependency:
    """
    A class encoding a single depencendy of the FoV_VersionInfo
    """

    def __init__(self, **kwargs):
        """
        Create a dependency

        Args:
            package - string name of the package
            version - string version of the package
            url     - location of the specific version of the package
        """

        # Check to see if the necessary arguments have been passed, raise an exception if one is missing
        for arg_name in ['package', 'version', 'url']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(self.__class__.__name__, arg_name) from None

        # Make sure that everything is stored as a string, to not cause trouble later
        self.package = str(kwargs.get("package"))
        self.version = str(kwargs.get("version"))
        self.url = str(kwargs.get("url"))


    def toDict(self):
        """
        Convert the version dependency to a Python dictionary
        """

        return { "package": self.package,
                 "version": self.version,
                 "url": self.url
               }


    def toJson(self):
        """
        Convert the version dependency to JSON format
        """

        return json.dumps(self.toDict())


class FoV_VersionInfo(BaseMessage):
    """
    A class encapsulating Field of View version info messages.

    Data in FoV version info messages consist of the following:

    version - version string of the FoV agent
    url     - url of the tag / release of the repo of the version of the agent
    dependencies - list of dependencys (packages) and their version information
    """


    def __init__(self, **kwargs):
        """
        Create a  message.

        Args:
            version - version string of the agent
            url     - url of the tag / release of the package's version
        """

        BaseMessage.__init__(self, **kwargs)    

        # Check to see if the necessary arguments have been passed, raise an exception if one is missing
        for arg_name in ['version', 'url']:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(self.__class__.__name__, arg_name) from None

        # TODO: Validate the passed arguments
        self.version = str(kwargs.get('version'))
        self.url = str(kwargs.get('url'))
        self.dependencies = []


    def __str__(self):
        """
        String representation of the message
        """

        return self.__class__.__name__


    def addDependency(self, dependency):
        """
        Add a dependency to the list of dependencies.

        Args:
            dependency - instance of a FoV_Dependency
        """

        self.dependencies.append(dependency)


    def toDict(self):
        """
        Convert the FoV to a Python dictionary
        """

        jsonDict = BaseMessage.toDict(self)

        jsonDict['data'] = { 'agent_name': 'PyGLFoVAgent',
                             'version': self.version,
                             'parameters': [{'url': self.url}] + [dependency.toDict() for dependency in self.dependencies]

                           }

        """
        jsonDict['data'] = {  'version': self.version,
                              'url': self.url,
                              'dependencies': [dependency.toDict() for dependency in self.dependencies]
                            }
        """

        return jsonDict


    def toJson(self):
        """
        Convert the FoV Message to a json message
        """

        return json.dumps(self.toDict())        
