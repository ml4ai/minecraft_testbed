"""
prob_map.py

Generate and update uncertainty distributions over rubble and victims
via Field-of-Vision calculations on preprocessed data.
Used by data_parsing.py (and no others?)

ASIST Study 2

CoDaS Lab, 5/25/21
Sean Anderson
"""


import numpy as np
import pandas as pd
from configuration_s3 import Configuration
from map_s3 import Map
from fov import compute_fov, MARKED_VISIBLE
from preprocess_s3 import assign_rubble_clusters
import matplotlib.pyplot as plt
from typing import List, Tuple, Union


class ProbMap:
    # tile knowledge status constants
    UNKNOWN = 0
    LABELED = 1
    OBSERVED = 2
    # density map constants
    MINIMAL_PROBABILITY = 0.0001
    DENSITY_UNLABELED = -1

    RUBBLE_GUESS_PROB = 1 / 8
    RUBBLE_DENSITY_PROB = 0.98  # belief for static labeled rubble
    RUBBLE_TRAVEL_THRESHOLD = 0.75

    def __init__(self, base_topography: str, topography_regions: str,
                 victim_knowledge_maps: List[str], rubble_knowledge_maps: List[str],
                 total_victims=55):
        """
        REQUIRES: base_topography, topography_regions are valid paths to .npy files
                  victim/rubble_knowledge_maps are lists of valid .npy file paths
                  total_rubble is ground truth total number of tiles with rubble on them.
                  0 < total_rubble, total_victims
        """
        # save input vars for deepcopy
        self.INPUT_VARS = {'base_topography': base_topography,
                           'topography_regions': topography_regions,
                           'victim_knowledge_maps': victim_knowledge_maps,
                           'rubble_knowledge_maps': rubble_knowledge_maps,
                           'total_victims': total_victims}

        self.TOTAL_VICTIMS = total_victims
        self.rubble_seen_count = 0
        self.victim_seen_count = 0
        # mark which observed victims are critical
        self.which_are_critical = set()

        self.last_victim_sample = None
        self.last_rubble_sample = None

        if set(np.unique(np.load(base_topography))) != {Map.WALL, Map.FURNITURE, Map.OPEN_SPACE}:
            raise ValueError(f'Base file has more than just walls and furniture: {base_topography}')
        self.regions = np.load(topography_regions)

        self.initial_rubble_density = self._initialize_density(rubble_knowledge_maps,
                                                               base_topography,
                                                               entity_type='rubble')

        self.initial_victim_density = self._initialize_density(victim_knowledge_maps,
                                                               base_topography,
                                                               entity_type='victim')

        self.tile_status = self._initialize_observed(base_topography, self.initial_rubble_density,
                                                     self.regions)

        self.victim_distr = self._initialize_distr(base_topography, self.initial_victim_density,
                                                   entity_type='victim')
        # must be called after victim distr initialized
        self.rubble_distr = self._initialize_distr(base_topography,
                                                   self.initial_rubble_density, entity_type='rubble')

        if not self._check_invariant():
            raise ValueError(f'invariant check did not pass')

    def copy(self):
        """
        EFFECTS: Returns a deep copy of self
        """
        # fixme: not efficient
        pm_copy = ProbMap(**self.INPUT_VARS)

        pm_copy.rubble_seen_count = self.rubble_seen_count
        pm_copy.victim_seen_count = self.victim_seen_count
        pm_copy.which_are_critical = self.which_are_critical.copy()
        pm_copy.tile_status = self.tile_status.copy()
        pm_copy.rubble_distr = self.rubble_distr.copy()
        pm_copy.victim_distr = self.victim_distr.copy()

        return pm_copy

    def _check_invariant(self) -> bool:
        """
        EFFECTS: Returns True if rubble and victim distrs are valid, tile status is valid,
                 and initial densities are valid.
        """
        THRESHOLD = 0.0001

        # written by cases for easier debugging
        # TODO: maintain single unit of probability mass per entity?
        if abs(np.sum(self.victim_distr) - self.TOTAL_VICTIMS) > THRESHOLD:
            #raise UserWarning('Victim distr mass incorrect')
            # TODO: at least print something...
            #print(f'UserWarning: Victim distr mass incorrect: {np.sum(self.victim_distr)},'
            #      f' should be: {self.TOTAL_VICTIMS}')
            return False
        # TODO: don't know how many total rubble there are, need a different check
        #elif abs(np.sum(self.rubble_distr) - self.TOTAL_RUBBLE) > THRESHOLD:
        #    raise UserWarning('Rubble distr mass incorrect')
        #    #return False

        for distr in [self.victim_distr, self.rubble_distr]:
            if not (distr >= 0).all():
                return False

        for density in [self.initial_victim_density, self.initial_rubble_density]:
            check = np.where(density == ProbMap.DENSITY_UNLABELED, 0, density)
            if not (check >= 0).all() and (check <= 1.0).all():
                return False

        if set(np.unique(self.tile_status)) != {ProbMap.UNKNOWN, ProbMap.LABELED, ProbMap.OBSERVED}:
            return False

        # all checks passed
        return True

    @classmethod
    def _initialize_observed(cls, base_topography: str, initial_density: np.ndarray,
                             regions: np.ndarray) -> np.ndarray:
        """
        REQUIRES: np.unique(np.load(base_topography)) == [Map.WALL, Map.FURNITURE, Map.OPEN_SPACE]
                  initial_density.shape == np.load(base_topography).shape
                  initial_density
                  regions == -3 outside Saturn map area and nowhere else
        EFFECTS:  Initializes and returns a categorical map
                  with values {0: unknown/unobserved, 1: labeled, 2: observed}
                  Walls and furniture labeled as observed,
                  tiles with initial_density != 2 labeled as labeled, and the rest unknown.
        """

        base_map = np.load(base_topography)
        tile_status = initial_density.copy()
        tile_status = np.where(tile_status != cls.DENSITY_UNLABELED, cls.LABELED, tile_status)
        tile_status = np.where(tile_status == cls.DENSITY_UNLABELED, cls.UNKNOWN, tile_status)
        tile_status = np.where(base_map == Map.WALL, cls.OBSERVED, tile_status)

        # mark tiles outside map boundary as observed. -3 is region label for outside Saturn map
        tile_status = np.where(regions == -3, cls.OBSERVED, tile_status)

        # Furniture locations do not appear in static knowledge maps. If otherwise:
        tile_status = np.where(base_map == Map.FURNITURE, cls.OBSERVED, tile_status)
        return tile_status.astype(int)

    @classmethod
    def _initialize_density(cls, knowledge_maps: List[str], base_topography: str,
                            entity_type='victim') -> np.ndarray:
        """
        REQUIRES: knowledge_maps are valid paths to npy files
                  knowledge_maps are all of the same type (victim or rubble)
                  knowledge_maps have following conventions:
                        0 -> labeled very low (minimal) probability
                        2 -> unlabeled (no information)
                        value in (0, 2) -> density value
                  base_topography valid path to correct topography.npy file
        EFFECTS:  Initializes and returns an array with density values
                  combined from all knowledge_maps
                  Values are {-1: unknown, [0.0001, 1]: density value}
                  TODO: use log probabilities
        """

        if entity_type not in {'victim', 'rubble'}:
            raise ValueError(f'Not a valid entity type: {entity_type}')

        density_maps = [ np.load(m) for m in knowledge_maps ]
        base_map = np.load(base_topography)

        if len(density_maps) > 1:
            # combine them all
            initial_density = cls._combine_density(density_maps[0], density_maps[1])

            if len(density_maps) > 2:
                # chained addition
                for dm in density_maps[2:]:
                    initial_density = cls._combine_density(initial_density, dm)
        else:
            initial_density = density_maps[0]

        # convert to desired format
        # number from study2_preprocess.get_kmaps
        initial_density = np.where(initial_density == 2, cls.DENSITY_UNLABELED, initial_density)
        initial_density = np.where(initial_density == 0, cls.MINIMAL_PROBABILITY, initial_density)

        # make sure walls are observed
        initial_density = np.where(base_map == Map.WALL, 0.0, initial_density)
        # rest are density values

        # explicitly normalize density values to expected probmass in density
        if entity_type == 'victim':
            # count expected number of victims
            num_clusters = np.sum(initial_density == 1.0)
            scale_factor = num_clusters / np.sum(np.where(initial_density != cls.DENSITY_UNLABELED,
                                                          initial_density, 0))
            initial_density = np.where(initial_density != cls.DENSITY_UNLABELED,
                                       initial_density * scale_factor, cls.DENSITY_UNLABELED)

            #THRESHOLD = 0.0001
            #total = np.sum(np.where(initial_density != cls.DENSITY_UNLABELED,
            #                        initial_density, 0))
            #assert(abs(total - num_clusters) < THRESHOLD)
        elif entity_type == 'rubble':
            # rubble density marks are 1.0, already above travel threshold
            #initial_density = np.where(np.logical_and(initial_density < 1,
            #                                          initial_density > cls.MINIMAL_PROBABILITY),
            #                           1.0, initial_density)
            initial_density = np.where(initial_density > cls.RUBBLE_DENSITY_PROB,
                                       cls.RUBBLE_DENSITY_PROB, initial_density)
        return initial_density

    @staticmethod
    def _combine_density(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        REQUIRES: (a > 0).all(), (b > 0).all()
                  a == b where a, b nonzero
                  a.shape = b.shape
        EFFECTS:  Returns array with 0 where a and b are 0 and
                  a or b if one is nonzero.
        """
        THRESHOLD = 0.0001
        WALL = 0
        DENSITY_UNKNOWN = 2

        # check requires clause
        if not (a > -THRESHOLD).all() and (b > -THRESHOLD).all():
            raise ValueError('Either a or b has negatives')

        # FIXME: below is buggy
        a_ = np.where(b == WALL, WALL, a)
        b_ = np.where(a == WALL, WALL, b)
        if not np.array_equal(a_, b_):
            #raise ValueError('kmaps are not congruent on shared sections')
            # TODO: fix this and actually error out!
            pass
            #print('kmaps might not be congruent on shared sections!!')

        #result = np.add(a, np.where(np.logical_and(b != WALL, a == WALL), b, WALL))
        result = np.where(np.logical_and(a <= 1, a >= 0), a, b)
        result = np.where(np.logical_and(b <= 1, b >= 0), b, result)

        return result

    @staticmethod
    def _initialize_distr_blank(base_topography: str, regions: np.ndarray) -> np.ndarray:
        """
        REQUIRES: np.unique(np.load(base_topography)) == [Map.WALL, Map.FURNITURE, Map.OPEN_SPACE]
        EFFECTS:  Initializes and returns a probability map with uniform positive probability
                  on all open spaces and zero probability on walls and furniture.
                  TODO: use log probabilities
        """
        distr = np.load(base_topography)

        uniform = 1 / np.sum(distr == Map.OPEN_SPACE)
        distr = np.where(distr == Map.OPEN_SPACE, uniform, distr)

        distr = np.where(distr == Map.WALL, 0.0, distr)
        distr = np.where(distr == Map.FURNITURE, 0.0, distr)

        # mark regions outside map as 0 as well. -3 is region label for outside map
        distr = np.where(regions == -3, 0.0, distr)

        return distr

    def _initialize_distr(self, base_topography: str, initial_density: np.ndarray,
                          entity_type='victim') -> np.ndarray:
        """
        REQUIRES: np.unique(np.load(base_topography)) == [Map.WALL, Map.FURNITURE, Map.OPEN_SPACE]
                  np.unique(initial_density) == [self.UNKNOWN, 0 through 1.0]
                  self.tile_status, self.regions initialized
                  if entity_type == 'rubble', self.victim_distr already initialized
        EFFECTS:  Initializes and returns a probability map with uniform positive probability
                  on all open spaces and zero probability on walls and furniture.
                  TODO: use log probabilities
        """

        if entity_type == 'victim':
            total_entities = self.TOTAL_VICTIMS

            distr = self._initialize_distr_blank(base_topography, self.regions)

            distr = np.where(self.tile_status == self.LABELED, initial_density, distr)
            grey_prob = self._grey_tile_prob_victim(total_entities, 0, self.tile_status, distr)
            distr = np.where(self.tile_status == self.UNKNOWN, grey_prob, distr)
            return distr

        elif entity_type == 'rubble':
            distr = self._initialize_distr_blank(base_topography, self.regions)
            distr = np.where(self.tile_status == self.LABELED, initial_density, distr)

            # # initial distribution is rubble surrounding hypothetical victims
            # possible_victims = self.sample_destinations('victim')
            # coords = possible_victims.sort_values('marginal').iloc[:self.TOTAL_VICTIMS][['x', 'z']]
            #
            # # get tiles surrounding coords
            # def add_surrounding_coords(row: pd.Series, tiles: List) -> None:
            #     # MODIFIES: tiles
            #     r, c = Map.convert_coords(row.x, row.z)
            #     neighbors = [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c),
            #                  (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
            #     # avoid walls
            #     neighbors = [ n for n in neighbors if distr[n] > self.MINIMAL_PROBABILITY ]
            #     tiles.extend(neighbors)
            #     return None
            # surrounding_tiles = list()
            # coords.apply(add_surrounding_coords, tiles=surrounding_tiles, axis=1)
            #
            # surrounding_tiles = np.array(surrounding_tiles)
            # stiles_x, stiles_y = surrounding_tiles[:, 0], surrounding_tiles[:, 1]
            #
            # distr[stiles_x, stiles_y] = self.RUBBLE_GUESS_PROB
            return distr

        else:
            raise ValueError(f'Not a valid distr type: {entity_type}')

    @classmethod
    def _grey_tile_prob_rubble(cls, total_entities_observed: int, tile_status: np.ndarray,
                               prob_map: np.ndarray) -> float:
        """
        REQUIRES: tiles_status values are {0: unknown, 1: labeled but unobserved, 2: observed}
                  hence np.unique(tiles_status) == [0, 1, 2]
                  tiles_status.shape == prob_map.shape
        EFFECTS:  Computes the degree of belief that an entity is
                  present on an unobserved, unknown (unlabeled) tile.
                  TODO: use log probabilities

        See equation updates under heading 2021-05-05 in
        https://docs.google.com/document/d/1GMdwaFL1X92MCAgc2fI98xNHVhN6m6HoWTNBK9TWXHA/
        edit?usp=sharing
        """
        # just assume same as initialization
        raise UserWarning("Don't update unknown tiles in rubble distr")

    @classmethod
    def _labeled_tile_probs_rubble(cls, total_entities_observed: int,
                                   tiles_status: np.ndarray, prob_map: np.ndarray,
                                   alpha=1.0) -> np.ndarray:
        """
        REQUIRES: tiles_status values are {0: unknown, 1: labeled but unobserved, 2: observed}
                  hence np.unique(tiles_status) == [0, 1, 2]
                  tiles_status.shape == prob_map.shape
        ?MODIFIES:?
        EFFECTS:  Computes the degree of belief that entity is present
                  on tiles that have already been labeled with density.
                  Returns a ndarray the same size as prob_map
                  with updated prob values where tiles_status == 1.
                  TODO: use log probabilities

        See equation updates under heading 2021-05-05 in
        https://docs.google.com/document/d/1GMdwaFL1X92MCAgc2fI98xNHVhN6m6HoWTNBK9TWXHA/
        edit?usp=sharing
        """
        raise UserWarning("Don't update labeled tiles after rubble distr initialized")

    @classmethod
    def _grey_tile_prob_victim(cls, total_entities: int, total_entities_observed: int,
                               tile_status: np.ndarray, prob_map: np.ndarray) -> float:
        """
        REQUIRES: tiles_status values are {0: unknown, 1: labeled but unobserved, 2: observed}
                  hence np.unique(tiles_status) == [0, 1, 2]
                  0 <= total_entities_observed <= total_entities
                  tiles_status.shape == prob_map.shape
        EFFECTS:  Computes the degree of belief that an entity is
                  present on an unobserved, unknown (unlabeled) tile.
                  TODO: use log probabilities

        See equation updates under heading 2021-05-05 in
        https://docs.google.com/document/d/1GMdwaFL1X92MCAgc2fI98xNHVhN6m6HoWTNBK9TWXHA/
        edit?usp=sharing
        """

        num_unobserved_tiles = np.sum(tile_status == cls.UNKNOWN)
        labeled_probmass = np.sum(np.where(tile_status == cls.LABELED, prob_map, 0))

        prob = total_entities - total_entities_observed - labeled_probmass
        prob = prob / num_unobserved_tiles

        return prob

    @classmethod
    def _labeled_tile_probs_victim(cls, total_entities: int, total_entities_observed: int,
                                   tiles_status: np.ndarray, prob_map: np.ndarray,
                                   alpha=1.0) -> np.ndarray:
        """
        REQUIRES: tiles_status values are {0: unknown, 1: labeled but unobserved, 2: observed}
                  hence np.unique(tiles_status) == [0, 1, 2]
                  0 <= total_entities_observed <= total_entities
                  tiles_status.shape == prob_map.shape
        ?MODIFIES:?
        EFFECTS:  Computes the degree of belief that entity is present
                  on tiles that have already been labeled with density.
                  Returns a ndarray the same size as prob_map
                  with updated prob values where tiles_status == 1.
                  TODO: use log probabilities

        See equation updates under heading 2021-05-05 in
        https://docs.google.com/document/d/1GMdwaFL1X92MCAgc2fI98xNHVhN6m6HoWTNBK9TWXHA/
        edit?usp=sharing
        """
        num_unobserved_tiles = np.sum(tiles_status == cls.UNKNOWN)
        labeled_probmass = np.sum(np.where(tiles_status == cls.LABELED, prob_map, 0))
        updated = (alpha * prob_map * (total_entities - total_entities_observed)) / \
                  (alpha * labeled_probmass + num_unobserved_tiles)
        updated = np.where(tiles_status == cls.LABELED, updated, prob_map)

        return updated

    @classmethod
    def _labeled_tile_probs_victim_alt(cls, total_entities: int, total_entities_observed: int,
                                       tiles_status: np.ndarray, initial_density: np.ndarray,
                                       grey_tile_prob: float, alpha=1.0) -> np.ndarray:
        """
        REQUIRES: tiles_status values are {0: unknown, 1: labeled but unobserved, 2: observed}
                  hence np.unique(tiles_status) == [0, 1, 2]
                  0 <= total_entities_observed <= total_entities
                  tiles_status.shape == prob_map.shape == initial_density.shape
                  0 <= grey_tile_prob <= 1.0
        EFFECTS:  Computes the degree of belief that entity is present
                  on tiles that have already been labeled with density.
                  Returns a ndarray the same size as prob_map
                  with updated prob values where tiles_status == 1.
                  See https://codaslab.slack.com/archives/D018XFYU2P6/
                  p1626118687016600?thread_ts=1626112913.005800&cid=D018XFYU2P6
                  TODO: use log probabilities

        See equation updates under heading 2021-05-05 in
        https://docs.google.com/document/d/1GMdwaFL1X92MCAgc2fI98xNHVhN6m6HoWTNBK9TWXHA/
        edit?usp=sharing
        """
        MAX_VALUE = 0.99

        num_unobserved_tiles = np.sum(tiles_status == cls.UNKNOWN)
        initial_labeled_probmass = np.sum(np.where(tiles_status == cls.LABELED, initial_density, 0))

        numerator = initial_density * (total_entities - total_entities_observed)
        denom = initial_labeled_probmass + grey_tile_prob * num_unobserved_tiles / alpha
        result = numerator / denom

        # cap values at 0.99
        result = np.where(result > MAX_VALUE, MAX_VALUE, result)

        return result

    def update_observed(self, tiles_seen: List[Tuple[int, int]],
                        victims_seen: List[Tuple[int, int]],
                        critical_victims_seen: List[Tuple[int, int]],
                        rubble_seen: List[Tuple[int, int]]) -> None:
        """
        REQUIRES: tiles_seen, victims_seen, rubble_seen are Map topography coordinates
                  i.e. 0 <= (r, c) < tile_status.shape, distr.shape
                  victims_seen, rubble_seen are subsets of tiles_seen
                  critical_victims_seen is a subset of victims_seen
        MODIFIES: self.[victim&rubble]_distr, self.[victim&rubble]_seen_count, self.tile_status
        EFFECTS:  Updates distribution to reflect newly observed tiles. Also updates
                  internal parameters and labeled and unknown tiles.
        EXPECTS:  All tiles_seen not in victims_seen or rubble_seen are assumed to have no entities
        """

        # update unique victims observed count
        count = [ 1 if self.tile_status[r, c] != self.OBSERVED else 0 for r, c in victims_seen ]
        self.victim_seen_count += sum(count)

        # update unique rubble blocks observed count
        r_count = [ 1 if self.tile_status[r, c] != self.OBSERVED else 0 for r, c in rubble_seen ]
        self.rubble_seen_count += sum(r_count)

        # mark seen tiles as observed
        # see https://stackoverflow.com/questions/41900738 for indexing explanation
        # TODO: use tiles_seen as numpy array?
        tiles_seen_r, tiles_seen_c = zip(*tiles_seen)
        self.tile_status[tiles_seen_r, tiles_seen_c] = self.OBSERVED

        self._update_observed_victims(tiles_seen_r, tiles_seen_c, victims_seen,
                                      critical_victims_seen)
        self._update_observed_rubble(tiles_seen_r, tiles_seen_c, rubble_seen)

        # TODO: remove
        self._check_invariant()
        return

    def _update_observed_victims(self, tiles_seen_r: List[int], tiles_seen_c: List[int],
                                 victims_seen: List[Tuple[int, int]],
                                 critical_victims_seen: List[Tuple[int, int]]) -> None:
        """
        REQUIRES: tiles_seen_r, tiles_seen_c are coindexed
                  self.tile_status[tiles_seen_r, tiles_seen_c] == self.OBSERVED
                  self.victim_seen_count includes victims in victims_seen
        MODIFIES: self.victim_distr
        EFFECTS:  Updates victim belief distr according to equations in game plan doc.
        """

        # update directly observed tiles
        # TODO: log probabilities
        self.victim_distr[tiles_seen_r, tiles_seen_c] = 0.0
        # this will update victims that were initially observed as unsaved and now observed after
        # they were saved correctly
        if len(victims_seen) > 0:
            victims_seen_r, victims_seen_c = zip(*victims_seen)
            self.victim_distr[victims_seen_r, victims_seen_c] = 1.0
            self.which_are_critical.update(critical_victims_seen)

        # update labeled and unknown tiles
        #labeled_tiles_update = self._labeled_tile_probs_victim(self.TOTAL_VICTIMS,
        #                                                       self.victim_seen_count,
        #                                                       self.tile_status, self.victim_distr)
        grey_tiles_update = self._grey_tile_prob_victim(self.TOTAL_VICTIMS, self.victim_seen_count,
                                                        self.tile_status, self.victim_distr)
        labeled_tiles_update = self._labeled_tile_probs_victim_alt(self.TOTAL_VICTIMS,
                                                                   self.victim_seen_count,
                                                                   self.tile_status,
                                                                   self.initial_victim_density,
                                                                   grey_tiles_update)
        self.victim_distr = np.where(self.tile_status == self.LABELED, labeled_tiles_update,
                                     self.victim_distr)
        self.victim_distr = np.where(self.tile_status == self.UNKNOWN, grey_tiles_update,
                                     self.victim_distr)
        return

    def _update_observed_rubble(self, tiles_seen_r: List[int], tiles_seen_c: List[int],
                                rubble_seen: List[Tuple[int, int]]) -> None:
        """
        REQUIRES: tiles_seen_r, tiles_seen_c are coindexed
                  self.tile_status[tiles_seen_r, tiles_seen_c] == self.OBSERVED
                  self.rubble_seen_count includes rubble in rubble_seen
        MODIFIES: self.rubble_distr
        EFFECTS:  Updates rubble belief distr according to equations in game plan doc.
        """
        # update directly observed tiles
        self.rubble_distr[tiles_seen_r, tiles_seen_c] = 0.0
        if len(rubble_seen) > 0:
            rubble_seen_r, rubble_seen_c = zip(*rubble_seen)
            self.rubble_distr[rubble_seen_r, rubble_seen_c] = 1.0

        # leave rest of tiles be...
        return

    def _sample_destinations_helper(self, entity_type='victim',
                                    rubble_locs=None) -> Tuple[List[Tuple[int, int]],
                                                               List[float]]:
        """
        REQUIRES: entity_type is victims or rubble
                  np.unique(self.regions) contains range(1, self.regions.max()+1)
                  (i.e. it starts at 1 and counts upwards)
                  self.regions.dtype == int
                  rubble_locs do not completely cover any region
        EFFECTS:  Samples one tile per region (defined in self.regions) from entity distr,
                  unless that region has 0 marginal probability. Does NOT sample actually
                  observed victims, those need to be added later.
                  Returns list of tile coordinates in Map.topography system. Also returns
                  a coindexed list of marginal probabilities for each victim.
                  If rubble_locs is passed, don't sample locations in rubble_locs.
        """
        THRESHOLD = 0.0001

        rng = np.random.default_rng()

        # iterative version (todo: vectorize)
        locs, marginals = list(), list()
        for r_i in range(1, self.regions.max()+1):
            # set up distr in this region
            distr = self.victim_distr if entity_type == 'victim' else self.rubble_distr
            distr_region = np.where(self.regions == r_i, distr, 0)
            # remove directly observed victims
            distr_region = np.where(self.tile_status != self.OBSERVED, distr_region, 0.0)
            # remove labeled victims...

            # skip regions with 0 probability
            region_marginal = distr_region.sum()
            if region_marginal < THRESHOLD:
                continue

            # prep region for sampling
            coords = np.argwhere(distr_region > 0)
            # leave out coords with ground truth rubble...
            if rubble_locs is not None:
                coords = np.array([ tuple(c) for c in coords if tuple(c) not in rubble_locs ])
                if len(coords) == 0:
                    # skip this sample if no tiles left
                    continue
            distr_region = distr_region / distr_region.sum()

            # sample location from this region
            probs = distr_region[coords[:, 0], coords[:, 1]]
            probs = probs / probs.sum()
            loc = tuple(rng.choice(coords, p=probs))
            assert(loc not in rubble_locs)

            locs.append(loc)
            marginals.append(region_marginal)

        if entity_type == 'victim':
            assert(abs(sum(marginals) - (self.TOTAL_VICTIMS - self.victim_seen_count)) < 0.0001,
                   'marginals of sampled belief victims is not correct')
        return locs, marginals

    def _package_victim_dest_sample(self, sampled_locs: List[Tuple[int, int]],
                                    marginals: List[float]) -> pd.DataFrame:
        """
        REQUIRES: sampled_locs and marginals coindexed
                  sampled_locs does not include directly observed victims
        EFFECTS:  Returns a dataframe in close-to-configuration.victims_gt format
                  with sampled_locs as regular victim destinations. Also included
                  in result are directly observed victims with their ground truth type (critical
                  or regular). Columns x and z will have topography coordinates, not minecraft
                  coordinates.
        """

        # just written here from minecraft coord system, most likely Y is unused
        DEFAULT_Y = 60
        UNSAVED_STATUS = 0

        regions = [ self.regions[r, c] for r, c in sampled_locs ]

        # FIXME: needed?
        sampled_victim_types = [ "normal" if loc not in self.which_are_critical else "critical"
                                 for loc in sampled_locs ]

        sampled_victims = [ (r, DEFAULT_Y, c, v_type, UNSAVED_STATUS, marginal, reg)
                            for (r, c), v_type, marginal, reg in zip(sampled_locs, sampled_victim_types,
                                                                     marginals, regions) ]
        sampled_df = pd.DataFrame(sampled_victims,
                                  columns=Configuration.VICTIM_COLUMNS+['marginal', 'region'])
        sampled_df['observed'] = False

        # add directly observed victims
        actual_victim_locs = np.argwhere(np.logical_and(self.tile_status == self.OBSERVED,
                                                        self.victim_distr > 0.9999))
        actual_victim_regions = [ self.regions[r, c] for r, c in actual_victim_locs ]
        actual_victim_types = [ 'normal' if tuple(loc) not in self.which_are_critical else 'critical'
                                for loc in actual_victim_locs ]
        actual_victims = [ (r, DEFAULT_Y, c, v_type, UNSAVED_STATUS, 1.0, reg)
                           for (r, c), v_type, reg in zip(actual_victim_locs, actual_victim_types,
                                                          actual_victim_regions) ]
        actual_df = pd.DataFrame(actual_victims,
                                 columns=Configuration.VICTIM_COLUMNS+['marginal', 'region'])
        actual_df['observed'] = True

        complete_sample = pd.concat((sampled_df, actual_df))
        return complete_sample

    def _package_rubble_dest_sample(self, sampled_locs: List[Tuple[int, int]],
                                    marginals: List[float]) -> pd.DataFrame:
        """
        REQUIRES: sampled_locs and marginals coindexed
                  sampled_locs does not include directly observed victims
                  sampled_locs are not contiguous (unless at the edges of neighboring regions),
                  i.e. they are assumed to be from different rubble clusters.
        EFFECTS:  Returns a dataframe in close-to-configuration.rubble_gt format
                  with sampled_locs as rubble block destinations. Also included
                  in result are directly observed rubble blocks.
                  Columns x and z will have topography coordinates, not minecraft
                  coordinates.
        """
        DEFAULT_Y = 60
        PRESENT_STATUS = 1

        # package directly observed rubble blocks
        # look for probabilities above self.RUBBLE_DENSITY_PROB
        actual_rubble_locs = np.argwhere(np.logical_and(self.tile_status == self.OBSERVED,
                                                        self.rubble_distr > 0.99))
        # match Configuration.RUBBLE_COLUMNS order
        actual_rubble = [ (r, c, PRESENT_STATUS, -1, 1.0) for (r, c) in actual_rubble_locs ]
        actual_df = pd.DataFrame(actual_rubble, columns=Configuration.RUBBLE_COLUMNS+['marginal'])
        actual_df['observed'] = True

        actual_df = assign_rubble_clusters(actual_df)
        next_cluster = actual_df.cluster_id.max() + 1

        # package hypothesized rubble blocks
        sampled_rubble = [ (r, c, PRESENT_STATUS, i+next_cluster, m)
                           for i, ((r, c), m) in enumerate(zip(sampled_locs, marginals)) ]
        sampled_df = pd.DataFrame(sampled_rubble, columns=Configuration.RUBBLE_COLUMNS+['marginal'])
        sampled_df['observed'] = False

        complete_sample = pd.concat((actual_df, sampled_df))
        return complete_sample

    def sample_destinations(self, entity_type='victim', rubble_locs=None) -> pd.DataFrame:
        """
        REQUIRES: entity_type is victims or rubble
                  np.unique(self.regions) contains range(1, self.regions.max()+1)
                  (i.e. it starts at 1 and counts upwards)
                  self.regions.dtype == int
        EFFECTS:  Samples one tile per region (defined in self.regions) from entity distr.
                  Returns list of tile coordinates in Map.topography system.
                  Victim IDs are NOT CONSISTENT.
        TODO: include believed 'critical' victims in sample
        """

        if entity_type == 'rubble' and rubble_locs is not None:
            raise ValueError('Pass rubble_locs=None with entity_type rubble')

        sampled_locs, marginals = self._sample_destinations_helper(entity_type,
                                                                   rubble_locs=rubble_locs)

        if entity_type == 'victim':
            complete_sample = self._package_victim_dest_sample(sampled_locs, marginals)
        elif entity_type == 'rubble':
            complete_sample = self._package_rubble_dest_sample(sampled_locs, marginals)
        else:
            raise ValueError(f'Invalid entity type: {entity_type}')

        # convert back to minecraft coordinates
        def converter(row: pd.Series) -> pd.Series:
            x, z = Map._convert_to_minecraft(row.x, row.z)
            return pd.Series([x, z], index=['x', 'z'])
        complete_sample[['x', 'z']] = complete_sample.apply(converter, axis=1)

        # UNIQUE VICTIM IDs required for utility.get_utilities_medic
        complete_sample.reset_index(drop=True, inplace=True)

        # FIXME: are we accounting for scenario that player1 observes victim
        #        and before player1 sees victim again, player2 saves it,
        #        but player1 still believes it is unsaved?

        # save for easier plotting (note: will be overwritten every time called.
        #                           also won't be copied)
        if entity_type == 'victim':
            self.last_victim_sample = complete_sample
        elif entity_type == 'rubble':
            self.last_rubble_sample = complete_sample

        return complete_sample

    def plot(self, player: str, trial_num: int, traj=None, entity_type='victim', save=True,
             topography_file='SaturnB_1.6_topography_v1.npy', tile_status=True):
        """
        REQUIRES: traj is pd.DataFrame if passed
                  player in traj.player_id.unique()
        EFFECTS:  Constructs a heatmap of the current entity_type distribution.
                  Labels the plot with player id, timestamp and trial number.
                  Plots trajectory if passed.
        """

        if entity_type not in {'victim', 'rubble'}:
            raise ValueError(f'{entity_type} is not a valid entity type')

        distr = self.victim_distr if entity_type == 'victim' else self.rubble_distr

        axesimage = plt.matshow(distr)
        ax = axesimage.axes

        # add colormap legend
        plt.colorbar(axesimage)

        # plot walls
        topography = np.load(topography_file)
        wall_coords = np.argwhere(topography.T == Map.WALL)
        wall_coords_x, wall_coords_z = wall_coords[:, 0], wall_coords[:, 1]
        ax.scatter(wall_coords_x, wall_coords_z, s=1.0, color='black', marker='s')
        ## color map
        ## see https://stackoverflow.com/questions/9707676/
        #cmap = colors.ListedColormap(['black'])
        #bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        #norm = colors.BoundaryNorm(bounds, cmap.N)
        #plt.matshow(topography, fignum=False, )

        # plot observed tiles
        if tile_status:
            observed_mask = np.logical_and(self.tile_status.T == self.OBSERVED,
                                np.logical_and(self.regions.T != -3,
                                np.logical_and(topography.T != Map.WALL,
                                               topography.T != Map.FURNITURE)))
            observed_coords = np.argwhere(observed_mask)
            observed_x, observed_z = observed_coords[:, 0], observed_coords[:, 1]
            ax.scatter(observed_x, observed_z, s=1.0, color='white', marker='s',
                       alpha=0.5)

        # remove axis labeling
        ax.axis('off')

        if traj is not None:
            # edited code from main.save_map_traj on 7/14/21
            X_ZERO = -2225
            Z_ZERO = -11
            Z_MAX = 72
            x = traj[traj.player_id == player].x.to_numpy() - X_ZERO
            z = traj[traj.player_id == player].z.to_numpy() - Z_ZERO
            x_trunc = x[z <= Z_MAX]
            z_trunc = z[z <= Z_MAX]
            ax.scatter(x_trunc, z_trunc, s=0.2, color='white')

        # annotate information
        if traj is not None:
            title = f'T{trial_num} @ t={traj.time.max()}: {player} {entity_type}'
            filename = f'figures/T{trial_num}_t{traj.time.max()}_{player}_{entity_type}_probmap.pdf'
        else:
            title = f'T{trial_num}: {player} {entity_type}'
            filename = f'figures/T{trial_num}_{player}_{entity_type}_probmap.pdf'
        ax.set_title(title)

        if save:
            plt.savefig(filename)
        else:
            plt.show()

        return axesimage


def normalize_yaw(m_yaw: float) -> float:
    """
    REQUIRES: -360 <= yaw <= 360
    EFFECTS:  normalizes yaw to interval [0, 360]
              in clockwise direction
    see https://darpa-asist.slack.com/archives/CPHABHZ42/p1617125386034600
    """
    n_yaw = (m_yaw / 2)
    if n_yaw < 0:
        n_yaw = 360 + n_yaw
    return n_yaw


def get_seen(x: int, z: int, yaw: float, m: Map) -> List[Tuple[int, int]]:
    """
    REQUIRES: (x, z) valid minecraft coordinate
              yaw is valid minecraft yaw
              m.update(desired configuration) already called
    EFFECTS:  Uses Map to get collection of topography coordinates
              of each square that was seen. TODO Returns a np.ndarray with
              first column being row coordinates and second column being col coordinates
    """

    # convert to topography, TODO: then to fov matrix coords?
    r, c = m.convert_coords(x, z)
    norm_yaw = normalize_yaw(yaw)

    # build map for fov code; requires walling off Saturn entranceway
    fov_result = m.topography.copy()
    ENTRANCE_COORDS = [(-2156, 61), (-2155, 61), (-2153, 61), (-2152, 61)]
    for ex, ez in ENTRANCE_COORDS:
        fov_result[m.convert_coords(ex, ez)] = m.WALL

    # reverse coords; c is x axis and r is y axis
    compute_fov((c, r), norm_yaw, fov_result.copy(), fov_result, square_walls=True)

    fov_coords = np.argwhere(fov_result == MARKED_VISIBLE)
    # TODO: consider returning these in their original np.ndarray format
    #return fov_coords
    return [(r, c) for r, c in fov_coords]


def get_entities_seen_old(tiles_seen: List[Tuple[int, int]], m: Map, c: Configuration,
                          entity_type='victim') -> Union[List[Tuple[int, int]],
                                                         Tuple[List[Tuple[int, int]],
                                                               List[Tuple[int, int]]]]:
    """
    REQUIRES: entity_type one of ['victim', 'rubble']
              tiles_seen in m.topography coordinates
    EFFECTS:  Returns subset of coordinates in tiles_seen where
              tile has entity on it. If entity_type is 'victim', returns an additional
              list marking which tiles have critical victims on them.
    """
    raise DeprecationWarning('this implementation too slow')
    converter = lambda r: m.convert_coords(r.x, r.z)

    # for speed
    tiles_seen_set = set(tiles_seen)

    if entity_type == 'victim':
        # FIXME: seeing a triaged victim may break distr sum... see line 451.
        victim_coords = c.victims_gt[c.victims_gt.status != 2].apply(converter, axis=1)
        seen = victim_coords[victim_coords.isin(tiles_seen_set)]
        critical_victim_coords = victim_coords[c.victims_gt.victim_type == 'critical']
        criticals_seen = critical_victim_coords[critical_victim_coords.isin(tiles_seen_set)]
        return seen.tolist(), criticals_seen.tolist()
    elif entity_type == 'rubble':
        rubble_coords = c.rubble_gt[c.rubble_gt.status != 0].apply(converter, axis=1)
        seen = rubble_coords[rubble_coords.isin(tiles_seen_set)]
        return seen.tolist()
    else:
        raise ValueError(f'Invalid entity type: {entity_type}')


def get_entities_seen(tiles_seen: List[Tuple[int, int]], m: Map, c: Configuration,
                      entity_type='victim') -> Union[List[Tuple[int, int]],
                                                     Tuple[List[Tuple[int, int]],
                                                           List[Tuple[int, int]]]]:
    """
    REQUIRES: entity_type one of ['victim', 'rubble']
              tiles_seen in m.topography coordinates
    EFFECTS:  Returns subset of coordinates in tiles_seen where
              tile has entity on it. If entity_type is 'victim', returns an additional
              list marking which tiles have critical victims on them.
    """
    if entity_type == 'victim':
        # fast match version, use this instead of hash table
        overlap_map = np.zeros_like(m.topography)

        victim_c = c.victims_gt[c.victims_gt.status == 0].loc[:, 'x'].apply(m.convert_coords_x)
        victim_r = c.victims_gt[c.victims_gt.status == 0].loc[:, 'z'].apply(m.convert_coords_z)
        victim_critical_c = victim_c[c.victims_gt.victim_type == 'critical']
        victim_critical_r = victim_r[c.victims_gt.victim_type == 'critical']

        overlap_map[victim_r, victim_c] = 1
        overlap_map[victim_critical_r, victim_critical_c] = 2

        seen = [ tile for tile in tiles_seen if (overlap_map[tile] == 1 or overlap_map[tile] == 2) ]
        criticals_seen = [ tile for tile in tiles_seen if overlap_map[tile] == 2 ]
        return seen, criticals_seen
    elif entity_type == 'rubble':
        overlap_map = np.full(m.topography.shape, False)

        rubble_c = c.rubble_gt[c.rubble_gt.status != 0].loc[:, 'x'].apply(m.convert_coords_x)
        rubble_r = c.rubble_gt[c.rubble_gt.status != 0].loc[:, 'z'].apply(m.convert_coords_z)
        overlap_map[rubble_r, rubble_c] = True
        seen = [ tile for tile in tiles_seen if overlap_map[tile] ]
        return seen
    else:
        raise ValueError(f'Invalid entity type: {entity_type}')
