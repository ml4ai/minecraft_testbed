import json

from abc import ABC, abstractmethod
from .parsers import ParserMap
from ..utils import Loggable



class RawMessage(object):
    def __init__(self, key, payload=None, jsondata=None):
        self.key = key
        self._payload, self._jsondata = payload, jsondata

        if jsondata is not None:
            self._payload = json.dumps(jsondata).encode('utf-8')
        if payload is not None:
            self._jsondata = json.loads(self.payload.decode('utf-8'))

    @property
    def jsondata(self):
        return self._jsondata

    @property
    def payload(self):
        return self._payload

    def __repr__(self):
        return f"RawMessage(key='{self.key}',payload={self.payload})"



class BaseBridge(ABC, Loggable):
    """
    An abstract base bridge class for handling connections to Minecraft.

    Attributes
    ----------
    name : string
        name of the bridge instance
    logger : logging.Logger
        instance of the logger than log messages are sent to
    isConnected : boolean
        indication of whether the bridge is connected to the bus source or not
    observers : dictionary
        dictionary mapping message classes to objects that wish to receive 
        messages of the given class


    Methods
    -------
    on_message(message)
        Callback for receiving and processing messages from the bus source
    register(observer, message_class)
        Register an observer to receive messages of a given class
    subscribe(topic)
        Subscribe to receive messages of a given topic from the bus source
    unsubscribe(topic)
        Unsubscribe from receiving messages of a given topic from the bus source
    send(message, **kwargs)
        Send a message to the bus source
    connect(start_loop=True)
        Connect to the bus source
    disconnect()
        Disconnect from the bus source
    start()
        Begin recieving messages from the bus source
    """

    def __init__(self, name, include_name_in_string=False, connected_on_creation=False, **kwargs):
        """
        Arguments
        ---------
        name : string
            The name of the bridge
        include_name_in_string : bool
            Whether or not to include the name in the string represention
        connected_on_creation : bool
            Whether or not this bridge is connected at creation
        """
        self.name = name
        self.agent_name = kwargs.get('agent_name', self.name)

        # Whether or not the bridge is going to be connected upon creation
        self.isConnected = connected_on_creation

        # String representation of the object
        # NOTE:  May want to be able to define this at initialization time,
        #        such as to avoid including the name
        if include_name_in_string:
            self.__string_name = f'[{self.__class__.__name__} - {self.name}]'
        else:
            self.__string_name = f'[{self.__class__.__name__}]'

        # Maintain a set of (observer, priority) pairs, indexed by
        # the type of message they want to receive
        self.observers = {}

        self.parser_map = ParserMap(self.agent_name)

        # Keep track of elapsed milliseconds
        self._elapsed_milliseconds = 0


    def __str__(self):
        """
        Return a string representation of the object.

        Returns
        -------
        string
            String representation of the object
        """
        return self.__string_name


    def on_message(self, message):
        """
        Callback after a message is received from the bus.

        Upon receiving a message, attempts to parse the message, and sends the
        parsed message instance to observers that are registered to receive 
        messages of the class.

        Parameters
        ----------
        message : RawMessage instance
            message, converted to RawMessage instance
        """

        # Determine which message class(es) can parse the message, and inform
        # the observers
        self.logger.debug(f'{self}: Received message {message}')

        # Get the MessageClass that would be needed to parse this message
        message_class = self.parser_map.getMessageClassByTopic(message.key)

        if message_class is None:
            self.logger.debug(f'{self}:  Topic {message.key} unknown to ParserMap')
            return

        try:
            msg = self.parser_map[message_class].parse(message.jsondata)
            self._elapsed_milliseconds = msg.elapsed_milliseconds

            # Send message to relevant observers (in priority order)
            observers = sorted(self.observers[message_class], key=lambda x: x[1]) # sort by priority
            for observer, _ in observers:
                try:
                    observer.receive(msg)
                except Exception as e:
                    self.logger.exception(f'{self}:  Exception when dispatching message {msg} to {observer}:')
                    self.logger.exception(f'{self}:  {str(e)}')

        except Exception:
            self.logger.exception(f'{self}:  Exception when parsing message.\nMessage:\n{message.jsondata}\n')


    def register(self, observer, message_class, priority=1):
        """
        Registers an observer to receive messages of a given type.

        Register an observer to receive messages of a certain type.  When 
        messages of the given class are received and parsed, the bridge calls
        observer.recieve(message), where message is the parsed message object.

        The passed message class is assumed to have a class attribute 'topic',
        indicating the topic to listen for on the bus, and class methods
        'parse', which generates an instance of the message object (or None, if
        not parsable by the class).

        When registered, the corresponding topic of the message class is 
        subscribed to.

        Parameters
        ----------
        observer : object
            Client object to receive messages
        message_class : class
            Message type the client should recieve
        priority : int
            Optional priority value that determines the order
            in which observers receive messages (smaller value = high priority)
        """
        self.logger.debug(f'{self}:  Registering {observer} to receive {message_class.__name__} messages')

        # Check if the message_class is in the observer dictionary.  If not,
        # create an empty set and subscribe to the topic if connected to the
        # bus
        if not message_class in self.observers.keys():
            self.observers[message_class] = set()
            if self.isConnected:
                parser = self.parser_map[message_class]
                if parser is not None:
                    self.subscribe(parser.topic)

        # Add the observer
        self.observers[message_class].add((observer, priority))


    def deregister(self, observer, message_class=None, silence_warnings=False):
        """
        Remove an observer from receiving messages of a given type.  If no
        message class if provided, then the observer is deregistered from _all_
        message classes

        Parameters
        ----------
        observer : object
            Client object to no longer receive messages
        message_class : class, default=None
            Message type the client should no longer receive
        """

        # Deregister the observer from _all_ message classes
        if message_class is None:
            for msg_class in list(self.observers.keys()):
                self.deregister(observer, message_class=msg_class, silence_warnings=True)
            return

        # Make sure the message class is in the observers dictionary
        if not message_class in self.observers.keys() and not silence_warnings:
            self.logger.warning(f'{self}:  Attempted to deregister observer {observer} from unregistered message class {message_class.__name__}')
            return

        # Get relevant observers and their corresponding priorities
        if len(self.observers[message_class]) > 0:
            observers, priorities = zip(*self.observers[message_class])
        else:
            observers, priorities = [], []

        # Make sure the observer is actually registered to receive the messages
        if not observer in observers and not silence_warnings:
            self.logger.warning(f'{self}:  Attempted to deregister observer {observer} that is not subscrbed to message class {message_class.__name__}')
            return

        # All safe, removing the observer (at all priorities)
        for priority in priorities:
            if (observer, priority) in self.observers[message_class]:
                self.observers[message_class].remove((observer, priority))

        # The message class may no longer be needed;
        # unsubscribe if it is currently empty
        if len(self.observers[message_class]) == 0:
            topic = self.parser_map[message_class].topic
            self.logger.info("%s:  Unsubscribing from %s -- no registered listeners", self, topic)
            self.unsubscribe(topic)
            self.observers.pop(message_class, None) # we can't resubscribe if the observers hold on to it


    @abstractmethod
    def subscribe(self, topic):
        """
        Subscribe to a topic published by the bus source.

        Parameters
        ----------
        topic : string
            Topic to subscribe to
        """
        pass


    @abstractmethod
    def unsubscribe(self, topic):
        """
        Unsubscribe to a topic published by the bus source.

        Parameters
        ----------
        topic : string
            Topic to unsubscribe to
        """
        pass


    @abstractmethod
    def send(self, message, **kwargs):
        """
        Send the message to the bus source.

        This method assumes the message is an instance of a message class
        defined in MinecraftBridge.messages.  Converting to JSON and topic
        publication is performed by the message instance and corresponding
        parser.

        Parameters
        ----------
        message : MinecraftBridge.message object
        """
        pass


    def connect(self, start_loop=True):
        """
        Connect to the bus source.
        """
        if start_loop:
            self.start()


    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the bus source.
        """
        pass


    @abstractmethod
    def start(self):
        """
        Start receiving messages from the bus source.
        """
        pass


    @property
    def _unwrapped(self):
        """
        Internal property that returns the underlying bridge.
        """
        return self

