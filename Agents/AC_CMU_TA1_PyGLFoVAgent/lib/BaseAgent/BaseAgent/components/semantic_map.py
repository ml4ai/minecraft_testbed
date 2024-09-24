# -*- coding: utf-8 -*-
"""
.. module:: semantic_map
   :platform: Linux, Windows, OSX
   :synopsis: A class for maintaining semantic map information.

.. moduleauthor:: Ini Oguntola <ioguntol@andrew.cmu.edu>

This file provides a class suitable for use by the agent ot maintain semantic
map information.  
"""
import numpy as np
import pickle

from collections import defaultdict
from MinecraftBridge.utils import Loggable
from pathlib import Path



### Constants

RESOURCES_DIR = Path(__file__).parent.parent.resolve() / 'resources'



### Helpers

def basemap_from_map_type(map_type):
    """
    Return the basemap as a BoundedGrid.
    """
    if 'saturn' in map_type.lower():
        basemap_path = RESOURCES_DIR / 'saturn_base.pkl'
        with open(basemap_path, 'rb') as file:
            return pickle.load(file)

    raise ValueError(f'Map type {map_type} not recognized.')


def bounds_from_map_type(map_type):
    """
    Determine bounds from map type.
    """
    if 'saturn' in map_type.lower():
        return {'xmin': -2226, 'xmax': -2087, 'zmin': -14, 'zmax': 66}

    raise ValueError(f'Map type {map_type} not recognized.')


def clip_to_bounds(x, z, bounds):
    """
    Clip an (x, z) location to be within the given bounds.
    """
    x = np.clip(x, bounds['xmin'], bounds['xmax'])
    z = np.clip(z, bounds['zmin'], bounds['zmax'])
    return x, z


def loc_to_2D(loc):
    """
    Convert a location to an (x, z) tuple.
    """
    assert isinstance(loc, tuple)

    if len(loc) == 2:
        x, z = loc
    elif len(loc) == 3:
        x, _, z = loc
    else:
        raise ValueError(f'Invalid argument: {loc}. Must be a tuple of length 2 or 3.')

    return x, z


def to_relative_coord(c, c_min, c_max):
    """
    Convert a single absolute coordinate (i.e. from Minecraft)
    to a relative coordinate (i.e. for internal grid).

    Arguments:
        - c: the absolute coordinate to convert (one of {slice, int, float})
        - c_min: the minimum coordinate value
        - c_max: the maximum coordinate value
    """
    if isinstance(c, slice):
        # Check range
        start, stop = c.start, c.stop
        if not (start is None or start >= c_min):
            raise IndexError(f'index {start} is out of range [{c_min}, {c_max}]')
        if not (stop is None or stop < c_max + 1):
            raise IndexError(f'index {stop} is out of range [{c_min}, {c_max}]')

        # Adjust values
        if start is not None:
            start -= c_min
        if stop is not None:
            stop -= c_min

        return slice(start, stop, c.step)

    elif isinstance(c, (np.integer, int, float)):
        # Check range
        if not (c >= c_min and c < c_max + 1):
            raise IndexError(f'index {c} is out of range [{c_min}, {c_max}]')

        # Adjust value
        return int(c - c_min)

    else:
        raise IndexError(f'Only integers, floats, and slices (`:`) are valid indices')


def expand_coords(*coords):
    """
    Return the set of tuple locations specified by the given coordinates.

    Arguments:
        - coords: list of coordinates of type {int, float, slice}
    """
    def coord_to_list(c):
        if isinstance(c, slice):
            return np.arange(c.start, c.stop, c.step)
        elif isinstance(c, (int, float)):
            return np.array([c])
        else:
            raise TypeError(c)

    coords = [coord_to_list(c) for c in coords]
    locs = zip(*[x.flat for x in np.meshgrid(*coords)])
    return set(tuple(loc) for loc in locs)



### Classes

class BoundedGrid:
    """
    Wrapper around a numpy array that allows for
    indexing via absolute coordinates within arbitrary (x, z) bounds.

    Attributes
    ----------
    bounds : dict
        Dictionary representing the grid bounds in absolute coordinates,
        with numerical values for keys {'xmin', 'xmax', 'zmin', 'zmax'}
    shape : tuple
        The dimensions of the 2D grid

    Methods
    -------
    __getitem__(loc)
        Get the grid value at an absolute location
    __setitem__(loc, val)
        Set the grid value at an absolute location
    __iter__():
        Iterator over all integer (x, z) locations within the grid bounds
    unique(exclude={None})
        Return a set of all unique values stored in the grid
    numpy()
        Return grid as a numpy array

    Usage
    -----
    ```
    >>> bounds = {'xmin':-10, 'xmax':10, 'zmin':20, 'zmax':30}
    >>> grid = BoundedGrid(bounds)

    >>> grid[-5, 25] = 'label'
    >>> grid[-5, 24:27]
    array([None, 'label', None], dtype=object)

    >>> grid[-15, 25]
    IndexError: index -15 is out of range [-10, 10]
    ```
    """

    def __init__(self, bounds, dtype=object):
        """
        Arguments:
            - bounds: dict representing the grid bounds in absolute coordinates,
                with numerical values for keys {'xmin', 'xmax', 'zmin', 'zmax'}
            - dtype: grid data type
        """
        self._bounds = bounds
        self._grid = np.empty(self.shape, dtype=dtype)


    def __getitem__(self, loc):
        """
        Get the value for an (x, z) location in absolute coordinates.

        Arguments:
            - loc: an absolute location tuple, either (x, y, z) or (x, z)
        """
        relative_loc = self._to_relative_coordinates(loc)
        return self._grid.__getitem__(relative_loc)


    def __setitem__(self, loc, val):
        """
        Set the value for an (x, z) location in absolute coordinates.

        Arguments:
            - loc: an absolute location tuple, either (x, y, z) or (x, z)
            - val: the value to set
        """
        relative_loc = self._to_relative_coordinates(loc)
        return self._grid.__setitem__(relative_loc, val)


    def __iter__(self):
        """
        Iterator over all integer (x, z) locations within the grid bounds.
        """
        x = slice(self.bounds['xmin'], self.bounds['xmax'] + 1)
        z = slice(self.bounds['zmin'], self.bounds['zmax'] + 1)
        return iter(expand_coords(x, z))


    @property
    def bounds(self):
        """
        Return a dictionary containing the absolute bounds of this grid.
        """
        return self._bounds


    @property
    def shape(self):
        """
        Return the (X, Z) shape of the 2D map.
        """
        return (
            self.bounds['xmax'] - self.bounds['xmin'] + 1,
            self.bounds['zmax'] - self.bounds['zmin'] + 1,
        )


    def unique(self, exclude={None}):
        """
        Return a set of all unique values stored in the grid.

        Arguments:
            - exclude: set of values to exclude
        """
        return set(self._grid.flat) - set(exclude)


    def numpy(self):
        """
        Return a numpy array with all the values 
        within the absolute bounds of this grid.
        """
        return self._grid[...]


    def _to_relative_coordinates(self, loc):
        """
        Convert an absolute location (in Minecraft coordinates)
        to a relative location (for internal grid coordinates).

        Arguments:
            - loc: an absolute location tuple, either (x, y, z) or (x, z)
        """
        x, z = loc_to_2D(loc)
        x = to_relative_coord(x, self.bounds['xmin'], self.bounds['xmax'])
        z = to_relative_coord(z, self.bounds['zmin'], self.bounds['zmax'])
        return (x, z)



class SemanticMap(Loggable):
    """
    A class for representing an ASIST semantic map.
    Useful for translating absolute (x, z) or (x, y, z) positions to room labels.

    Attributes
    ----------
    name : string
        The name of the SemanticMap
    bounds : dict
        Dictionary representing the grid bounds in absolute coordinates,
        with numerical values for keys {'xmin', 'xmax', 'zmin', 'zmax'}
    connections : dict
        Dictionary mapping room IDs to set of connection locations
        (i.e. set of locations for doors / openings, in absolute coordinates)
    basemap : BoundedGrid
        Grid indicating wall locations in the ASIST basemap that can be indexed
        via (x, z) or (x, y, z) Minecraft absolute coordinates
    rooms : BoundedGrid
        Grid of room labels that can be indexed
        via (x, z) or (x, y, z) Minecraft absolute coordinates
    subrooms : BoundedGrid
        Grid of subroom labels that can be indexed
        via (x, z) or (x, y, z) Minecraft absolute coordinates
    hallways : set
        Set of hallway room IDs

    Methods
    -------
    init_from_msg(msg)
        Initialize from a SemanticMapInitialized message
    is_in_bounds(loc)
        Return whether an absolute location is within bounds of the map
    get_room(loc, return_name=False)
        Get the room corresponding to a given location
    closest_room(loc, exclude={None}, mode='L2')
        Find the closest room to a location, excluding a given set of room IDs
    distance(source, destination)
        Return the distance from the specified source to the given destination
    direction(source, destination)
        Return a unit vector indicating the direction from the specified source
        to the given destination

    Usage
    -----
    ```
    >>> my_map = SemanticMap()
    >>> my_map.init_from_message(msg)

    >>> my_map.rooms[-2220, 60, 20]
    'lib'

    >>> my_map.subrooms[-2220, 60, 20]
    'lib_4'

    >>> my_map.connections['lib']
    {(-2216, 45), (-2216, 29)}
    ```
    """

    def __init__(self, minecraft_bridge=None):
        """
        Arguments
        ---------
        minecraft_bridge : MinecraftBridge.bridge
            Callback-decorated Minecraft bridge instance
        """
        self._name = None
        self._closest_room_cache = {}
        self._connections = defaultdict(set) # maps room IDs to set of connection locations
        self._subroom_to_room = {} # maps child location IDs (i.e. subrooms) to room IDs
        self._room_names = defaultdict(type(None)) # maps room IDs to names
        self._hallways = set()
        self._reset({'xmin': 0, 'xmax': 0, 'zmin': 0, 'zmax': 0})


    def __str__(self):
        """
        String representation of this object.
        """
        if self._name is None:
            return f"[{self.__class__.__name__}]"
        else:
            return f"[{self.__class__.__name__} - {self._name}]"


    @property
    def name(self):
        """
        Return the name of this SemanticMap.
        """
        return self._name


    @property
    def bounds(self):
        """
        Return a dictionary containing the absolute bounds of this map.
        """
        return self._bounds


    @property
    def connections(self):
        """
        Return a dictionary mapping room IDs to set of connection locations
        (i.e. set of locations for doors / openings, in absolute coordinates).
        """
        return self._connections


    @property
    def basemap(self):
        """
        Return the Minecraft basemap as a BoundedGrid.
        Elements are one of {'wall', 'furniture', None}.
        """
        return self._basemap


    @property
    def rooms(self):
        """
        Return grid of room labels as a BoundedGrid.
        """
        return self._rooms


    @property
    def subrooms(self):
        """
        Return grid of subroom labels (i.e. location IDs) as a BoundedGrid.
        """
        return self._subrooms


    @property
    def hallways(self):
        """
        Return set of hallway room IDs.
        """
        return self._hallways


    @property
    def shape(self):
        """
        Return the (X, Z) shape of the 2D map.
        """
        return (
            self.bounds['xmax'] - self.bounds['xmin'] + 1,
            self.bounds['zmax'] - self.bounds['zmin'] + 1,
        )


    def is_in_bounds(self, loc):
        """
        Return whether or not the given location in absolute coordinates
        is within bounds of this map.

        Arguments:
            - loc: an absolute location tuple, either (x, y, z) or (x, z)
        """
        x, z = loc_to_2D(loc)
        return (x >= self.bounds['xmin'] and x <= self.bounds['xmax']
            and z >= self.bounds['zmin'] and z <= self.bounds['zmax'])


    def init_from_message(self, msg):
        """
        Initialize from a SemanticMapInitialized message.

        Arguments:
            - msg: MinecraftBridge.messages.SemanticMapInitialized
        """
        self.logger.info(f'{self}:  Initializing SemanticMap from {msg.semantic_map_name}')
        self._name = msg.semantic_map_name.strip('.json')

        # Reset semantic map
        bounds = bounds_from_map_type(msg.semantic_map_name)
        self._reset(bounds)

        # Set basemap
        try:
            basemap = basemap_from_map_type(msg.semantic_map_name)
            assert basemap.bounds == self.bounds
            self._basemap = basemap
        except Exception as e:
            self.logger.error(f"{self}:  Could not load basemap - {e}")

        # Set room / subroom labels
        for loc in msg.semantic_map['locations']:
            # Get room / subroom IDs
            room_id = loc['id'].rsplit('_', 1)[0]
            subroom_id = loc['id']

            # Get room / subroom bounds and assign IDs
            if 'bounds' in loc:
                assert loc['bounds']['type'] == 'rectangle'
                coords = self._parse_rect_coords(loc['bounds']['coordinates'])
                self.rooms[coords] = room_id
                self.subrooms[coords] = subroom_id

            # Set room name
            self._room_names[loc['id']] = loc['name']

            # Keep track of child locations
            if 'child_locations' in loc:
                for child in loc['child_locations']:
                    self._subroom_to_room[child] = room_id

            # Keep track of hallways
            if loc['type'] in {'hallway', 'hallway_part'}:
                self.hallways.add(room_id)

        # Set room connections
        for connection in msg.semantic_map['connections']:
            room_ids = set(loc.rsplit('_', 1)[0] for loc in connection['connected_locations'])
            if len(room_ids) > 1:
                assert connection['bounds']['type'] == 'rectangle'
                coords = self._parse_rect_coords(connection['bounds']['coordinates'])

                # Update connections map
                for room_id in room_ids:
                    self._connections[room_id] |= expand_coords(*coords) # union


    def get_room(self, loc, return_name=False):
        """
        Get the room corresponding to a given location.

        Arguments:
            - loc: a location tuple or string room / subroom ID
            - return_name: bool indicating whether to return the room name (instead of ID)
        """
        room_id = None
        if loc in self.rooms.unique():
            room_id = loc
        elif loc in self._subroom_to_room:
            room_id = self._subroom_to_room[loc]
        elif isinstance(loc, tuple) and self.is_in_bounds(loc):
            room_id = self.rooms[loc]

        return self._room_names[room_id] if return_name else room_id


    def closest_room(self, loc, exclude={None}, mode='L2'):
        """
        Find the closest room to a location, excluding a given set of room IDs.

        Arguments:
            - loc: an absolute location tuple, either (x, y, z) or (x, z)
            - exclude: set of values to excludes
            - mode: distance metric to use
        """
        key = (loc, tuple(exclude))
        if key in self._closest_room_cache:
            return self._closest_room_cache[key]

        locations = [loc for loc in self.rooms if self.rooms[loc] not in exclude]
        diffs = loc_to_2D(loc) - np.array(locations)

        # Return the room for the closest location
        if mode == 'L1':
            norms = np.einsum('ij->i', np.abs(diffs))
            room = self.rooms[locations[norms.argmin()]]
            self._closest_room_cache[key] = room
        elif mode == 'L2':
            squared_norms = np.einsum('ij,ij->i', diffs, diffs)
            room = self.rooms[locations[squared_norms.argmin()]]
            self._closest_room_cache[key] = room
        else:
            raise NotImplementedError(mode)

        return room


    def distance(self, source, destination, mode='L2'):
        """
        Return the distance from the specified source to the given destination.
        If the destination is a room, returns the distance to the nearest
        door / opening.

        Arguments:
            - source: an absolute location tuple, either (x, y, z) or (x, z)
            - destination: a location tuple or a room ID
            - mode: distance metric to use
        """
        source = loc_to_2D(tuple(source))

        if isinstance(destination, str):
            room_id = destination

            # Handle edge cases
            if self.rooms[source] == room_id:
                return 0
            elif room_id not in self._connections:
                return float('inf')

            # Calculate displacements between our location and room connection locations
            connection_locs = np.array(list(self._connections[room_id]))
            diffs = source - connection_locs

            # Return the minimum norm of the displacements
            if mode == 'L1':
                norms = np.einsum('ij->i', np.abs(diffs))
                return norms.min()
            elif mode == 'L2':
                squared_norms = np.einsum('ij,ij->i', diffs, diffs)
                return np.sqrt(squared_norms.min())
            else:
                raise NotImplementedError(mode)

        else:
            # Calculate displacement between source and destination
            destination = np.array(loc_to_2D(tuple(destination)))
            diff = source - destination

            # Return the norm of the displacement
            if mode == 'L1':
                return np.einsum('i->', np.abs(diff))
            elif mode == 'L2':
                return np.sqrt(np.einsum('i,i->', diff, diff))
            else:
                raise NotImplementedError(mode)


    def direction(self, source, destination):
        """
        Return a unit vector indicating the direction from the specified source
        to the given destination. If the destination is a room, returns the average
        direction to the room doors / openings.

        Arguments:
            - source: an absolute location tuple, either (x, y, z) or (x, z)
            - destination: a location tuple or a room ID
        """
        source = loc_to_2D(tuple(source))

        if isinstance(destination, str):
            room_id = destination

            # Handle edge cases
            if self.rooms[source] == room_id:
                return np.zeros(len(self.shape))
            elif room_id not in self._connections:
                return np.zeros(len(self.shape))

            # Calculate average displacement between our location and room connection locations
            room_vector = np.mean([np.array(loc) for loc in self._connections[room_id]], axis=0)
            displacement_vector = room_vector - source

        else:
            # Calculate displacement between source and destination
            destination = np.array(loc_to_2D(tuple(destination)))
            displacement_vector = destination - source

        return displacement_vector / np.linalg.norm(displacement_vector)


    def _parse_rect_coords(self, coords):
        """
        Parse bound coordinates for a rectangle from a SemanticMapInitialized message.
        Converts to a tuple of slices, with a slice for each dimension.
        """
        x_min, z_min = clip_to_bounds(coords[0]['x'], coords[0]['z'], self.bounds)
        x_max, z_max = clip_to_bounds(coords[1]['x'], coords[1]['z'], self.bounds)
        return (slice(x_min, x_max), slice(z_min, z_max))


    def _reset(self, bounds_dict):
        """
        Reset semantic map given the provided bounds.
        """

        # Reset bounds
        assert isinstance(bounds_dict, dict)
        assert all(k in bounds_dict for k in {'xmin', 'xmax', 'zmin', 'zmax'})
        self._bounds = bounds_dict

        # Reset rooms / subrooms / basemap
        self._rooms = BoundedGrid(self._bounds)
        self._subrooms = BoundedGrid(self._bounds)
        self._basemap = BoundedGrid(self._bounds)

        # Clear hallways
        self._hallways.clear()

        # Clear caches
        self._closest_room_cache.clear()
