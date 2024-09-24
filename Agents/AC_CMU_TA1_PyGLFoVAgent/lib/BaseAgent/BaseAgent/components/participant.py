# -*- coding: utf-8 -*-
"""
.. module:: participant
   :platform: Linux, Windows, OSX
   :synopsis: Definition of a lightweight participant class for storing various
              participant information

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a participant class and collection for storing participant
information.  The class is a simple lightweight object to store participant
information within a single namespace, while the collection allows for 
accessing participants by any identifier for the participant.
"""

from MinecraftBridge.utils import Loggable



class Participant:
    """
    Lightweight class for storing information related to a participant.

    Attributes
    ----------
    participant_id : string
        Unique ID of the participant
    id : string
        Alias for `participant_id`
    playername : string
        Minecraft playername of the participant
    callsign : string
        Callsign of the participant
    role : string
        The participant's role
    """

    def __init__(self, participant_id, playername, callsign):

        self._participant_id = participant_id
        self._playername = playername
        self._callsign = callsign
        self._role = None


    def __str__(self):
        """
        String representation of the participant
        """

        return "%s: \n   participant_id: %s\n   playername: %s\n   callsign: %s" % (self.__class__.__name__, self.participant_id, self.playername, self.callsign)


    @property
    def participant_id(self):
        return self._participant_id

    @participant_id.setter
    def participant_id(self, _):
        pass

    @property
    def id(self):
        return self._participant_id

    @id.setter
    def id(self, _):
        pass

    @property
    def playername(self):
        return self._playername

    @playername.setter
    def playername(self, _):
        pass

    @property
    def callsign(self):
        return self._callsign

    @callsign.setter
    def callsign(self, _):
        pass

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        # Can only be set once
        if self._role is None:
            self._role = value



class ParticipantCollection(Loggable):
    """
    Basic class that stores a set of Participant instances, and provides basic
    functionality for managing the collection.

    Methods
    -------
    add(participant)
        Adds a participant to the set
    remove(participant)
        Removes a participant from the set
    clear()
        Removes all participants from the set
    __getitem__(key)
        Returns an instance of Participant.  Parcipants can be accessed by
        the instance of the participant (redundant), or the participant_id, 
        playername, or callsign of the participant.

    Usage
    -----
    An instance of ParticipantCollection is initialized without any parameters.
    Once created, instances of participants can be added to the collection with
    the `add` method::

        >>> participants = ParticipantCollection()
        >>> participant1 = Participant("p1", "player1", "red")
        >>> participant2 = Participant("p2", "player2", "blue")
        >>> participants.add(participant1)
        >>> participants.add(participant2)

    Any instance of Participant will be stored only once, and `participant_id`
    is assumed to be unique for all Participants in the collection.  Attempting
    to add a Participant already contained in a collection will be ignored::

        >>> participants.add(participant1)
        >>> participants.add(participant1)

    trying to add a Participant with the same `participant_id` as one in the
    collection will result in an Exception being raised::

        >>> participants = ParticipantCollection()
        >>> participant1 = Participant("p1", "player1", "red")
        >>> participant3 = Participant("p1", "player3", "green")
        >>> participants.add(participant1)
        >>> participants.add(participant3)
    """

    def __init__(self):
        """
        Arguments
        ---------
        minecraft_bridge : MinecraftBridge.bridge
            Callback-decorated Minecraft bridge instance
        """

        self._participants = set()

###        # Register the ParticipantCollection to populate itself from Trial messages
###        if minecraft_bridge is not None:
###            from ..messages import Trial
###            minecraft_bridge.register_callback(Trial, self.__onTrial, priority=-1)


    def __str__(self):
        """
        Return a string representation of the object.
        """

        return self.__class__.__name__


    def __len__(self):
        """
        Returns the number of participants in the collection.
        """

        return len(self._participants)


    def __iter__(self):
        """
        Returns an iterator over the participants in the colleciton.
        """

        return self._participants.__iter__()


    def __contains__(self, key):
        """
        Check to see if a participant is in the collection.  Checks for 
        membership in the following order:

        1.  key refers to a Participant instance
        2.  key refers to the participant_id
        3.  key refers to the playername
        4.  key refers to the callsign
        5.  key refers to the role

        Returns
        -------
        boolean
            True if the key matches one of the Participants in the container or
            an attribute of one of the Participants, False otherwise.
        """

        # 1.  Check if the key refers to an actual Participant
        if key in self._participants:
            return True

        # 2.  Check by participant_id
        for participant in self._participants:
            if participant.participant_id == key:
                return True

        # 3.  Check for playername
        for participant in self._participants:
            if participant.playername == key:
                return True

        # 4.  Check for callsign
        for participant in self._participants:
            if participant.callsign == key:
                return True

        # 5.  Check for role
        if key is not None:
            for participant in self._participants:
                if participant.role == key:
                    return True

        # Not found
        return False
        

    def add(self, participant):
        """
        Add a participant to the collection.  Checks to ensure that the provided
        participant is an instance of Participant.  If the participant already
        is in the collection, it is not added a second time.

        Arguments
        ---------
        participant : Participant
            Participant to add to the set.
        """

        # Raise a warning if trying to add a non-Participant
        if not isinstance(participant, Participant):
            self.logger.warning("%s: Attempting to add non-Participant instance: %s.  Ignoring", self, participant)
            return

        # Check to see if the participant already exists, and do nothing if so
        if participant in self._participants:
            self.logger.info("%s: Attempting to add already existing Participant: %s.  Ignoring", self, participant)
            return

        # Check to see if the participant_id is already in the collection, and
        # raise an warning message if so
        for _participant in self._participants:
            if _participant.participant_id == participant.participant_id:
                self.logger.warning("%s: Attempting to add Participant with ID existing in collection: %s.  Ignoring", self, participant)               
                return
        
        # Chec to see if the participant has an valid callsign. E.g. observers will not have a callsign
        # and should not be part of the participant collection.
        if participant.callsign.lower() not in ["red", "green", "blue"]:
            self.logger.warning("%s: Attempting to add Participant with invalid call sign '%s' to collection: %s.  Ignoring", self, participant.callsign, participant) 
            return

        self._participants.add(participant)


    def remove(self, participant):
        """
        Removes a participant from the collection.  If the participant is not
        in the collection, then nothing is removed.

        Arguments
        ---------
        participant : Participant
            Participant to remove from the set
        """

        if not participant in self._participants:
            self.logger.warning(f"{self}: Attempting to remove a participant not in the collection: {participant}")

        self._participants.remove(participant)


    def clear(self):
        """
        Remove all participants from the collection
        """

        self._participants.clear()


    def copy(self):
        """
        Creates a shallow copy of the participant collection.
        """

        new_collection = ParticipantCollection()

        # Copy over the Participant objects (pointers) into the new collection
        for participant in self:
            new_collection.add(participant)

        return new_collection


    def __getitem__(self, key):
        """
        Attempts to get a participant from the collection based on one of the
        participant attributes.  Attributes are checked in the following order:

            1.  Instance (i.e., Participant object ID)
            2.  participant_id
            3.  playername
            4.  callsign
            5.  role

        If no participant is found, returns `None`.  If multiple matches to the
        key are found, returns the first match.  Typical use case will be to 
        find by `participant_id`, which is forced to be unique in the 
        collection.

        Arguments
        ---------
        key : Participant or string
            key to access the participant from the collection

        Returns
        -------
        Participant or None
        """

        # 1.  Return the key if it is an instance of Participant already in the 
        #     collection
        if key in self._participants:
            return key

        # 2.  Check by participant_id
        for participant in self._participants:
            if participant.participant_id == key:
                return participant

        # 3.  Check for playername
        for participant in self._participants:
            if participant.playername == key:
                return participant

        # 4.  Check for callsign
        for participant in self._participants:
            if participant.callsign == key:
                return participant

        # 5.  Check for role
        if key is not None:
            for participant in self._participants:
                if participant.role == key:
                    return participant

        # Participant wasn't found, return None
        self.logger.warning("%s: Participant not found by key: %s", self, key)
        return None

