# -*- coding: utf-8 -*-
"""
.. module:: Minecraft.mqtt
   :platform: Linux, Windows, OSX
   :synopsis: Bridge classes for receiving (and sending) messages from Minecraft
              through a MQTT broker.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

The mqtt module contains classes to process messages received from Minecraft
through an MQTT broker.  This module contains two bridge classes:

*  `Bridge`: a class for connecting to Minecraft through an MQTT broker
*  `FileBridge`: a class for processing Minecraft messages stored in a file

Both classes can also send messages---`Bridge` by publishing messages to the 
MQTT broker, and `FileBridge` by writing messages to a separate file.

Usage
-----
Typical bridge usage will involve the following steps:

    1.  Create an instance of a bridge, providing a name for the pridge, as
        well as additional class-specific parameters::

        >>> bridge = mqtt.Bridge("MinecraftBridge", ...)

    2.  Create one or more client objects to receive messages::

        >>> client1 = MinecraftClient(...)
        >>> client2 = MinecraftClient(...)

    3.  Register the clients to receive specific messages types::

        >>> bridge.register(client1, ScoreboardEvent)
        >>> bridge.register(client1, PlayerState)
        >>> bridge.register(client2, PlayerState)

    4.  Connect to the MQTT broker or input file.  This will automatically 
        start a callback loop, which will send message instances to registered
        clients::

        >>> bridge.connect()

    5.  Messages can be constructed and sent to be MQTT broker or output file::

        >>> message = ChatEvent(...)
        >>> bridge.send(message)

    6.  Once complete, disconnect from the MQTT broker or input / output files::

        >>> bridge.disconnect()
"""

from .bridge import Bridge
from .file_bridge import FileBridge

# Temporary alias
from .interfaces import CallbackInterface as CallbackDecorator

__all__ = ['Bridge', 'FileBridge', 'CallbackDecorator']