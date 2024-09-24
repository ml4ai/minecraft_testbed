# -*- coding: utf-8 -*-
"""
.. module:: callback_interface
   :platform: Linux, Windows, OSX
   :synopsis: An interface class to allow for registering individual callbacks
              to a base Minecraft bridge instance.

.. moduleauthor:: Ini Oguntola <ioguntol@andrew.cmu.edu>

This file provides an interface class to extend MinecraftBridge instances with
functionality to register and deregister individual callback methods for
specific message classes, as opposed to registering objects to handle message 
reception.  The interface also allows for publishing messages.
"""
from .base import MinecraftInterface
from ...messages import BaseMessage
from collections import defaultdict



class CallbackInterface(MinecraftInterface):
    """
    Interface that extends MinecraftBridge instances with
    functionality to register and deregister individual callback methods for
    specific message classes.

    Methods
    -------
    register_callback(message_class, callback, priority=1)
        Register the callback as a processor for the given message class
    deregister_callback(callback, message_class=None)
        Deregister the callback as a processor for the given message class
    publish(message)
        Publish a message to the message bus
    """

    def __init__(self, bridge, registration_priority=1):
        """
        Arguments
        ---------
        bridge : MinecraftBridge.BaseBridge or MinecraftInterface instance
        registration_priority : int
            The priority value that this interface uses when registering with
            its underlying bridge (smaller value = high priority)
        """
        super().__init__(bridge)
        self.__message_processors = defaultdict(list)
        self.__registration_priority = registration_priority



    ### RECEIVE METHOD REQUIRED TO REGISTER WITH THE MINECRAFT BRIDGE ###

    def receive(self, message):
        """
        Receive a message from the MinecraftBridge.  Delegate the message to a
        callback registered in the message processors dictionary based on the
        message class.

        Arguments
        ---------
        message : MinecraftBridge.messages.BaseMessage instance
            Message received from the bus
        """
        self.logger.debug(f'{self}:  Received {message} message')

        # Get the processors for the message, and send to each callback
        if message.__class__ in self.__message_processors:
            processors = self.__message_processors[message.__class__]
            processors = sorted(processors, key=lambda x: x[1])
            for callback, _ in processors:
                try:
                    callback(message)
                except Exception as e:
                    self.logger.exception(f'{self}:  Exception raised when dispatching {message} to callback {callback}:')
                    self.logger.exception(f'{self}:  {str(e)}')
        else:
            self.logger.warning(
                f'{self}:  No message processors found for {message} message.  Ignoring message.')



    ### INTERFACE FUNCTIONALITY ###

    def register_callback(self, message_class, callback, priority=1):
        """
        Register a callback, indicating the function that should be called when
        a message of the given class is received.  Note that multiple callbacks
        may be registered, however, for a given message class,
        each callback will only be registered once.

        Arguments
        ---------
        callback : function
            Function to call when a message of message_class is received
        message_class : MinecraftBridge.messages class
            Message class to register
        priority : int
            Optional priority value that determines the order
            in which callbacks are called (smaller value = high priority)
        """

        # Validate arguments.  If the message_class is not a class inheriting 
        # from BaseMessage, then do not register the callback.  Similarly, if
        # the callback is not callable, do not register.  In either case, log
        # an error message indicating the error.
        if not isinstance(message_class, type):
            self.logger.error(f"{self}:  Expected <class 'type'> instance for message class, not {type(message_class)}")
            return
        if BaseMessage not in message_class.mro():
            self.logger.error(f"{self}:  Invalid message class: {message_class}.  Must inherit from BaseMessage.")
            return
        if not callable(callback):
            self.logger.error(f"{self}:  Callback {callback} is not callable.")
            return

        # Issue a warning if a client is trying to register the same callback
        # for the same message_class
        if (callback, priority) in self.__message_processors[message_class]:
            self.logger.warning(
                f'{self}:  Attempting to register existing callback for Message Class {message_class}')
            return

        # Add the callback
        self.__message_processors[message_class].append((callback, priority))

        # Register with the bridge to receive this message
        self._bridge.register(self, message_class, priority=self.__registration_priority)


    def deregister_callback(self, callback, message_class=None):
        """
        Deregister the callback as a message processor for the given message class.

        Arguments
        ---------
        callback : function
            Callback function to deregister
        message class : MinecraftBridge.messages class
            Message class to deregister the call back from
            If `None`, deregister from all message classes
        """

        # Keep track of potential message parsers we don't need anymore
        delete_list = []

        # Remove the callback from self.__message_processors
        for msg_class in list(self.__message_processors.keys()):
            if message_class in {None, msg_class}:
                for _callback, _priority in self.__message_processors[msg_class]:
                    if callback == _callback:
                        self.__message_processors[msg_class].remove((_callback, _priority))

            # Deregister with the bridge from any unneeded message classes
            if len(self.__message_processors[msg_class]) == 0:
                self.logger.info(f"{self}:  Deregistering from {msg_class} -- no registered callbacks")
                self._bridge.deregister(self, message_class=msg_class)
                del self.__message_processors[msg_class]

        # Delete the message processor if the message is not needed anymore
        for key in delete_list:
            self.__message_processors.pop(key, None)


    def publish(self, message):
        """
        Send the message to the MinecraftBridge for publication.

        Arguments
        ---------
        message : MinecraftBridge message
            Message to publish
        """

        # Pass the message to the bridge
        self._bridge.send(message)

