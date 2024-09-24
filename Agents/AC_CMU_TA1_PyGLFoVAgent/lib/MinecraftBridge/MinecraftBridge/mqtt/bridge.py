# -*- coding: utf-8 -*-
"""
.. module:: mqtt.bridge
   :platform: Linux, Windows, OSX
   :synopsis: Bridge connecting to MQTT clients

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of the Bridge class to connect to MQTT clients
"""

from .base import RawMessage, BaseBridge
from ..messages import BusHeader, MessageHeader

import paho.mqtt.client as mqtt


import json
import time



class Bridge(BaseBridge):
    """
    A bridge class for handling connections to Minecraft through a MQTT client.

    This bridge is used to connect to a running Minecraft instance through a
    MQTT broker.  This class assumes that the Minecraft instance is using the
    ASISTMod, though this is technically not a _strict_ requirement.  Messages
    are received in JSON format, and are parsed using parsers defined in the
    mqtt.parsers subpackage.


    Examples
    --------
    Typically bridge usage will involve the following steps:

    1.  Create an instance of the mqtt.Bridge::

        >>> bridge = mqtt.Bridge("MinecraftBridge")

    2.  Create one or more client objects to receive messages::

        >>> client1 = MinecraftClient(...)
        >>> client2 = MinecraftClient(...)

    3.  Register the clients to receive specific messages types::

        >>> bridge.register(client1, ScoreboardEvent)
        >>> bridge.register(client1, PlayerState)
        >>> bridge.register(client2, PlayerState)

    4.  Connect to the MQTT broker.  This will automatically start a callback
        loop, which will send message instances to registered clients::

        >>> bridge.connect("localhost", 1883)

    5.  Messages can be constructed and sent to be MQTT broker::

        >>> message = ChatEvent(...)
        >>> bridge.send(message)

    6.  Once complete, disconnect from the MQTT broker::

        >>> bridge.disconnect()


    Attributes
    ----------
    name : string
        name of the bridge instance, used by the MQTT Client to identify the
        connection
    logger : logging.Logger
        instance of the logger than log messages are sent to
    isConnected : boolean
        indication of whether the bridge is connected to the MQTT broker or not
    observers : dictionary
        dictionary mapping message classes to objects that wish to receive 
        messages of the given class


    Methods
    -------
    register(observer, message_class)
        Register an observer to receive messages of a given class
    subscribe(topic)
        Subscribe to received messages of a given topic from the MQTT broker
    send(message, qos, retain)
        Send a message to the MQTT broker
    start()
        Begin recieving messages from the MQTT broker
    connect(host, port, start_loop)
        Connect to the MQTT broker
    disconnect()
        Disconnect from the MQTT broker
    """

    def __init__(
        self, name, host='127.0.0.1', port=1883, keepalive=60, bind_address='', 
        include_name_in_string=False, **kwargs):

        super().__init__(name, include_name_in_string=include_name_in_string)

        self.host = host
        self.port = port

        # Create the MQTT client, and set up the callbacks
        self.__mqtt_client = mqtt.Client(name)
        self.__mqtt_client.on_message = self.on_message
        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.on_disconnect = self.__on_disconnect

        # Parameters to pass when connections are made
        self.__keepalive = keepalive
        self.__bind_address = bind_address
        self.__background_loop = False


    @property
    def publish(self):
        """
        Alias of `send`, as decorators use publish
        """

        return self.send
    


    def __on_connect(self, client, userdata, flags, result_code):
        """
        Callback when the bridge receives a CONNACK response from the broker.

        If the connection is successful, set the `isConnect` property to `True`.
        Upon connecting, if any observers are registered, the bridge will also
        subscribe to the topics associated with each message class.

        If the connection is unsuccessful, a warning is logged with result code
        information.

        Parameters
        ----------
        client : 
            client instance for this callback
        userdata : 
            private user data set when the MQTT client instance was created
        flags : dictionary
            response flags sent by the MQTT broker
        result_code :  integer
            the connection result, indicating success or not
        """

        self.logger.debug("%s:  __on_connect", self)

        # Check to see if the connection was successful
        if result_code == 0:
            # Connection was successful
            self.isConnected = True

            self.logger.info('%s:  Connection Successful', self)
            self.logger.info('%s:    Host: %s', self, self.host)
            self.logger.info('%s:    Port: %d', self, self.port)

            # Subscribe to topics based on what observers are listening for
            for message_class in self.observers.keys():
                self.subscribe(self.parser_map[message_class].topic)

        else:
            # Connection was refused
            
            if self.logger:
                self.logger.warning("%s:  Connection Unsuccessful.  Connection Returned Result: %s", self, mqtt.connack_string(result_code))


    def __on_disconnect(self, client, userdata, result_code):
        """
        Callback when MQTT client disconnects from the broker.

        If disconnection is successful, sets the `isConnected` flag to `False`, 
        otherwise, logs a warning with the result code information.

        Parameters
        ----------
        client : 
            the client instance for this callback
        userdata : 
            private user data as set in the MQTT client instance
        result_code : 
            the disconnection result, indicating if the callback is in response
            to a `disconnect()`, or network error.
        """

        self.logger.debug("%s: __on_disconnect", self)

        # Check to see if the disconnection was successful
        if result_code == 0:
            # Disconnection was successful
            self.isConnected = False

            if self.logger:
                self.logger.info('%s:  Disconnected.', self)

        else:
            # Connection was refused
            if self.logger:
                self.logger.warning("%s:  Unexpected Disconnection.  Disconnection Message: %s", self, mqtt.connack_string(result_code))


    def on_message(self, client, userdata, msg):
        """
        Callback when bridge receives a message from the broker.

        Upon receiving a message, attempts to parse the message, and sends the
        parsed message instance to observers that are registered to receive 
        messages of the class.

        Parameters
        ----------
        client : 
            the client instance for this callback
        userdata : 
            private user data set in the MQTT client instance
        msg : MQTT message
            the received MQTT message
        """

        self.logger.debug("%s:  on_message", self)

        # Parse the message data
        try:
            jsondata = json.loads(msg.payload.decode("utf-8"))

            topic = msg.topic

            message = RawMessage(topic, payload=msg.payload)
            super().on_message(message)

        except:
            self.logger.exception("%s:  Exception when handling message payload.\nMessage Payload:\n%s", self, msg.payload.decode("utf-8"))


    def subscribe(self, topic):
        """
        Subscribe to a topic published by the MQTT broker.

        Parameters
        ----------
        topic : string
            Topic to subscribe to
        """

        self.logger.info("%s:  Subscribing to %s", self, topic)
        self.__mqtt_client.subscribe(topic)


    def unsubscribe(self, topic):
        """
        Unsubscribe from a topic published by the MQTT broker.

        Parameters
        ----------
        topic : string
            Topic to unsubscribe from
        """

        self.logger.info("%s:  Unsubscribing from %s", self, topic)
        self.__mqtt_client.unsubscribe(topic)


    def send(self, message, qos=0, retain=False):
        """
        Send the message to the MQTT broker.

        This method assumes the message is an instance of a message class
        defined in MinecraftBridge.messages.  Converting to JSON and topic
        publication is performed by the message instance and corresponding
        parser.

        Parameters
        ----------
        message : MinecraftBridge.message object
        """

        # Determine the topic to publish to, and generate the payload (JSON string)
        topic = self.parser_map[message.__class__].topic
        payload = message.toJson().encode("utf-8")

        self.logger.debug("%s:  Publishing message: %s", self, message)

        self.__mqtt_client.publish(topic, payload, qos=qos, retain=retain)


    def start(self):
        """
        Start the background callback loop to receive messages from the MQTT
        broker.
        """

        self.logger.info("%s:  Starting Callback Loop with MQTT bus", self)
        self.__background_loop = True
        self.__mqtt_client.loop_start()

        running = True
        while running:
            try:
                time.sleep(1)
            except:
                running = False


    def connect(self, start_loop=True):
        """
        Connect to the MQTT broker.

        Upon connecting, the background callback loop will be started if the
        `start_loop` parameter is set to `True`.

        Parameters
        ----------
        start_loop : boolean
            Flag indicating if the background callback loop should be started
        """

        self.logger.info("%s:  Connecting to MQTT Broker (%s:%s)", self, self.host, self.port)
        self.__mqtt_client.connect(host=self.host, port=self.port, keepalive=self.__keepalive, bind_address=self.__bind_address)
        super().connect(start_loop=start_loop)


    def disconnect(self):
        """
        Disconnect from the MQTT broker.
        """

        self.logger.info("%s:  Disconnecting from MQTT Broker", self)

        # Stop the callback loop, if it is running
        if self.__background_loop:
            self.__mqtt_client.loop_stop()
            self.__background_loop = False

        self.__mqtt_client.disconnect() 
