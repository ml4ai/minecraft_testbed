"""
fovWorker.py

Class definition of worker threads for performing FoV calculations

Author: Dana Hughes
email: danahugh@andrew.cmu.edu
"""

import enum

import time
import threading

import pygl_fov

import endpoints

from dispatchers import Queue
from dispatchers import LatestPlayerStateDispatcher
from dispatchers import IgnoreMultiplePlayerStateDispatcher

from MinecraftBridge.messages import (
    PlayerState, 
    DoorEvent, 
    LeverEvent, 
    MissionStateEvent, 
    VictimList, 
    BlockageList, 
    VictimsExpired, 
    TriageEvent, 
    Trial, 
    MarkerDestroyedEvent, 
    MarkerPlacedEvent, 
    MarkerRemovedEvent, 
    PerturbationRubbleLocations,
    RubbleCollapse,
    RubbleDestroyedEvent, 
    RubblePlacedEvent, 
    ThreatSignList, 
    VictimNoLongerSafe, 
    VictimPickedUp, 
    VictimPlaced, 
    FreezeBlockList, 
    FoV_MapMetadata, 
    FoVProfile,
    BusHeader, 
    MessageHeader
)
from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype
from MinecraftBridge.utils import Loggable

import MinecraftElements

from participant import Participant

import numpy as np


__author__ = 'danahugh'


class FoVWorker(threading.Thread,Loggable):
    """
    A worker for performing FoV calculations on a separate thread for a single
    trial.

    Attributes
    ----------
    worker_key : tuple of strings
        Key associated with this worker, consisting of
        (experiment_id, trial_id, replay_id)
    state : FoVWorker.State
        State that the worker is currently in
    """


    class State(enum.Enum):
        """
        Indicates the state of an FoVWorker thread.  States are indicated as::

        * INITIALIZING - Worker is currently initializing, and is not ready
                         to be run
        * READY -        Worker is ready to be run, thread has yet to be started
        * RUNNING -      Worker thread is running
        * STOPPING -     Worker is not accepting messages, and is processing
                         remaining messages
        * STOPPED -      Worker has completed execution, and is ready to be 
                         joined
        """

        INITIALIZING = "INITIALIZING"
        READY = "READY"
        RUNNING = "RUNNING"
        STOPPING = "STOPPING"
        STOPPED = "STOPPED"


    def __init__(self, parent, config, key=None, map_path=None):
        """
        Create a new FoVWorker.

        Arguments
        ---------
        parent : PyGLFoVAgent
            Agent that created and is managing this worker
        key : tuple 
            Key this worker is referred to by
        map_path : stirng
            Path to JSON file containing map block information
        """

        # Initialize thread-related aspect
        threading.Thread.__init__(self)

        # Create the FoV worker's name
        self.__string_name = '[FoVWorker]'

        self.config = config
        self.parent = parent
        self.key = key
        self.map_path = map_path

        self.state = FoVWorker.State.INITIALIZING


        # Message Queue and related locks for handling the fact that messages
        # may be pushed to the Queue from one thread while consumed by another
        self.message_lock = threading.Lock()
        self.feeder_lock = threading.Lock()


        # Determine which message dispatcher is needed
        # NOTE: For submission to TA3, hard coded to drop stale player state
        #       messages
###        self.messageQueue = Queue()
###        self.messageQueue = LatestPlayerStateDispatcher()
        self.messageQueue = IgnoreMultiplePlayerStateDispatcher()

        # pygl related items:
        #   world contains the set of block feeders containing block instances
        #   player_block_store contains a dummy block for each participant
        #   player_vertex_store contains a composite vertex store for rendering players
        #   vertex_store contains a composite vertex store for rendering
        #   perspective is the viewport
        #   fov is the FoV wrapper
        # NOTE: OpenGL components need to be created in the execution thread 
        #       where it will be used in order to ensure context is available
        self.world = None
        self.world_vertex_store = None
        self.player_vertex_store = None
        self.perspective = None
        self.fov = None
        self.color_map = None

        # Dictionary of hidden blocks -- hidden blocks are moved to a location
        # technically outside of Minecraft (with a negative y value).  The 
        # dictionary maps block instances to original locations.
        self.hidden_location = (0.0, -10000.0, 0.0)
        self.hidden_blocks = {}

        # Dictionary of marker block locations, mapping location to the 
        # original block stored
        self.marker_block_replacements = {}

        # Participant information -- a pair of dictionaries mapping player 
        # names to Participant instances and lists of endpoints
        self.participants = {}
        self.endpoints = {}

        # Endpoint factories will be used to create endpoints as participants
        # are generated
        self.endpoint_factories = []
        self.buildEndpointFactories()

        # Cache for victim and blockage list messages.  Victim and blockage list
        # messages will be stored until the map is created
        self.victimAndBlockageMessageCache = []

        # Everything is initialized, and the worker is ready to be started.
        self.state = FoVWorker.State.READY

        # Lookup map for how to process each message type
        self.messageProcessors = { PlayerState:          self.processPlayerState,
                                   LeverEvent:           self.processLeverEvent,
                                   DoorEvent:            self.processDoorEvent,
                                   MissionStateEvent:    self.processMissionStateEvent,
                                   VictimList:           self.processVictimList,
                                   BlockageList:         self.processBlockageList,
                                   VictimsExpired:       self.processVictimsExpired,
                                   TriageEvent:          self.processTriageEvent,
                                   MarkerDestroyedEvent: self.processMarkerDestroyedEvent,
                                   MarkerPlacedEvent:    self.processMarkerPlacedEvent,
                                   MarkerRemovedEvent:   self.processMarkerRemovedEvent,
                                   PerturbationRubbleLocations: self.processBlockageList,
                                   RubbleCollapse:       self.processRubbleCollapseEvent,
                                   RubbleDestroyedEvent: self.processRubbleDestroyedEvent,
                                   RubblePlacedEvent:    self.processRubblePlacedEvent,
                                   VictimNoLongerSafe:   self.processVictimNoLongerSafe,
                                   VictimPickedUp:       self.processVictimPickedUp,
                                   VictimPlaced:         self.processVictimPlaced,
                                   FreezeBlockList:      self.processFreezeBlockList,
                                   ThreatSignList:       self.processThreatSignList
                                 }

        self.process_player_state_times = []




    def __str__(self):
        """
        String representation of the FoV worker)
        """

        return self.__string_name




    def __hide(self, block):
        """
        Hide the block by setting its y value to a negative number.  The block
        and its original location will be stored, so that it can later be
        unhidden

        Args:
            block - instance of Block to hide
        """

        self.logger.debug("%s:  Hiding block: %s", self, block)

        # Does the feeder actually contain this block?
        if not block.id in self.world:
            self.logger.warning("%s:    Attempting to hide block not in feeder: %s.  Ignoring.", self, block)
            return

        if block in self.hidden_blocks.keys():
            self.logger.warning("%s:    Block already hidden, ignoring.", self)

        # Store a tuple with the block and its current location
        self.hidden_blocks[block] = block.location

        # Remove the block from this feeder
        self.world.removeBlock(block.id)

        # Change the location of the block so it's y value is the negative of
        # the current y value (which will be outside of the Minecraft universe)
        block.location = self.hidden_location
    



    def __unhide(self, block, new_location=None):
        """
        Restore a hidden block to its original position.

        Args:
            block - instance of Block to unhide
        """

        self.logger.debug("%s:  Unhiding block: %s", self, block)

        # Does the feeder actually contain this block?
        if not block in self.hidden_blocks.keys():
            self.logger.warning("%s:    Attempting to unhide block not in hidden feeder: %s.  Ignoring.", self, block)
            return

        if new_location is None:
            block.location = self.hidden_blocks[block]
        else:
            block.location = new_location

        # Add the block back to the feeder
        self.world.add(block)

        del self.hidden_blocks[block]



    def buildEndpointFactories(self):
        """
        Build and add the factories defined by the config file, and add them to
        the worker.
        """

        # TODO: Change this to a DI-type framework, by dynamically importing
        #       the classes from the config file

        for EndpointClass, arguments in self.parent.config["endpoints"].items():

            self.logger.info("%s:  Creating %s Factory", self, EndpointClass)

            # MatplotVisualizer
            if EndpointClass == "MatplotVisualizer":
                colormap_path = arguments.get("colormap_path", None)
                factory = endpoints.factories[EndpointClass](self, 
                                                             colormap_path=colormap_path, 
                                                             fov_agent=self.parent)#.publisher)
                self.endpoint_factories.append(factory)


            if EndpointClass == "BlockSummaryMessageEndpoint":
                blocks_to_summarize = arguments.get("blocks_to_summarize", None)
                timestamp_delay = arguments.get("timestamp_delay", -1)
                scaling_factor = arguments.get("scaling_factor", 1)
                factory = endpoints.factories[EndpointClass](self,
                                                             blocks_to_summarize=blocks_to_summarize,
                                                             fov_agent=self.parent,#.publisher,
                                                             timestamp_delay=timestamp_delay,
                                                             scaling_factor=scaling_factor)
                self.endpoint_factories.append(factory)


            if EndpointClass == "BlockLocationListMessageEndpoint":
                timestamp_delay = arguments.get("timestamp_delay", -1)
                factory = endpoints.factories[EndpointClass](self,
                                                             fov_agent=self.parent,#.publisher,
                                                             timestamp_delay = timestamp_delay)
                self.endpoint_factories.append(factory)




    def addEndpointFactory(self, factory):
        """
        Add a factory to generate endpoints as particpants are generated
        """

        self.logger.info("%s:  Adding endpoint factory: %s", self, factory)

        self.endpoint_factories.append(factory)




    def initializeFoV(self):
        """
        Initialize all the FoV components.  This needs to be called after the
        thread has started.
        """

        self.logger.info("%s:  Creating pygl_fov objects", self)

        # Needed components for the FoV instance: a common color map instance
        # for converting block id to color and back, a composite block feeder
        # for storing chunks of blocks, and a composite vertex store for
        # storing corresponding vertices of each block.
        self.logger.info("%s:      Creating Color Mapper", self)
        self.color_map = pygl_fov.BlockColorMapper()
        self.logger.info("%s:      Creating World Block Feeder", self)        
        self.world = pygl_fov.BlockFeeder(name="World Block Feeder")
        self.logger.info("%s:      Creating World Vertex Store", self)        
        self.world_vertex_store = pygl_fov.CompositeVertexStore(name="World Vertex Store")

        # Create the vertex store for players, and add to the world stores
        self.logger.info("%s:      Creating World Vertex Store", self)
        self.player_vertex_store = pygl_fov.CompositeVertexStore(name="Participant Vertex Store")
        self.world_vertex_store.addStore(self.player_vertex_store)


        # Create an instance of Perspective, which will be the OpenGL context
        # rendered to.
        self.logger.info("%s:      Creating Perspective", self)
        self.perspective = pygl_fov.Perspective(position=(0,0,0),
                                                orientation=(0,0,0),
                                                window_size=(self.config["window_size"]["width"],
                                                             self.config["window_size"]["height"]))

        # Finally, create the FoV instance
        self.logger.info("%s:      Creating FoV", self)
        self.fov = pygl_fov.FOV(self.perspective, self.world_vertex_store, False, color_map=self.color_map)

        backend_info = self.perspective.context.getBackendInfo()

        self.logger.info("%s:", self)
        self.logger.info("%s:  OpenGL Context and Content Created", self)
        self.logger.info("%s:    Backend:      %s", self, backend_info['backend'])
        self.logger.info("%s:    Vendor:       %s", self, backend_info['vendor'])
        self.logger.info("%s:    Renderer:     %s", self, backend_info['renderer'])
        self.logger.info("%s:    Version:      %s", self, backend_info['version'])
        self.logger.info("%s:    SL Version:   %s", self, backend_info['sl_version'])
        self.logger.info("%s:", self)




    def addBlocksToFoV(self, blocks, vertex_store=None):
        """
        Construct a vertex store for the provided feeder, and add the feeder
        and store to the existing composites used by the FoV instance
        """

        self.logger.debug("%s:  Adding blocks to FoV", self)

        # Make sure that the world and vertex_store exist before attempting to
        # add to them
        if self.world is None:
            self.logger.error("%s:    Attempting to add to non-existant world.  (Was initializeFoV called?)", self)
            return
        if self.world_vertex_store is None:
            self.logger.error("%s:    Attempting to add to non-existant vertex store.  (Was initializeFoV called?)", self)
            return

        # Create a vertex store instance for the provided block_feeder, if one
        # is not provided
        if vertex_store is None:
            self.logger.debug("%s:    Creating Vertex Store", self)
            vertex_store = pygl_fov.StaticVboStore(blocks)

        # Add the block_feeder to the world, and the vertex_store to the 
        # world_vertex_store
        for block in blocks:
            self.logger.debug("%s:      Adding Block %s", self, block)
            self.world.add(block)
        self.world_vertex_store.addStore(vertex_store)



    def createParticipant(self, participant_id, **kwargs):
        """
        Create a participant and associated endpoints, and add to the store
        of participants
        """

        # Check if the participant already exists in the store, and ignore if
        # so.
        if participant_id in self.participants.keys():
            self.logger.warning("%s:  Attempted to add participant with existing name: %s", self, participant_id)
            return


        position = kwargs.get("position", (0,0,0))
        orientation = kwargs.get("orientation", (0,0,0))
        window_size = kwargs.get("window_size", (self.config["window_size"]["width"],
                                                 self.config["window_size"]["height"]))

        participant = Participant(participant_id, position=position, 
                                                  orientation=orientation, 
                                                  window_size=window_size)

        self.world.add(participant.block)
        self.player_vertex_store.addStore(participant.vertices)

        self.logger.info("%s:  Participant Block ID: %d", self, participant.block.id)
        self.logger.info("%s:  Participant Block Color: %s", self, str(participant.vertices.color))
       

        # Create a list of endpoints for the participant using the list of
        # endpoint factories
        endpoints = [factory(participant) for factory in self.endpoint_factories]


        self.participants[participant_id] = participant
        self.endpoints[participant_id] = endpoints

        # Provide information to the logger
        self.logger.info("%s:  Added new participant to the store: %s", self, self.participants[participant_id])
        self.logger.info("%s:    Participant Name: %s", self, self.participants[participant_id].name)
        self.logger.info("%s:    Participant Position: %s", self, str(self.participants[participant_id].position))
        self.logger.info("%s:    Participant Orientation: %s", self, str(self.participants[participant_id].orientation))
        self.logger.info("%s:    Participant Window Size: %s", self, str(self.participants[participant_id].window_size))
        self.logger.info("%s:    Endpoints:", self)
        for endpoint in self.endpoints[participant_id]:
            self.logger.info("%s:      %s", self, endpoint)


    ###
    ### HELPERS
    ###

    def __drop_rubble(self, hole_location):
        """
        Function to drop any rubble immediately above the given location

        Arguments
        ---------
        hole_location : triple
            (x,y,z) location to drop rubble into
        """

        ### TODO: MAKE RECURSIVE

        # Move any rubble (or other movable blocks) down due to gravity
        # Check the spot above the recently removed rubble.  If there's a 
        # rubble block there, move that block down and repeat
        dropping_rubble = True
        
        while dropping_rubble:
            # Check immediately above the current rubble location
            check_location = (hole_location[0], hole_location[1]+1, hole_location[2])

            # Check if there's a block there
            if self.world.containsBlockAt(check_location):
                # Check if it's a gravel block
                check_block = self.world.getBlockAt(check_location)
                if check_block.block_type == MinecraftElements.Block.gravel:

                    # Move the block down
                    self.logger.debug("%s:      Moving Rubble at %s down to %s", self, str(check_block.location), str(hole_location))

                    self.world.removeBlock(check_block.id)
                    check_block.location = hole_location
                    self.world.add(check_block)

                    # And check the next block up
                    hole_location = check_location

                else:
                    # Not a rubble block, nothing further to check
                    dropping_rubble = False

            else:
                # No block found in the check spot
                dropping_rubble = False



    ###
    ### PROCESSING SPECIFIC MESSAGES ###
    ###

    def processDoorEvent(self, message):
        """
        Callback method for processing Door Events

        Arguments
        ---------
        message : MinecraftBridge.messages.DoorEvent
            Received DoorEvent message
        """

        self.logger.debug("%s:  Processing %s message", self, message)


        with self.feeder_lock:
            location = message.position

            # Get the door block at the location, 
            door_block = self.world.getBlockAt(location)

            if door_block == None:
                self.logger.warning("%s:  Door does not exist at location %s in DoorEvent message", self, str(location))
                return

            door_block.open = message.opened

            # Do the same for the other half of the door
            if door_block.half == MinecraftElements.Half.upper:
                second_location = (location[0], location[1]-1, location[2])
            else:
                second_location = (location[0], location[1]+1, location[2])

            second_door_block = self.world.getBlockAt(second_location)

            second_door_block.open = message.opened


    def processLeverEvent(self, message):
        """
        Callback method for processing Lever Events

        Arguments
        ---------
        message : MinecraftBridge.messages.LeverEvent
            Received LeverEvent message
        """

        self.logger.debug("%s:  Processing %s message", self, message)



    def processMissionStateEvent(self, message):
        """
        Method for processing Lever Events

        Args:
            message - a lever event
        """

        pass


    def processPlayerState(self, message):
        """
        Method for processing Player State

        Args:
            message - a player state
        """

        self.logger.debug("%s:  Processing %s message", self, message)
        
        # The participant may not have been created, so ignore the message is not
        if not message.participant_id in self.participants:
            self.logger.warning("%s:  Participant not in participants: %s", self, message.participant_id)
            return

        start_time = time.time()

        with self.feeder_lock:
            # Grab the relevant participant
            participant = self.participants[message.participant_id]

            participant.set_pose(message.position, message.orientation + (0,))
            self.perspective.set_pose(message.position, message.orientation + (0,))

            # Create the pixel to block ID map -- do not render vertices of the
            # participant's avatar
            pixelMap = self.fov.calculatePixelToBlockIdMap(ignore=[participant.vertices])

            # Send the calcualted pixel map to all of the participant's
            # endpoints
            for endpoint in self.endpoints[message.participant_id]:
                endpoint(pixelMap, player_state_message=message)

        end_time = time.time()

        self.process_player_state_times.append(end_time - start_time)


    def processVictimList(self, message):
        """
        Create block instances of the victims in the message and add to the 
        world
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Add the victims in the list to the block feeder
        with self.feeder_lock:
            self.logger.debug("%s:      Number of blocks prior to processing: %d", self, len(self.world))

            # Start a new block feeder to store victim blocks in
            victim_blocks = [] #pygl_fov.BlockFeeder(name="Victims")

            for victim in message.victims:
                self.logger.debug("%s:    Creating Victim Block of type %s at location %s", self, victim.block_type, str(victim.location))

                # Hide any block this victim is re-occupying
                if self.world.containsBlockAt(victim.location):
                    self.__hide(self.world.getBlockAt(victim.location))

                block = pygl_fov.Block(victim.location, block_type=victim.block_type,
                                       victim_id = victim.unique_id)
                victim_blocks.append(block)

            # Add the victim feeder to the world, also creating a VBO store
            self.addBlocksToFoV(victim_blocks)

            self.logger.debug("%s:      Number of blocks after processing: %d", self, len(self.world))


    def processBlockageList(self, message):
        """
        Create block instances of the blockages and add to the world
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        
        # Add the blockages to the block feeder
        with self.feeder_lock:
            self.logger.debug("%s:      Number of blocks prior to processing: %d", self, len(self.world))

            # Start a new block feeder to store blockages in
            blockage_blocks = [] # = pygl_fov.BlockFeeder(name="Blockages")

            for blockage in message.blockages:
                block = pygl_fov.Block(blockage.location, 
                                       block_type=blockage.block_type)

                self.logger.debug("%s:  Blockage: %s", self, block)

                # If the 'blockage' is air, remove the block at that location
                # from the feeder
                if block.block_type == MinecraftElements.Block.air:

                    # Hide the block -- this is to avoid the need to
                    # recalculate the VBO, as would need to be done if the block
                    # was removed.
                    self.__hide(self.world.getBlockAt(block.location))

                    # If the configuration is such to render a wireframe for
                    # these openings, then set the block_type to a
                    # ProxyBlock.opening and add to the feeder
                    if self.config["include_openings"]:
                        block.block_type = MinecraftElements.Block.perturbation_opening

                        self.logger.debug("%s:        Adding opening block at location %s", self, block.location)
                        blockage_blocks.append(block)                       

                else:
                    self.logger.debug("%s:        Adding block of type %s at location %s", self, block.block_type, block.location)

                    # See if we need to remove a block first
                    if self.world.containsBlockAt(block.location):
                        removed_block = self.world.getBlockAt(block.location)

                        # Hide the block to remove
                        self.__hide(removed_block)

                    blockage_blocks.append(block)

            # Add the blockage feeder to the world, also creating a vertex
            # store in the process
            self.addBlocksToFoV(blockage_blocks)

            self.logger.debug("%s:      Number of blocks after processing: %d", self, len(self.world))       


    def processFreezeBlockList(self, message):
        """
        Create block instances of the freeze blocks and add to the world
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Add the freeze blocks to the feeder
        with self.feeder_lock:
            self.logger.debug("%s:    Number of blocks prior to processing: %d", self, len(self.world))

            # Start a new list of blocks for freeze block lists
            freeze_blocks = []

            for freezeblock in message.freezeblocks:

                # Create the block
                block = pygl_fov.Block(freezeblock.location,
                                       block_type=freezeblock.block_type)

                self.logger.debug("%s      Adding Freeze Block %s at %s", self, block, str(block.location))

                # Check if there's a block to hide
                if self.world.containsBlockAt(block.location):
                    block_to_remove = self.world.getBlockAt(block.location)
                    self.logger.debug("%s:        Removing existing Block %s at %s", self, block_to_remove, str(block.location))
                    self.__hide(block_to_remove)

                freeze_blocks.append(block)


            # Add the freeze blocks to the world, creating a vertex store in
            # the process
            self.addBlocksToFoV(freeze_blocks)

            self.logger.debug("%s:      Number of Blocks after processing: %d", self, len(self.world))


    def processThreatSignList(self, message):
        """
        Create block instances of threat signs and add to the world
        """


        self.logger.debug("%s:  Processing %s message", self, message)

        # Add the freeze blocks to the feeder
        with self.feeder_lock:
            self.logger.debug("%s:    Number of blocks prior to processing: %d", self, len(self.world))

            # Start a new list of blocks for freeze block lists
            signs = []

            for sign in message.threat_signs:

                # Create the block
                block = pygl_fov.Block(sign.location,
                                       block_type=sign.block_type)

                self.logger.debug("%s      Adding Threat Sign %s at %s", self, block, str(block.location))

                # Check if there's a block to hide
                if self.world.containsBlockAt(block.location):
                    block_to_remove = self.world.getBlockAt(block.location)
                    self.logger.debug("%s:        Removing existing Block %s at %s", self, block_to_remove, str(block.location))
                    self.__hide(block_to_remove)

                signs.append(block)


            # Add the freeze blocks to the world, creating a vertex store in
            # the process
            self.addBlocksToFoV(signs)

            self.logger.info("%s:      Number of Blocks after processing: %d", self, len(self.world))


    def processTriageEvent(self, message):
        """
        Change the block type at the provided location to "victim_saved" to
        indicate the victim was triaged
        """

        self.logger.debug("%s:  Processing %s message", self, message)


        with self.feeder_lock:

            # Double check -- event type should be TriageState.SUCCESS
            if message.triage_state != TriageEvent.TriageState.SUCCESSFUL:
                self.logger.debug("%s:    Received non-success triage event message", self)
                return

            # Get the block at the location
            victim_block = self.world.getBlockAt(message.victim_location)

            if victim_block is not None:
                # Make sure that the block is indeed a victim type
                if victim_block.block_type in [MinecraftElements.Block.block_victim_1, 
                                               MinecraftElements.Block.block_victim_2,
                                               MinecraftElements.Block.block_victim_1b,
                                               MinecraftElements.Block.block_victim_proximity]:
                    # Convert the block to a saved victim
                    victim_block.block_type = MinecraftElements.Block.block_victim_saved
                else:
                    self.logger.warning("%s:    Received %s message; block type %s at location %s not an untriaged victim type.", self, message, victim_block.block_type, victim_block.location)
            else:
                self.logger.warning("%s:    Received %s message; no block at location %s.", self, message, message.victim_location)


    def processVictimsExpired(self, message):
        """
        Change all "block_victim_2" blocks to "block_victim_expired"
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        with self.feeder_lock:
            # Iterate through the blocks in the feeder, and change any of 
            # type "block_victim_2"
            for block in self.world:
                if block.block_type == MinecraftElements.Block.block_victim_2:
                    block.block_type = MinecraftElements.Block.block_victim_expired


    def processMarkerDestroyedEvent(self, message):
        """
        Remove the marker block from the set of blocks
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Location of the marker to be removed
        location = message.location

        # Check to see if a block exists there
        if not self.world.containsBlockAt(location):
            self.logger.error("%s:    Attempting to remove non-existant marker block at %s", self, str(location))
            return

        marker_block = self.world.getBlockAt(location)

        # Check to see if the block is indeed a marker block
        if marker_block.block_type is not MinecraftElements.Block.marker_block:
            self.logger.error("%s:    Attempting to remove non-marker block %s: expecting marker block", self, marker_block)

        # Hide the block
        self.__hide(marker_block)

        # Restore whatever prior block was there
        if location in self.marker_block_replacements.keys():
            self.__unhide(self.marker_block_replacements[location])
            del self.marker_block_replacements[location]

        # Drop any rubble
        self.__drop_rubble(location)            


    def processMarkerPlacedEvent(self, message):
        """
        Add a marker block to the set of blocks
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Get the location and type of marker placed
        location = message.location
        marker_type = message.marker_type
        owner = message.participant_id

        # Create the marker block
        marker_block = pygl_fov.Block(location, 
                                      MinecraftElements.Block.marker_block,
                                      marker_type = marker_type,
                                      playername = owner)

        # Check to see if a block exists where the marker is being placed.  If
        # it's a marker block, no need to store it for future retrieval.
        if self.world.containsBlockAt(location):
            self.logger.debug("%s:    Placing marker block %s at occupied location: %s", self, marker_block, str(location))
            if self.world.getBlockAt(location).block_type is not MinecraftElements.Block.marker_block:
                self.marker_block_replacements[location] = self.world.getBlockAt(location)
            self.__hide(self.world.getBlockAt(location))


        # Add the block to the world.  Vertices for the block will be created
        # automatically and loaded into OpenGL
        self.addBlocksToFoV([marker_block])


    def processMarkerRemovedEvent(self, message):
        """
        Remove the marker block from the set of blocks
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Location of the marker to be removed
        location = message.location

        # Check to see if a block exists there
        if not self.world.containsBlockAt(location):
            self.logger.error("%s:  Attempting to remove non-existant marker block at %s", self, str(location))
            return

        marker_block = self.world.getBlockAt(location)

        # Check to see if the block is indeed a marker block
        if marker_block.block_type is not MinecraftElements.Block.marker_block:
            self.logger.error("%s:  Attempting to remove non-marker block %s: expecting marker block", self, marker_block)

        # Hide the block
        self.__hide(marker_block)

        # Restore whatever prior block was there
        if location in self.marker_block_replacements.keys():
            self.__unhide(self.marker_block_replacements[location])
            del self.marker_block_replacements[location]

        # Drop any rubble
        self.__drop_rubble(location)



    def processRubbleCollapseEvent(self, message):
        """
        Add rubble blocks defined in the given message
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Sort the x, y, and z values of the two end points, to make sure that
        # the lower values are indeed less than the upper values
        x_min = min(message.fromBlock_x, message.toBlock_x)
        x_max = max(message.fromBlock_x, message.toBlock_x)
        y_min = min(message.fromBlock_y, message.toBlock_y)
        y_max = max(message.fromBlock_y, message.toBlock_y)
        z_min = min(message.fromBlock_z, message.toBlock_z)
        z_max = max(message.fromBlock_z, message.toBlock_z)

        # Get all the locations in the rectangular region
        rubble_locations = [(x,y,z) for x in range(x_min, x_max+1)
                                    for y in range(y_min, y_max+1)
                                    for z in range(z_min, z_max+1)]

        # Go through the locations, and add blocks where applicable
        blocks = []

        for location in rubble_locations:
            # Was there a block here?
            if self.world.containsBlockAt(location):
                block_to_remove = self.world.getBlockAt(location)

                # Is the block a marker block or sign
                if block_to_remove.block_type in MinecraftElements.Block.markers():
                    self.logger.debug("%s:    Ignoring Block %s", self, block_to_remove)
                elif block_to_remove.block_type == MinecraftElements.Block.wall_sign:
                    self.logger.debug("%s:    Ignoring Block %s", self, block_to_remove)
                else:
                    blocks.append(pygl_fov.Block(location, MinecraftElements.Block.gravel))
                    self.__hide(block_to_remove)

            # No block, go ahead and add the rubble
            else:
                blocks.append(pygl_fov.Block(location, MinecraftElements.Block.gravel))


        # Create blocks in each of the rubble locations, if there isn't already
        # a block in the world at that location
###        blocks = [pygl_fov.Block(location, MinecraftElements.Block.gravel)
###                  for location in rubble_locations]


###        for block in blocks:
###            if self.world.containsBlockAt(block.location):
###                block_to_remove = self.world.getBlockAt(block.location)
###                self.__hide(block_to_remove)

        self.logger.debug("%s:  Added %d rubble blocks due to collapse", self, len(blocks))

        self.addBlocksToFoV(blocks)


    
    def processRubbleDestroyedEvent(self, message):
        """
        Remove a rubble block from the set of blocks
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        rubble_location = message.location
        rubble_block = self.world.getBlockAt(rubble_location)

        if rubble_block is None:
            self.logger.warning("%s:    Rubble block not present at %s.", self, str(rubble_location))
            return

        self.logger.debug("%s:    Removing Rubble at %s", self, str(rubble_location))

        self.__hide(rubble_block)

        self.__drop_rubble(rubble_location)

###        # Move any rubble (or other movable blocks) down due to gravity
###        # Check the spot above the recently removed rubble.  If there's a 
###        # rubble block there, move that block down and repeat
###        dropping_rubble = True
###        hole_location = rubble_location
###
###        while dropping_rubble:
###            # Check immediately above the current rubble location
###            check_location = (hole_location[0], hole_location[1]+1, hole_location[2])
###
###            # Check if there's a block there
###            if self.world.containsBlockAt(check_location):
###                # Check if it's a gravel block
###                check_block = self.world.getBlockAt(check_location)
###                if check_block.block_type == MinecraftElements.Block.gravel:
###
###                    # Move the block down
###                    self.logger.debug("%s:      Moving Rubble at %s down to %s", self, str(check_block.location), str(hole_location))
###
###                    self.world.removeBlock(check_block.id)
###                    check_block.location = hole_location
###                    self.world.add(check_block)
###
###                    # And check the next block up
###                    hole_location = check_location
###
###                else:
###                    # Not a rubble block, nothing further to check
###                    dropping_rubble = False
###
###            else:
###                # No block found in the check spot
###                dropping_rubble = False


    def processRubblePlacedEvent(self, message):
        """
        Add a rubble block to the set of blocks
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # TODO: Check with JCR if this is really used?

        pass


    def processVictimNoLongerSafe(self, message):
        """
        Change the victim type to the corresponding color
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # TODO: Check with JCR if this is still used

        pass


    def processVictimPickedUp(self, message):
        """
        Remove the victim block from the set of rendered blocks, and place with
        the participant
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Make sure there is a victim in the location indicated in the message
        if not self.world.containsBlockAt(message.location):
            self.logger.warning("%s:    No block located in position %s", self, str(message.location))
            return

        # What is the victim block and who picked it up?
        victim_block = self.world.getBlockAt(message.location)
        participant = self.participants.get(message.participant_id, None)

        # Make sure it's a victim block
        if victim_block.block_type not in [MinecraftElements.Block.block_victim_1,
                                           MinecraftElements.Block.block_victim_2,
                                           MinecraftElements.Block.block_victim_1b,
                                           MinecraftElements.Block.block_victim_saved_a,
                                           MinecraftElements.Block.block_victim_saved_b,
                                           MinecraftElements.Block.block_victim_saved_c,
                                           MinecraftElements.Block.block_victim_expired,
                                           MinecraftElements.Block.block_victim_saved,
                                           MinecraftElements.Block.block_victim_proximity]:
            self.logger.warning("%s:    Non-victim block at position %s: %s", self, str(message.location), victim_block.block_type)
            return

        # Issue a warning if the worker thinks the participant is carrying a
        # victim
        if participant is not None and participant.victim_block is not None:
            self.logger.warning("%s    Participant %s currently carrying a victim: %s.  Replacing.", self, participant, participant.victim_block)

        # Hide the victim block, and give the victim block to the participant
        # (if the participant exists)
        self.__hide(victim_block)
        if participant is not None:
            participant.victim_block = victim_block


    def processVictimPlaced(self, message):
        """
        Place a victim block in the provided location, and remove from the 
        participant
        """

        self.logger.debug("%s:  Processing %s message", self, message)

        # Who is placing the victim
        participant = self.participants.get(message.participant_id, None)

        # Check to see if the participant exists; if not, raise a warning
        if participant is None:
            self.logger.warning("%s:  Participant not in participant store: %s", self, message.participant_id)
            return

        # Make sure the participant has a victim block
        if participant.victim_block is None:
            self.logger.warning("%s:    Participant %s not carrying a victim block", self, participant)
            return

        # Unhide the victim block, and change the block's location
        if participant.victim_block in self.hidden_blocks.keys():
            self.__unhide(participant.victim_block, message.location)
        else:
            self.logger.warning("%s:    Victim block %s not present in hidden block store", self, participant.victim_block)
            # TODO: Create a victim block and add it to the store

        # Make sure the participant is no longer holding a block
        participant.victim_block = None



    def consume(self, message):
        """
        Consume the message, updating the correspnding FoV component
        """

        self.logger.debug("%s:  Consuming %s message", self, message)        

        # message shouldn't be None, but check just in case
        if message is None:
            self.logger.warning("%s:  Consume received None for argument", self)
            return

        # Get a processor for the message, if it exists
        processor = self.messageProcessors.get(message.__class__, None)

        # Process the message
        if processor is not None:
            processor(message)


    def run(self):
        """
        Start the FoVWorker thread
        """

        # OpenGL components need to be created in the execution thread where 
        # it will be used
        self.initializeFoV()

        # Create participants
        # HACK:  Participants will be overwritten if provided the same position.
        #        Start the participants at an offset of 0.5 on each access, and
        #        increment one axis
        _x, _y, _z = (0.5, 0.5, 0.5)
        for participant in self.parent.participants:
            self.logger.info("%s:  Creating a new participant: %s", self, participant.participant_id)
            self.createParticipant(participant.participant_id,
                                   position=(_x,_y,_z),
                                   orientation=(0,0,0))
            _z += 1


        self.logger.info("%s:      Loading Minecraft World Data", self)

        if self.map_path is None:
            self.logger.error("%s:      No path provided to Mission map.  Cannot load blocks of base map.", self)
            return
        
        # Load the block feeder from the provided json path, and add it to the
        # FoV instance
        block_feeder = pygl_fov.BlockFeeder.loadFromJson(self.map_path)
        self.addBlocksToFoV(block_feeder)



        # Pass the initial victim and blockage lists
        self.logger.info("%s:  Processing Cached Victim and Blockage List Messages", self)
        for message in self.victimAndBlockageMessageCache:
            self.consume(message)

        # Wait until the worker is ready -- yield so that another process
        # can get some execution time in
        while self.state != FoVWorker.State.READY:
            time.sleep(0)        

        self.logger.info("%s:  Starting FoV Worker Thread", self)

        self.state = FoVWorker.State.RUNNING

        while self.state == FoVWorker.State.RUNNING:

            # Inner loop ensures that the message queue gets to complete
            # after stop is called
            while len(self.messageQueue) > 0:
                with self.message_lock:
                    message = self.messageQueue.next()

                if message is not None:
                    self.consume(message)

                # Yield the thread
                time.sleep(0)


    def stop(self):
        """
        Indicate the thread should stop
        """

        # No need to do anything if already stopping or stopped
        if self.state in [FoVWorker.State.STOPPING, FoVWorker.State.STOPPED]:
            return

        # Change the state to STOPPING, to indicate that there could still
        # be some messages in the queue to process.
        self.state = FoVWorker.State.STOPPING
        self.logger.info("%s:  Stopping FoV Worker Thread", self)



    def kill(self):
        """
        Force a quick stop to the thread, deleting the remaining contents of
        the messageQueue
        """

        self.stop()
        self.messageQueue.empty()


    def addMessage(self, message):
        """
        Add a message to the message queue to be processed
        """

        # Don't queue any messages if this worker is done
        if self.state in [FoVWorker.State.STOPPING, FoVWorker.State.STOPPED]:
            return

        # Queue any received messages while running
        if self.state == FoVWorker.State.RUNNING:
            with self.message_lock:
                self.messageQueue.add(message)
        else:
            if message.__class__ in [VictimList, BlockageList]:
                self.victimAndBlockageMessageCache.append(message)


    def get_profile_stats(self):
        """
        Return the profiling statistics for PlayerState processing times.

        Returns
        -------
        dictionary
            "counts": Number of times PlayerState was processed
            "average_time": Average time to process PlayerState messages
            "stdev_time": Standard deviation of time to process PlayerState messages
            "min_time": Minimum time to process PlayerState messages
            "max_time": Maximum time to process PlayerState messages
        """

        # Calculate the statistics, or provide dummy values if no method calls
        # have been made yet
        if len(self.process_player_state_times) == 0:
            average_time = 0.0
            stdev_time = 0.0
            min_time = 0.0
            max_time = 0.0
        else:
            average_time = np.mean(self.process_player_state_times)
            stdev_time = np.std(self.process_player_state_times)
            min_time = min(self.process_player_state_times)
            max_time = max(self.process_player_state_times)

        return { "counts": len(self.process_player_state_times),
                 "average_time": average_time,
                 "stdev_time": stdev_time,
                 "min_time": min_time,
                 "max_time": max_time
               }

    def reset_profile_stats(self):
        """
        """

        self.process_player_state_times.clear()


###    def print_stats(self):
###        """
###        Print out statistics
###        """
###
###        # Don't print anything if there isn't at least three entries.  The
###        # first is discarded, as that one involves transfer of vertices to the
###        # VBO and should be considered an outlier; the remaining two are needed
###        # to get a reasonable standard deviation
###        if len(self.process_player_state_times) < 3:
###            return
###
###        self.logger.info("%s:  Process Player State Profile:  ", self)
###        self.logger.info("%s:    Total Counts: %d", self, len(self.process_player_state_times[1:]))
###        self.logger.info("%s:    Average Time: %f", self, np.mean(self.process_player_state_times[1:]))
###        self.logger.info("%s:    Stdev Time:   %f", self, np.std(self.process_player_state_times[1:]))
###        self.logger.info("%s:    Min Time:     %f", self, min(self.process_player_state_times[1:]))
###        self.logger.info("%s:    Max Time:     %f", self, max(self.process_player_state_times[1:]))        
