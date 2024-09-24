# -*- coding: utf-8 -*-
"""
.. module:: logging
   :platform: Linux, Windows, OSX
   :synopsis: Various logging utilities.

.. moduleauthor:: Ini Oguntola <ioguntol@andrew.cmu.edu>

This file provides a place for various logging utilities.
"""
import logging


class Loggable:
    """
    Mixin to provide class-specific logging capabilities.  Including this mixin
    provides an object with a `logger` property, whose methods match those in
    logging.  Additionally, provides a static method for pre-configuration of
    loggers based on class name.

    Usage
    -----
    Including logging functionality only requires inheriting from the Loggable
    mixin.  If included, objects will have a `logger` attribute, which allows
    for logging messages at varying levels of importance (DEBUG, INFO, WARNING,
    ERROR, CRITICAL).  Note that `Loggable` has no `__init__` method, so does
    not need to be initialized by the inheriting class::

        class SomeClass(BaseClass, Loggable):

            def some_method(self):

                self.logger.debug("A debug message")
                self.logger.info("An info message")
                self.logger.warning("A warning message")
                self.logger.error("An error message")
                self.logger.critical("A critical message")

    Loggers can be configured using the `configure` method.  This method takes
    a dictionary as an argument, mapping class names to configuration
    dictionaries.  Currently, the configuration dictionary maps the key "level"
    to a string indicating log level ("DEBUG", "INFO", "WARNING", "ERROR", 
    "CRITICAL")::

        log_configuration = { "SomeClass": { "level": "INFO" } }
        Loggable.configure(log_configuration)


    Static Methods
    --------------
    configure(logger_configs)
        Configures the logging level of loggers for each specific class, so 
        that each class can provide logging at different levels.

    Properties
    ----------
    logger : logging.Logger
        Class-specific logger
    """

    @staticmethod
    def configure(logger_configs):
        """
        Configure class-specific logging.

        Arguments
        ---------
        logger_configs : dictionary
            dictionary mapping class name to configuration properties for the
            corresponding logger
        """

        # Configure loggers, if there's an entry in the config file
        logging.basicConfig(level=logging.WARNING)
    
        for name, config in logger_configs.items():
    
            # Get the logger from logging
            logger = logging.getLogger(name)
    
            # Set the logging level (DEBUG, INFO, WARNING, ERROR)
            if "level" in config.keys():
                if config["level"].upper() == "DEBUG":
                    logger.setLevel(logging.DEBUG)
                elif config["level"].upper() == "INFO":
                    logger.setLevel(logging.INFO)
                elif config["level"].upper() == "WARNING":
                    logger.setLevel(logging.WARNING)
                elif config["level"].upper() == "ERROR":
                    logger.setLevel(logging.ERROR)
                elif config["level"].upper() == "CRITICAL":
                    logger.setLevel(logging.CRITICAL)
                else:
                    logger.setLevel(logging.NOTSET)

    @property
    def logger(self):
        """
        Grab a handle to logger for the class, if it exists,
        otherwise use the default logger.
        """

        if self.__class__.__name__ in logging.Logger.manager.loggerDict:
            return logging.getLogger(self.__class__.__name__)
        else:
            return logging.getLogger(__name__)

    @logger.setter
    def logger(self, _):
        pass



def initLogger(logger_configs):
    """
    Initialize class-specific loggers.

    Arguments
    ---------
    logger_configs : dictionary
        dictionary mapping class name to configuration properties for the
        corresponding logger
    """

    # Configure loggers, if there's an entry in the config file
    logging.basicConfig(level=logging.WARNING)

    for name, config in logger_configs.items():

        # Get the logger from logging
        logger = logging.getLogger(name)

        # Set the logging level (DEBUG, INFO, WARNING, ERROR)
        if "level" in config.keys():
            if config["level"].upper() == "DEBUG":
                logger.setLevel(logging.DEBUG)
            elif config["level"].upper() == "INFO":
                logger.setLevel(logging.INFO)
            elif config["level"].upper() == "WARNING":
                logger.setLevel(logging.WARNING)
            elif config["level"].upper() == "ERROR":
                logger.setLevel(logging.ERROR)
            elif config["level"].upper() == "CRITICAL":
                logger.setLevel(logging.CRITICAL)
            else:
                logger.setLevel(logging.NOTSET)

