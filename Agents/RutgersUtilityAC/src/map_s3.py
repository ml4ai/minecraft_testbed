"""
map.py

Implements map and distance functionality
for ASIST Study 3 analysis, using the topography
of the Saturn maps.

CoDaS Lab, 1/26/22
"""

import itertools
import sys
import logging
from collections import deque
import math
import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plt
from matplotlib import colors
from typing import List, Dict, Set, Tuple, Optional

from configuration_s3 import Configuration, get_SaturnA_starting_config
# from shrink_rewind import Toposkeleton
# from python_tsp.exact import solve_tsp_dynamic_programming
# from python_tsp.heuristics import solve_tsp_simulated_annealing
# from attempted_3rdparties.Medium_Article_master import BaijayantaRoy_Astar as BRastar
# from attempted_3rdparties.nswift_astar import astar_alg as NSastar


# straight copied from https://stackoverflow.com/questions/5434891/
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


class Map:
    # Topography constants
    OPEN_SPACE = 0
    WALL = 3
    FURNITURE = 2
    RUBBLE = 1
    # TODO: add victims (as path blockers)
    # TODO: freezing plate (threat), danger sign?

    # for checking if player is within Saturn map area (FOV purposes)
    FOV_Z_MAX = 64.5

    def __init__(self, topo_path="preprocessed_data/topography.npy", 
                 tsp='exact'):
        """
        REQUIRES: path is path to map topography file (npy)
                  np.unique(np.load(path)) == {self.OPEN_SPACE,
                                               self.FURNITURE,
                                               self.WALL}
                  rubble locations and victim locations match
        MODIFIES: self
        """

        # store base algorithms choice
        if tsp not in {'exact', 'heuristic'}:
            raise ValueError(f'Invalid TSP objective choice: f{tsp}')

        self.tsp_objective = tsp

        self._configuration = Configuration.make_empty_config()

        self.INITIAL_TOPOGRAPHY = np.load(topo_path)
        self.topography = self.INITIAL_TOPOGRAPHY.copy()

        # # wall block missing in some renditions
        # # https://darpa-asist.slack.com/archives/CQM3UQSKC/p1624981910048600
        # if self.INITIAL_TOPOGRAPHY[self.convert_coords(-2123, 54)] != self.WALL:
        #     raise ValueError('Missing wall block at (-2123, 54).')

        # don't build shrink-rewind topology unless we need to use it
        self.topology = None

        # replace all obstacles with 1 for 3rd parties astar
        #self._gen_astar_map()

        # memos for speed
        self._dist_memo = dict()
        self._path_memo = dict()
        return

    def _configuration_has_changed(self, c: Configuration) -> bool:
        """
        REQUIRES: self._configuration
        EFFECTS:  Returns true if c is different than current
                  configuration.
        """
        # ignore players information and uncertainty information
        current_rubble = self._configuration.rubble_gt
        current_victims = self._configuration.victims_gt

        changed = (not current_rubble.equals(c.rubble_gt)) or \
                  (not current_victims.equals(c.victims_gt))
        return changed

    def _gen_topology(self) -> None:
        """
        REQUIRES: self.topography
        MODIFIES: self.topology
        EFFECTS:  Generates topology of self.topography, to prep for
                  testing path existence between points.
        """

        # FIXME: DFS recursion depth exceeded often
        RECURSION_LIMIT = 1800  # def should not go much higher
        sys.setrecursionlimit(RECURSION_LIMIT)
        # TODO: pythonic way of managing Configuration's dynamic memory. Multiple copies going
        #       around right now.
        self.topology = Toposkeleton(self.topography, self._configuration.copy())
        return

    def _gen_astar_map(self) -> None:
        """
        REQUIRES: self.topography
        MODIFIES: self.astar_map
        EFFECTS:  Resets astar_map representation to match self.topography.
                  Should be called any time self.topography is altered.
        """
        self.astar_map = np.where(self.topography == self.OPEN_SPACE, self.topography, 1).tolist()
        raise DeprecationWarning('A* no longer used')

    def _refresh(self):
        """
        MODIFIES: self
        EFFECTS:  Restores to original topography, empty configuration.
                  Clears memos
        """
        self._configuration = Configuration.make_empty_config()
        self.topography = self.INITIAL_TOPOGRAPHY.copy()
        # must call these every time topography is altered
        #self._gen_astar_map()
        self.topology = None  # don't build topology until we need it
        # reset memos
        self._dist_memo = dict()
        self._path_memo = dict()
        return

    def update(self, c: Configuration) -> None:
        """
        REQUIRES: c is a utility.Configuration
        MODIFIES: self
        EFFECTS:  Clears rubble marked as removed in c
                  in self.topography. Maintains invariant: that
                  self.topology, self.topography, self._path/dist_memo,
                  self._astar_map, self._configuration, etc. are all congruent.
        """

        if not self._configuration_has_changed(c):
            # no need to update
            return

        # clear all memos and restore to initial settings
        self._refresh()

        # Note: seems more Pythonic to explicitly make a deep copy here, rather than
        #       attempt to implement the Big 3 as Configuration internals.
        self._configuration = c.copy()

        # update rubble
        def add_rubble_block(rub: pd.Series):
            # MODIFIES: self.topography
            # not a member on its own because we don't want to check invariant each time
            if rub.status != 0:  # present
                # add rubble
                row, col = self.convert_coords(rub.x, rub.z)
                self.topography[row, col] = self.RUBBLE

        # skipping rubble removal avoids problem of rubble blocks on top
        # of one another. As long as one rubble at (x, z) is present,
        # self.topography will have np.inf at rubble location
        # TODO: may want to change this later.
        c.rubble_gt.apply(add_rubble_block, axis=1)

        def remove_rubble_block(victim: pd.Series):
            # MODIFIES: self.topography
            if victim.status == 0:  # unsaved (present on map)
                # remove rubble
                row, col = self.convert_coords(victim.x, victim.z)
                self.topography[row, col] = self.OPEN_SPACE

        # removing rubble on top of (or underneath?) victims on map.
        # Note that TA1 will not place rubble on top of victims.
        # Victims will still be inaccessible if rubbles/walls cover
        # all four sides.
        # FIXME: Victims cannot be used to block doorways, etc. with this implementation.
        c.victims_gt.apply(remove_rubble_block, axis=1)

        # TODO: update victims (if they change map topography)

        # self.topology is reset to None in self._refresh
        return

    def get_configuration(self) -> Configuration:
        """
        REQUIRES: self.configuration
        EFFECTS:  Returns copy of current configuration used.
        """
        return self._configuration.copy()

    def _store_path(self, x1: int, z1: int, x2: int, z2: int,
                    path: List[Tuple[int, int]]) -> None:
        """
        REQUIRES: path[0] == (x1, z1) and path[-1] == (x2, z2)
                  path is a valid path (does not cross walls,
                  contiguous)
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Stores the path between (x1, z1) and (x2, z2)
                  to save future computation. Stores the corresponding
                  distance if not already in the memo.
        """

        # don't store in both directions, saves memory
        # Note: issues can occur if using both A* and BFS paths.
        #       3rd party A*'s can't do diagonals but _BFS can.
        #   ->  Reverse paths may be different than normal, and have
        #       different lengths, and they won't be caught!
        path_name = ((x1, z1), (x2, z2))
        # TODO: update path length convention
        path_length = len(path) if len(path) > 1 else 0

        self._path_memo[path_name] = path
        self._dist_memo[path_name] = path_length
        return None

    def _lookup_path(self, x1: int, z1: int, x2: int, z2: int,
                     mode='exact') -> Optional[List[Tuple[int, int]]]:
        """
        REQUIRES: self._accessible(x1, z1, x2, z2) (soft req)
        EFFECTS:  Returns path between (x1,z1) and (x2,z2) if
                  stored in memo. Otherwise returns None
                  Heuristic mode: checks for any paths "similar"
                  enough to stored paths. Returns an extension of
                  a stored path if such a solution is found.
        """
        if mode not in {'exact', 'heuristic'}:
            raise ValueError(f'Invalid path lookup mode: {mode}')

        if mode == 'heuristic':
            raise NotImplementedError

        # look up both directions
        path_name = ((x1, z1), (x2, z2))
        path_name_rev = ((x2, z2), (x1, z1))
        if path_name in self._path_memo:
            return self._path_memo[path_name]
        elif path_name_rev in self._path_memo:
            # reverse path if in reverse direction
            return list(reversed(self._path_memo[path_name_rev]))
        else:
            return None

    def _store_distance(self, x1: int, z1: int, x2: int, z2: int,
                        dist: float) -> None:
        """
        REQUIRES: dist is actual distance between x1,z1 and x2,z2
                  with current map configuration
                  (thus, a valid path exists, both points are valid map coords,
                  and neither points are furniture or walls)
        MODIFIES: self.dist_memo
        EFFECTS:  Stores distance between points to save
                  future computation. Overwrites previously
                  computed distances!
        """

        # Note: don't store in both directions, saves memory.
        # Have _lookup_distance lookup in both directions
        distance_name = ((x1, z1), (x2, z2))
        self._dist_memo[distance_name] = dist
        return

    def _lookup_distance(self, x1: int, z1: int, x2: int, z2: int) -> Optional[int]:
        """
        REQUIRES: self._accessible(x1, z1, x2, z2) (soft req)
        EFFECTS:  Returns distance between points if stored
                  in memo. Otherwise returns None
        """

        # look up both directions
        distance_name = ((x1, z1), (x2, z2))
        distance_name_rev = ((x2, z2), (x1, z1))

        if distance_name in self._dist_memo:
            return self._dist_memo[distance_name]
        elif distance_name_rev in self._dist_memo:
            return self._dist_memo[distance_name_rev]
        else:
            return None

    def _check_start_loc(self, x: float, z: float) -> Tuple[float, float]:
        """
        REQUIRES: (x, z) is a valid map coordinate
                  x, z is the location of a player. Otherwise furniture check doesn't make sense
        EFFECTS:  Raises error if the map has a wall, rubble,
                  victim at (x, z) and true otherwise.
                  If there is furniture at (x, z), checks if x, z seems to be
                  the result of a precision error and should actually point to
                  a neighboring block. If yes, returns the minecraft coordinates
                  of the center of that block; otherwise raises error.
        TODO: victims on map
        """
        r, c = self.convert_coords(x, z)
        if self.topography[r, c] == self.FURNITURE:
            result = self._furniture_exception(x, z)
            if result is not None:
                logging.debug(f'Applying walked-on-furniture exception: '
                              f'replacing {x, z} with {result}')
                return result
            else:
                raise ValueError(f'Invalid starting coordinate: ({x}, {z})')
        elif self.topography[r, c] == self.OPEN_SPACE:
            return x, z
        else:
            raise ValueError(f'Invalid starting coordinate: ({x}, {z})')

    def connected(self, x1: float, z1: float, x2: int, z2: int, c: Configuration,
                  can_reach=True, use_BFS=True) -> bool:
        """
        REQUIRES: self.topology
                  (x1, z1) is an open space in self.topography
                  (x2, x2) is an open space in self.topography unless can_reach is True
        EFFECTS:  Returns true if there exists a path between (x1, z1)
                  and (x2, z2) in the current configuration, and false otherwise.
                  If can_reach is True, returns true if there is a path
                  to any of the 4 surrounding blocks of (x2, z2).
        """
        self.update(c)

        # sanity checking
        x1, z1 = self._check_start_loc(x1, z1)  # checks for furniture exception
        if not can_reach and self.topography[self.convert_coords(x2, z2)] != self.OPEN_SPACE:
            raise ValueError(f'Invalid ending coordinate: ({x2}, {z2})')

        if can_reach:
            # TODO: add victim to valid ending coord types
            if not use_BFS:
                raise ValueError(f'Pass use_BFS=True for can_reach option')
            if not self.topography[self.convert_coords(x2, z2)] in {self.OPEN_SPACE, self.RUBBLE}:
                raise ValueError(f'Invalid ending coordinate: ({x2}, {z2})')

        if use_BFS:
            # BFS faster on its own than BFS on topology for connectedness
            path = self._BFS(x1, z1, [(x2, z2)], use_topology=False)
            if len(path) == 0:
                path = None
            else:
                # store in memo because we're using topography
                self._store_path(x1, z1, x2, z2, path[(x2, z2)])
        else:
            #path = self._astar(x1, z1, x2, z2, use_topology=True)
            raise DeprecationWarning('A* no longer used')
        # don't store path since it's not on topography
        return path is not None

    def connected_multiple(self, x: int, z: int, points: List[Tuple[int, int]], c: Configuration,
                           can_reach=False, use_BFS=True) -> List[Tuple[int, int]]:
        """
        REQUIRES: self.topology
                  (x1, z1) is an open space in self.topography
                  (x2, x2) is an open space in self.topography unless can_reach is True
        EFFECTS:  Returns p if there exists a path between (x1, z1)
                  and p (for p in points) in the current configuration, and false otherwise.
                  If can_reach is True, returns true if there is a path
                  to any of the 4 surrounding blocks of p.
        """
        self.update(c)

        # sanity checking
        x, z = self._check_start_loc(x, z)
        for p in points:
            if not can_reach and self.topography[self.convert_coords(p[0], p[1])] != self.OPEN_SPACE:
                raise ValueError(f'Invalid ending coordinate: ({p[0]}, {p[1]})')

        if can_reach:
            # TODO: add victim to valid ending coord types
            if not use_BFS:
                raise ValueError(f'Pass use_BFS=True for can_reach option')
            for p in points:
                if not self.topography[self.convert_coords(p[0], p[1])] in {self.OPEN_SPACE,
                                                                            self.RUBBLE}:
                    raise ValueError(f'Invalid ending coordinate: ({p[0]}, {p[1]})')

        if use_BFS:
            # about twice as fast without building topology
            paths = self._BFS(x, z, points, use_topology=False)
            for dest, path in paths.items():
                self._store_path(x, z, dest[0], dest[1], path)
            return list(paths.keys())
        else:
            raise DeprecationWarning
            # don't store path since it's not on topography

    def _astar(self, x1: int, z1: int, x2: int, z2: int,
               use_topology=False) -> Optional[List[Tuple[int, int]]]:
        """
        REQUIRES: both (x1, z1) and (x2, z2) are valid map coordinates
                  a valid path exists between (x1, z1) and (x2, z2) (near hard-req)
        EFFECTS:  Uses A* to find a path between the points. Returns a list
                  of coordinates in self.topography (TODO: NOT MINECRAFT COORDINATES?)
                  with both endpoints included.
        """

        raise DeprecationWarning('soon A* will be unavailable')

        # use A*
        r1, c1 = self.convert_coords(x1, z1)
        r2, c2 = self.convert_coords(x2, z2)

        # for self.connected
        maze = self.astar_map if not use_topology else self.topology.mapmat_shrunk

        if self.astar_alg == 'BR':
            path = BRastar.search(maze, 1, (r1, c1), (r2, c2))
        elif self.astar_alg == 'NS':
            path = NSastar.astar(maze, (r1, c1), (r2, c2))
        else:
            raise ValueError('Map.astar_alg not set properly')

        if path[-1] != (r2, c2):
            # needed because some paths are too difficult for A* (computation horizon)
            print(f"Warning: A* could not find path: {(x1, z1)} to {(x2, z2)}")
            return None
        else:
            # FIXME: remove
            print('start', x1, z1, '   end:', x2, z2)
            print(path)
            return path

    def _BFS(self, x: float, z: float, points: List[Tuple[int, int]],
             use_topology=False) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        # TODO: DFS option?
        """
        REQUIRES: self.connected(x, z, point[0], point[1]) for point in points
                  (soft req)
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Uses BFS to find paths from start point (x, z) to each point in
                  points. Returns dict of paths. Returned dict will be
                  same length as points if all are found.
                  If a point in points is not found, that path will not be present in
                  returned dict.
                  Each path is in self.topography coordinates and includes
                  both start point and end point.
        """

        if use_topology:
            if self.topology is None:
                self._gen_topology()
            maze = self.topology.mapmat_shrunk
        else:
            # prep topography by plugging entrance with walls
            maze = self.topography
            ENTRANCE_COORDS = [(-2156, 61), (-2155, 61), (-2153, 61), (-2152, 61)]
            for ex, ez in ENTRANCE_COORDS:  # don't overshadow params
                maze[self.convert_coords(ex, ez)] = self.WALL

        def can_walk_diagonal(r1: int, c1: int, r2: int, c2: int) -> bool:
            # REQUIRES: (r1,c1) and (r2,c2) are diagonally positioned
            # EFFECTS:  Returns whether it is allowed to traverse between (r1, c1)
            #           and (r2, c2) given topography.
            #assert((abs(r1 - r2) == 1) and (abs(c1 - c2) == 1))
            diag1 = (r1, c2)
            diag2 = (r2, c1)
            # TODO: should this be and? Or continue to allow cutting corners?
            return maze[diag1] == self.OPEN_SPACE or maze[diag2] == self.OPEN_SPACE

        def gen_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
            # REQUIRES: r, c valid indices of maze
            # EFFECTS:  Generate neighbor nodes based on maze. Rubble
            #           and Victim spaces do not have neighbors,
            #           but can be added as neighbors from open spaces.
            #           Walls and Furniture cannot be added as neighbors.
            # Note: including diagonals here. Order nondiagonals first
            #       so resulting paths look more realistic.

            # TODO: rubble threshold (simplification of Dijkstra)
            if maze[r, c] != self.OPEN_SPACE:
                return list()

            neighbors = [(r-1, c), (r, c-1), (r, c+1), (r+1, c)]
            diagonals = [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
            neighbors.extend([ d for d in diagonals if can_walk_diagonal(r, c, d[0], d[1]) ])
            neighbors = [ n for n in neighbors if maze[n[0]][n[1]] not in {self.WALL, self.FURNITURE} ]
            return neighbors

        def backtrace(r: int, c: int, parents: np.ndarray) -> List[Tuple[int, int]]:
            # R: 0 <= r < parents.shape[0]
            #    0 <= r < parents.shape[1]
            #    source node in parents has -1, -1 marked. valid path to there
            path = list()
            current_r, current_c = r, c
            while parents[current_r][current_c][0] != -1:
                path.append((current_r, current_c))
                # need to be assigned at same time
                current_r, current_c = parents[current_r][current_c][0], \
                                       parents[current_r][current_c][1]
            # add starting node (last parent)
            path.append((current_r, current_c))
            return list(reversed(path))

        # prep data structures
        start = self.convert_coords(x, z)
        goals = { self.convert_coords(p[0], p[1]): p for p in points }
        visited = np.full(maze.shape, False, dtype=bool)
        visited[start] = True
        parents = np.ones((maze.shape[0], maze.shape[1], 2), dtype=int) * -1
        frontier = deque([start])
        paths = dict()

        while frontier and len(goals) > 0:
            # use frontier.pop() for DFS
            current = frontier.popleft()

            # check if we've reached a goal
            if current in goals:
                paths[goals[current]] = backtrace(current[0], current[1], parents)
                del goals[current]

            # expand valid neighboring nodes
            possible_neighbors = gen_neighbors(*current)
            # don't add already visited nodes
            neighbors = [ n for n in possible_neighbors if not visited[n[0], n[1]] ]

            # mark visited (and parent node for backtrace)
            for n in neighbors:
                r, c = n[0], n[1]
                visited[r, c] = True
                parents[r][c][0] = current[0]
                parents[r][c][1] = current[1]

            # add neighbors to frontier
            frontier.extend(neighbors)

        return paths

    def _dijkstra(self, x: int, z: int, player: str,
                  points: List[Tuple[int, int]]) -> Dict[Tuple[int, int],
                                                         List[Tuple[float, Tuple[int, int]]]]:
        """
        REQUIRES: (x, z) and all coords in points are valid Minecraft coordinates
                  self.connected(x, z, p[0], p[1]) for p in points TODO hard req?
                  player is in self._configuration.players.player_id
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Performs Dijkstra's algorithm to compute the shortest paths
                  from (x, z) to each point in points. Stores successful paths and
                  their distances in path and distance memos. Returns a map from
                  destination to (distance, path) where path is an ordered list of
                  coordinates. Uses a combination of the player's victim_prob_map and
                  rubble_prob_map
        """

        raise NotImplementedError

    def get_accessible_rubble(self, x: int, z: int, c: Configuration,
                              use_BFS=True) -> pd.DataFrame:
        """
        REQUIRES: (x1, z1) is a valid map coordinate and isn't a wall or a rubble
        EFFECTS:  Returns dataframe of currently accessible rubble clusters
                  in Configuration.rubble_info format. "Accessible" means
                  there exists a path from (x, z) to any point
                  _next to_ any block in a rubble cluster
        """
        self.update(c)

        if use_BFS:
            # from https://stackoverflow.com/questions/55336870
            points = list(map(tuple, self._configuration.rubble_gt.loc[:, ['x', 'z']].to_numpy()))
            # TODO: find a way to only save one path per cluster. Otherwise memory wasted
            paths = self._BFS(x, z, points)

            # glean which clusters were found
            rubbles_seen_mask = self._configuration.rubble_gt.apply(lambda r: (r.x, r.z) in paths,
                                                                    axis=1)
            rubbles_seen = self._configuration.rubble_gt[rubbles_seen_mask]
            rubble_cluster_ids = rubbles_seen.cluster_id.unique()
            clusters_seen = self._configuration.rubble_gt[self._configuration.rubble_gt.cluster_id
                                                          .isin(rubble_cluster_ids)]

            # store paths
            for dest, path in paths.items():
                # TODO: only store one per cluster
                self._store_path(x, z, dest[0], dest[1], path)

            return clusters_seen.copy()
        else:
            if self.topology is None:
                self._gen_topology()
            rubble_cluster_ids = self.topology.get_accessible_rubble_cluster(self.topology.mapmat,
                                                                             self.convert_coords(x, z))
            accessibles = self._configuration.rubble_gt[self._configuration.rubble_gt.cluster_id
                                                        .isin(rubble_cluster_ids)]
            return accessibles.copy()

    def get_accessible_victims(self, x: int, z: int, c: Configuration,
                               use_BFS=True) -> pd.DataFrame:
        """
        REQUIRES: (x, z) is a valid map coordinate and isn't a wall or rubble
                  self.topology.config.victims[[Configuration.VICTIM_COLS]] ==
                      self._configuration.victims
                  (i.e. they have the same victims in the same order)
        EFFECTS:  Returns dataframe of victims currently accessible from (x,z)
                  in Configuration.victim_info format. "Accessible" means
                  there exists a path from (x, z) to any point _next to_
                  the victim
        """
        self.update(c)

        if use_BFS:
            victims = self._configuration.victims_gt
            # from https://stackoverflow.com/questions/55336870
            points = list(map(tuple, victims[victims.status == 0].loc[:, ['x', 'z']].to_numpy()))
            paths = self._BFS(x, z, points)

            # glean which victims were found
            victims_seen_mask = victims.apply(lambda r: (r.x, r.z) in paths, axis=1)
            victims_found = victims[victims_seen_mask]

            # store paths
            for dest, path in paths.items():
                self._store_path(x, z, dest[0], dest[1], path)

            return victims_found.copy()
        else:
            if self.topology is None:
                self._gen_topology()
            if self.topology.victims_connected_matrix is None:
                self.topology.victims_connected_matrix = \
                    self.topology.get_victims_connected_matrix(self.topology.victims_mapmat)

            # just for shorthand
            victims = self.topology.config.victims_gt
            v_connected = self.topology.victims_connected_matrix

            # TODO: may need to optimize later
            found_victim = False
            i = 0
            while not found_victim and i < len(self._configuration.victims_gt):
                # skip saved or scout-held victims
                if victims.iloc[i].status == 0:
                    target = victims.iloc[i]
                    found_victim = self.connected(x, z, target.x, target.z, c)
                i += 1

            if i == len(victims):
                # didn't find any!
                return pd.DataFrame(columns=Configuration.VICTIM_COLUMNS)

            first_found = victims.iloc[i-1]
            connected_victims_idx = np.nonzero(v_connected[first_found.matrix_idx])[0]

            connected_mask = victims.matrix_idx.isin(connected_victims_idx)
            # assumes Map's victim configuration and Toposkeleton's victim configuration
            # are coindexed
            return self._configuration.victims_gt[connected_mask].copy()

    def path(self, x1: float, z1: float, x2: int, z2: int, c: Configuration) -> List[Tuple[int, int]]:
        """
        REQUIRES: self.connected(x1, z1, x2, z2) (there exists a valid path between
                  the points)
                  both (x1, z1) and (x2, z2) are valid map coordinates
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Uses algorithm of choice to find the best (or near-best) path
                  from (x1, z1) to (x2, z2). The returned path includes both start and
                  end points.
        """
        self.update(c)

        # check if we remember this path
        x1, z1 = self._check_start_loc(x1, z1)
        lookup = self._lookup_path(x1, z1, x2, z2, mode='exact')
        if lookup is not None:
            return lookup

        # remove later for speedups
        if not self.connected(x1, z1, x2, z2, c, use_BFS=True):
            raise ValueError(f'Path does not exist between points {(x1,z1)} and {(x2,z2)}')
        else:
            # rely on memo! self.connected now saves found paths to memo
            return self._lookup_path(x1, z1, x2, z2, mode='exact')

    def distance(self, x1: int, z1: int, x2: int, z2: int, c: Configuration) -> int:
        """
        REQUIRES: both (x1, y1) and (x2, y2) are valid map coordinates
        MODIFIES: self._dist_memo
        EFFECTS:  Returns travel distance (in blocks) between start and
                  end point, inclusive. If points are inaccessible
                  returns a distance of np.inf.
        """
        self.update(c)

        x1, z1 = self._check_start_loc(x1, z1)

        # check if we've already computed this
        lookup = self._lookup_distance(x1, z1, x2, z2)
        if lookup is not None:
            return lookup

        if not self.connected(x1, z1, x2, z2, c):
            return np.inf

        # TODO: switch for other faster distance-only algorithms
        path = self.path(x1, z1, x2, z2, c)  # updates dist memo
        # TODO: handle A* failures
        # TODO: update lengths convention
        path_length = len(path) if len(path) > 1 else 0
        return path_length

    @staticmethod
    def convert_coords(x: float, z: float) -> (int, int):
        """
        REQUIRES: (x, z) are in Testbed coordinates:
                      x in [-2225, -2087]
                      z in [-11, 61]
        EFFECTS:  Returns corresponding indices for self.topography
                  matrix.
        Note that 0->+ left-to-right on x,
                  and 0->+ top-to-bottom on z in self.topography.
                  x indexes the columns and z indexes the rows.
                  y deals with height and is unused.
        """
        THRESHOLD = 0.0001

        # gleaned from TA3 map excel spreadsheet
        X_ZERO = -2225
        X_MAX = -2087
        Z_ZERO = -11
        Z_MAX = 64  # inclusive

        topography_x = math.floor(x) - X_ZERO
        topography_z = math.floor(z) - Z_ZERO

        # validate
        if not (X_ZERO <= x <= X_MAX and Z_ZERO <= z <= Z_MAX):
            raise ValueError(f'Coordinates out of bounds: {(x, z)}')
        # TODO: validate against self.topography

        # TODO: remove
        ## Exception for trial 426
        #if abs(x - -2170.3182) < THRESHOLD and abs(z - 7.925) < THRESHOLD:
        #    topography_z = math.ceil(z) - Z_ZERO
        ## Exception for trial 479
        #if abs(x - -2169.0749) < THRESHOLD and abs(z - 30.31316) < THRESHOLD:
        #    topography_x = math.ceil(x) - X_ZERO
        ## Exception for trial 503
        #if abs(x - -2169.05094) < THRESHOLD and abs(z - 16.2775) < THRESHOLD:
        #    topography_x = math.ceil(x) - X_ZERO

        # z indexes rows, x indexes columns
        return topography_z, topography_x

    @staticmethod
    def convert_coords_z(z: float) -> int:
        """
        REQUIRES: z is in Testbed coordinates:
                      z in [-11, 61]
        EFFECTS:  Returns corresponding ROW index for self.topography
                  matrix.
        Note that 0->+ left-to-right on x,
                  and 0->+ top-to-bottom on z in self.topography.
                  x indexes the columns and z indexes the rows.
                  y deals with height and is unused.
        """

        # gleaned from TA3 map excel spreadsheet
        Z_ZERO = -11
        Z_MAX = 64  # inclusive

        # FIXME: check this is cast in the appropriate direction
        topography_z = math.floor(z) - Z_ZERO

        # validate
        if not Z_ZERO <= z <= Z_MAX:
            raise ValueError(f'Coordinate out of bounds: {z}')

        # z indexes rows, x indexes columns
        return topography_z

    @staticmethod
    def convert_coords_x(x: float) -> int:
        """
        REQUIRES: x in [-2225, -2087]
        EFFECTS:  Returns corresponding COLUMN index for self.topography
                  matrix.
        Note that 0->+ left-to-right on x,
                  and 0->+ top-to-bottom on z in self.topography.
                  x indexes the columns and z indexes the rows.
                  y deals with height and is unused.
        """

        # gleaned from TA3 map excel spreadsheet
        X_ZERO = -2225
        X_MAX = -2087

        # FIXME: check this is cast in the appropriate direction
        topography_x = math.ceil(x) - X_ZERO

        # validate
        if not X_ZERO <= x <= X_MAX:
            raise ValueError(f'Coordinate out of bounds: {x}')

        # z indexes rows, x indexes columns
        return topography_x

    @staticmethod
    def _convert_to_minecraft(r: int, c: int) -> Tuple[int, int]:
        """
        REQUIRES:
        EFFECTS:  Converts topography numpy array coordinates back to minecraft
                  coordinates
        Note: Not the inverted Map.convert_coords function. That's not invertible!
        """

        # gleaned from TA3 map excel spreadsheet
        X_ZERO = -2225
        X_MAX = -2087
        Z_ZERO = -11
        Z_MAX = 64  # inclusive

        # FIXME: check these are cast in the appropriate direction (esp. z)
        minecraft_x = c + X_ZERO
        minecraft_z = r + Z_ZERO

        # validate
        if not (X_ZERO <= minecraft_x <= X_MAX and Z_ZERO <= minecraft_z <= Z_MAX):
            raise ValueError(f'Coordinates out of bounds: {(minecraft_x, minecraft_z)}')

        # z indexes rows, x indexes columns
        return minecraft_x, minecraft_z

    def paths_to(self, start: Tuple[int, int], points: List[Tuple[int, int]],
                 c: Configuration) -> (List[List[Tuple[int, int]]], List[int]):
        """
        REQUIRES: start and all points are valid minecraft map coordinates
                  all p in points satisfy self.connected(*start, *p) (soft req)
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Returns coindexed list of paths from start point to each point in points
                  (effectively, computes a tree). Also returns the lengths of each path.
        """
        self.update(c)

        # stored path lookup
        paths = dict()
        for i, point in enumerate(points):
            lookup = self._lookup_path(*start, *point)
            if lookup is not None:
                paths[point] = lookup

        points_todo = [ p for p in points if p not in paths ]

        # connected check
        for dest in points_todo:
            # invariant: memo stored paths are already connected
            if not self.connected(start[0], start[1], dest[0], dest[1], c):
                raise ValueError(f'Point {dest} not reachable from {start}')

        paths.update(self._BFS(start[0], start[1], points_todo))

        # save computed paths
        for dest, path in paths.items():
            # stores distance automatically
            self._store_path(*start, dest[0], dest[1], path)

        # ensure order is correct
        paths = [ paths[dest] for dest in points ]
        # TODO: update lengths convention
        path_lengths = [ len(p) if len(p) > 1 else 0 for p in paths ]

        return paths, path_lengths

    def tsp_path_nn(self, points: List[Tuple[int, int]], c: Configuration,
                    method = "euclidean") -> (List[Tuple[int, int]], List[float]):
        """
        REQUIRES:
        EFFECTS:  Computes a greedy path to visit all locations in points.
                  Paths will always begin at points[0].
                  Returns the path, the segment lengths, and the total path length.
        """
        self.update(c)

        if method == "euclidean" or method == "pure_euclidean":
            dist_matrix = self.dist_matrix_euclidean(points)
        elif method == "pure_BFS":
            dist_matrix = self.dist_matrix(points, c)

        # greedily choose closest neighbor
        path_lengths = []
        path_i = [0]  # this is also the exclude_index
        current_i = 0
        while len(path_i) < len(points):
            vec = dist_matrix[current_i, :]  # consider problem from current victim
            vec[path_i] = np.inf  # never visit visted victims again
            min_ind = vec.argmin()  # find nearest neighbor (nn)
            if method == "euclidean":
                init_x = points[current_i][0]
                init_z = points[current_i][1]
                dest_x = points[min_ind][0]
                dest_z = points[min_ind][1]
                min_path = self.path(init_x, init_z, dest_x, dest_z, c)
                path_lengths.append(len(min_path))
            elif method == "pure_BFS" or method == "pure_euclidean":
                min_dist = vec[min_ind]
                path_lengths.append(min_dist)
            path_i.append(min_ind)  # add nn to path
            current_i = min_ind  # on to next victim

        assert not ( len(path_i) > len(set(path_i)) ), "repeated victim visit"

        # convert back to coordinates
        path = [ points[i] for i in path_i ]

        return path, path_lengths, path_i

    def tsp_path_nn_change_one(self, points: List[Tuple[int, int]],
                               c: Configuration,
                               distance_matrix, start_ind, change_var,
                               method = "pure_euclidean") -> (List[Tuple[int, int]], List[float]):
        """
        """
        assert method == "pure_euclidean", "only pure_euclidean allowed \
                                            as a method for this function"

        self.update(c)
        dist_matrix = distance_matrix.copy()

        x = np.array([val[0] for val in points])
        z = np.array([val[1] for val in points])

        # compute distance to change
        if type(change_var) is int:
            ind_to_change = change_var
            xr = x[ind_to_change]
            zr = z[ind_to_change]
            dist_vec = np.sqrt((x - xr)**2 + (z - zr)**2)
            dist_matrix[ind_to_change,:] = dist_vec
            dist_matrix[:,ind_to_change] = dist_vec
        elif type(change_var) is tuple:
            xz_to_add = change_var
            xr = xz_to_add[0]
            zr = xz_to_add[1]
            dist_vec = np.sqrt((x - xr)**2 + (z - zr)**2)
            dist_matrix = np.vstack((dist_matrix, dist_vec[:-1]))
            dist_matrix = np.hstack((dist_matrix, dist_vec.reshape((len(dist_vec),1))))

        # greedily choose closest neighbor
        path_lengths = []
        path_i = [start_ind]  # this is also the exclude_index
        current_i = start_ind
        while len(path_i) < len(points):
            vec = dist_matrix[current_i, :]  # consider problem from current victim
            vec[path_i] = np.inf  # never visit visted victims again
            min_ind = vec.argmin()  # find nearest neighbor (nn)
            min_dist = vec[min_ind]
            path_lengths.append(min_dist)
            path_i.append(min_ind)  # add nn to path
            current_i = min_ind  # on to next victim

        assert not ( len(path_i) > len(set(path_i)) ), "repeated victim visit"

        # convert back to coordinates
        path = [ points[i] for i in path_i ]

        return path, path_lengths, path_i


    @staticmethod
    def dist_matrix_euclidean(points: List[Tuple[int, int]]) -> np.ndarray:
        x = np.array([val[0] for val in points])
        z = np.array([val[1] for val in points])
        dist_mat = np.sqrt(np.subtract.outer(x,x)**2 + np.subtract.outer(z,z)**2)
        return (dist_mat).astype(float)


    def tsp_path(self, points: List[Tuple[int, int]], c: Configuration,
                 exact_threshold=30) -> (List[Tuple[int, int]], List[float]):
        """
        REQUIRES: self._check_if_open(p) for p in points
                  TODO: deal with victims being destinations and affecting topography
        EFFECTS:  Computes the best (or a near-best) path to visit all locations
                  in points. Returns the path, the segment lengths, and the total path length.
                  Will not compute exact TSP solutions if len(points) > exact_threshold.
        """
        self.update(c)

        dist_matrix = self.dist_matrix(points, c)

        ## check if all nodes are accessible
        #if (dist_matrix == np.inf).any():
        #    print(points)
        #    print(dist_matrix)
        #    print("WARNING: TSP maybe completely incorrect")

        # solve OPEN tsp problem: agent is not required to go back to the origin.
        dist_matrix[:, 0] = 0
        mode = 'heuristic' if len(points) > exact_threshold else 'exact'
        if mode == 'exact':
            path_i, total_length = solve_tsp_dynamic_programming(dist_matrix)
        elif mode == 'heuristic':
            path_i, total_length = solve_tsp_simulated_annealing(dist_matrix)
        else:
            raise ValueError(f'invalid mode: {mode}')

        # should always start at origin
        #assert(path_i[0] == 0)
        #assert(path_i[-1] != 0)  # shouldn't return

        # get segment lengths
        path_lengths = [dist_matrix[i, j] for i, j in pairwise(path_i) ]
        #assert(sum(path_lengths) == total_length)

        # convert back to coordinates
        path = [ points[i] for i in path_i ]

        return path, path_lengths

    def dist_matrix(self, points: List[Tuple[int, int]], c: Configuration) -> np.ndarray:
        """
        REQUIRES: self._connected(*p1, *p2) for p1, p2 in itertools.product(points) (soft req)
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Computes an adjacency matrix with travel distances between
                  each location in points given current topography.
                  Returns len(points) x len(points) array coindexed with points.
        """
        self.update(c)

        # initialize
        dist_matrix = np.ones((len(points), len(points))) * np.inf
        np.fill_diagonal(dist_matrix, 0)

        # loops through each pair of points once, with indices
        for start_idx, start in enumerate(points[:-1]):
            destinations = points[start_idx+1:]
            paths, distances = self.paths_to(start, destinations, c)
            dist_matrix[start_idx, start_idx+1:len(points)] = distances

        # make dist matrix symmetric
        dist_matrix = np.where(dist_matrix == np.inf, dist_matrix.T, dist_matrix)

        # FIXME: save for debugging
        # np.save('dist_matrix_tmp.npy', dist_matrix)

        return dist_matrix

    def _furniture_exception(self, x: float, z: float) -> Optional[Tuple[float, float]]:
        """
        REQUIRES: self.topography[self.convert_coords(x, z)] == self.FURNITURE
        EFFECTS:  Checks if (x, z) on furniture might be a precision error,
                  and returns Minecraft coordinates of closest open tile.
                  If it is clearly not a precision error returns None.
        """
        THRESHOLD_WIDTH = 0.1

        def euclidean(x1: float, z1: float, x2: int, z2: int) -> float:
            return math.sqrt((x1-x2)**2 + (z1-z2)**2)

        x_on_edge = math.ceil(x) - THRESHOLD_WIDTH < x < math.ceil(x) or \
                    math.floor(x) < x < math.floor(x) + THRESHOLD_WIDTH
        z_on_edge = math.ceil(z) - THRESHOLD_WIDTH < z < math.ceil(z) or \
                    math.floor(z) < z < math.floor(z) + THRESHOLD_WIDTH
        if not (x_on_edge or z_on_edge):
            # coordinate is too close to center of tile; no exception allowed
            return None

        r, c = self.convert_coords(x, z)
        # get possible spaces the player could be on
        possible_coords = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1),
                           (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]
        possible_coords = [ coord for coord in possible_coords
                            if self.topography[coord] == self.OPEN_SPACE ]

        # get center of available tiles in continuous Minecraft space
        mine_coords = [ self._convert_to_minecraft(r, c) for (r, c) in possible_coords ]
        # needs to be + because integers point to lowest edge
        mine_coords = [ (r+0.5, c+0.5) for r, c in mine_coords ]
        distances = [ euclidean(x, z, *p) for p in mine_coords ]

        min_dist = min(distances)
        return mine_coords[distances.index(min_dist)]

    def dist_matrix_regional(self, points: List[Tuple[int, int]],
                             c: Configuration, n_neighbors: int) -> np.ndarray:
        """
        REQUIRES: self._connected(*p1, *p2) for p1, p2 in itertools.product(points) (soft req)
        MODIFIES: self._path_memo, self._dist_memo
        EFFECTS:  Same as dist_matrix but restricted to n_neighbors
        """
        self.update(c)

        raise NotImplementedError

    # TODO: make static or require configuration update
    def visualize_astar_path(self, path: List[Tuple[int, int]]) -> None:
        """
        REQUIRES: each coord in path is valid index to self.topography
        EFFECTS:  plots the path on a topography map
        """
        img_mat = self.topography.copy()
        for i, j in path:
            img_mat[i, j] = 6

        plt.matshow(img_mat, interpolation='none')
        plt.show()

        return

    # TODO: make static/class method? or delete
    def plot_blank(self):
        """
        REQUIRES: self initiated with JUST WALLS AND FURNITURE (initial npy file)
        EFFECTS:  Plots map topography without rubble or victims or players, etc.
        """

        # check if extraneous junk in topography
        assert(set(np.unique(self.INITIAL_TOPOGRAPHY)) == {0, 2, np.inf})

        # color map
        # see https://stackoverflow.com/questions/9707676/
        # TODO: not necessary, just copied to speed imp
        cmap = colors.ListedColormap(['white', 'cyan', 'green', 'y', 'grey', 'black'])
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # create discrete matrix with linearly spaced values
        # demarking [open space, furniture, green victims, yellow victims, rubble, walls]
        WALLS_VAL = 5
        FURNITURE_VAL = 1
        OPEN_SPACE_VAL = 0

        image_matrix = self.INITIAL_TOPOGRAPHY.copy()
        # set walls (initially np.inf)
        image_matrix = np.where(image_matrix > 100, WALLS_VAL, image_matrix).astype(int)

        # furniture labeled as 2 in topography
        image_matrix = np.where(image_matrix == 2, FURNITURE_VAL, image_matrix)

        # plot
        paxesimage = plt.matshow(image_matrix, cmap=cmap, norm=norm)
        ax = paxesimage.axes

        #plt.show()
        return ax

    # TODO: make static method
    def plot(self, c: Configuration, annotate_rubble=False):
        """
        REQUIRES: self initiated with JUST WALLS AND FURNITURE.
        EFFECTS:  Plots map topography of configuration (without utilities)
        """

        # check if extraneous junk in topography
        assert(set(np.unique(self.INITIAL_TOPOGRAPHY)) == {self.OPEN_SPACE, self.FURNITURE,
                                                           self.WALL})

        # color map
        # see https://stackoverflow.com/questions/9707676/
        cmap = colors.ListedColormap(['white', 'cyan', 'green', 'y', 'grey', 'black'])
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # create discrete matrix with linearly spaced values
        # demarking [open space, furniture, green victims, yellow victims, rubble, walls]
        WALLS_VAL = 5
        RUBBLE_VAL = 4
        CRITICAL_VICTIM_VAL = 3
        REGULAR_VICTIM_VAL = 2
        FURNITURE_VAL = 1
        OPEN_SPACE_VAL = 0
        image_matrix = self.INITIAL_TOPOGRAPHY.copy()
        # set walls (initially np.inf)
        image_matrix = np.where(image_matrix > 100, WALLS_VAL, image_matrix).astype(int)

        # furniture labeled as 2 in topography
        image_matrix = np.where(image_matrix == 2, FURNITURE_VAL, image_matrix)

        # label rubble
        def label_rubble(rub: pd.Series, img_matrix: np.ndarray):
            if rub.status != 0:  # present
                row, col = self.convert_coords(rub.x, rub.z)

                # check for invalid rubble coordinates
                if img_matrix[row, col] == WALLS_VAL:
                    # have to skip this because some rubble blocks ARE in walls...
                    pass
                    #raise ValueError(f'Invalid coordinates for rubble: {(rub.x, rub.z)}'
                    #                 f' mapping to {(row, col)}')
                img_matrix[row, col] = RUBBLE_VAL
            return

        c.rubble_gt.apply(label_rubble, axis=1, img_matrix=image_matrix)

        # label victims
        def label_victim(v: pd.Series, img_matrix: np.ndarray):
            if v.status == 0:  # unsaved
                row, col = self.convert_coords(v.x, v.z)

                # check for invalid victim coordinates
                if img_matrix[row, col] == WALLS_VAL:
                    raise ValueError(f'Invalid coordinates for victim: {(v.x, v.z)}'
                                     f' mapping to {(row, col)}')

                img_matrix[row, col] = CRITICAL_VICTIM_VAL if v.victim_type == 'critical' \
                    else REGULAR_VICTIM_VAL
            return

        c.victims_gt.apply(label_victim, axis=1, img_matrix=image_matrix)

        # plot
        paxesimage = plt.matshow(image_matrix, cmap=cmap, norm=norm)
        ax = paxesimage.axes

        if annotate_rubble:
            # needed to look up rubble block id
            assert('block_id' in c.rubble_gt.columns)

            def annotate_rubble_block(rub: pd.Series, ax):
                # write rubble id next to rubble block
                if rub.status != 0:  # present
                    row, col = self.convert_coords(rub.x, rub.z)
                    label = rub.block_id  # block_id
                    # row denotes plotting y axis location, col denotes x axis location
                    # subtract 0.5 to attempt to center text
                    #ax.annotate(label, (col, row), xytext=(row, col), fontsize=0.3)
                    ax.text(col-0.25, row, label, fontsize=5)

            # Note: this does not handle overlapping rubbles well.
            c.rubble_gt.apply(annotate_rubble_block, axis=1, ax=ax)

        #plt.show()

        # maybe return something that makes main.plot_map_topology easier?
        return ax


"""
Preprocessing helpers; don't use these in model
"""


def map_to_csv(path: str, sheet: str) -> pd.DataFrame:
    """
    REQUIRES: path is valid path to an .xls (old excel) file. Yup. you read that correctly
              walls in that EXCEL file are marked with the color grey.
              Rubble is R, critical victims are Y, and noncritical victims
              are G. Furniture is F.
              sheet is a valid sheet name in excel file
    EFFECTS:  Parses the excel file and marks the walls with a much more reasonable
              strategy like the letter 'x'. Saves the resulting file to a csv.
              Prunes unnecessary info above map in the sheet
    """
    TA3_GREY = 48  # in excel's color indexing scheme...

    # use xlrd to get grey color
    # see https://stackoverflow.com/questions/47857112/
    wb = xlrd.open_workbook(path, formatting_info=True)
    sheet = wb.sheet_by_name(sheet)

    bgcol = np.zeros([sheet.nrows, sheet.ncols])

    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            cell = sheet.cell(row, col)
            fmt = wb.xf_list[cell.xf_index]
            bgcol[row, col] = fmt.background.background_colour_index

    colormask = pd.DataFrame(bgcol)
    colormask = colormask.iloc[1:, 1:]  # shave off coordinates

    # load actual excel file
    saturnA = pd.read_excel(path, sheet_name=sheet, index_col=0)

    # TODO: finish
    #saturnA.mask(colormask == TA3_GREY)

    return saturnA, colormask


def preprocess_map(path: str, just_walls_and_furn=False) -> np.ndarray:
    """
    REQUIRES: path is path to testbed Saturn map spec (with victims)
              extraneous info, like "Total Victims" cells, are already deleted
    EFFECTS:  Returns a numpy array that can be used to instantiate a Map obj
    """

    # turn saturn map into matrix
    topography = pd.read_csv(path, index_col=0)
    # replace walls with infinity and open space with zero
    topography = topography.where(topography != 'x', np.inf)
    topography = topography.where(topography.notna(), 0)

    # cannot jump on top of furniture
    topography = topography.where(topography != 'F', 2)

    if just_walls_and_furn:
        topography = topography.where(topography.isin([0, 2, np.inf]), 0)
    else:
        # TODO: assume victim and rubble locations are stored elsewhere
        # Replace victims with jump cost and rubble locations with infinite cost
        topography = topography.where(topography != 'Y', 1)
        topography = topography.where(topography != 'G', 1)
        # Players CANNOT jump on top of single rubble blocks
        topography = topography.where(topography != 'R', np.inf)
        topography = topography.where(topography != 'RR', np.inf)
        topography = topography.where(topography != 'RRR', np.inf)
        topography = topography.where(topography != 'YR', np.inf)
        topography = topography.where(topography != 'YRR', np.inf)
        topography = topography.where(topography != 'GR', np.inf)
        topography = topography.where(topography != 'GRR', np.inf)
        # TODO: test one liner for above
        #topography = topography.where(~topography.isin(['RR', 'RRR', 'YR', 'GR',
        #                                                'YRR', 'GRR']), np.inf)

    # preprocessing: fix typos in provided map
    topography = topography.where(topography != ' ', 0)
    topography = topography.where(topography != '  ', 0)
    topography = topography.where(topography != 'F ', 2)

    # truncate
    ROW_START_IDX = 3
    ROW_END_IDX = -5
    COL_START_IDX = 1
    COL_END_IDX = -1
    topography = topography.iloc[ROW_START_IDX:ROW_END_IDX, COL_START_IDX:COL_END_IDX]
    #assert(topography.iloc[0].name == -11)
    #assert(topography.iloc[-1].name == 61)
    #assert(topography.iloc[:, 0].name == '-2225')
    #assert(topography.iloc[:, -1].name == '-2087')

    topography = topography.to_numpy().astype(float)

    return topography


def main():

    file = 'SaturnA_topography.npy'
    m = Map(file)
    m.plot_blank()

    # attempt to plot map
    jwf = 'SaturnA_topography.npy'
    r_path = '../study2/preprocessed_data/rubble_T290_v1.csv'
    v_path = '../study2/preprocessed_data/victim_T290_v1.csv'
    c = get_SaturnA_starting_config(r_path, v_path)
    # rough
    c.rubble_gt.index.rename('block_id')
    m2 = Map(jwf)
    m2.plot(c, annotate_rubble=False)

    return 0


if __name__ == "__main__":
    main()
