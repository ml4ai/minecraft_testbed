# -*- coding: utf-8 -*-
"""
.. module:: agent_template.py
   :platform: Linux, Windows, OSX
   :synopsis: Template demonstrating the creation of a BaseAgent to publish and
              subscribe to the internal (Redis) and external (MQTT) bus

.. moduleauthor:: CMU-TA1 <danahugh@andrew.cmu.edu>

This file provide a simple template for being able to create an agent using the
BaseAgent superclass, with boilerplate code to start the agent from command
line.


Configuration File
------------------
This template assumes the existence of a configuration file in JSON format.  At
a minimum, the configuration file should contain the host and port of the MQTT
and Redis buses (if being used).  If not using either (i.e., the agent is only
being used to process metadata files, and does not use the Redis bus), then the
_contents_ of the JSON can be empty, though the file must exist with an empty
JSON object at a minimum.

A minimal configuration file is provided here::

    {
        "mqtt_bus": {
            "host": <mqtt_host>,
            "port": <mqtt_port>
        },
        "redis_bus": {
            "host": <redis_host>,
            "port": <redis_port>
        }
    }


The fields above should be populated with the following information:

    * mqtt_host : string, default="localhost"
        Hostname of the MQTT broker
    * mqtt_port : int, default=1833
        Port number of the MQTT broker
    * redis_host : string, default="localhost"
        Hostname of the Redis bus
    * redis_port : int, default=6379
        Port number of the Redis bus


If the `mqtt_bus` field is omitted, and the boilerplate code is executed to 
work with an MQTT bus (i.e., no input / output files are provded), then the
boilerplate code will attempt to connect to an MQTT bus with the default host
and port.

If the `redis_bus` field is omitted, the agent will be provided with a Redis
Bridge using a "dummy" Redis server (i.e., the Redis bus doesn't actually exist
and published messages are simply discarded).  If the `redis_bus` field exists,
but points to an empty JSON object, then default values of host and port will
be used.

Additional configuration parameters can be provided in the config file, as long
as they are valid JSON.  The contents of the config file is available as the
agents `config` attribute, in dictionary format.


Callback Interfaces
-------------------
This template agent creates CallbackInterfaces for both the Redis and Minecraft
bridges.  These are typically simpler and safer to use than interacting directly
with the bridge instances themselves.  Additionally, both components share the
same interface


Registering and Deregistering Callbacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The callback interfaces implement the following two methods to allow the agent
to register and deregister callback methods to be called when messages of a
given class (MinecraftBridge) or channel (RedisBridge) is received

The MinecraftBridge methods have the following signature:

    * `register_callback(self, message_class, callback, priority=1)`

    Indicates that the agent should listen for messages of the given class, and
    call the callback when the message is received.  Note that the agent can
    register multiple callbacks to the same message class, and can have the 
    same callback handle multiple message classes, but this method needs to be
    invoked for each message_class / callback pair.

    Arguments
    ---------
        message_class : MinecraftBridge.messages.<MessageClass>
            Message class that is being listened for
        callback : callable
            Method / function to call when the message is received.  The
            callback must accept a single argument (`message`) of the type of
            the MessageClass being listened for, and does not return a value
        priority : int, default=1
            The priority of the callback, to determine the order in which 
            callbacks are called.  Callbacks with smaller values are called
            prior to callbacks with higher values.


    * `deregister_callback(self, callback, message_class=None)`

    Indicates that the agent should no longer call the provided callback when
    a message is received.

    Arguments
    ---------
        callback : callable
            Method / function that should no longer receive messages
        message_class : MincraftBridge.messages.<MessageClass>, default=None
            Message class that should no longer be received.  Used if the
            callback is registered to recieve messages of multiple classes, and
            only one class should no longer be attended to.  `None` indicates
            that _all_ message classes should be deregistered for the callback.


The RedisBridge methods have similar signatures, though argument types and
semantics may differ slightly:

    * `register_callback(self, callback, channel, message_type=None)`

    Indicates that the agent should listen for messages of the given channel, 
    and call the callback when the message is received.  As with the 
    MinecraftBridge interface, multiple callbacks can be registered to a single
    channel, and vice-versa.

    Arguments
    ---------
        callback : callable
            Method / function to call when the message is received.  The
            callback must accept a single argument (`message`), and does not
            return a value
        channel : string
            Name of the channel
        message_type : default=None
            Message type that should trigger the callback.  If `None`, all
            message types trigger the callback.


    * `deregister_callback(self, callback, channel=None, message_type=None)`

    Indicates that the agent should no longer call the provided callback when
    a message is received.

    Arguments
    ---------
        callback : callable
            Method / function that should no longer receive messages
        channel : string, default=None
            String indicating the name of the channel that should no longer be
            listened to.  If `None`, deregisters the callback from all channels
        message_type : string, default=None
            Message type that should be deregistered.  If `None`, deregisters
            the callback from all message types.


Publishing Messages
~~~~~~~~~~~~~~~~~~~
The callback interface for the MinecraftBridge provides a single method to 
publish messages to the MQTT bus:

    * `publish(self, message)`

    Publishes a message to the MQTT message bus.

    Arguments
    ---------
    message : MinecraftBridge.messages.<MessageClass> instance
        Message to be published.


The callback interface to the RedisBridge provides a method for sending
messages, and a pair of messages to handle requests and responses:

    * `send(self, data, channel)`

    Publishes a message to the internal Redis bus.

    Arguments
    ---------
    data 
        The message data to be published.
    channel
        The channel to publish the data to.


    * `request(self, data, channel, blocking=True, timeout=None)`

    Send a request with the provided data on the given channel to the Redis bus

    Arguments
    ---------
    data
        The request data to be published
    channel
        The channel on which to publish the request
    blocking : boolean, default=True
        Indicate whenter or not to block and return the response, or return the
        request ID immediately
    timeout : int, default=None
        Number of seconds to wait for a response


    * `respond(self, data, channel, request_id)`

    Send a response to the given request on the given channel, with the provided
    data through the Redis bus

    Arguments
    ---------
    data
        The request data to be published
    channel
        The channel on which to pulish the request
    request_id
        The ID of the message being responded to


Running the Agent
-----------------
One constructed, the agent can be started by simply calling the `run()` method
of the agent.


Usage
-----
This file also contains boilerplate code to execute the agent from command-line
using two modes of execution:  bus-based and file-based.  Note that, in both 
cases, a Redis server needs to be running prior to execution, if used by the
agent.

To connect the agent to an existing MQTT bus and run, the following command
should be used::

    python agent_template.py <config_path>

To run a metadata file through the agent, the following command should be used::

    python agent_template.py <config_path> -i <input_path> [-o <output_path>]


Command Line Arguments
~~~~~~~~~~~~~~~~~~~~~~
config_path
    Path to the JSON configuration file containing the configuration of the
    agent.
input_path (optional, for file-based execution)
    Path to the input metadata file to run through the agent.
output_path (optional, for file-based execution)
    File path to write messages published to the MQTT bus from the agent to.
    If this argument is not provided, then the output will be piped to 
    `/dev/null`.
"""


# Bootstraping and bus components
import MinecraftBridge
import RedisBridge

from MinecraftBridge.mqtt.interfaces import MinecraftCallbackInterface
from RedisBridge.interfaces import CallbackInterface as RedisCallbackInterface

from BaseAgent import BaseAgent
from BaseAgent.utils import parseCommandLineArguments



class AgentTemplate(BaseAgent):
    """
    A template agent inheriting from BaseAgent.  The properties of this agent
    are primarily inherited from BaseAgent, but also includes a RedisBridge
    instance and callback interfaces for both bridges.  These may be removed
    from developed agents if unneeded.

    Properties
    ----------
    minecraft_bridge : MinecraftBridge instance
        Bridge connection to Minecraft (e.g. MQTT Message Bus)
    mission_clock : MissionClock
        MissionClock instance used to maintain an estimate of the current 
        mission time
    participants : ParticipantCollection
        Collection of participants in current trial
    semantic_map : SemanticMap
        Representation of the semantic map for the current trial
    trial_id : dictionary
        Dictionary with Experiment, Trial, and Replay IDs

    Methods
    -------
    get_status()
        Returns status information about the agent, used by the heartbeat
        thread during generation of heartbeat messages.
    run()
        Create buses for the agent, if necessary, and connect the agent to
        the bridges
    stop()
        Stop the agent's execution, and clean up the connection with the bridges
    """

    def __init__(self, minecraft_bridge, redis_bridge, config, **kwargs):

        BaseAgent.__init__(self, minecraft_bridge, config, **kwargs)

        # The `minecraft_bridge` and `config` arguments are stored as attributes
        # of the agent.  Store the `redis_bridge` as a property of the agent as
        # well.
        self.redis_bridge = redis_bridge

        # Callback interfaces for the Minecraft and Redis bridges.  This allows
        # for registering callbacks methods directly without having to deal
        # with low-level setup.
        self.minecraft_interface = MinecraftCallbackInterface(self.minecraft_bridge)
        self.redis_interface = RedisCallbackInterface(self.redis_bridge)


    def __str__(self):
        """
        String representation of the agent
        """

        return "Template Agent Name"


    def run(self):
        """
        """

        self.redis_bridge.start()

        BaseAgent.run(self)

        self.redis_bridge.stop()


def get_redis_bridge(config=None):
    """
    Simple helper function for extracting the redis bridge from the config
    file, if it exists.
    """

    # Return a dummy redis bridge if no config is provided
    if config is None:
        return RedisBridge.RedisBridge(dummy_redis_server=True)

    # Return a dummy redis bridge if no "redis_bus" entry is in the config
    if not 'redis_bus' in config:
        return RedisBridge.RedisBridge(dummy_redis_server=True)

    # Grab the host and port, use 'localhost:6379' by default
    host = config['redis_bus'].get('host', 'localhost')
    port = int(config['redis_bus'].get('port', 6379))

    return RedisBridge.RedisBridge(host=host, port=port)



if __name__ == '__main__':
    """
    Parse command line and config file arguments, create an instance of the
    InterventionManagerAgent, and run it.
    """

    # Parse the command line arguments
    args, config, bridge = parseCommandLineArguments()
    redis_bridge = get_redis_bridge(config)

    # Create the agent, and start it
    atlas = ATLAS(bridge, redis_bridge, config)
    atlas.run()
