# -*- coding: utf-8 -*-
"""
.. module:: player_state
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Player State information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Player State messages.
"""


import json

import ciso8601

from .message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from .base_message import BaseMessage

class PlayerState(BaseMessage):
    """
    A class encapsulating PlayerState messages.

    Attributes
    ----------
    participant_id: string
        Unique identifier of participant (e.g. "P000420")
    playername : string
        Name of the entity
    name : string
        Alias of `playername`
    id : string
        A UUID unique identifier for the entity
    entity_id : string
        Alias of `id`        
    entity_type : string
        The type of the entity (e.g., "human")
    observation_number : int
        Sequence number of the observation, since beginning of trial run
    timestamp : string
        Timestamp when the data was captured, in ISO 8601 format
    world_time : int
        Current time in ticks
    total_time : int
        Total world time (in ticks) independent of server
    position : tuple of floats
        (x,y,z) position of the entity
    x : float
        x position of the entity (alias of `position[0]`)
    y : float
        y position of the entity (alias of `position[1]`)
    z : float
        z position of the entity (alias of `position[2]`)
    orientation : tuple of floats
        (pitch, yaw) of the entity
    pitch : float
        Pitch of the entity (alias of `orientation[0]`)
    yaw : float
        Yaw of the entity (alias of `orientation[1]`)
    velocity : tuple of floats
        (x,y,z) of the velocity of the entity
    motion_x : float
        x value of the entity's velocity (alias of `velocity[0]`)
    motion_y : float
        y value of the entity's velocity (alias of `velocity[1]`)
    motion_z : float
        z value of the entity's velocity (alias of `velocity[2]`)
    life : float
        Current life value of the entity
    """

    def __init__(self, **kwargs):
        """
        participant_id : string
            Unique identifier of the participant
        playername : string, optional
            Name of the player, if provided.  Defaults to participant_id
        entity_id : string
            ID of the entity
        entity_type : string
            Type of entity whose state is provided
        position : tuple of floats
        x : float
        y : float
        z : float
            (x,y,z) position of the player
        orientation : tuple of floats
        pitch : float
        yaw : float
            (pitch, float) facing of the player
        velocity : tuple of floats
        motion_x : float
        motion_y : float
        motion_z : float
            (x,y,z) velocity of the player
        life : float
            Current life value of the player
        observation_number : int
            Sequence number of the observation
        world_time : int
            Total time (in ticks) of the message
        total_time : int
            Server-independent time (in ticks)
        timestamp : string, ISO8601 format
            Timestamp the state was collected on
        """

        BaseMessage.__init__(self, **kwargs)

        # Get the participant ID and playername.  Note that, depending on the
        # provided keyword arguments, these may be one and the same.
        self._participant_id = kwargs.get('participant_id',
                               kwargs.get('playername', None))
        if self._participant_id is None:
            raise MissingMessageArgumentException(str(self),
                                                  'participant_id') from None

        self._playername = kwargs.get('playername', self._participant_id)


        # Check to see if the necessary remaining arguments have been passed, 
        # raise an exception if one is missing
        for arg_name in ["observation_number", "timestamp", "entity_type",
                         "world_time", "total_time", "life"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._entity_id = kwargs.get("id",
                          kwargs.get("entity_id", None))
        if self._entity_id is None:
            raise MissingMessageArgumentException(str(self), "id") from None

        self._entity_type = kwargs["entity_type"]
        self._observation_number = int(kwargs["observation_number"])
        self._timestamp = ciso8601.parse_datetime(kwargs["timestamp"][:-1])
        self._world_time = int(kwargs["world_time"])
        self._total_time = int(kwargs["total_time"])
        self._life = float(kwargs["life"])

        # Get the position of the player: try `position` first, followed by
        # `x`, `y`, and `z`
        position = kwargs.get('position', None)

        if position is None:
            try:
                position = (kwargs['x'], kwargs['y'], kwargs['z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'position') from None

        # Position needs to be able to be coerced into a tuple of floats. Raise
        # an exception if not possible
        try:
            self._position = tuple([float(x) for x in position][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'position',
                                                    position) from None


        # Get the velocity of the player: try `velocity` first, followed by
        # `motion_x`, `motion_y`, and `motionz`
        velocity = kwargs.get('velocity', None)

        if velocity is None:
            try:
                velocity = (kwargs['motion_x'], 
                            kwargs['motion_y'], 
                            kwargs['motion_z'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'velocity') from None

        # Velocity needs to be able to be coerced into a tuple of floats. Raise
        # an exception if not possible
        try:
            self._velocity = tuple([float(x) for x in velocity][:3])
        except:
            raise MalformedMessageCreationException(str(self), 'velocity',
                                                    velocity) from None


        # Get the orientation of the player: try `orientation` first, followed by
        # `pitch` and `yaw`
        orientation = kwargs.get('orientation', None)

        if orientation is None:
            try:
                orientation = (kwargs['pitch'], kwargs['yaw'])
            except KeyError:
                raise MissingMessageArgumentException(str(self),
                                                      'orientation') from None

        # Orientation needs to be able to be coerced into a tuple of floats.
        # Raise an exception if not possible
        try:
            self._orientation = tuple([float(x) for x in orientation][:2])
        except:
            raise MalformedMessageCreationException(str(self), 'orientation', 
                                                    orientation) from None


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'PlayerState')
        """

        return self.__class__.__name__


    @property
    def participant_id(self):
        """
        Get the unique identifier for the participant.  

        Attempting to set `participant_id` raises an `ImmutableAttributeException`.
        """

        return self._participant_id

    @participant_id.setter
    def participant_id(self, name):
        raise ImmutableAttributeException(str(self), "participant_id")


    @property
    def playername(self):
        """
        Get the name of the entity.  

        Attempting to set `playername` raises an `ImmutableAttributeException`.
        """

        return self._playername

    @playername.setter
    def playername(self, name):
        raise ImmutableAttributeException(str(self), "playername")


    @property
    def name(self):
        """
        Alias of `playername`.  
        """

        return self._playername

    @name.setter
    def name(self, name):
        raise ImmutableAttributeException(str(self), "name")


    @property
    def id(self):
        """
        Alias of  `entity_id`.  
        """

        return self._entity_id

    @id.setter
    def id(self, _id):
        raise ImmutableAttributeException(str(self), "id")


    @property
    def entity_id(self):
        """
        Get the unique id of the entity.  

        Attempting to set `entity_id` raises an `ImmutableAttributeException`.
        """

        return self._entity_id

    @entity_id.setter
    def entity_id(self, _id):
        raise ImmutableAttributeException(str(self), "entity_id")
     

    @property
    def entity_type(self):
        """
        Get the type of the entity.  

        Attempting to set `entity_type` raises an `ImmutableAttributeException`.
        """

        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        raise ImmutableAttributeException(str(self), "entity_type")


    @property
    def observation_number(self):
        """
        Get the sequence number of the observation.  

        Attempting to set `observation_number` raises an `ImmutableAttributeException`.
        """

        return self._observation_number

    @observation_number.setter
    def observation_number(self, observation_number):
        raise ImmutableAttributeException(str(self), "observation_number")


    @property
    def timestamp(self):
        """
        Get the timestamp of when the observation was collected.  

        Attempting to set `timestamp` raises an `ImmutableAttributeException`.
        """

        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        raise ImmutableAttributeException(str(self), "timestamp")


    @property
    def world_time(self):
        """
        Get the world time, in ticks, since the start of the trial.  

        Attempting to set `world_time` raises an `ImmutableAttributeException`.
        """

        return self._world_time

    @world_time.setter
    def world_time(self, world_time):
        raise ImmutableAttributeException(str(self), "world_time")


    @property
    def total_time(self):
        """
        Get the total time passed, independent of the server properties.  

        Attempting to set `total_time` raises an `ImmutableAttributeException`.
        """

        return self._total_time

    @total_time.setter
    def total_time(self, time):
        raise ImmutableAttributeException(str(self), "total_time")


    @property
    def position(self):
        """
        Get the position of the entity.  

        Attempting to set `position` raises an `ImmutableAttributeException`.
        """

        return self._position

    @position.setter
    def position(self, position):
        raise ImmutableAttributeException(str(self), "position")


    @property
    def x(self):
        """
        Alias of  `position[0]`.  
        """

        return self._position[0]

    @x.setter
    def x(self, x):
        raise ImmutableAttributeException(str(self), "x")


    @property
    def y(self):
        """
        Alias of  `position[1]`.  
        """

        return self._position[1]

    @y.setter
    def y(self, y):
        raise ImmutableAttributeException(str(self), "y")


    @property
    def z(self):
        """
        Alias of  `position[2]`.  
        """

        return self._position[2]

    @z.setter
    def z(self, z):
        raise ImmutableAttributeException(str(self), "z")        


    @property
    def orientation(self):
        """
        Get the orientation of the entity.  

        Attempting to set `orientation` raises an `ImmutableAttributeException`.
        """

        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        raise ImmutableAttributeException(str(self), "orientation")


    @property
    def pitch(self):
        """
        Alias of  `orientation[0]`.  
        """

        return self._orientation[0]

    @pitch.setter
    def pitch(self, angle):
        raise ImmutableAttributeException(str(self), "pitch")


    @property
    def yaw(self):
        """
        Alias of  `orientation[1]`.  
        """

        return self._orientation[1]

    @yaw.setter
    def yaw(self, angle):
        raise ImmutableAttributeException(str(self), "yaw")


    @property
    def velocity(self):
        """
        Get the velocity of the entity.  

        Attempting to set `velocity` raises an `ImmutableAttributeException`.
        """

        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        raise ImmutableAttributeException(str(self), "velocity")


    @property
    def motion_x(self):
        """
        Alias of  `velocity[0]`.  
        """

        return self._velocity[0]

    @motion_x.setter
    def motion_x(self, velocity):
        raise ImmutableAttributeException(str(self), "motion_x")


    @property
    def motion_y(self):
        """
        Alias of  `velocity[1]`.  
        """

        return self._velocity[1]

    @motion_y.setter
    def motion_y(self, velcoity):
        raise ImmutableAttributeException(str(self), "motion_y")


    @property
    def motion_z(self):
        """
        Alias of  `velocity[2]`.  
        """

        return self._velocity[2]

    @motion_z.setter
    def motion_z(self, velocity):
        raise ImmutableAttributeException(str(self), "motion_z")


    @property
    def life(self):
        """
        Get the life of the entity.  

        Attempting to set `life` raises an `ImmutableAttributeException`.
        """

        return self._life

    @life.setter
    def life(self, life):
        raise ImmutableAttributeException(str(self), "life")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the PlayerState.
        """

        jsonDict = BaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["observation_number"] = self.observation_number
        jsonDict["data"]["timestamp"] = str(self.timestamp) + 'Z'
        jsonDict["data"]["world_time"] = self.world_time
        jsonDict["data"]["total_time"] = self.total_time
        jsonDict["data"]["entity_type"] = self.entity_type
        jsonDict["data"]["yaw"] = self.yaw
        jsonDict["data"]["x"] = self.x
        jsonDict["data"]["y"] = self.y
        jsonDict["data"]["z"] = self.z
        jsonDict["data"]["pitch"] = self.pitch
        jsonDict["data"]["id"] = self.id
        jsonDict["data"]["motion_x"] = self.motion_x
        jsonDict["data"]["motion_y"] = self.motion_y
        jsonDict["data"]["motion_z"] = self.motion_z
        jsonDict["data"]["life"] = self.life
        jsonDict["data"]["playername"] = self.playername

        return jsonDict


    def toJson(self):
        """
        Generates a JSON representation of the message.  Message information is
        contained in a JSON object under the key "data".  Additional named
        headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            PlayerState message.
        """

        return json.dumps(self.toDict())
