"""
configuration.py

Defines configuration custom object.
For ASIST Study 3.

CoDaS Lab, 1/26/22
"""

import pandas as pd
from typing import List, Tuple


class Configuration:
    # here for convenience
    RUBBLE_COLUMNS = ['x', 'z', 'status', 'cluster_id']
    VICTIM_COLUMNS = ['x', 'y', 'z', 'victim_type', 'status']
    PLAYER_COLUMNS = ['player_id', 'map_knowledge', 'current_role', 'x', 'y', 'z', 'yaw',
                      'holding_victim']

    MODEL_KNOWLEDGE_CONDS = {'perfect', 'imperfect-shared', 'imperfect-indiv'}
    MODEL_UTILITY_CONDS = {'collaborative', 'individual'}

    # game state struct
    def __init__(self, rubble_info: pd.DataFrame, victims_info: pd.DataFrame,
                 players_info: pd.DataFrame, knowledge_cond='perfect',
                 utility_cond='collaborative', time=None, beliefs_info=None, score=None):
        """
        EXPECTS:
        victims_info: columns are [x, y (not useful), z,
                                   victim_type {"unknown", "normal", "critical"},
                                   (triage) status {0: unsaved, 1: triaged, 2: held unsaved,
                                                    3: held triaged (by scout)},
                      rows indexed by victim_id
        rubble_info: (updated 7/22/21)
                     columns are [x, z, status {0: removed, >=1: present}, cluster_id]
                     rows indexed by block_id
                     TODO: have status accurately reflect how many blocks stacked there
        players_info: len == 3, columns are [player_id,
                                             map_knowledge {TODO},
                                             current_role {medic, scout, rubbler}, x, y, z]
                                index is same as player_id
        knowledge_cond: in MODEL_KNOWLEDGE_CONDS
        utility_cond: in MODEL_UTILITY_CONDS
        beliefs_info: len == 3, dict from players_info.player_id to ProbMaps, if knowledge_cond is
                      imperfect-indiv
                      Otherwise a ProbMap directly.
        time: None or 0 <= time <= 60 sec/min * 15 minutes == 900
        score: None or 0 <= score <= (50 * 10) + (50 * 5) == 750
        """

        # # some basic checks
        # if sorted(rubble_info.columns) != sorted(self.RUBBLE_COLUMNS) \
        #         or sorted(victims_info.columns) != sorted(self.VICTIM_COLUMNS) \
        #         or sorted(players_info.columns) != sorted(self.PLAYER_COLUMNS):
        #     raise ValueError(f'Invalid configuration: columns are not correct')
        # if time is not None and not 0 <= time <= 905:
        #     raise ValueError(f'Invalid configuration: time not within 15 min: {time}')
        # if score is not None and not 0 <= score <= 751:
        #     raise ValueError(f'Invalid score, outside bounds: {score}')
        # # require time marking if passing uncertainty maps
        # if beliefs_info is not None and time is None:
        #     raise ValueError('time required if using uncertainty maps')

        # # enforce model conditions
        # if utility_cond not in self.MODEL_UTILITY_CONDS:
        #     raise ValueError(f'Invalid model utility condition: {utility_cond}')
        # if knowledge_cond not in self.MODEL_KNOWLEDGE_CONDS:
        #     raise ValueError(f'Invalid model knowledge condition: {knowledge_cond}')
        # elif knowledge_cond == 'perfect' and beliefs_info is not None:
        #     #raise ValueError('No need for belief ProbMaps if perfect knowledge assumed')
        #     print('No need for belief ProbMaps if perfect knowledge assumed')
        # elif knowledge_cond == 'imperfect-shared' and beliefs_info is dict:
        #     #raise ValueError('Use only one ProbMap for shared knowledge')
        #     print('Use only one ProbMap for shared knowledge')
        # elif knowledge_cond == 'imperfect-indiv':
        #     if beliefs_info is not None and (len(beliefs_info) != len(players_info)
        #        or set(beliefs_info.keys()) != set(players_info.player_id.unique())):
        #         #raise ValueError('ProbMaps do not match players')
        #         print('ProbMaps do not match players')

        # FIXME: check mission details elsewhere. Configurations no longer need
        #        to have 3 players and 55 victims
        #NUM_VICTIMS = 55
        #NUM_PLAYERS = 3
        #valid_input = len(victims_info) == NUM_VICTIMS
        #valid_input = valid_input and len(players_info) == NUM_PLAYERS

        #if not valid_input:
        #    raise ValueError(f'Invalid configuration')

        # initialize
        self.knowledge_cond = knowledge_cond
        self.utility_cond = utility_cond
        self.rubble_gt = rubble_info
        self.victims_gt = victims_info
        # TODO: freezing plate states
        self.players = players_info
        self.time = time
        self.score = score
        self.beliefs = beliefs_info

    def copy(self):
        """
        REQUIRES: columns in self.[rubble, victims, players] have not been edited
        EFFECTS: Instantiates and returns a deep copy of self.
                 Seems more pythonic for our purposes than something like the Big 3, etc.
        Be sure to call this when you want a fresh copy of the configuration
        (and not a tag of the same instance)
        """

        # make deep copies of uncertainty-relevant information
        if self.knowledge_cond == 'imperfect-indiv' and self.beliefs is not None:
            beliefs_copy = { player: prob_map.copy() if prob_map is not None else None
                             for player, prob_map in self.beliefs.items() }
        elif self.knowledge_cond == 'imperfect-shared' and self.beliefs is not None:
            beliefs_copy = self.beliefs.copy()
        else:
            beliefs_copy = None

        return Configuration(self.rubble_gt.copy(), self.victims_gt.copy(), self.players.copy(),
                             self.knowledge_cond, self.utility_cond, self.time, beliefs_copy,
                             self.score)

    @classmethod
    def make_empty_config(cls):
        """
        EFFECTS: Returns an empty configuration (no rubble, no victims).
                 Useful for initializing a Map object.
        """
        rubble_info = pd.DataFrame([], columns=cls.RUBBLE_COLUMNS)
        victim_info = pd.DataFrame([], columns=cls.VICTIM_COLUMNS)
        players_info = pd.DataFrame([], columns=cls.PLAYER_COLUMNS)
        return Configuration(rubble_info, victim_info, players_info)

    def get_medic_locations(self) -> List[Tuple[int, int]]:
        """
        EFFECTS: Returns a list of coordinates of all players
                 in medic roles. For convenience
        """

        raise NotImplementedError


# TODO: define action representation here? Categorical
# rubbler actions: one of rubble_cluster_id
# medic actions: one of victim_id
# TODO: scout actions


def get_SaturnA_starting_config(rubble_path: str, victims_path: str):
    """
    REQUIRES: both are paths to rubble_info df and victims_info df, resp
    EFFECTS:  Returns configuration based on files
    """

    rubble = pd.read_csv(rubble_path, index_col=0)
    victims = pd.read_csv(victims_path, index_col=0)
    # TODO: place players
    players = pd.DataFrame([], columns=Configuration.PLAYER_COLUMNS)

    return Configuration(rubble, victims, players)
