"""
belief.py

Generate and update uncertainty distributions over victims
via Field-of-Vision calculations on preprocessed data.
Used by rutgers_ac.py

ASIST Study 3

CoDaS Lab, 3/4/22
Sean Anderson
"""

import numpy as np
import pandas as pd
import json

from configuration_s3 import Configuration
from map_s3 import Map
from data_parsing_s3 import Mission
from fov import compute_fov, MARKED_VISIBLE
from typing import Dict, List, Tuple, Union
from data_prep import ROOM_SET

from scipy.special import comb
from scipy.stats import entropy
from scipy.special import entr

import logging
# logging.basicConfig(filename='log.log', level=logging.DEBUG, filemode='w')

class BeliefDiff:
    def __init__(self, mission: Mission, t: float, player_callsign: Dict):
        
        self.mission = mission
        self.t = t
        self.player_callsign = player_callsign

        self.memo = pd.DataFrame(columns=['N_c', 'N_r', 'N_R', 's_0', 's_r', 's_c', 
                                          'flag', 'entropy'])
        
        self.entropy_df = pd.DataFrame(columns=["room_id", "shared", 
                                                "RED_indiv", "BLUE_indiv", "GREEN_indiv",
                                                "RED_marker", "BLUE_marker", "GREEN_marker"])
        self.entropy_df["room_id"] = ROOM_SET
    
        self.first_entries = self.get_first_entries_all(self.mission, self.t)

        self.AC_belief_diff() #updates self.entropy_df
        
        
    def AC_belief_diff(self) -> pd.DataFrame:
        """
        REQUIRES: self.mission, self.t
        EFFECTS: updates self.entropy, self.memo
        """
        
        mission = self.mission
        t = self.t

        players = self.mission.players

        # shared
        # logging.debug("shared model\n")
        player_id = 'all'
        room_belief_df = self.get_room_belief(mission, player_id, t)
        self.entropy_df["shared"] = self.compute_rooms_entropy(room_belief_df).entropy.to_list()

        #  indiv and marker models
        for player_id in players:
            if self.player_callsign[player_id] == 'Red':
                # marker model
                # logging.debug("RED marker model\n")
                room_belief_df = self.get_room_belief(mission, player_id, t)
                self.entropy_df["RED_marker"] = self.compute_rooms_entropy(room_belief_df).entropy.to_list()
                # indiv model
                # logging.debug("RED indiv model\n")
                cut_belief_df = room_belief_df.copy()
                cut_belief_df["marker_no"] = np.nan
                cut_belief_df["marker_regular"] = np.nan
                cut_belief_df["marker_critical"] = np.nan
                self.entropy_df["RED_indiv"] = self.compute_rooms_entropy(cut_belief_df).entropy.to_list()
            elif self.player_callsign[player_id] == 'Green':
                # marker model
                room_belief_df = self.get_room_belief(mission, player_id, t)
                self.entropy_df["GREEN_marker"] = self.compute_rooms_entropy(room_belief_df).entropy.to_list()
                # indiv model
                cut_belief_df = room_belief_df.copy()
                cut_belief_df["marker_no"] = np.nan
                cut_belief_df["marker_regular"] = np.nan
                cut_belief_df["marker_critical"] = np.nan
                self.entropy_df["GREEN_indiv"] = self.compute_rooms_entropy(cut_belief_df).entropy.to_list()
            elif self.player_callsign[player_id] == 'Blue':
                # marker model
                room_belief_df = self.get_room_belief(mission, player_id, t)
                self.entropy_df["BLUE_marker"] = self.compute_rooms_entropy(room_belief_df).entropy.to_list()
                # indiv model
                cut_belief_df = room_belief_df.copy()
                cut_belief_df["marker_no"] = np.nan
                cut_belief_df["marker_regular"] = np.nan
                cut_belief_df["marker_critical"] = np.nan
                self.entropy_df["BLUE_indiv"] = self.compute_rooms_entropy(cut_belief_df).entropy.to_list()

        self.entropy_df.loc["overall"] = self.entropy_df.sum()
        self.entropy_df.loc["overall", "room_id"] = "overall"

        return self.entropy_df


    @staticmethod
    def get_first_entries_all(mission: Mission, t: float) -> pd.DataFrame:
        df = mission.mission
        m = df[df.time <= t].copy()
        m = m[(m.action == 'move')]
        m = m[m.z <= (Map.FOV_Z_MAX-0.5)]

        if len(m) == 0:
            return pd.DataFrame(columns=['location', 'time', 'player_id'])

        # in case m has no entry        
        # m['location'] = np.nan

        m['location'] = m.apply(lambda row: mission.find_room(row.x, row.z), axis=1)
        m = m[m.groupby(["location", "player_id"]).time.transform(min) == m.time]

        return m
    
    
    def get_first_entries_player(self, player_id: str) -> pd.DataFrame:
        df = self.first_entries
        if player_id == 'all':
            return df[df.groupby(["location"]).time.transform(min) == df.time]
        else:
            return df[df.player_id == player_id]


    def get_room_belief(self, mission: Mission, player_id: str, t: float) -> pd.DataFrame:
        """
        REQUIRES:
        EFFECTS:
        """
        # initialize
        room_belief_df = pd.DataFrame(columns = ["room_id", "explored", "signal", 
                                                "marker_no", "marker_regular", "marker_critical",
                                                "n_critical", "n_regular"])

        # assign room_id 
        room_belief_df['room_id'] = ROOM_SET

        # assign explored
        entry_t = self.get_first_entries_player(player_id)
        room_explored = entry_t.location.to_list()
        # room_belief_df["explored"] = room_belief_df.apply(lambda row: row.room_id in room_explored, axis=1)
        # apply is not much slower than the 3 lines below
        room_belief_df["explored"] = False
        inds = room_belief_df.room_id.isin(room_explored)
        room_belief_df.loc[inds, "explored"] = True

        # assign signal
        def get_message(s_t, room_id):
            msg = s_t[s_t.room_id == room_id].message.values
            if len(msg) == 1:
                return msg[0]
            else:
                return 'no_signal_triggered'

        if (player_id == 'all') or ('GREEN' in player_id):
            s_t = mission.get_signals_info_minimal(t)
            room_belief_df["signal"] = room_belief_df.apply(lambda row: get_message(s_t, row.room_id), axis=1)
        else:
            room_belief_df['signal'] = 'no_signal_triggered'

        # assign marker info
        marker_t = mission.get_markers_info(t)
        nearest_room_list = marker_t.nearest_room.to_list()
        inds = room_belief_df.room_id.isin(nearest_room_list)
        if np.sum(inds) > 0:
            room_belief_df.loc[inds, "marker_no"] = marker_t.novictim.to_list()
            room_belief_df.loc[inds, "marker_regular"] = marker_t.regularvictim.to_list()
            room_belief_df.loc[inds, "marker_critical"] = marker_t.criticalvictim.to_list()

        # assign n_critical and n_regular
        v_gt = mission.victims_ground_truth.copy()
        n_regular_gt = v_gt[v_gt.victim_type.isin(['A','B'])].groupby("room_name").victim_type.count()
        n_critical_gt = v_gt[v_gt.victim_type == 'C'].groupby("room_name").victim_type.count()

        def get_n_victim(n_victims_in_room: pd.Series, room_id:str):
            if room_id in n_victims_in_room.index:
                return n_victims_in_room[room_id]

        room_belief_df["n_critical"] = room_belief_df.apply(lambda row: 
                                                            get_n_victim(n_critical_gt, row.room_id), axis=1)
        room_belief_df["n_regular"] = room_belief_df.apply(lambda row: 
                                                        get_n_victim(n_regular_gt, row.room_id), axis=1)

        # # signal correction so that signal matches ground_truth
        # def signal_correction(signal, n_critical, n_regular):
        #     if signal is None:
        #         return None
        #     else:
        #         if ~np.isnan(n_critical):
        #             return 'critical'
        #         elif np.isnan(n_critical) and ~np.isnan(n_regular):
        #             return 'regular'
        #         else:
        #             return 'no'

        # temp = room_belief_df
        # temp['signal'] = temp.apply(lambda row: signal_correction(row.signal, 
        #                                           row.n_critical, row.n_regular), axis=1)

        return room_belief_df


    def compute_rooms_entropy(self, room_belief_df: pd.DataFrame) -> pd.DataFrame:
        """
        REQUIRES: room_beliefs with columns: 
                ["room_id", "explored", "signal", 
                "marker_no", "marker_regular", "marker_critical", 
                "n_critical", "n_regular"]
        EFFECTS: produce ent_df with columns: ["room_id", "entropy"]
        TERMINOLOGY:
            N_c: TOTAL_CRITICAL $-$ the number of critical victims in explored rooms
            N_r: TOTAL_REGULAR $-$ the number of regular victims in explored rooms
            N_R: TOTAL_ROOMS $-$ the number of explored rooms
            s_0: the number of unexplored rooms at whose hotspots the device signaled no victim
            s_r: the number of unexplored rooms at whose hotspots the device signaled regular victim
            s_c: the number of unexplored rooms at whose hotspots the device signaled critical victim
        """

        TOTAL_REGULAR = 20
        TOTAL_CRITICAL = 15
        TOTAL_ROOM = len(ROOM_SET)

        ent_df = pd.DataFrame(columns=["room_id", "entropy"])
        ent_df["room_id"] = ROOM_SET

        n_room_explored = room_belief_df.explored.sum()
        n_regular_explored = room_belief_df[room_belief_df.explored].n_regular.sum()
        n_critical_explored = room_belief_df[room_belief_df.explored].n_critical.sum()

        N_c = TOTAL_CRITICAL - n_critical_explored
        N_r = TOTAL_REGULAR - n_regular_explored
        N_R = TOTAL_ROOM - n_room_explored

        room_belief_df['merged_signal'] = np.nan
        for ind, row in room_belief_df.iterrows():
            # logging.debug(f"room {row['room_id']}; signal {row['signal']}")
            if row["signal"] != "no_signal_triggered":
                if row["signal"] == "No_Victim_Detected":
                    room_belief_df.loc[ind, "merged_signal"] = "no_victim"
                elif row["signal"] == "Regular_Victim_Detected":
                    room_belief_df.loc[ind, "merged_signal"] = "only_regular_victim"
                elif row["signal"] == "Critical_Victim_Detected":
                    room_belief_df.loc[ind, "merged_signal"] = "critical_victim"
            else:
                if row["marker_no"] > 0:
                    room_belief_df.loc[ind, "merged_signal"] = "no_victim"
                elif row["marker_regular"] > 0:
                    room_belief_df.loc[ind, "merged_signal"] = "only_regular_victim"
                elif row["marker_critical"] > 0:
                    room_belief_df.loc[ind, "merged_signal"] = "critical_victim"
                else:
                    room_belief_df.loc[ind, "merged_signal"] = "no_signal_triggered"

        rb = room_belief_df 
        s_0 = np.sum((rb.merged_signal == "no_victim") & (~rb.explored))
        s_r = np.sum((rb.merged_signal == "regular_victim") & (~rb.explored))
        s_c = np.sum((rb.merged_signal == "critical_victim") & (~rb.explored))

        for ind, row in ent_df.iterrows():
            # logging.debug( (f"room: {row['room_id']};"
            #               f"merged signal: {rb[rb.room_id == row['room_id']].merged_signal.item()}") )
            r_ind = rb.room_id == row['room_id']
            explored_flag = rb[r_ind].explored.item()
            no_victim_flag = rb[r_ind].merged_signal.item() == 'no_victim'
            regular_victim_flag = rb[r_ind].merged_signal.item() == 'only_regular_victim'
            critical_victim_flag = rb[r_ind].merged_signal.item() == 'critical_victim'
            if explored_flag or no_victim_flag:
                ent_df.loc[ind, "entropy"] = 0
            elif regular_victim_flag:
                ent_df.loc[ind, "entropy"] = self.compute_entropy('only_regular_victim_flag', 
                                                                  N_c, N_r, N_R, s_0, s_r, s_c)
            elif critical_victim_flag:
                ent_df.loc[ind, "entropy"] = self.compute_entropy('critical_victim_flag', 
                                                                  N_c, N_r, N_R, s_0, s_r, s_c)
            else: # no signal
                ent_df.loc[ind, "entropy"] = self.compute_entropy('no_signal_flag', 
                                                                  N_c, N_r, N_R, s_0, s_r, s_c)

        return ent_df


    def compute_entropy(self, flag, N_c, N_r, N_R, s_0, s_r, s_c):
        """
        REQUIRES: 
            memo: df containing computed oconfigurations
            flag in ["only_regular_victim_flag", "critical_victim_flag", "no_signal_flag"]
            N_c: TOTAL_CRITICAL $-$ the number of critical victims in explored rooms
            N_r: TOTAL_REGULAR $-$ the number of regular victims in explored rooms
            N_R: TOTAL_ROOMS $-$ the number of explored rooms
            s_0: the number of unexplored rooms at whose hotspots the device signaled no victim
            s_r: the number of unexplored rooms at whose hotspots the device signaled regular victim
            s_c: the number of unexplored rooms at whose hotspots the device signaled critical victim
        EFFECTS: produce an entropy from the above parameters, updates self.memo
        """
        
        m = self.memo
        match_ind  = (m.N_c == N_c) & (m.N_r == N_r) & (m.N_R == N_R) & \
                     (m.s_0 == s_0) & (m.s_r == s_r) & (m.s_r == s_r) & (m.flag == flag)

        # return value if computed before
        if np.sum(match_ind) == 1:
            return m[match_ind].entropy.item()

        # if not computed before, compute
        elif np.sum(match_ind) == 0:
            prob = np.zeros([4,4,4])

            log_c_denom = np.log(comb(N_c - s_c + N_R - s_0 - s_r - 1,\
                                    N_R - s_0 - s_r - 1))
            log_r_denom = np.log(comb(N_r - s_r + N_R - s_0 - 1,\
                                    N_R - s_0 - 1))

            n_c_max = int(min(4, N_c - s_c + 1))
            n_r_max = int(min(4, N_r - s_r + 1))

            if flag == "only_regular_victim_flag":
                for n_c in range(0, 1):
                    log_c_numer = np.log(comb(N_c - n_c - s_c + N_R - s_0 - s_r - 2,\
                                              N_R - s_0 - s_r - 2))
                    for n_r in range(1, n_r_max):
                        log_r_numer = np.log(comb(N_r - (n_r - 1) - s_r + N_R - s_0 - 2,\
                                                  N_R - s_0 - 2))
                        if (n_r_max == 1):
                            prob[n_c, n_r, 0] = np.exp(log_c_numer + log_r_numer - \
                                                    log_c_denom - log_r_denom)
                        for n_ab in range(1,n_r):
                            prob[n_c, n_r, n_ab+1] = np.exp(log_c_numer + log_r_numer - \
                                                    log_c_denom - log_r_denom - np.log(n_r))    
            elif (flag == "critical_victim_flag") and (n_c_max > 1):
                for n_c in range(1, n_c_max):
                    log_c_numer = np.log(comb(N_c - n_c - s_c + N_R - s_0 - s_r - 2,\
                                              N_R - s_0 - s_r - 2))
                    for n_r in range(0, n_r_max):
                        log_r_numer = np.log(comb(N_r - (n_r - 1) - s_r + N_R - s_0 - 2,\
                                                  N_R - s_0 - 2))
                        if (n_r_max == 1):
                            prob[n_c, n_r, 0] = np.exp(log_c_numer + log_r_numer - \
                                                    log_c_denom - log_r_denom)
                        for n_ab in range(0, n_r):
                            prob[n_c, n_r, n_ab+1] = np.exp(log_c_numer + log_r_numer - \
                                                    log_c_denom - log_r_denom - np.log(n_r))
            elif (flag == "critical_victim_flag") and (n_c_max == 1):
                n_c = 0
                log_c_numer = np.log(comb(N_c - n_c - s_c + N_R - s_0 - s_r - 2,\
                            N_R - s_0 - s_r - 2))
                for n_r in range(0, n_r_max):
                    log_r_numer = np.log(comb(N_r - (n_r - 1) - s_r + N_R - s_0 - 2,\
                                                N_R - s_0 - 2))
                    if (n_r_max == 1):
                        prob[n_c, n_r, 0] = np.exp(log_c_numer + log_r_numer - \
                                                log_c_denom - log_r_denom)
                    for n_ab in range(0, n_r):
                        prob[n_c, n_r, n_ab+1] = np.exp(log_c_numer + log_r_numer - \
                                                log_c_denom - log_r_denom - np.log(n_r))    
            elif flag == "no_signal_flag":
                for n_c in range(0, n_c_max):
                    log_c_numer = np.log(comb(N_c - n_c - s_c + N_R - s_0 - s_r - 2,\
                                              N_R - s_0 - s_r - 2))
                    for n_r in range(0, n_r_max):
                        log_r_numer = np.log(comb(N_r - (n_r - 1) - s_r + N_R - s_0 - 2,\
                                                  N_R - s_0 - 2))
                        if (n_r_max == 1):
                            prob[n_c, n_r, 0] = np.exp(log_c_numer + log_r_numer - \
                                                    log_c_denom - log_r_denom)
                        for n_ab in range(0, n_r):
                            prob[n_c, n_r, n_ab+1] = np.exp(log_c_numer + log_r_numer - \
                                                    log_c_denom - log_r_denom - np.log(n_r))  
            
            # room_ent = entr(prob.flatten()).sum() # unnormalized version
            room_ent = entropy(prob.flatten()) # normalized version
            
            # save computed value in memo
            self.memo = self.memo.append({'N_c':N_c, 'N_r':N_r, 'N_R':N_R, 
                                        's_0':s_0, 's_r':s_r, 's_c':s_c,
                                        'flag':flag, 'entropy':room_ent}, ignore_index=True)

            # logging.debug( (f"N_c:{N_c}, N_r:{N_r}, N_R:{N_R},"
            #                 f"s_0:{s_0}, s_r:{s_r}, s_c:{s_c}, flag:{flag}, entropy:{room_ent},"
            #                 f"non_zeros: {np.count_nonzero(prob)}") )

            return room_ent

        else:
            print('Memo in compute_entropy not functioning as expected')


# copied from study 2
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


def get_seen(x: int, z: int, yaw: float, m: Map) -> np.ndarray:
    """
    REQUIRES: (x, z) valid minecraft coordinate
              yaw is valid minecraft yaw
              m.update(desired configuration) already called
    EFFECTS:  Uses Map to get collection of topography coordinates
              of each square that was seen.
              Returns matrix of shape same as m.topography, where
              fov.py:MARKED_VISIBLE denotes seen tiles, and all other
              values denote unseen tiles
    """

    # convert to topography
    r, c = m.convert_coords(x, z)
    norm_yaw = normalize_yaw(yaw)

    # build map for fov code; requires walling off Saturn entranceway (still needed for study 3)
    # TODO: move this computation outside of the loop?
    fov_result = m.topography.copy()
    ENTRANCE_COORDS = [(-2156, 60), (-2155, 60), (-2153, 60), (-2152, 60)]
    for ex, ez in ENTRANCE_COORDS:
        fov_result[m.convert_coords(ex, ez)] = m.WALL

    # reverse coords; c is x axis and r is y axis
    compute_fov((c, r), norm_yaw, fov_result.copy(), fov_result, square_walls=True)

    #fov_coords = np.argwhere(fov_result == MARKED_VISIBLE)
    return fov_result


def get_victims_seen(fov_map: np.ndarray, m: Map, victim_r: pd.Series,
                     victim_c: pd.Series) -> np.ndarray:
    """
    REQUIRES: entity_type one of ['victim', 'rubble']
              fov_map has same shape as m.topography, includes some values fov.py:MARKED_VISIBLE
              victim_c.shape == victim_r.shape
    EFFECTS:  Returns subset of coordinates of fov_map where
              tile has entity on it. First col is row coords and second col is column coordinates
    """
    # fast match version, use this instead of hash table
    overlap_map = np.zeros_like(m.topography, dtype=bool)
    overlap_map[victim_r, victim_c] = True
    overlap_map = np.where(np.logical_and(fov_map == MARKED_VISIBLE, overlap_map), True, False)

    return np.argwhere(overlap_map)


def get_rubble_seen(fov_map: np.ndarray, m: Map, c: Configuration) -> List[Tuple[int, int]]:
    """
    REQUIRES: fov_map has same shape as m.topography, includes some values fov.py:MARKED_VISIBLE
    EFFECTS:  Returns subset of coordinates of fov_map where
              tile has rubble on it.
    """
    raise DeprecationWarning('no rubble beliefs in s3 models')
    overlap_map = np.full(m.topography.shape, False)

    rubble_c = c.rubble_gt[c.rubble_gt.status != 0].loc[:, 'x'].apply(m.convert_coords_x)
    rubble_r = c.rubble_gt[c.rubble_gt.status != 0].loc[:, 'z'].apply(m.convert_coords_z)
    overlap_map[rubble_r, rubble_c] = True
    seen = [ tile for tile in tiles_seen if overlap_map[tile] ]
    return seen


def update_victims_seen(mission_chunk: pd.DataFrame, rubble: pd.DataFrame,
                        victims: pd.DataFrame) -> (pd.DataFrame, Dict[str, np.ndarray]):
    """
    REQUIRES: mission_chunk has columns:
                x, z, player_id, yaw, time
              mission_chunk.z.min() > Map.FOV_Z_MAX
    MODIFIES: victims
    EFFECTS:  Computes earliest time seen (FOV) for each victim, and by which player.
              Assumes rubble config and victim locations do not change for duration of
              mission_chunk. Returns victims with appended columns (one for each player):
                {player_id}_saw_at_time
              Also returns map from player_id to tiles appearing in FoV during mission_chunk.
    """

    # build topography with rubble
    m = Map()
    c = m.get_configuration()  # respect the interface!
    c.rubble_gt = rubble
    m.update(c)

    all_tiles_seen = dict()

    # FoV loop
    for player in mission_chunk.player_id.unique():
        player_col_str = f'{player}_saw_at_time'
        player_victims_seen, player_tiles_seen = build_victim_belief_player(player, mission_chunk,
                                                                            victims, m)
        victims[player_col_str] = player_victims_seen[player_col_str]
        all_tiles_seen[player] = player_tiles_seen

    return victims, all_tiles_seen


def build_victim_belief_player(player_id: str, mission_chunk: pd.DataFrame, victims: pd.DataFrame,
                               m: Map) -> (pd.DataFrame, np.ndarray):
    """
    REQUIRES: player_id in mission_chunk.player_id
    EFFECTS:  Computes the time each victim in victims appeared in
              player player_id's FoV in m.topography. Returns COPY of victims with
              extra column: seen_at_time (np.nan if player did not see victim). Also
              returns a boolean matrix with tiles in topography that player_id
              has seen during the mission_chunk
    """
    time_seen = pd.Series(index=victims.index, name='time_seen')
    c = m.get_configuration()
    c.victims_gt = victims.copy()
    c.victims_gt['topography_c'] = c.victims_gt.x.apply(m.convert_coords_x)
    c.victims_gt['topography_r'] = c.victims_gt.z.apply(m.convert_coords_z)
    # to speed get_victims_seen computation
    victim_c = c.victims_gt[c.victims_gt.status == 0].loc[:, 'x'].apply(m.convert_coords_x)
    victim_r = c.victims_gt[c.victims_gt.status == 0].loc[:, 'z'].apply(m.convert_coords_z)

    c.victims_gt[f'{player_id}_saw_at_time'] = np.nan

    all_tiles_seen = np.zeros_like(m.topography, dtype=bool)

    def fov_row(action: pd.Series, mm: Map, cc: Configuration, victim_rr: pd.Series,
                victim_cc: pd.Series, r: pd.Series, tiles: np.ndarray):
        # REQUIRES: not action.x.isna(), action.z > Map.FOV_Z_MAX
        #           victim_rr.shape == victim_cc.shape, all values are valid mm.topography coords
        # MODIFIES: r, tiles
        # Computes which victims (if any) in c.victims_gt were in FoV of
        # x, z, and yaw in action. Marks action.time in r for victims that are.
        # Also checks locations in tiles that have appeared in tiles_seen at any point.
        tiles_seen = get_seen(action.x, action.z, action.yaw, mm)
        victims_seen = get_victims_seen(tiles_seen, mm, victim_rr, victim_cc)

        # mark all locations appearing in FoV
        #nptiles_seen = np.array(tiles_seen)
        #tiles[nptiles_seen[:, 0], nptiles_seen[:, 1]] = True
        #tiles = np.where(tiles_seen == MARKED_VISIBLE, True, tiles)
        new_tiles = np.argwhere(tiles_seen == MARKED_VISIBLE)
        tiles[new_tiles[:, 0], new_tiles[:, 1]] = True

        # keep earliest time a victim appears in FoV
        if len(victims_seen) > 0:
            # match coordinates to victims
            for victim_coord in victims_seen:
                victim_selection = cc.victims_gt.apply(lambda row: row.topography_r == victim_coord[0]
                                                                   and row.topography_c == victim_coord[1],
                                                       axis=1)
                victim = cc.victims_gt[victim_selection].iloc[0]
                idx = victim.name
                if np.isnan(r.loc[idx]) or action.time < r.loc[idx]:
                    # update
                    r.loc[idx] = action.time
        return

    selection = (mission_chunk.action == 'move') & (mission_chunk.z < Map.FOV_Z_MAX) & \
                (mission_chunk.player_id == player_id)
    mission_chunk[selection].apply(fov_row, args=(m, c, victim_r, victim_c,
                                                  time_seen, all_tiles_seen), axis=1)
    c.victims_gt[f'{player_id}_saw_at_time'] = time_seen

    return c.victims_gt.copy(), all_tiles_seen


def main():
    # simple testing script
    # load messages
    filename = 'subj_data/study-3_spiral-3_pilot_NotHSRData_TrialMessages_Trial-T000448_' \
               'Team-TM000074_Member-na_CondBtwn-ASI-UAZ-TA1_CondWin-na_Vers-1.metadata'
    with open(filename) as f:
        data_list = f.readlines()

    # simulate incoming messages
    topic_msg_list = [json.loads(l) for l in data_list]
    mission_raw = pd.json_normalize(topic_msg_list)
    BASE_MSG_N = 4000
    mission_raw_base = mission_raw[:BASE_MSG_N]
    mission_news = mission_raw[BASE_MSG_N:]

    return 0


if __name__ == "__main__":
    main()
