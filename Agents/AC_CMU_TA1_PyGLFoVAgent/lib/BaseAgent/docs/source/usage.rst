Usage
=====

The typical use cases for MinecraftBridge is to provide a simple approach for an object to receive Minecraft messages from an arbitrary backend, without having to have the object be responsible for establishing, maintaining, or working with low-level connections, or parse backend-specific data.  This typically involves the following steps:

1.  Create a client object with the appropriate callback for receiving messages from the bus (i.e., `receive(self, message)`).

2.  Create an instance of the Bridge suitable for connecting to the backend.

3.  Register the client object with the bridge instance for each message type the client should receive.

4.  Create the bridge connection.

5.  (Optional) Generate messages and send to the Bridge connection.

6.  Disconnect the bridge when complete.


Creating a Client Class
-----------------------

The only stipulation placed on a client object is that it must implement a `receive` method, which accepts a `message` argument.  For example, a minimal class definition would be::

    class ClientClass:
        """
        Minimal client class for connecting with a MinecraftBridge instance.
        """

        def receive(self, message):
            """
            Callback method for receiving messages from the Bridge instance.
            """

            # Define object's behavior here
            pass


In practice, the object will want to invoke different behavior based on the class of the received message.  A simple pattern for managing message-specific behavior is to utilize a dictionary mapping message class to specific callback function, which can be created during object initialization.  In the `receive` method, the mapping can be used to look up which method to call, and pass the message to that method.  As an example, assuming the object wants to process the `BeepEvent` and `ChatEvent` messages, the `ClientClass` can be extended as follows::

    from MinecraftBridge.messages import BeepEvent, ChatEvent

    class ClientClass:
        """
        Minimal client class for connecting with a MinecraftBridge instance.
        """

        def __init__(self):

            # Message callback dictionary -- a simple approach for handling 
            # which message types the client should receive, and what methods
            # to call when they are received.
            self.__message_callbacks = { BeepEvent: self.__onBeepEvent,
                                         ChatEvent: self.__onChatEvent
                                       }

        def __onBeepEvent(self, message):
           """
           Callback method for handling BeepEvent messages
           """

           # Define BeepEvent behavior here
           pass

        def __onChatEvent(self, message):
           """
           Callback method for handling ChatEvent messages
           """

           # Define ChatEvent behavior here
           pass

        def receive(self, message):
            """
            Callback method for receiving messages from the Bridge instance.
            """

            # Determine which method to call based on the message's class, and
            # pass the message to that method.
            
            # Note that it is possible that a message type is received that
            # isn't in the callback dictionary, so check this first.
            if not message.__class__ in self.__message_callbacks:
                return

            # Call the appropriate callback method, passing the message
            self.__message_callbacks[message.__class__](message)


Creating a Bridge
-----------------

While specific Bridge classes are typically instantiated with specific arguments, once created, the interface should remain consistent between differen classes, allowing the client object to interact with bridges without consideration to the concrete implementation being used.  Specifically, the client interacts with the bridge using the following methods:

* `register(client_object, message_class)`:  Indicates that the provided client should receive message instances of the message class type.  A client can register with a bridge multiple times (once for each message class of instance), as well as register with multiple bridges.

* `send(message)`:  Method for allowing clients to *generate* instances of a message, and push the message to the bridge.  This allows for client code to communicate back to the Minecraft backend, assuming such communication can be properly handled.

In addition, Bridge classes also implement the following methods to connect / disconnect to the corresponding Minecraft backend:

* `connect()`:  Connect to the Minecraft backend, and start receiving messages.

* `disconnect()`:  Disconnect from the Minecraft backend, and stop receiving messages.

As with `send`, the behavior invoked by these two methods will vary with specific Bridge classes.  Additionally, the client object should `register` all desired message classes *prior* to invoking `connect` or `send`.


As an example, an instance of the `ClientClass` above can be connected to a `MinecraftBridge.mqtt.Bridge` instance in the following manner::

    from MinecraftBridge.mqtt import Bridge as MessageBusBridge
    from MinecraftBridge.messages import BeepEvent, ChatEvent

    # Create instances of the ClientClass and MessageBusBridge
    client = ClientClass()
    bridge = MessageBusBridge()

    # Register the client with the bridge, indicating that it wants to receive
    # `BeepEvent` and `ChatEvent` messages
    bridge.register(client, BeepEvent)
    bridge.register(client, ChatEvent)

    # Connect the bridge instance to the message bus, to start receiving messages
    # Note that, when connecting, this bridge takes as arguments the host and 
    # port number of the MQTT server.
    bridge.connect('localhost', 1883)


In typical use cases, it may make sense to allow the client to maintain an instance of the bridge as an attribute, allowing for interactions between the client and bridge (e.g., sending messages) to remain encapsulated in the client.  In this case, extending the `ClientClass` initialization to take an instance of a bridge as an attribute allows for simplifying client registration for each messaage::

    from MinecraftBridge.messages import BeepEvent, ChatEvent

    class ClientClass:
        """
        Minimal client class for connecting with a MinecraftBridge instance.
        """

        def __init__(self, bridge):

            # Keep the reference to the provided bridge as an attribute, to
            # simplify sending messages in the future
            self.__bridge = bridge

            # Message callback dictionary -- a simple approach for handling 
            # which message types the client should receive, and what methods
            # to call when they are received.
            self.__message_callbacks = { BeepEvent: self.__onBeepEvent,
                                         ChatEvent: self.__onChatEvent
                                       }

            # Register each of the message classes in the callback dictionary 
            # with the bridge
            for message_class in self.__message_callbacks.keys():
                self.__bridge.register(self, message_class)


        def __onBeepEvent(self, message):
           """
           Callback method for handling BeepEvent messages
           """

           # Define BeepEvent behavior here
           pass


        def __onChatEvent(self, message):
           """
           Callback method for handling ChatEvent messages
           """

           # Define ChatEvent behavior here
           pass


        def receive(self, message):
            """
            Callback method for receiving messages from the Bridge instance.
            """

            # Determine which method to call based on the message's class, and
            # pass the message to that method.
            
            # Note that it is possible that a message type is received that
            # isn't in the callback dictionary, so check this first.
            if not message.__class__ in self.__message_callbacks:
                return

            # Call the appropriate callback method, passing the message
            self.__message_callbacks[message.__class__](message)


        def connect(self):
            """
            Connect the bridge to the Minecraft backend
            """

            self.__bridge.connect()


        def disconnect(self):
            """
            Disconnect the bridge from the Minecraft backend
            """

            self.__bridge.disconnect()


Using the above approach, a bridge can be created in conjunction with the `ClientClass`, and the addition of the `connect` and `disconnect` methods allows for interaction with a single object for both connection and message handling, while still allowing for versatility in backend connection.  As an example, switching between using a `MessageBusBridge` and `FileBridge` simply involves changing the class and arguments used for the bridge; compare the code using a `MessageBusBridge`::

    from MinecraftBridge.mqtt import Bridge as MessageBusBridge

    client = ClientClass(MessageBusBridge())
    client.connect()

and code using a `FileBridge`::

    from MinecraftBridge.mqtt import FileBridge

    client = ClientClass(FileBridge())
    client.connect()


Handling Messages
-----------------

Messages received by the client are generally lightweight objects, with properties corresponding to the contents or information contained in the events that produced the message.  For many messages, properties are *aliased*, allowing, for instance, to refer to a location either as a tuple using the `location` property, or by accessing the individual `x`, `y`, `z` components.  Additionally, messages should be considered *immutable*; attempts to set properties will generally raise an Exception.

As an example, `BeepEvent` messages contain `source_entity`, `message`, and `location` properties; `source_entity` and `location` have additional aliases.  When a `BeepEvent` message is received, the client can simply access the values of these properties directly, with aliases providing equivalent behavior::

    def __onBeepEvent(self, message):
        """
        Callback method for handling BeepEvent messages
        """

        # These two properties are aliases, and will produce the same data
        source = message.source_entity
        source = message.sourceEntity

        message = message.message

        # Individual values in the `location` property can also be accessed
        # with `beep_x`, `beep_y`, and `beep_z`
        x, y, z = message.location
        x = message.beep_x
        y = message.beep_y
        z = message.beep_z


Generating and Sending Messages
-------------------------------

In addition to receiving messages, Bridge instances also allow for sending messages.  Generally speaking, messages are instantiated with a set of keyword argument specific to the message type.  Additionally, messages are *immutable*; once instantiated, properties of the message instance cannot be modified.  Once the message is generated, it is simply a matter of passing the message to the bridge instance using the `send` method.  For example::

    from MinecraftBridge.messages import BeepEvent
    from MinecraftBridge.mqtt import Bridge as MessageBusBridge

    # Create the bridge to the message bus and connect
    bridge = MessageBusBridge()
    bridge.connect('localhost', 1883)

    # Create a BeepEvent message and send to the message bus through the bridge
    message = BeepEvent(sourceEntity='Location Device',
                        message='beep beep',
                        location=(-2187,56,61))
    bridge.send(message)

When generating a message, the following exceptions may be raised:

* `MissingMessageArgumentException`: raised when an expected keyword argument is not provided during creation.

* `MalformedMessageCreationException`: raised when a specific keyword argument cannot be coerced into the format expected by the message class.  A common example is when a `location` argument is passed that isn't an tuple, list, or similar data type with three elements.




