"""
data_parsing.py

Defines Mission data structure.
Implements all functionality that interacts
directly with preprocessed mission files.
Study 3 pilot version

CoDaS Lab, 1/18/22
"""

import pandas as pd
import numpy as np
import logging
from typing import Union, Dict, List, Tuple, Generator, Optional
from map_s3 import Map
from configuration_s3 import Configuration
import prob_map

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(filename='log.log', level=logging.DEBUG)


class Mission:
    SMALL_UTILITY = 0.01

    def __init__(self, mission_df, rubble_df, victims_df, 
                 topography_regions_file='preprocessed_data/room_name_s3.npy',
                 plate_coord_csv='preprocessed_data/plate_coord.csv',
                 knowledge_cond = "none", utility_cond="none",
                 map_knowledge_cond='gt'):
        """
        REQUIRES: mission_file is valid path to preprocessed mission csv file.
                  knowledge/utility_cond are valid model conditions (see Configuration def)
                  topography_regions_file is valid path to .npy file.
                  map_knowledge_cond is of form:
                    Saturn[A|B]_[1|2|3|5|6]4
        """

        if map_knowledge_cond != 'gt' and knowledge_cond != 'imperfect-indiv':
            raise ValueError(f'for now, only specify a static knowledge map'
                             f'in individual knowledge condition')

        self.mission = mission_df

        self.topography_file = 'preprocessed_data/topography.npy'

        self.knowledge_cond = knowledge_cond
        self.utility_cond = utility_cond

        self.init_rubble_info = rubble_df
        self.victims_ground_truth = victims_df

        self.topography_regions_file = topography_regions_file
        self.map_regions = np.load(topography_regions_file, allow_pickle=True)
        
        self.plate_coord = pd.read_csv(plate_coord_csv)

        self.players = self.mission.player_id.unique()

        # mark when players first enter the Saturn map area (after initial role selection)
        # self.mission_start = self._get_mission_start_time()

        self.rubble_log = self._build_rubble_log()
        self.victims_log = self._build_victims_log()
        self.markers_log = self._build_markers_log()
        self.signals_log = self._build_signals_log()
        # self.door_open_log = self._build_door_open_log()

        # self.changepoints = self._mark_changepoints()  # to speed up uncertainty

        # for map inference
        # self.mission_map_kind = mission_map
        # self.player_static_maps = self.mission.groupby('player_id').map_knowledge_cond \
        #                                       .first().to_dict()
        # self.static_map_cond = map_knowledge_cond

    def _get_mission_start_time(self):
        """
        REQUIRES: self.mission
        EFFECTS:  gets the first timestamp where at least one player is in Saturn map area
                  and all players have at least one 'move' action recorded (x and z coordinates
                  defined)
        """
        guess = self.mission[self.mission.z < Map.FOV_Z_MAX].iloc[0].time
        if len(self.mission[(self.mission.time <= guess) &
                            self.mission.z.notna()].player_id.unique()) < len(self.players):
            # revise time to make sure all players have coordinates
            guess = self.mission[self.mission.z < Map.FOV_Z_MAX].iloc[3].time
            # might as well error here
            if len(self.mission[(self.mission.time <= guess) &
                                self.mission.z.notna()].player_id.unique()) < len(self.players):
                logging.debug('Cannot find a start time')
                raise NotImplementedError
        return guess

    def get_configuration(self, t: float, with_uncertainty=False) -> Configuration:
        """
        REQUIRES: t is valid timestamp of mission
        EFFECTS:  Packages game state information at time t,
                  returns a configuration with victim, rubble, and player state
        """
        rubble_info = self.get_rubble_info(t)  # these are ground truth
        victims_info = self.get_victims_info(t)
        players_info = self.get_players_info(t)
        score = self.get_score(t)

        if with_uncertainty and self.knowledge_cond == 'imperfect-shared':
            beliefs = self.get_config_uncertainty_shared([t])[0]
        elif with_uncertainty and self.knowledge_cond == 'imperfect-indiv':
            beliefs = dict()
            for player in players_info.player_id:
                pm = self.get_config_uncertainty([t], player)[0]
                beliefs[player] = pm
        else:
            beliefs = None

        return Configuration(rubble_info, victims_info, players_info, time=t, beliefs_info=beliefs,
                             knowledge_cond=self.knowledge_cond, utility_cond=self.utility_cond,
                             score=score)

    def get_configurations(self, times: List[float], with_uncertainty=False) -> List[Configuration]:
        """
        REQUIRES: times are valid timestamps of mission
        MODIFIES: times
        EFFECTS:  Packages game state information at each time in times,
                  returns a list of configurations coindexed with sorted(times).
        Note:     Implemented so get_config_uncertainty can yield probmaps iteratively
        """
        times = sorted(times)

        rubble_infos = [ self.get_rubble_info(t) for t in times ]
        victims_infos = [ self.get_victims_info(t) for t in times ]
        players_infos = [ self.get_players_info(t) for t in times ]
        scores = [ self.get_score(t) for t in times ]

        # TODO: make get_config_uncertainties a generator, and exploit here? Making this a generator?
        if with_uncertainty and self.knowledge_cond == 'imperfect-shared':
            beliefs = self.get_config_uncertainty_shared(times)
        elif with_uncertainty and self.knowledge_cond == 'imperfect-indiv':
            beliefs_by_player = dict()
            player_ids = players_infos[0].player_id.unique()  # TODO: remove this in favor of self.players
            for player in player_ids:
                player_beliefs = self.get_config_uncertainty(times, player)
                beliefs_by_player[player] = player_beliefs
            beliefs = [ { p: bs[i] for p, bs in beliefs_by_player.items() }
                        for i in range(len(times)) ]
        else:
            beliefs = [None] * len(times)

        # package results
        result = [ Configuration(r, v, p, time=t, score=score, beliefs_info=b,
                                 knowledge_cond=self.knowledge_cond,
                                 utility_cond=self.utility_cond)
                   for r, v, p, b, t, score in zip(rubble_infos, victims_infos,
                                                   players_infos, beliefs, times, scores) ]
        return result

    def _timestep_range(self, times: List[float], interval=0.3) -> Generator[float, None, None]:
        """
        REQUIRES: times in sorted order
                  times[0] >= self.mission_start
        EFFECTS:  Returns a generator yielding increasing times at every TIMESTEP_INTERVAL,
                  except giving a time in times when it gets close enough, i.e.
                  (t - TIMESTEP_INTERVAL < times < t + TIMESTEP_INTERVAL). First yield is
                  the mission_start timestamp. Also each yielded
                  float is guaranteed to be in self.mission.time.unique()
        """
        if times[0] < self.mission_start:
            raise ValueError(f'Players have not entered Saturn map yet at time {times[0]}. '
                             f'Use Mission.mission_start as starting time')

        times_idx = 0
        t = self.mission_start
        while t < times[-1] and times_idx < len(times):
            # check if close to a desired timestamp
            if t + interval > times[times_idx]:  # TODO: remove + interval
                t = times[times_idx]
                times_idx += 1
                yield t
            else:
                # find closest time t in mission timestamps
                timestamp = self.mission[self.mission.time <= t].iloc[-1].time
                yield timestamp
            t += interval

    def _tile_timestep_range(self, times: List[float], player: str) -> Generator[float, None, None]:
        """
        REQUIRES: player in self.players_info
        EFFECTS:  Returns a generator yielding increasing times, where each time
                  is when the player crosses a tile boundary, except giving a time
                  in tmies when it gets close enough. First yield is
                  the mission_start timestamp. Each yielded float is guaranteed
                  to be in self.mission.time.unique()
        """
        INTERVAL = 0.3

        # parse necessary parts of trajectory
        player_traj_mask = (self.mission.player_id == player) & (self.mission.action == 'move')
        player_traj = self.mission[player_traj_mask][['x', 'z', 'time']]
        player_traj.index = player_traj.time
        player_traj.x = player_traj.x.astype(int)  # truncation is okay for this comparison
        player_traj.z = player_traj.z.astype(int)

        times_idx = 0
        t = self.mission_start
        # TODO: possible key error here with imperfect-indiv, T432 9.652?
        x, z = player_traj.loc[t, ['x', 'z']]
        while t < times[-1] and times_idx < len(times):
            # check if close to a desired timestamp
            if t + INTERVAL > times[times_idx]:
                t = times[times_idx]
                times_idx += 1
                yield t
            else:
                # find closest time t in mission timestamps
                timestamp = self.mission[self.mission.time <= t].iloc[-1].time
                yield timestamp
            # get next tile crossing
            t = player_traj[(player_traj.time > t) &
                            ((player_traj.x != x) | (player_traj.z != z))].iloc[0].time

    def get_config_uncertainty_shared(self, times: List[float],
                                      incremental=True) -> List[prob_map.ProbMap]:
        """
        REQUIRES: 0 < t < mission end for t in times
        MODIFIES: times
        EFFECTS:  Constructs and builds ProbMap at each time t in times.
                  prob maps will be returned in sorted order based on times. times
                  will be sorted as well. If incremental is True, build prob map by
                  passing through every timestep until highest t. May be slower than
                  using fov log. ProbMap is built with fov updates from every player at
                  every time.
                  TODO: make a generator?
        """
        raise DeprecationWarning(f'carryover from study 2 code, will be dropped')
        # TODO: reduce code duplication with get_config_uncertainty?
        TIMESTEP_INTERVAL = 0.2  # sec

        if self.knowledge_cond != 'imperfect-shared':
            raise UserWarning('Only use this with imperfect shared knowledge.')
        if not incremental:
            raise NotImplementedError('skipping a smarter way of doing this')

        times = sorted(times)

        # get density maps for all players
        if self.static_map_cond == 'gt':
            player_static_maps = self.mission.map_knowledge_cond.unique()
        else:
            player_static_maps = self.static_map_cond
        player_densities = [ extract_knowledge_maps(sm, self.mission_map_kind)
                             for sm in player_static_maps ]
        # see https://stackoverflow.com/questions/12974474 for an explanation
        victim_densities, rubble_densities = [ list(t) for t in zip(*player_densities) ]

        pm_list = list()
        m = Map(self.topography_file)
        pm = prob_map.ProbMap(self.topography_file, self.topography_regions_file,
                              victim_densities, rubble_densities, len(self.victims_ground_truth))

        prev_t = 0
        for t in self._timestep_range(times, TIMESTEP_INTERVAL):
            c = self.get_configuration(t, with_uncertainty=False)
            player_coords = c.players[['x', 'z', 'yaw']].to_numpy()

            # only call map update if we've passed or hit a changepoint (should speed up)
            if not np.array_equal((self.changepoints <= t), (self.changepoints < prev_t)):
                m.update(c)

            # get all tiles seen by players at this time
            tiles_seen = list()
            for x, z, yaw in player_coords:
                # skip fov for players not inside the map area yet
                if z > m.FOV_Z_MAX:
                    continue
                tiles_seen.extend(prob_map.get_seen(x, z, yaw, m))

            # skip if no players in map area
            if len(tiles_seen) == 0:
                continue

            # update distr
            victims_seen, criticals_seen = prob_map.get_entities_seen(tiles_seen, m, c,
                                                                      entity_type='victim')
            rubble_seen = prob_map.get_entities_seen(tiles_seen, m, c, entity_type='rubble')
            pm.update_observed(tiles_seen, victims_seen, criticals_seen, rubble_seen)

            if t in times:
                # won't work if all times are before all players have entered Saturn area
                pm_list.append(pm.copy())
            prev_t = t

        return pm_list

    def get_config_uncertainty(self, times: List[float], player=None,
                               incremental=True) -> List[prob_map.ProbMap]:
        """
        REQUIRES: 0 < t < mission end for t in times
                  player in pd.unique(self.mission.player_id)
        MODIFIES: times
        EFFECTS:  Constructs and builds ProbMap for player at each time t in times.
                  prob maps will be returned in sorted order based on times. times
                  will be sorted as well. If incremental is True, build prob map by
                  passing through every timestep until highest t. May be slower than
                  using fov log. Use only with imperfect-indiv knowledge cond
                  TODO: make this a generator?
        """
        TIMESTEP_INTERVAL = 0.2  # sec

        if self.knowledge_cond != 'imperfect-indiv':
            raise UserWarning('Only use this with imperfect individual knowledge.')

        times = sorted(times)

        # get player information
        if self.static_map_cond == 'gt':
            player_static_map = self.mission[self.mission.player_id == player]\
                                    .iloc[0].map_knowledge_cond
        else:
            player_static_map = self.static_map_cond
        victim_density, rubble_density = extract_knowledge_maps(player_static_map,
                                                                self.mission_map_kind)

        pm_list = list()

        if incremental:
            m = Map(self.topography_file)
            pm = prob_map.ProbMap(self.topography_file, self.topography_regions_file,
                                  [victim_density], [rubble_density], len(self.victims_ground_truth))

            # update at each timestep incrementally!
            prev_t = 0
            for t in self._timestep_range(times, interval=TIMESTEP_INTERVAL):
                # unpack agent loc and get map
                c = self.get_configuration(t, with_uncertainty=False)
                x, z, yaw = tuple(c.players.loc[player][['x', 'z', 'yaw']])

                # only call map update if we've passed or hit a changepoint (should speed up)
                if not np.array_equal((self.changepoints <= t), (self.changepoints < prev_t)):
                    m.update(c)

                # if player hasn't entered Saturn map area yet, skip this timestep
                if z > m.FOV_Z_MAX:
                    # FIXME: if this is a desired timestep, mark as None to prevent analysis...
                    if t in times:
                        pm_list.append(None)
                    continue

                # fov calculations
                tiles_seen = prob_map.get_seen(x, z, yaw, m)
                victims_seen, criticals_seen = prob_map.get_entities_seen(tiles_seen, m, c,
                                                                          entity_type='victim')
                rubble_seen = prob_map.get_entities_seen(tiles_seen, m, c, entity_type='rubble')

                # update
                pm.update_observed(tiles_seen, victims_seen, criticals_seen, rubble_seen)

                if t in times:
                    # FIXME: won't work if all times are before player has entered Saturn area?
                    pm_list.append(pm.copy())
                prev_t = t

        else:
            raise NotImplementedError
            # initialize probmap
            # get changepoints before t
            # get configuration for each of those changepoints, build a map for each
            # ProbMap.update_observed for tiles_seen, entities seen, in each of these... separately!

        # return resulting ProbMap
        return pm_list

    def get_rubble_info(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.init_rubble_info, self.rubble_log
                  self.rubble_log.columns[3]
                  self.rubble_log coindexed with self.init_rubble_info
        EFFECTS: Returns rubble_info at or just before t;
                 format same format as init_rubble_info but with updated status
        """
        REMOVED_STATUS = 0
        PRESENT_STATUS = 1

        rubble_info = self.init_rubble_info.copy()

        # should be quite fast, see https://stackoverflow.com/questions/41588034
        rub_log_values = self.rubble_log.values
        rubble_info.status = np.where(rub_log_values[:, self.RUBBLE_LOG_TIMEREMOVED_IDX] <= t,
                                      REMOVED_STATUS, PRESENT_STATUS)

        # FIXME: assumes removing one rubble at a location removes
        #        all rubble at that location. Can't match based on coordinates
        #        because y value of rubble changes (Minecraft gravel block).
        #        This is incorrect, should use rubble.status to count remaining blocks
        #        and turn rubble_info into a pure 2D representation
        #for i, pos in log.iterrows():
        #    bool_inds = (self.init_rubble_info['x'] == pos['x']) & \
        #                (self.init_rubble_info['z'] == pos['z'])
        #                # (self.init_rubble_info['y'] == pos['y']) & \

        #    # if np.sum(bool_inds) > 1:
        #    #     raise Exception("More than 1 rubble matched action!")
        #    # hacking to say that if all stack of rubbles are removed at once

        #    rubble_info.loc[bool_inds, 'status'] = 0

        return rubble_info


    def get_near_critical_time(self, player_mv: pd.DataFrame) -> pd.DataFrame:
        """
        REQUIRES: player_mv with columns [player_id, x, z, action, time, location]
        EFFECTS: output ee columns ['player_id', 'time', 'location', 'near_critical', 'exit']
        """
        
        # ee stands for entries and exits
        ee = player_mv.copy()

        # find all the times when location changes
        ee = player_mv[player_mv.ne(player_mv.shift()).location].reset_index()

        # get critical rooms
        v_gt = self.victims_ground_truth.copy()
        critical_rooms = v_gt[v_gt.victim_type == 'C'].room_name.unique()

        # find the earliest time player is near critical victim in location
        ee['near_critical'] = np.nan
        ee['exit'] = np.nan
        for ind, row in ee.iterrows():
            # the [:2] below is because H1A is coded as H1 in v_gt, 
            # similarly for other rooms with A
            if row['location'][:2] in critical_rooms:
                t_enter = row['time']
                t_exit = ee.loc[ind+1].time
                ee.loc[ind, 'exit'] = t_exit
                v_t = self.get_victims_info_minimal(t_enter)
                v_c = v_t[(v_t.victim_type == 'C') & (v_t.action.isnull())]
                mv = player_mv[(player_mv.time >= t_enter) & (player_mv.time <= t_exit)].copy()
                for v_ind, v_row in v_c.iterrows():
                    mv_ind = ((mv.x - v_row['x'])**2 + (mv.z - v_row['z'])**2) < 9
                    if np.sum(mv_ind) > 0:
                        ee.loc[ind, 'near_critical'] = mv[mv_ind].iloc[0].time
        
        return ee[ee.exit > 0][['player_id', 'time', 'location', 'near_critical', 'exit']]


    def get_markers_info(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.markers_log
        EFFECTS: Returns df at or just before t
                    columns: nearest_room, criticalvicitm, regularvictim, novictim
        """

        # initialize type list
        type_list = ["criticalvictim", "regularvictim", "novictim"]

        # filter markers_log
        m = self.markers_log.copy()
        m = m[m.time <= t]        
        if len(m) == 0:
            return pd.DataFrame(columns=['nearest_room', 'criticalvicitm', 'regularvictim', 'novictim'])

        m['type'] = m.apply(lambda row: row.type.split('_')[-1], axis=1)
        m = m[m.type.isin(type_list)]
        if len(m) == 0:
            return pd.DataFrame(columns=['nearest_room', 'criticalvicitm', 'regularvictim', 'novictim'])
        
        # find location of markers inside rooms first
        m['nearest_room'] = m.apply(lambda row: self.find_room(row.x, row.z), axis=1)

        # if not inside room, find nearest room
        def get_nearest_plate(room, x, z):
            if isinstance(room, str):
                return room
            else:
                return self.nearest_plate(x, z)

        m['nearest_room'] = m.apply(lambda row: get_nearest_plate(row.nearest_room, row.x, row.z), axis=1)

        # put DataFrame to desired forma
        m = m.groupby(["nearest_room","type"]).type.count().unstack()
        m = m.reset_index("nearest_room")
        for marker_type in type_list:
            if marker_type not in m.columns:
                m[marker_type] = np.nan
        
        return m


    def get_first_entries(self, player_id: str, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.door_open_log
        EFFECTS: Returns door opened at or just before t
        """

        if player_id == 'all':
            m = self.mission[(self.mission.time <= t)].copy()
        else:
            m = self.mission[(self.mission.player_id == player_id) & (self.mission.time <= t)].copy()
        
        # in case m has no entry
        m['location'] = np.nan

        m = m[(m.action == 'move')]
        m = m[m.z <= (Map.FOV_Z_MAX-0.5)]
        m['location'] = m.apply(lambda row: self.find_room(row.x, row.z), axis=1)
        m = m[m.groupby("location").time.transform(min) == m.time]

        return m


    def get_doors_info_minimal(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.door_open_log
        EFFECTS: Returns door opened at or just before t
        """
        d = self.door_open_log.copy()
        d = d[d.time <= t]

        return d


    def get_rubble_info_minimal(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.rubble_log
        EFFECTS: Returns rubble not removed at or just before t
        """
        r = self.rubble_log.copy()
        r = r[np.isinf(r.time_removed)] # rubble not removed
        r = r[r.time_added <= t] # added at or before t

        return r


    def get_signals_info_minimal(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.signals_log
        EFFECTS: Returns signals_info at or just before t
        """
        s = self.signals_log.copy()
        s = s[s.time <= t]
        earliest_time_ind = s.groupby('room_id').time.transform(min) == s.time
        s = s[earliest_time_ind]

        return s


    def get_victims_info_minimal(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.victims_ground_truth, self.victims_log
        EFFECTS: Returns victims_info at or just before t;
                 format same format as victims_ground_truth
                 but with updated status and locations
        """
        # get and process victims_ground_truth
        v_gt = self.victims_ground_truth.copy()
        v_gt = v_gt.reset_index('victim_id')
        v_gt['time'] = 0

        # get vicitms_log before time t, process to match ground_truth format
        v_log = self.victims_log.copy()
        v_log = v_log[v_log.time <= t]
        v_log = v_log.rename(columns={'room_id':'room_name'})
        v_log['victim_type'] = v_log.apply(lambda row: row.victim_type.split('_')[-1].upper(), axis = 1)

        # get the most updated location and status by victim_id
        v = pd.concat((v_gt, v_log))
        max_time_idx = v.groupby('victim_id').time.transform(max) == v.time
        v = v[max_time_idx]
        v.loc[v.action == 'pickup_victim', 'status'] = 1
        v = v.set_index('victim_id').sort_index()

        return v


    def get_victims_info(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.victims_ground_truth, self.victims_log
        EFFECTS: Returns victims_info at or just before t;
                 format same format as victims_ground_truth
                 but with updated status and locations
        """

        victims_info = self.victims_ground_truth.copy()
        log = self.victims_log[self.victims_log['time'] <= t]

        # prep marking which victims are held by each scout
        bools_ind = log['action'].isin(['pickup_victim', 'place_victim'])
        scout_names = log[bools_ind].player_id.unique()
        #scout_names = list(set(log[bools_ind]['player_id'].to_list()))  # Series.unique()?
        scout_hold_victim_dict = {}
        for name in scout_names:
            scout_hold_victim_dict[name] = -1  # value is victim_id

        def apply_action(d: pd.Series):
            # MODIFIES: victims_info
            # TODO: may be a bug... this might incorrectly match victim IDs if a
            #       victim is moved more than once.
            bool_inds = (victims_info['x'] == d['x']) & \
                        (victims_info['z'] == d['z']) & \
                        (victims_info['victim_type'] == d['victim_type']) & \
                        (d['action'] in ['triage', 'pickup_victim'])

            if np.sum(bool_inds) > 1:
                raise Exception("More than 1 victim matched action!")

            if (np.sum(bool_inds) == 0) and (d['action'] != 'place_victim'):
                raise Exception("Victim actions not on any victim!")

            if np.sum(bool_inds) == 1:
                victim_id = bool_inds.index[bool_inds][0]
                if victims_info.loc[victim_id, 'status'] == 1 and d.action == 'triage':
                    raise Exception("Triaged victims cannot be triaged again.")

            if d['action'] == 'triage':
                victim_id = bool_inds.index[bool_inds][0]
                victims_info.loc[victim_id, 'status'] = 1
            elif d['action'] == 'pickup_victim':
                which_scout = d['player_id']
                if scout_hold_victim_dict[which_scout] != -1:
                    raise Exception("Scout carrying more than 1 victim")
                else:
                    victim_id = bool_inds.index[bool_inds][0]
                    # maintain whether this victim has been triaged or not
                    current_status = victims_info.loc[victim_id, 'status']
                    # 1 is triaged, 3 is held-triaged, 2 is held-unsaved
                    victims_info.loc[victim_id, 'status'] = 3 if current_status == 1 else 2
                    victims_info.loc[victim_id, 'x'] = np.nan
                    victims_info.loc[victim_id, 'z'] = np.nan
                    scout_hold_victim_dict[which_scout] = victim_id
            elif d['action'] == 'place_victim':
                which_scout = d['player_id']
                if scout_hold_victim_dict[which_scout] == -1:
                    raise Exception("Scout dropping off victim not carried")
                else:
                    placed_victim_id = scout_hold_victim_dict[which_scout]
                    # maintain whether this victim has been triaged or not
                    current_status = victims_info.loc[placed_victim_id, 'status']
                    # 1 is triaged, 3 is held-triaged, 2 is held-unsaved
                    victims_info.loc[placed_victim_id, 'status'] = 1 if current_status == 3 else 0
                    victims_info.loc[placed_victim_id, 'x'] = d['x']
                    victims_info.loc[placed_victim_id, 'z'] = d['z']
                    scout_hold_victim_dict[which_scout] = -1  # return to initial value
            return

        log.apply(apply_action, axis=1)

        if np.sum(log['action'] == 'triage') != np.sum(victims_info.status.isin([1, 3])):
            raise Exception("Triages recorded improperly!")

        return victims_info

    def get_score(self, t: float) -> int:
        """
        REQUIRES: t >= self.mission.iloc[0].time
        EFFECTS:  Returns the team score at time t
        """
        score = self.mission[self.mission.time <= t].iloc[-1].score
        return score

    def get_players_info(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: t >= self.mission.iloc[3].time  (need at least one row per player)
        EFFECTS: Returns player_info at or just before t:
                 columns: time, player_id, x, y, z, current_role
        """

        cols = ['player_id', 'x', 'y', 'z', 'yaw', 'current_role', 'map_knowledge_cond']

        is_holding_victim = { p: False for p in self.players }

        players_info = pd.DataFrame(columns=cols, index=self.players)
        for i, p_id in enumerate(self.players):
            bool_inds = (self.mission['time'] <= t) & \
                        (self.mission['player_id'] == p_id)
            players_info.loc[p_id] = self.mission[bool_inds][cols].iloc[-1]

            # mark which victim each scout is holding
            if players_info.loc[p_id, 'current_role'] == 'scout':
                scoutaction_mask = (self.victims_log.time <= t) & \
                                   (self.victims_log.action.isin({'pickup_victim',
                                                                  'place_victim'}))
                if scoutaction_mask.any():
                    lastaction = self.victims_log[scoutaction_mask].sort_values('time').iloc[-1]
                    if lastaction.action == 'pickup_victim':
                        # TODO: actually write down victim id
                        is_holding_victim[p_id] = True

        for player in self.players:
            players_info.loc[player, 'holding_victim'] = is_holding_victim[player]

        # to match Configuration spec
        players_info.rename(columns={'map_knowledge_cond': 'map_knowledge'},
                            inplace=True)
        players_info.index = players_info.player_id
        return players_info

    def get_players_traj(self, t: float) -> pd.DataFrame:
        """
        REQUIRES: self.mission, time
        EFFECTS:  Returns player movement for time <=t; see cols for columns
        """

        bool_inds = self.mission['time'] <= t
        cols = ['time', 'x', 'z', 'player_id', 'current_role']
        return self.mission[bool_inds][cols]

    def get_decision_points(self, decision_point_type: str) -> pd.DataFrame:
        """
        TODO: Do this later. one series for each player or one series for each role?
        EFFECTS: Returns decision point timestamp arrays for each TODO
        OUTPUT: DataFrame columns: time, player_id, role, action
        """

        #TODO: add scouts actions
        #TODO: add rubble cluster info
        action_list = ['remove_rubble', 'triage', 'pickup_victim', 'place_victim']
        cols = ['time','player_id','current_role', 'action']
        bool_inds = self.mission['action'].isin(action_list)

        return self.mission[bool_inds][cols]

    def get_decision_points_single(self, player_id: str, role: str,
                                   decision_point_type: str) -> pd.Series:
        """
        REQUIRES: player_id in self.mission.player_id.unique()
                  role in {'medic', 'rubbler', 'scout'}
        EFFECTS:  Returns an iterable of all the decision point timestamps for
                  Player player_id in Role role, using decision_point_type formalism.
                  E.g. all time points for player Alpha in the Medic role
                  triaging victims. Note that the timestamps may not be from contiguous
                  roles, meaning timestamps from both Alpha's initial medic role
                  and Alpha's second spree as the medic role would be included, if Alpha
                  switched to a different role during the mission.
        FIXME: possibly want to change to datetime str index for better accuracy
               when generating decision points from timestamps.
        """

        # standard decision_point_type:
        # medic: victim triages
        # rubbler: rubble removes where the next rubble removed is in a different cluster
        if decision_point_type not in {'standard'}:
            raise ValueError(f'Invalid decision point type: {decision_point_type}')

        if role == 'scout':
            # TODO: match scout holding to victim id in get_players_info, then can
            #       operate on all decision points
            # some decision points: victim pickups when only a single scout is holding a victim
            def check_num_scouts(time: float):
                player_info = self.get_players_info(time)
                if player_info.current_role.value_counts().scout > 1:
                    return False
                else:
                    # FIXME: remove for speed
                    assert(player_info.holding_victim.value_counts().loc[True] == 1)
                    return True
            decision_point_mask = (self.mission.player_id == player_id) & \
                                  (self.mission.current_role == role) & \
                                  (self.mission.action == 'pickup_victim')
            possibles = self.mission[decision_point_mask].time
            decision_points = possibles[possibles.apply(check_num_scouts)]
            return decision_points
        elif role == 'medic':
            decision_point_mask = (self.mission.player_id == player_id) & \
                                  (self.mission.current_role == role) & \
                                  (self.mission.action == 'triage')
            return self.mission[decision_point_mask].time
        elif role == 'rubbler':
            def lookup_cluster_id(coord: Tuple[int, int]) -> int:
                # get ground truth cluster id for this coordinate
                matches = self.init_rubble_info[(self.init_rubble_info.x == coord[0])
                                                & (self.init_rubble_info.z == coord[1])]
                if len(matches) == 0:
                    raise ValueError(f'Cluster id not found for rubble at {coords}')
                return matches.iloc[0].cluster_id

            rubble_removes = (self.mission.player_id == player_id) & \
                             (self.mission.current_role == role) & \
                             (self.mission.action == 'remove_rubble')
            rubble_decisions = self.mission[rubble_removes].copy()
            if len(rubble_decisions) == 0:
                return pd.Series()
            rubble_decisions['coords'] = rubble_decisions.action_data.apply(self._extract_coord)
            rubble_decisions['cluster_id'] = rubble_decisions.coords.apply(lookup_cluster_id)

            # calculate when rubbler removes a rubble block for last consecutive time in a cluster
            # i.e. every rubble remove before cluster_id changes
            rubble_decision_mask = (rubble_decisions.cluster_id.diff() != 0).iloc[1:].to_list()
            rubble_decision_mask.append(False)
            decision_points = rubble_decisions[rubble_decision_mask].time
            return decision_points

    def get_action_picked(self, c: Configuration, player: str,
                          utilities: pd.DataFrame = None) -> Optional[Tuple[int, float]]:
        """
        REQUIRES: player in c.players.index
                  options is pd.DataFrame of "accessible victims" (medic, imperfect knowledge case)
                    that is coindexed with whatever utility array is being used.
                  options passed when self.knowledge_cond is not 'perfect'
                  for rubbler, options has columns:
                    utility, cluster_id (ground truth), x (todo), z (todo), marginal
                  for medic, options has columns:
                    utility, observed (boolean), x, z, region, marginal
                  for scout, options has columns:
                    TODO
        EFFECTS:  Computes action taken by player after c.time. Depends on player's role.
                  If knowledge condition is 'perfect' then an index of c.victims_gt or c.rubble_gt
                  will be returned. Otherwise an index of options will be returned. If an index
                  of -1 is returned, that means a valid action was taken that isn't in options.
                  Also returns the time the action was taken (guaranteed to be > c.time).
        """
        if c.knowledge_cond != 'perfect' and utilities is None:
            raise ValueError(f'utility options needed in imperfect knowledge conditions')

        role = c.players.loc[player, 'current_role']
        if role == 'medic':
            victim_save_mask = (self.victims_log.time > c.time) & \
                               (self.victims_log.player_id == player) \
                               & (self.victims_log.action == 'triage')
            next_victim_saved = self.victims_log[victim_save_mask]

            if len(next_victim_saved) == 0:
                return None
            next_victim_saved = next_victim_saved.iloc[0]  # fixme: check this is correct
            triage_time = next_victim_saved.time

            if self.knowledge_cond == 'imperfect-shared' or self.knowledge_cond == 'imperfect-indiv':

                # check if this victim was accessible to player at decision point time t
                matching_victim = utilities[utilities.xz == (next_victim_saved.x, next_victim_saved.z)]
                if len(matching_victim) > 0:
                    # found a matching ground truth victim (player knew about it at decision point)
                    # return index of utility in options
                    return matching_victim.iloc[0].name, triage_time
                else:
                    # player did not know about this victim, use corresponding region score...
                    belief_regions = c.beliefs.regions if self.knowledge_cond == 'imperfect-shared' \
                                                       else c.beliefs[player].regions
                    region_selected = belief_regions[Map.convert_coords(next_victim_saved.x,
                                                                        next_victim_saved.z)]
                    # get index in options for victim sample in this region
                    choice = utilities[utilities.region == region_selected]
                    if len(choice) > 0:
                        return choice.iloc[0].name, triage_time
                    else:
                        # victim saved was in a region not in options,
                        # which means victim-saved-region was inaccessible at decision point time.
                        return -1, triage_time
        elif role == 'rubbler':
            rubble_remove_mask = (self.rubble_log.player_id == player) & \
                                 (self.rubble_log.time_removed > c.time)
            next_rubble_removed = self.rubble_log[rubble_remove_mask]
            if len(next_rubble_removed) == 0:
                return None
            # need to do it this way because self.rubble_log is not sorted
            next_rubble_removed = next_rubble_removed.loc[next_rubble_removed.time_removed.idxmin()]
            remove_time = next_rubble_removed.time_removed

            if self.knowledge_cond == 'imperfect-indiv' or self.knowledge_cond == 'imperfect-shared':
                cluster_id = next_rubble_removed.cluster_id
                if cluster_id not in utilities.cluster_id.unique():
                    # rubbler removed a block that they didn't know about at decision point time
                    return -1, remove_time
                return cluster_id, remove_time
            else:
                return next_rubble_removed.cluster_id, remove_time
        elif role == 'scout':
            # TODO: switch here if scout is holding victim or not?
            if c.players.loc[player, 'holding_victim']:
                scout_dropoff_mask = (self.victims_log.player_id == player) & \
                                     (self.victims_log.action == 'place_victim') & \
                                     (self.victims_log.time > c.time)
                next_dropoff = self.victims_log[scout_dropoff_mask]
                if len(next_dropoff) == 0:
                    return None
                next_dropoff = next_dropoff.loc[next_dropoff.time.idxmin()]

                # prep map for finding nearest
                nearest_config = c.copy()
                nearest_config.rubble_gt.status = 0  # pretend no rubble on map
                m = Map(self.topography_file)
                m.update(nearest_config)
                # all victim dropoff locations are accessible according to the player's rubble
                # belief distr at decision time. So we will match against those
                coords = utilities.apply(lambda r: (r.x, r.z), axis=1).to_list()
                paths, distances = m.paths_to((next_dropoff.x, next_dropoff.z), coords,
                                              nearest_config)
                utility_chosen = utilities.iloc[np.argmin(distances)]
                return utility_chosen.name, next_dropoff.time

                ## get nearest victim location to next dropoff
                #def filter_viable(xs: int, zs: int, row: pd.Series, config: Configuration) -> bool:
                #    # returns true if row location is an open square and is accessible from (x, z)
                #    # MODIFIES: config, Map
                #    loc = m.convert_coords(row.x, row.z)
                #    if m.topography[loc] != m.OPEN_SPACE:
                #        # just darn make it an open space (so m.connected can run)
                #        config.rubble_gt.loc[(config.rubble_gt.x == row.x) &
                #                             (config.rubble_gt.z == row.z), 'status'] = 0
                #    return m.connected(xs, zs, row.x, row.z, config)

                ## only consider ground truth accessible locations?
                #viable_mask = utilities.apply(filter_viable, axis=1, xs=next_dropoff.x,
                #                              zs=next_dropoff.z)
                #coords = utilities[viable_mask].apply(lambda r: (r.x, r.z), axis=1).to_list()
                #paths, distances = m.paths_to((next_dropoff.x, next_dropoff.z), coords, c)
                #utility_chosen = utilities[viable_mask].iloc[np.argmin(distances)]
                #return utility_chosen, next_dropoff.time

            else:
                scout_pickup_mask = (self.victims_log.player_id == player) & \
                                    (self.victims_log.action == 'pickup_victim') & \
                                    (self.victims_log.time > c.time)
                raise NotImplementedError

        raise NotImplementedError

    def prune_utility_options(self, choice: int, action_time: float, player: str,
                              utilities: pd.DataFrame, c: Configuration) -> Tuple[pd.DataFrame, int]:
        """
        REQUIRES: choice in utilities.index
                  action_time is the moment when the player triaged/removed/picked up/placed
                    utilities.loc[choice]
                  c is Configuration used to calculate utilities and options (at decision time)
                  if player is in rubbler role, utilities.cluster_id are same as ground truth
                    cluster ids (unless above max), and utilities.index == utilities.cluster_id
        MODIFIES: utilities
        EFFECTS:  Returns utilities dataframe with rows removed according to the following strategy:
                  medic:
                    utilities are included if they are a ground truth victim or a region
                    containing a ground truth victim at action_time. They are excluded if
                    they are a region which does not contain a ground truth victim.
                    Rows for each region with
                    a ground truth victim but not present in utilities will be added.
                  rubbler:
                    utilities included if they are a ground truth rubble cluster at action_time.
                    All other utilities are excluded.
                    Rows for each rubble cluster not present in utilities will be added.
                  scout:
                    todo; same as medic
                  Also returns new index of choice in resulting dataframe
        """
        def get_region(victim: pd.Series) -> int:
            row, col = Map.convert_coords(victim.x, victim.z)
            return self.map_regions[row, col]

        if self.knowledge_cond == 'perfect':
            raise UserWarning("Don't use this in perfect knowledge condition")

        role = c.players.loc[player, 'current_role']

        if role == 'rubbler':
            before_remove_time = self.mission[self.mission.time < action_time].iloc[-1].time
            remove_time_rubble = self.get_rubble_info(before_remove_time)
            remove_time_rubble = remove_time_rubble[remove_time_rubble.status > 0]

            # get utilities matching ground truth rubble cluster
            to_keep = utilities[utilities.cluster_id.isin(remove_time_rubble.cluster_id.unique())]

            # add entry for each cluster not present in utilities
            clusters_to_add = frozenset(remove_time_rubble.cluster_id.unique()) - \
                              frozenset(to_keep.cluster_id.unique())
            new_rows = [ pd.Series((self.SMALL_UTILITY, cluster), index=['utility', 'cluster_id'],
                                   name=i)
                         for cluster, i in zip(clusters_to_add,
                                               range(len(utilities),
                                                     len(utilities) + len(clusters_to_add))) ]

            if choice is None:
                selected_idx = None
            else:
                selected_idx = to_keep.index.get_loc(choice)
            utilities = to_keep.append(new_rows).reset_index(drop=True)
            return utilities, selected_idx
        else:
            # get regions of unsaved victims at action time
            before_triage_time = self.mission[self.mission.time < action_time].iloc[-1].time
            triage_time_victims = self.get_victims_info(before_triage_time)
            triage_time_unsaved = triage_time_victims[triage_time_victims.status == 0]
            # need to calculate these here because they can change...
            # TODO: provide region in get_victims_info, then don't do this
            triage_time_unsaved['region'] = triage_time_unsaved.apply(get_region, axis=1)
            regions_with_victim = frozenset(triage_time_unsaved.region.unique())

            if role == 'medic':
                # TODO: test with new medic utility format
                # keep ground truth victims and regions containing ground truth victims
                to_keep = utilities[utilities.observed | utilities.region.isin(regions_with_victim)]
                # utilities for regions without ground truth victims are already removed

                # add arbitrary small utilities for regions containing ground truth victims
                # but didn't appear in original utilities
                regions_to_add = regions_with_victim - frozenset(to_keep.region.unique())
                new_rows = [ pd.Series((self.SMALL_UTILITY, False, np.nan, np.nan, region, np.nan),
                                       index=['utility', 'observed', 'x', 'z', 'region', 'marginal'])
                             for region in regions_to_add ]

                if choice is None:
                    selected_idx = None
                else:
                    selected_idx = to_keep.index.get_loc(choice)
                utilities = to_keep.append(new_rows).reset_index(drop=True)
                return utilities, selected_idx

            elif role == 'scout':
                # TODO: don't prune?
                return utilities, choice
                # keep all utilities associated with a victim that is untraiged at action time,
                # remove the rest.
                actual_coords = triage_time_unsaved.apply(lambda r: (r.x, r.z), axis=1).to_list()
                to_keep_mask = utilities.apply(lambda r: (r.x, r.z), axis=1).isin(actual_coords)
                to_keep = utilities[to_keep_mask]
                selected_idx = choice

                if choice is not None and choice not in to_keep.index:
                    # need to re-compute closest untriaged victim
                    nearest_config = Configuration.make_empty_config()
                    nearest_config.victims_gt = triage_time_victims
                    m = Map(self.topography_file)
                    # TODO: this computes closest victim to assigned action, not to actual victim
                    #       dropoff location. Will be slightly incorrect sometimes
                    dropoff_coord = (utilities.loc[choice, 'x'], utilities.loc[choice, 'z'])
                    paths, distances = m.paths_to(dropoff_coord, actual_coords, nearest_config)

                    # compute new index in to_keep
                    # using labels, so they should match...
                    selected_idx = triage_time_unsaved.iloc[np.argmin(distances)].name

                return to_keep, selected_idx

    def prune_utility_options_old(self, choice: int, triage_time: float, options: pd.DataFrame,
                                  utilities: Dict[int, float], c: Configuration) -> Dict[int, float]:
        """
        REQUIRES: choice in utilities.keys()
                  options.index == utilities.keys()
                  triage_time is moment when victim indexed by choice was saved
                  c is Configuration used to calculate utilities and options (and choice/triage time)
        EFFECTS:  Returns a dict from victim id's (as found in utilities.keys() ) to utility values,
                  a proper subset of utilities.items(). Uses the following pruning strategy:
                    If a victim is known/accessible at c.time, their utility is included.
                    If a region contains a ground truth victim at triage_time, any utilities
                        associated with that region are included. If there are no utilities associated,
                        a utility entry is added with MINIMAL_UTILITY.
                    All other utilities are removed: utilities for regions that do not contain an
                        accessible victim at triage_time.
        """
        raise PendingDeprecationWarning

        if self.knowledge_cond == 'perfect':
            raise UserWarning("Don't use this in perfect knowledge condition")

        # assume regions used in belief distr sampling are same across subjs
        if c.knowledge_cond == 'imperfect-shared':
            belief_regions = c.beliefs.regions
        else:
            prob_maps = [ pm for pm in c.beliefs.values() if pm is not None ]
            belief_regions = prob_maps[0].regions

        def get_region(victim: pd.Series) -> int:
            row, col = Map.convert_coords(victim.x, victim.z)
            return belief_regions[row, col]

        # get all unsaved victims at time of triage. leave out held victims
        triage_time = self.mission[self.mission.time < triage_time].iloc[-1].time
        triage_time_unsaved = self.get_victims_info(triage_time)
        triage_time_unsaved = triage_time_unsaved[triage_time_unsaved.status == 0]
        # lookup regions for unsaved victims
        triage_time_unsaved['region'] = triage_time_unsaved.apply(get_region, axis=1)

        # get pruned utilities list
        pruned_utilities = utilities.copy()
        actual_actions_regions = set(triage_time_unsaved.region.unique())
        options_regions = set(options.region.unique())

        # keep utility values of directly observed (accessible) victims at c.time
        # TODO: will match by location be okay? What if scout picked up and moved victim?
        #keep_mask = (options.x.isin(triage_time_unsaved.x)) & (options.z.isin(triage_time_unsaved.z))
        observed_gt_victims_mask = (abs(options.marginal - 1) < 0.0001)  # assume observed have marginal 1
        #utilities_keep = options[keep_mask].index

        # regions in actual available actions not in options (utilities)
        # these are inaccessible at c.time, but could be accessible at triage_time
        inaccessible_regions = actual_actions_regions - options_regions

        # regions in both actual available actions and in options (utilities)
        #all_utilities_regions_match = actual_actions_regions.intersection(options_regions)

        extra_regions = options_regions - actual_actions_regions
        utilities_to_prune = options[~observed_gt_victims_mask & options.region.isin(extra_regions)].index

        # build pruned utilities
        for utility_id in utilities_to_prune:
            pruned_utilities.pop(utility_id, None)

        new_utility_id_start = max(utilities.keys()) + 1
        pruned_utilities.update({ i: self.SMALL_UTILITY
                                  for i in range(new_utility_id_start,
                                                 new_utility_id_start+len(inaccessible_regions)) })

        if choice is not None and choice not in pruned_utilities:
            raise AssertionError('something wrong')
        return pruned_utilities

    def _get_rubble_cluster_picked(self, c1: Configuration, c2: Configuration, player: str) -> str:
        """
        REQUIRES: player is rubbler role
        EFFECTS:  Return rubble_cluster_id that player is clearing?
        """

        raise NotImplementedError

    def _get_victim_medic_picked(self, c1: Configuration, c2: Configuration, player: str) -> str:
        """
        REQUIRES: player is medic role
        EFFECTS:  Return victim_id that player is trying to triage
        """

        raise NotImplementedError

    def get_ppt_role_velocity(self, player: str, role: str) -> float:
        """
        EFFECTS: Gets average velocity of player when they play as role.
        Note: for now, just return the avg for that role or something.
        """

        raise NotImplementedError

    def _build_victims_log(self) -> pd.DataFrame:
        """
        REQUIRES: self.mission, self.victims_ground_truth
        EFFECTS:  Returns dataframe containing:
                    time, x, z,
                    victim_type (normal, critical),
                    action_type (triaged, pickup_victim, place_victim)
        """

        action_list = ['triage', 'pickup_victim', 'place_victim']
        bool_inds = self.mission['action'].isin(action_list)
        victims_log = self.mission[bool_inds][['time', 'action', 'player_id']].copy()

        # initialize new columns
        victims_log['victim_type'] = np.nan
        victims_log['x'] = np.nan
        victims_log['z'] = np.nan
        victims_log['room_id'] = np.nan
        victims_log['victim_id'] = np.nan
        
        action_data_df = self.mission[bool_inds][['action_data']]
        for ind, row in action_data_df.iterrows():
            d = row['action_data']
            if isinstance(d, str):
                type_xz = d[1:-1].split(',')  # 1:-1 strips parentheses
                x_f = float(type_xz[1])
                z_f = float(type_xz[2])
                victims_log.loc[ind, 'victim_type'] = type_xz[0][1:-1]
                victims_log.loc[ind, 'x'] = x_f
                victims_log.loc[ind, 'z'] = z_f
                victims_log.loc[ind, 'room_id'] = self.map_regions[Map.convert_coords(x_f, z_f)]
                victims_log.loc[ind, 'victim_id'] = int(float(type_xz[3]))
            elif isinstance(d, tuple):
                victims_log.loc[ind, 'victim_type'] = d[0]
                victims_log.loc[ind, 'x'] = d[1]
                victims_log.loc[ind, 'z'] = d[2]
                victims_log.loc[ind, 'room_id'] = self.map_regions[Map.convert_coords(d[1], d[2])]
                victims_log.loc[ind, 'victim_id'] = int(d[3])
            else:
                print("in _build_victims_log: unaccounted for data type!!")

        return victims_log

    @staticmethod
    def _extract_coord(action_datum: str) -> Tuple[int, int]:
        # extracts rubble location from action_data string
        if isinstance(action_datum, str):
            ax, az, _ = action_datum[1:-1].split(',')  # 1:-1 strips parentheses
            ax, az = int(float(ax)), int(float(az))
        elif isinstance(action_datum, tuple):
            ax = action_datum[0]
            az = action_datum[1]
        return ax, az

    def _build_rubble_log(self) -> pd.DataFrame:
        """
        REQUIRES: self.mission
        EFFECTS:  Returns dataframe in same format as self.init_rubble_info.
                  Indices match those in self.init_rubble_info.
                  Replaces status column with time_removed column and adds player_id column.
        """

        if len(self.init_rubble_info) == 0:
            rubble_log = pd.DataFrame(columns = ['x', 'z', 'status', 'cluster_id',
                                                'time_added', 'room_name',
                                                'player_triggered', 'player_removed'])
        else:
            rubble_log = self.init_rubble_info.copy()
            rubble_log['time_added'] = -1e-6
            rubble_log['room_name'] = np.nan
            rubble_log['player_triggered'] = np.nan
            rubble_log['player_removed'] = np.nan
        
        # add rubble collapse
        rubble_collapse_mask = self.mission.action == 'trigger_rubble_collapse'
        action_data = self.mission[rubble_collapse_mask]['action_data'].to_list()
        player_id_data = self.mission[rubble_collapse_mask].player_id.to_list()
        collapse_times = self.mission[rubble_collapse_mask]['time'].to_list()  # should be coindexed
        for i, pos in enumerate(action_data):
            x, z = self._extract_coord(pos)
            rubble_log = rubble_log.append({'x':x, 'z':z, 'status':1, 'cluster_id':np.nan,
                                            'time_added':collapse_times[i],
                                            'room_name': self.map_regions[Map.convert_coords(x, z)],
                                            'player_triggered':player_id_data[i],
                                            'player_removed': np.nan}, #rubble_log.cluster_id.to_numpy().max() + 1},
                                            ignore_index=True)

        # add rubble remove
        rubble_log['time_removed'] = np.inf
        self.RUBBLE_LOG_TIMEREMOVED_IDX = list(rubble_log.columns).index('time_removed')
        rubble_remove_mask = self.mission.action == 'remove_rubble'
        action_data = self.mission[rubble_remove_mask]['action_data'].to_list()
        player_id_data = self.mission[rubble_remove_mask].player_id.to_list()
        remove_times = self.mission[rubble_remove_mask]['time'].to_list()  # should be coindexed
        for i, pos in enumerate(action_data):
            # ignore y coordinate!
            x, z = self._extract_coord(pos)
            # logging.debug(f"Location of rubble removed: {x}, {z}")
            # TODO: consider indexing directly by x, z
            tile_mask = (rubble_log.x == x) & (rubble_log.z == z) &\
                        (rubble_log.time_added < remove_times[i]) &\
                        (np.isinf(rubble_log.time_removed))
            if np.sum(tile_mask.to_numpy()) > 0:
                block_id = rubble_log.loc[tile_mask].index[-1]
                rubble_log.loc[block_id, 'status'] = rubble_log.loc[block_id, 'status'] - 1
                if (rubble_log.loc[block_id, 'status'] == 0):#.all():
                    # mark this as the time rubble was removed
                    rubble_log.loc[block_id, 'time_removed'] = remove_times[i]
                    rubble_log.loc[block_id, 'player_removed'] = player_id_data[i]
            else:
                logging.debug(f"Removal of rubble at {x},{z} not in rubble list")

        rubble_log['wait_time'] = rubble_log.apply(lambda row: row.time_removed - row.time_added, axis=1)

        return rubble_log

    def _build_markers_log(self) -> pd.DataFrame:
        """
        REQUIRES: self.mission
        EFFECTS:
        """
        bool_inds = self.mission['action'] == 'marker_placed'
        markers_log = self.mission[bool_inds][['time', 'action', 'player_id']].copy()

        # initialize new columns
        markers_log['type'] = np.nan
        markers_log['x'] = np.nan
        markers_log['z'] = np.nan
        
        action_data_df = self.mission[bool_inds][['action_data']]
        for ind, row in action_data_df.iterrows():
            d = row['action_data']
            if isinstance(d, str):
                type_xz = d[1:-1].split(',')  # 1:-1 strips parentheses
                x_f = float(type_xz[1])
                z_f = float(type_xz[2])
                markers_log.loc[ind, 'type'] = type_xz[0][1:-1]
                markers_log.loc[ind, 'x'] = x_f
                markers_log.loc[ind, 'z'] = z_f
            elif isinstance(d, tuple):
                markers_log.loc[ind, 'type'] = d[0]
                markers_log.loc[ind, 'x'] = d[1]
                markers_log.loc[ind, 'z'] = d[2]

        return markers_log


    def _build_signals_log(self) -> pd.DataFrame:
        """
        REQUIRES: self.mission
        EFFECTS:
        """
        bool_inds = self.mission['action'] == 'signal_detected'
        signals_log = self.mission[bool_inds][['time', 'action', 'player_id']].copy()

        # initialize new columns
        signals_log['room_id'] = np.nan
        signals_log['message'] = np.nan
        
        action_data_df = self.mission[bool_inds][['action_data']]
        for ind, row in action_data_df.iterrows():
            d = row['action_data']
            if isinstance(d, str):
                room_msg = d[1:-1].split(',')  # 1:-1 strips parentheses
                room = room_msg[0][1:-1]
                msg = room_msg[1][1:-1]
                signals_log.loc[ind, 'room_id'] = room
                signals_log.loc[ind, 'message'] = msg
            elif isinstance(d, tuple):
                signals_log.loc[ind, 'room_id'] = d[0]
                signals_log.loc[ind, 'message'] = d[1]

        # signals_log['message'] = signals_log.apply(lambda row: row.message.split('_')[0].lower(), axis=1)

        return signals_log


    def find_room(self, x, z):
        r,c = Map.convert_coords(x,z)
        return self.map_regions[r,c]


    def nearest_plate(self, marker_x, marker_z):
        plate_df = self.plate_coord
        min_ind = ((plate_df.x.to_numpy() - marker_x)**2 + (plate_df.z.to_numpy() - marker_z)**2).argmin()
        return plate_df.iloc[min_ind].room_id


    def _build_door_open_log(self) -> pd.DataFrame:
        """
        REQUIRES: self.mission
        EFFECTS:
        """
        bool_inds = self.mission['action'] == 'door_open'
        door_log = self.mission[bool_inds][['time', 'action', 'player_id']].copy()

        # initialize new columns
        door_log['door_x'] = np.nan
        door_log['door_z'] = np.nan
        
        action_data_df = self.mission[bool_inds][['action_data']]
        for ind, row in action_data_df.iterrows():
            d = row['action_data']
            if isinstance(d, str):
                xzy = d[1:-1].split(',')  # 1:-1 strips parentheses
                x_ = xzy[0][1:-1]
                z_ = xzy[1][1:-1]
                door_log.loc[ind, 'door_x'] = x_
                door_log.loc[ind, 'door_z'] = z_
            elif isinstance(d, tuple):
                door_log.loc[ind, 'door_x'] = d[0]
                door_log.loc[ind, 'door_z'] = d[1]

        door_log['room_id'] = door_log.apply(lambda row: self.find_room(row.door_x, row.door_z), axis=1)

        return door_log


    def _mark_changepoints(self) -> np.ndarray:
        """
        REQUIRES: self._victims_log, self._rubble_log
        EFFECTS:  Marks timestamps where visible configuration changes,
                  i.e. the timestamps when what is visible to a player on
                  the map changes.
        """

        # get timestamps when rubble is removed, victims are picked up, or victims are placed.
        rows = self.mission[self.mission.action.isin(['remove_rubble', 'pickup_victim',
                                                      'place_victim'])]
        changepoints = rows.time.tolist()
        #changepoints = rows.index.tolist()

        # todo: add first observation timestamp as first changepoint
        # TODO: why above line?
        return np.array(changepoints)

    def _build_fov_log(self, topography_file: str) -> pd.DataFrame:
        """
        REQUIRES: self._victims_log, self._rubble_log, self._config_changepoints
                  topography_file is valid path to .npy topography file
        EFFECTS:  Returns a DataFrame with configuration and tiles observed (by each player)
                  information for each interval, where intervals determined by
                  self._config_changepoints. end_time column == self._config_changepoints
                  columns: end_time, config, alpha_seen, bravo_seen, delta_seen
        """
        # increase this to get coarser timestamp fov readings
        FOV_INCREMENT = 2  # observations

        raise NotImplementedError

    def _build_players_log(self) -> pd.DataFrame:
        """
        TODO: output format
        REQUIRES: self.mission
        EFFECTS:  Returns timestamp-indexed representation of which players
                  were in what role/state, when.
        """

        raise NotImplementedError


def extract_knowledge_maps(map_knowledge_cond: str, check_map_kind=None) -> (str, str):
    """
    REQUIRES: map_knowledge_cond is pulled from study2_preprocess.boil output
              i.e. a preprocessed data file
    EFFECTS:  Returns the filenames of the corresponding victim and rubble
              density maps (npy), in that order.
    """

    # TODO: make smarter
    base_map_type = map_knowledge_cond[:-4]
    map_kind = map_knowledge_cond[6]
    section1 = int(map_knowledge_cond[-2])
    section2 = int(map_knowledge_cond[-1])

    if base_map_type != 'Saturn':
        raise ValueError('Only Saturn maps enabled.')
    if map_kind not in ['A', 'B']:
        raise NotImplementedError
    elif check_map_kind is not None:
        # solely for use inside Mission, to make sure we only test static knowledge maps
        # for the same map kind (A or B) as the actual trial.
        if check_map_kind != base_map_type+map_kind:
            raise ValueError(f'Did not pass correct map kind (A or B): {map_kind}')
    if section2 != 4:
        raise NotImplementedError("last section is not 4, can't deal with this yet")

    # build filename
    filename = 'saturn_'
    filename += map_kind.lower()
    filename += '_15_region' + str(section1) + str(section2)

    rubble_filename = 'knowledge_maps/' + filename + '_rubble_kmap.npy'
    victims_filename = 'knowledge_maps/' + filename + '_victim_kmap.npy'

    return victims_filename, rubble_filename


def count_critical_triages(filename: str) -> int:
    """
    REQUIRES: filenmae is preprocessed data csv
    EFFECTS:  Returns total number of critical victim triages in entire mission
    NOTE: to count regular triages, change last line
    """
    mission = pd.read_csv(filename, index_col=0)
    triages = mission[mission.action == 'triage']
    types = triages.action_data.apply(lambda s: s[2:-1].split()[0][:-2])
    return types.value_counts().loc['critical']
