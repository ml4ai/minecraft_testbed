# -*- coding: utf-8 -*-
"""
.. module:: mqtt.file_bridge
   :platform: Linux, Windows, OSX
   :synopsis: Bridge connecting to files containing MQTT-type messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of the Bridge class to read ASIST-formatted messages from a file
"""

from .base import RawMessage, BaseBridge
from .parsers.message_parser_arguments import MQTT_PARSERS
from ..messages import BusHeader, MessageHeader

import ciso8601
import json

from pathlib import Path



class FileBridge(BaseBridge):
    """
    A bridge class for handling connections to Minecraft through a file.

    This bridge is used to connect to a running Minecraft instance through a
    file.  This class assumes that messages are stored in JSON format.
    Messages are parsed using parsers defined in the mqtt.parsers subpackage.

    Examples
    --------
    Typically bridge usage will involve the following steps:

    1.  Create an instance of the mqtt.FileBridge::

        >>> bridge = mqtt.FileBridge("MinecraftBridge", "input.metadata", "output.metadata")

    2.  Create one or more client objects to receive messages::

        >>> client1 = MinecraftClient(...)
        >>> client2 = MinecraftClient(...)

    3.  Register the clients to receive specific messages types::

        >>> bridge.register(client1, ScoreboardEvent)
        >>> bridge.register(client1, PlayerState)
        >>> bridge.register(client2, PlayerState)

    4.  Connect to the input and output files.  This will automatically start a callback
        loop, which will send message instances to registered clients::

        >>> bridge.connect()

    5.  Messages can be constructed and sent via the bridge::

        >>> message = ChatEvent(...)
        >>> bridge.send(message)

    6.  Once complete, disconnect::

        >>> bridge.disconnect()


    Attributes
    ----------
    name : string
        name of the bridge instance
    logger : logging.Logger
        instance of the logger than log messages are sent to
    input_path : string or list of string
        path to file / directory or list of paths to read messages in from
    output_path : string
        path of the file to write messages to
    input_file : File instance
        file to read messages from
    output_file : File instance
        file to write messages to
    subscriptions : set of strings
      set of topics subscribed to by the bridge
    isConnected : boolean
        indication of whether the bridge is connected to its source or not
    observers : dictionary
        dictionary mapping message classes to objects that wish to receive 
        messages of the given class


    Methods
    -------
    register(observer, message_class)
        Register an observer to receive messages of a given class
    subscribe(topic)
        Subscribe to received messages of a given topic
    send(message)
        Send a message
    start()
        Begin recieving messages
    connect(host, start_loop)
        Connect to the bridge source
    disconnect()
        Disconnect from the bridge source
    """


    def __init__(
        self, name, input_path, output_path,
        include_name_in_string=False, sort_by_time=True, **kwargs):

        super().__init__(
            name, include_name_in_string=include_name_in_string, connected_on_creation=True)

        if isinstance(input_path, list):
            self.input_paths = input_path
        else:
            input_path = Path(input_path).resolve()
            if input_path.is_file():
                self.input_paths = [input_path]
            elif input_path.is_dir():
                self.input_paths = list(input_path.glob('*.metadata'))
            else:
                self.logger.error(f"{self}:  Could not find {input_path}.")

        self.output_path = output_path

        self.input_file = None
        self.output_file = None

        self.subscriptions = set()

        self.sort_by_time = sort_by_time


    @property
    def publish(self):
        """
        Alias for `send`
        """
        
        return self.send
    


    def subscribe(self, topic):
        """
        Subscribe to a topic in the input file's message data.

        Parameters
        ----------
        topic : string
            Topic to subscribe to
        """

        self.logger.info("%s:  Subscribing to %s", self, topic)
        self.subscriptions.add(topic)


    def unsubscribe(self, topic):
        """
        Unsubscribe from a topic in the input file's message data.

        Parameters
        ----------
        topic : string
            Topic to unsubscribe from
        """

        self.logger.info("%s:  Unsubscribing from %s", self, topic)
        if not topic in self.subscriptions:
            self.logger.warning(
                "%s:  Attempting to unsubscribe to topic not currently subscribed to: %s", self, topic)
        else:
            self.subscriptions.remove(topic)


    def send(self, message):
        """
        Send the message by writing it to the output file and
        forwarding to relevant observers.

        This method assumes the message is an instance of a message class
        defined in MinecraftBridge.messages.  Converting to JSON and topic
        publication is performed by the message instance and corresponding
        parser.

        Parameters
        ----------
        message : MinecraftBridge.message object
        """

        self.logger.debug("%s:  Writing message to output file: %s", self, message)

        # Write to output file
        try:
            self.output_file.write(message.toJson())
            self.output_file.write('\n')
        except ValueError:
            self.logger.warning("%s:  Attempting to write message to closed file", self)

        # Simulate sending message on bus
        if message.__class__ in MQTT_PARSERS:
            # Add dummy headers if absent
            if len(message.headers) == 0:
                msg_type = MQTT_PARSERS[message.__class__]['type']
                msg_subtype = MQTT_PARSERS[message.__class__]['subtype']
                message.addHeader('header', BusHeader(msg_type))
                message.addHeader('msg', MessageHeader(msg_subtype, None, None, None))

            # Pass on to relevant registered observers
            topic = MQTT_PARSERS[message.__class__]['topic']
            msg = RawMessage(topic, payload=message.toJson().encode('utf-8'))
            self.on_message(msg)


    def connect(self, start_loop=True):
        """
        Connect to the input and output files

        Upon connecting, the background callback loop will be started if the
        `start_loop` parameter is set to `True`.

        Parameters
        ----------
        start_loop : boolean
            Flag indicating if the background callback loop should be started
        """

        self.logger.info(f"{self}:  Connecting to output file")
        self.output_file = open(self.output_path, 'a')
        super().connect(start_loop=start_loop)


    def start(self):
        """
        Read in the contents of the input file, converting JSON to dictionary
        format.  After sorting by @timestamp, send messages to observers.
        """

        for path in self.input_paths:
            try:
                self.input_file = open(path, 'r')
                self.logger.info(f"{self}:  Starting callback loop with input file {path}.")

                if self.sort_by_time:
                    # Read all lines in at once and send out in timestamp order
                    json_lines = [json.loads(line) for line in self.input_file.readlines()]
                    json_lines = sorted(json_lines, key=self._get_timestamp)
                    self.send_messages_from_json(json_lines)

                else:
                    # Read and send messages one line at a time
                    for line in self.input_file:
                        self.send_messages_from_json([json.loads(line)])

            except Exception as e:
                self.logger.exception(f"{self}:  {e}")

            finally:
                self.logger.info(f"{self}:  Closing input file.")
                if self.input_file is not None:
                    self.input_file.close()
                    self.input_file = None



    def send_messages_from_json(self, json_lines):
        """
        Convert a list of json lines to message objects,
        and send them in order as if they were coming off the bus.

        Parameters
        ----------
        json_lines : list
            List of json lines
        """

        for jsondata in json_lines:
            topic = self._get_topic(jsondata)

            # Create a RawMessage
            if topic:
                if topic in self.subscriptions:
                    message = RawMessage(topic, jsondata=jsondata)
                    self.on_message(message)

            # Ignore "export" messages
            elif jsondata['header']['message_type'] == 'export':
                pass

            else:
                self.logger.warning(f"{self}: Message provided with no topic: {jsondata}")


    def disconnect(self):
        """
        Disconnect from the input and output files.
        """

        self.logger.info(f"{self}:  Closing input and output files")
        if self.input_file is not None:
            self.input_file.close()
            self.input_file = None

        if self.output_file is not None:
            self.output_file.close()


    def _get_timestamp(self, jsondata):
        """
        Get the timestamp from the JSON data for a single line from a metadata file.
        """

        return ciso8601.parse_datetime(jsondata['header']['timestamp'][:-1].split('+')[0])


    def _get_topic(self, jsondata):
        """
        Get the topic from the JSON data for a single line from a metadata file.
        """

        if 'topic' in jsondata:
            return jsondata['topic']

        # Get AgentVersionInfo topic for other agents that omit it (e.g. uaz_dialog_agent)
        if jsondata.get('header', {}).get('message_type', None) == 'agent':
            if jsondata.get('msg', {}).get('sub_type', None) == 'versioninfo':
                agent_name = jsondata.get('data', {}).get('agent_name', None)
                if agent_name:
                    return f"agent/{jsondata['data']['agent_name']}/versioninfo"
