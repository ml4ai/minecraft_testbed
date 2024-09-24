#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from RawConnection import *

################################################################################
# Message object

def getUnixTimestamp():
    return int(datetime.datetime.utcnow().timestamp() * 1000)

class Message(object):

    # Static members
    __endian = 'big'
    __enc = "utf-8"

    def __init__(self, key = None, unixTimestamp = None, appId=None, type=None,contentType=None,contentEncoding=None,payload=None,jsondata=None):
        self.key = key
        if unixTimestamp is None:
            self.unixTimestamp = getUnixTimestamp()
        else:
            self.unixTimestamp = unixTimestamp
        self.appId = appId
        self.type = type
        self.contentType = contentType
        self.contentEncoding = contentEncoding
        self.payload = payload

        if jsondata:
            self.contentType = "application/json"
            self.contentEncoding = 'utf-8'
            self.payload = json.dumps(jsondata).encode('utf-8')
    @property
    def jsondata(self):
        return json.loads(self.payload.decode("utf-8"))
    def __repr__(self):
        return f"Message(key='{self.key}',unixTimestamp={self.unixTimestamp},appId='{self.appId}', type='{self.type}',contentType='{self.contentType}',contentEncoding='{self.contentEncoding}' payload={self.payload})"


    # Decode Message
    @classmethod
    def fromRawMessage(cls, msg):
        if not(isinstance(msg, RawMessage)):
            raise TypeError ("Not a RawMessage")

        message = cls(msg.key)

        i=0

        # Word 0
        if not(msg.payload[i:i+4] == b"MSA\0"):
            raise ValueError("Invalid header")
        i+=4

        # Words 1-2
        message.unixTimestamp = int.from_bytes(msg.payload[i:i+8], byteorder=Message.__endian, signed=True)
        i+=8

        # Word 3
        n = msg.payload[i]
        i+=4

        # Properties
        for j in range(n):
            numBytes = int.from_bytes(msg.payload[i:i+2], byteorder=Message.__endian, signed=True)
            i+=2
            prop = msg.payload[i:i+numBytes].decode(Message.__enc)
            i+=numBytes
            if (j == 0):
                message.appId = prop
            elif (j == 1):
                message.type = prop
            elif (j == 2):
                message.contentType = prop
            elif (j == 3):
                message.contentEncoding = prop
            else:
                raise ValueError("Invalid number of properties for decode.")

        # Payload
        message.payload = msg.payload[i:]
        return message

    # Encode Message
    def toRawMessage(message):
        if not(isinstance(message, Message)):
            raise TypeError ("Not a Message")

        # Word 0
        payload = bytearray(b'MSA\0')

        # Words 1-2
        payload += (message.unixTimestamp).to_bytes(8, Message.__endian)

        # Properties
        n = 0
        properties = bytearray()

        if not(message.contentEncoding == None):
            bytes = message.contentEncoding.encode(Message.__enc)
            properties = bytes + properties
            properties = len(bytes).to_bytes(2, Message.__endian) + properties
            n+=1

        if not(message.contentType == None):
            bytes = message.contentType.encode(Message.__enc)
            properties = bytes + properties
            properties = len(bytes).to_bytes(2, Message.__endian) + properties
            n+=1
        elif (n > 0):
            properties = b'\x00\x00' + properties
            n+=1

        if not(message.type == None):
            bytes = message.type.encode(Message.__enc)
            properties = bytes + properties
            properties = len(bytes).to_bytes(2, Message.__endian) + properties
            n+=1
        elif (n > 0):
            properties = b'\x00\x00' + properties
            n+=1

        if not(message.appId == None):
            bytes = message.appId.encode(Message.__enc)
            properties = bytes + properties
            properties = len(bytes).to_bytes(2, Message.__endian) + properties
            n+=1
        elif (n > 0):
            properties = b'\x00\x00' + properties
            n+=1

        # Word 3
        payload += (n).to_bytes(1, Message.__endian)
        payload += b'\x00\x00\x00'
        payload += properties
        payload += message.payload

        msg = RawMessage(message.key, payload)
        return msg

################################################################################
# Connection class

class Connection(object):
    def __init__(self, rawConnection):
        if not(isinstance(rawConnection, RawConnection)):
            raise TypeError ("Not a RawConnection")
        self.__logger = logging.getLogger(__name__)
        self.__rawConnection = rawConnection
        self.__rawConnection.onMessage = self.__onMessage
        self.__onMessageCallback = None

    # Callbacks
    def __onMessage(self, msg):
        callback = self.onMessage
        if callback:
            # Decode Message
            message = Message.fromRawMessage(msg)
            callback(message)
        else:
            self.__logger.info('Connection dropping message, {}'.format(msg.key))

    @property
    def onConnectionStateChange(self):
        self.__rawConnection.onConnectionStateChange

    @onConnectionStateChange.setter
    def onConnectionStateChange(self, value):
        self.__rawConnection.onConnectionStateChange = value

    @property
    def onMessage(self):
        return self.__onMessageCallback

    @onMessage.setter
    def onMessage(self, value):
        self.__onMessageCallback = value

    # Publish
    def publish(self, message):
        # Check AppId
        if (message.appId == None):
            message.appId = self.__rawConnection.clientId
        # Encode message
        msg = message.toRawMessage()
        self.__rawConnection.publish(msg)

    # Subscribe
    def subscribe(self, topic):
        self.__rawConnection.subscribe(topic)


    # deliver messages that match subscription filter to callback.
    # only messages that don't match any callbacks will be delivered to onMessage callback.
    def message_callback_add(self,sub,callback):
        def my_callback(raw):
            try:
                callback(Message.fromRawMessage(raw))
            except Exception as ex:
                self.__logger.error('Failed message callback', exc_info=True)
        self.__rawConnection.message_callback_add(sub,my_callback)

    # remove subscription callback
    def message_callback_remove(self,sub):
        self.__rawConnection.message_callback_remove(sub)

    # Unsubscribe
    def unsubscribe(self, topic):
        self.__rawConnection.unsubscribe(topic)

    # Connect
    def connect(self,start_loop=True):
        self.__rawConnection.connect(start_loop=start_loop)

    # start a network loop in background thread
    def start_loop(self):
        self.__rawConnection.start_loop()

    # start network loop in foreground
    def loop_forever(self):
        self.__rawConnection.loop_forever()

    # if not looping forever, or looping in background, call me periodically
    def loop(self):
        self.__rawConnection.loop()

    # Disconnect
    def disconnect(self):
        self.__rawConnection.disconnect()

################################################################################
