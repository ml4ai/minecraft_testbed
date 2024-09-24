# -*- coding: utf-8 -*-
"""
.. module:: parser_higher_order_function
   :platform: Linux, Windows, OSX
   :synopsis: Higher-order function for creating parse functions

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of higher-order functions for creating message parsers and 
generators.  Parsers consume messages in JSON format and produce a BaseMessage
object, while generators consumea BaseMessage object to produce JSON versions 
of the message.

For most message types, parsing and generating 
"""

from .bus_header import BusHeaderParser
from .message_header import MessageHeaderParser
from .parser_exceptions import MissingHeaderException


def simple_parse_functoid(message_class, message_type, message_subtype, **kwargs):
	"""
	A simple functoid for creating a parser for a specific message class.

	Keyword arguments are included to allow for additional parser constructors
	to be built with the same interface.  This simple parser does not use any
	received keyword arguments.

	The parse function produced assumes that the `data` field of the received
	message can be used as keyword arguments in the `__init__` method of the
	provided message_class.  

	Arguments
	---------
	message_class : BaseMessage subclass
		Type of message generated when a received message is parsed
	message_type : MessageType
		top-level message type (in "header" header)
	message_subtype : MessageSubtype
		message subtype (in "msg" header)


	Returns
	-------
	function : dictionary -> message_class
		Parsing function for the given message_class
	"""

	def parse(json_message):
		
		# Make sure that there's a "header" and "msg" field in the message
		if not "header" in json_message.keys() or not "msg" in json_message.keys():
			raise MissingHeaderException(json_message)

		# Parse the header and message header
		busHeader = BusHeaderParser.parse(json_message["header"])
		messageHeader = MessageHeaderParser.parse(json_message["msg"])

		# Check to make sure that this parser can handle the provided message 
		# type.  If not, then return None
		# TODO: Raise a parse exception instead?
		if busHeader.message_type != message_type:
			return None
		if messageHeader.sub_type != message_subtype:
			return None

		# Parse the data
		data = json_message["data"]

		message = message_class(**data)
		message.addHeader("header", busHeader)
		message.addHeader("msg", messageHeader)

		return message


	# Add the documentation to the parser
	parse.__doc__ = \
	"""Convert a Python dictionary representation of the message from the MQTT
	broker to a %s instance.

	Arguments
	---------
	json_message : dictionary
		Dictionary representation of the message received from the MQTT broker.

	Returns
	-------
	Instance of a %s.
	""" % (message_class.__name__, message_class.__name__)


	return parse


def simple_generate_functoid():
	"""
	A simple functoid for generating JSON messages for publication to the MQTT
	bus.

	Returns
	-------
	function : Message -> string
		JSON representation of the message, as a string
	"""

	# For the moment, the generate function can rely on the `toJson` method of
	# a message

	return lambda x: x.toJson()