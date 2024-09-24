# -*- coding: utf-8 -*-
"""
.. module:: MinecraftBridge.mqtt.parser_map
   :platform: Linux, Windows, OSX
   :synopsis: Mapping of Message class to corresponding parsers and generators

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class for creating a mapping from Message classes to parser /
generator instances.
"""

from .parser_higher_order_function import (
	simple_parse_functoid,
	simple_generate_functoid
)
from .message_parser_arguments import (
	MQTT_PARSERS,
	UNIQUE_MQTT_PARSER_CLASSES,
	UNIQUE_MQTT_PARSER_STATIC_CLASSES
)

from .agent_version_info import AgentVersionInfoParser
from ...messages import AgentVersionInfo
from ...utils import Loggable

from .message_types import MessageType, MessageSubtype



class MessageParser:
	"""
	A MessageParser is a lightweight class encapsulating functions to parse
	messages from the MQTT bus (JSON to Message object), and generate messages
	for the MQTT bus (Message object to JSON).  Additionally, a MessageParser
	contains the topic for the message, and the Message class it is able to
	handle.

	Attributes
	----------
	topic : string
		MQTT bus topic the MessageParser will subscribe to
	MessageClass : MinecraftBridge.messages.BaseMessage subclass
		Message type the MessageParser is capable of handling
	parse : function
		Function for parsing MQTT bus messages (JSON to MessageClass)
	generate : function
		Function for generating MQTT bus messages (MessageClass to JSON)
	"""

	def __init__(self, topic, message_class, 
		                parse_function, generate_function,
		                msg_type, msg_subtype, alt_subtypes=[]):
		
		self.topic = topic
		self.MessageClass = message_class
		self.parse = parse_function
		self.generate = generate_function
		self.msg_type = msg_type
		self.msg_subtype = msg_subtype
		self.alternatives = alt_subtypes


class ParserMap(Loggable):
	"""
	A ParserMap maintains a set of MessageParsers and means to access the
	parsers.

	The ParserMap accepts an `agent_name` argument during initialization.  This
	argument is used to populate templated topic fields, and therefore should
	be ammenable to message topic formats (e.g., using snake_case).
	"""

	def __init__(self, agent_name):
		"""
		Arguments
		---------
		agent_name : string
			Name of the agent using the ParserMap
		"""

		self._agent_name = agent_name

		# The parser map is a dictionary mapping MessageClass to MessageParser.
		self._parser_map = {}

		self._topic_to_message_class_map = {}
		self._type_subtype_to_topic_map = {}

		# Populate the parser map with the set of parsers
		self.__construct_parsers()


	def __str__(self):
		"""
		String representation of the ParserMap
		"""

		return self.__class__.__name__


	def __construct_parsers(self):
		"""
		Helper function to construct parsers using the MQTT_PARSERS dictionary
		"""

		# Add the simpler parsers in MQTT_PARSERS
		for message_class, parser_args in MQTT_PARSERS.items():

			topic = parser_args["topic"].format(agent_name=self._agent_name)
			parser = simple_parse_functoid(message_class,
				                           parser_args["type"],
				                           parser_args["subtype"])
			generator = simple_generate_functoid()

			self.add(MessageParser(topic, 
				                    message_class, 
				                    parser, 
				                    generator, 
				                    parser_args["type"],
				                    parser_args["subtype"],
				                    parser_args.get("alternatives", [])))

		# Add the parsers that require unique MessageParsers instances
#		for ParserClass in UNIQUE_MQTT_PARSER_CLASSES.values():
#			self.add(ParserClass(agent_name=self._agent_name))

#		self.add(AgentVersionInfoParser(agent_name=self._agent_name))
		self._parser_map[AgentVersionInfo] = AgentVersionInfoParser(agent_name=self._agent_name)

		# Add the parsers that have their own unique classes
		for parser in UNIQUE_MQTT_PARSER_STATIC_CLASSES.values():
			self.add(parser)


	def add(self, parser, replace=True):
		"""
		Arguments
		---------
		parser : MessageParser
			Parser to add to the map
		replace : boolean, default=True
			Indicate if the parser should replace a currently existing one in
			the map, if present
		"""

		if parser.MessageClass in self._parser_map and not replace:
			self.logger.info("%s: Attempted to add parser for message type %s.  Parser already exists, ignoring.", self, parser.MessageClass)
			return

		self.logger.info("%s:  Added parser for message type %s", self, parser.MessageClass)
		self._parser_map[parser.MessageClass] = parser

		self._topic_to_message_class_map[parser.topic] = parser.MessageClass

		self._type_subtype_to_topic_map[(parser.msg_type, parser.msg_subtype)] = parser.topic
		for alt in parser.alternatives:
			self._type_subtype_to_topic_map[(parser.msg_type, alt)] = parser.topic




	def __getitem__(self, key):
		"""
		Returns a MessageParser based on the provided key.

		Arguments
		---------
		key : MessageClass
			The type of message to return the parser for
		"""

		# Check to see if the parser is in the map
		if not key in self._parser_map:
			self.logger.warning("%s: No parser found for key %s", self, key)
			return None

		return self._parser_map[key]


	def getMessageClassByTopic(self, topic):
		"""
		Return the MessageClass associated with a topic, if it's int eh ParserMap.

		Arguments
		---------
		topic : string
			The topic to search by

		Returns
		-------
			Message Class referenced by topic, or None if not in map
		"""

		return self._topic_to_message_class_map.get(topic, None)


	def getTopicByTypeAndSubtype(self, msg_type, msg_subtype):
		"""
		Return the MessageClass associated with a type and subtype, if it's in the
		ParserMap.

		Arguments
		---------
		msg_type : string
			Message Type
		msg_subtype : string
			Message Subtype
		"""

		_type = None
		_subtype = None

		try:
			_type = MessageType(msg_type)
		except:
			self.logger.warning("%s: Received unknown message type: %s", self, msg_type)

		try:
			_subtype = MessageSubtype(msg_subtype)
		except:
			self.logger.warning("%s: Received unknown message subtype: %s", self, msg_subtype)

		topic = self._type_subtype_to_topic_map.get((_type,_subtype), None)

		if topic is None:
			self.logger.warning("%s: Received unknown type/subtype combo: (%s,%s)", self, msg_type, msg_subtype)
			return None

		return topic
			








