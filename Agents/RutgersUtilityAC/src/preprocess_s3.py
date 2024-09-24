"""
study3_preprocess.py

Wrangles incoming DARPA TA3 ASIST Minecraft Metadata into
format analyzable by Study 3 models and analytic components (AC).
Input is a single '.metadata' (json) file per mission,
output is a trajectory file (.csv).

There are 3 human subjs in a single mission.

CoDaS Lab
1/18/22
"""

import os
import json
import sys
import pandas as pd
import numpy as np
from typing import List, Dict, Set, Tuple, Optional

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def read_file(filename: str) -> pd.DataFrame:
    """
    REQUIRES: filename is valid path to a .metadata asist file
    EFFECTS:  Returns data in filename in DataFrame format
    """

    with open(filename) as f:
        data_list = f.readlines()

    json_list = [ json.loads(l) for l in data_list ]
    df = pd.json_normalize(json_list)

    return df

def add_timing_minimal(raw_mission: pd.DataFrame) -> pd.DataFrame:
    if 'data.elapsed_milliseconds' in raw_mission.columns:
        raw_mission['time'] = raw_mission['data.elapsed_milliseconds']/1000
    else:
        raw_mission['time'] = -1
        return raw_mission[raw_mission.time >= -1]

def add_timing(raw_mission: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is output of read_file('... .metadata')
    MODIFIES: raw_mission
    EFFECTS:  Extracts mission start and end time. Adds a column
              with mission-normalized timestamp in seconds.
              Truncates output so rows before and after mission start/end
              are not included.
    Note: get everything you need from before/after mission before calling this
    """

    # extract start and end time
    start_row = raw_mission[raw_mission['data.mission_state'] == 'Start'].tail(1).iloc[0]
    if len(raw_mission[raw_mission['data.mission_state'] == 'Start']) != 1:
        print('Warning: multiple Start mission events. Using the last one')
    start_time = pd.to_datetime(start_row['@timestamp'])

    # Remove to avoid error when mission ends unexpectedly
    # end_row = raw_mission[(raw_mission['data.mission_timer'] == '0 : 0') &
    #                       (raw_mission.topic == 'observations/state')].iloc[-1]
    # end_time = pd.to_datetime(end_row['@timestamp'])

    # convert timestamps to running seconds in mission
    time = pd.to_datetime(raw_mission['@timestamp'])
    raw_mission['time'] = time.map(lambda t: (t - start_time).total_seconds())

    # truncate mission to within-mission timestamps
    raw_mission.index = time
    raw_mission = raw_mission[raw_mission.index.notna()]  # drop first row
    # todo: test, may need to remove topic mask for end_row
    raw_mission = raw_mission[start_time:] # can go the :end_time if necessary

    return raw_mission


def get_start_time(raw_mission: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: raw_mission
    MODIFIES: 
    EFFECTS:  Extracts mission start time.
    """

    # extract start and end time
    start_row = raw_mission[raw_mission['data.mission_state'] == 'Start'].tail(1).iloc[0]
    if len(raw_mission[raw_mission['data.mission_state'] == 'Start']) != 1:
        print('Warning: multiple Start mission events. Using the last one')
    start_time = pd.to_datetime(start_row['@timestamp'])

    return start_time


def add_timing_news(raw_mission: pd.DataFrame, start_time) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is output of read_file('... .metadata')
              start_time is the output of get_start_time(raw_mission)
    MODIFIES: raw_mission
    EFFECTS:  Adds a column with mission-normalized timestamp in seconds.
              Truncates output so rows before and after mission start/end
              are not included.
    """

    # convert timestamps to running seconds in mission
    time = pd.to_datetime(raw_mission['@timestamp'])
    raw_mission['time'] = time.map(lambda t: (t - start_time).total_seconds())

    # truncate mission to within-mission timestamps
    raw_mission.index = time
    raw_mission = raw_mission[raw_mission.index.notna()]  # drop first row

    return raw_mission


def extract_trial_info(raw_mission: pd.DataFrame) -> (str, str, str, Dict[str, str]):
    """
    REQUIRES: raw_mission is output of read_file('... .metadata')
              (i.e. add_timing has not been called, etc)
    EFFECTS:  Extracts mission number (1 = first or 2 = second) (TODO),
              between-subj/team condition (team or individual planning), and
              within-subj/team map condition (1 = SaturnA or 2 = SaturnB)
              from mission data. Also extracts map knowledge condition
              for each participant.
    """

    firstrow = raw_mission.iloc[0]
    secondrow = raw_mission.iloc[1]

    # get trial number/id
    trial_num = int(firstrow['data.metadata.trial.trial_number'][-6:])
    # hardcode fix for incorrect trial num in Trial 317
    if firstrow['data.metadata.trial.trial_number'] == 'T000317_TM000022':
        trial_num = 317

    # TODO: get mission number (first or second)

    # get between-subj planning condition
    # todo: more pythonic error handling
    planning_cond_i = int(firstrow['data.metadata.trial.condition'])
    if planning_cond_i == 1:
        planning_cond = 'team'
    elif planning_cond_i == 2:
        planning_cond = 'individual'
    else:
        raise ValueError('Could not find btwn-subj planning condition')

    # get within-team map condition
    # TODO: find message spec for this...
    map_cond = secondrow['data.experiment_mission']
    if map_cond == 'Saturn_1':
        map_cond = 'SaturnA_Feb4_Pilot'  # T290
    elif map_cond not in {'Saturn_A', 'Saturn_B'}:
        raise ValueError(f'Could not find within-subj team map condition: {map_cond}')

    # get within-subj map knowledge conditions
    map_knowledge_conds = extract_map_knowledge_conds(raw_mission, trial_num)

    return trial_num, planning_cond, map_cond, map_knowledge_conds


def extract_map_knowledge_conds(raw_mission: pd.DataFrame) -> Dict[str, str]:
    """
    REQUIRES: raw_mission has not been pruned (add_timing has not been called)
              i.e. raw_mission is pd.json_normalize(pd.read_csv('raw_data_file.metadata'))
    EFFECTS:  Reads off the static knowledge density maps assigned to each player.
              Returns a dict from player id to name of static density map.
    """

    startrow = raw_mission[raw_mission.topic == 'trial'].iloc[0]

    client_info = startrow['data.client_info']
    playername_key = 'playername' if 'playername' in next(iter(client_info)) \
                                  else 'participant_id'
    map_knowledge_conds = { info[playername_key]: info['staticmapversion'] for info in client_info }

    return map_knowledge_conds


def extract_mission_victims(raw_mission: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is ouptut of read_file('... .metadata')
              i.e. add_timing has not been run yet.
    EFFECTS:  Returns a dataframe in preprocessed format listing
              victim types and locations.
    """
    VICTIM_TYPE_MAP = {'block_victim_1': 'normal', 'block_victim_proximity': 'critical',
                       'block_victim_2': 'critical'}  # for T290

    victims = raw_mission[raw_mission['msg.sub_type'] == 'Mission:VictimList'].iloc[0]
    victims = pd.json_normalize(victims['data.mission_victim_list'])

    # build output format
    victims.drop(columns=['room_name'], inplace=True)
    victims.rename(columns={'block_type': 'victim_type'}, inplace=True)
    victims.victim_type = victims.victim_type.apply(lambda v: VICTIM_TYPE_MAP[v])
    victims['status'] = 0  # unsaved
    victims.index = range(len(victims))
    victims.index.name = 'victim_id'

    # reorder columns
    victims = victims.reindex(columns=['x', 'y', 'z', 'victim_type', 'status'])

    return victims


def extract_mission_rubble(raw_mission: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is output of read_file('... .metadata')
              i.e. add_timing has not been run yet
    EFFECTS:  Returns rubble locations in this format:
              TODO
    """

    blockages = raw_mission[raw_mission['msg.sub_type'] == 'Mission:BlockageList'].iloc[0]
    blockages = blockages['data.mission_blockage_list']

    # TODO: assign cluster ids automatically
    return blockages


def verify_map(raw_mission: pd.DataFrame, map_type: str) -> bool:
    """
    REQUIRES: raw_mission is output of read-file('... .metadata')
              map_type in {'SaturnA', 'SaturnB'}
              map_type matches map used in raw_mission
    EFFECTS:  Returns true if victim and rubble locations provided
              match those specified in raw_mission. Returns false otherwise
    """

    mission_victims = get_init_victims_info(raw_mission).sort_values('x').sort_index(1)
    mission_rubble = get_init_rubble_info(raw_mission).drop(columns='cluster_id').sort_values('x')
    mission_rubble.sort_index(1, inplace=True)

    if map_type == 'SaturnA':
        victims_gt = pd.read_csv('preprocessed_data/Study2_SaturnA_victims.csv', index_col=0)
        rubble_gt = pd.read_csv('preprocessed_data/Study2_SaturnA_rubble.csv', index_col=0)
    elif map_type == 'SaturnB':
        victims_gt = pd.read_csv('preprocessed_data/Study2_SaturnB_victims.csv', index_col=0)
        rubble_gt = pd.read_csv('preprocessed_data/Study2_SaturnB_rubble.csv', index_col=0)
    else:
        raise ValueError(f'Invalid map type: {map_type}')

    victims_gt = victims_gt.sort_values('x').sort_index(1)
    rubble_gt = rubble_gt.drop(columns='cluster_id').sort_values('x').sort_index(1)

    if not victims_gt.equals(mission_victims):
        return False
    if not rubble_gt.equals(mission_rubble):
        return False

    return True


def boil(raw_mission: pd.DataFrame, trial_num: int, team_id: int, trial_order: int, planning_cond: str,
         mission_map: str, map_knowledge_conds: Dict[str, str], initial_roles=None) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is output of add_timing
    EFFECTS:  Boils raw_mission down to a format best used for utility analysis.
              Output will be in long format with columns:
                player_id, x, y, z, yaw, map_area, map_knowledge_cond, current_role,
                time, score, teamwork_cond, mission_map, mission_number, action, action_data
              action will contain one of {move, switch_role, triage, remove_rubble,
                                          pickup_victim, place_victim, unfreeze, get_frozen,
                                          tool_depleted}
              action_data will contain info relevant to corresponding action.
                e.g. action: triage, action_data: [victim coords] [victim type]
                     action: remove_rubble, action_data: [rubble coords]
                     action: switch_role, action_data: [old role]
                        (new role will be in current_role col)
                     action: tool_depleted, action_data: [current role]
              time will be in seconds from start of the mission.
    Note:     Designed so that, hopefully, changes will amount to simply adding
              a new column or possible value for action/action_data.
    """

    COLS = ['player_id', 'x', 'y', 'z', 'yaw', 'map_area', 'map_knowledge_cond',
            'current_role', 'score', 'teamwork_cond', 'mission_map',
            'action', 'action_data', 'time', 'trial_num', 'trial_order', 'team_id']
    COLS_MAPPING = {'data.playername': 'player_id', 'data.participant_id': 'player_id',
                    'data.x': 'x', 'data.y': 'y', 'data.z': 'z', 'data.yaw': 'yaw', 'time': 'time',
                    'data.scoreboard.TeamScore': 'score'}
    VICTIM_TYPE_MAP = {'victim_a': 'victim_a', 'victim_saved_a': 'victim_saved_a',
                       'victim_b': 'victim_b', 'victim_saved_b': 'victim_saved_b',
                       'victim_c': 'victim_c', 'victim_saved_c': 'victim_saved_c', }

    MISSION_BASE_COLS = ['data.x', 'data.z', 'data.y', 'data.yaw', 'time']
    MISSION_BASE_COLS.append('data.playername' if 'data.playername' in raw_mission.columns
                             else 'data.participant_id')

    # wrangle into output format
    # (movement, score) using 'observations/state' MQTT message bus topic
    df = raw_mission[raw_mission.topic == 'observations/state'][MISSION_BASE_COLS]
    df.rename(columns=COLS_MAPPING, inplace=True)
    df['action'] = 'move'

    # initialize all desired columns
    for c in COLS:
        if c not in df.columns:
            df[c] = np.nan
    # assuming you have to move before you can score
    df.loc[df.head(1).index, 'score'] = 0

    # lookup successful role switches and add
    df = pd.concat((df, get_roleswitches(raw_mission, MISSION_BASE_COLS, COLS_MAPPING,
                                         initial_roles=initial_roles)))

    # lookup successful victim triages and add
    df = pd.concat((df, get_triages(raw_mission, MISSION_BASE_COLS, COLS_MAPPING, VICTIM_TYPE_MAP)))

    # lookup successful rubble removals and add
    df = pd.concat((df, get_rubble_removes(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup successful victim pickups/placements and add
    df = pd.concat((df, get_victim_actions(raw_mission, MISSION_BASE_COLS, COLS_MAPPING,
                                          VICTIM_TYPE_MAP)))

    # lookup freezes and medic unfreezes
    df = pd.concat((df, get_freezes(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup when tools run out
    df = pd.concat((df, get_tooldepletions(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup markers placed
    df = pd.concat((df, get_markers_placed(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup rubble collapse
    df = pd.concat((df, get_rubble_collapse(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))


    # add fov data
    # TODO: finish implementing
    #df = pd.concat((df, parse_fov(raw_mission, COLS_MAPPING)))

    # fill in missing location and role values
    # TODO: spend more time verifying this is correct
    df.sort_index(inplace=True)
    df[['x', 'y', 'z', 'yaw', 'current_role']] = df.groupby('player_id')[['x', 'y', 'z',
                                                                          'yaw', 'current_role']]\
                                                 .transform(lambda grp: grp.fillna(method='ffill'))
    df.score = df.score.fillna(method='ffill')

    if not check_roles(df):
        raise ValueError('something wrong with role and action matching.')

    # add mission metadata
    df.trial_num = trial_num
    df.trial_order = trial_order
    df.team_id = team_id
    df.teamwork_cond = planning_cond
    df.mission_map = mission_map
    # add static map knowledge map cond for each ppt
    df.map_knowledge_cond = df.apply(lambda r: map_knowledge_conds[r.player_id], axis=1)

    # change player_id to callsign

    return df

def boil_minimal(raw_mission: pd.DataFrame, mission_map: str) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is output of add_timing
    EFFECTS:
    Note:
    """

    COLS = ['player_id', 'x', 'y', 'z', 'yaw', 'current_role', 'mission_map',
            'action', 'action_data', 'time', 'score']
    COLS_MAPPING = {'data.playername': 'player_id', 'data.participant_id': 'player_id',
                    'data.x': 'x', 'data.y': 'y', 'data.z': 'z', 'data.yaw': 'yaw', 'time': 'time',
                    'data.scoreboard.TeamScore': 'score'}
    VICTIM_TYPE_MAP = {'victim_a': 'victim_a', 'victim_saved_a': 'victim_saved_a',
                       'victim_b': 'victim_b', 'victim_saved_b': 'victim_saved_b',
                       'victim_c': 'victim_c', 'victim_saved_c': 'victim_saved_c', }

    MISSION_BASE_COLS = ['data.x', 'data.z', 'data.y', 'data.yaw', 'time']
    MISSION_BASE_COLS.append('data.playername' if 'data.playername' in raw_mission.columns
                             else 'data.participant_id')

    # initialize all desired columns
    df = pd.DataFrame(columns=COLS)

    # # wrangle into output format
    # # (movement, score) using 'observations/state' MQTT message bus topic    
    # df = raw_mission[raw_mission.topic == 'observations/state'][MISSION_BASE_COLS]
    # df.rename(columns=COLS_MAPPING, inplace=True)
    # df['action'] = 'move'

    # # initialize all desired columns
    # for c in COLS:
    #     if c not in df.columns:
    #         df[c] = np.nan

    # fill time column
    if 'data.elapsed_milliseconds' in raw_mission.columns:
        raw_mission['time'] = raw_mission['data.elapsed_milliseconds']/1000
    else:
        raw_mission['time'] = -1

    # add movement data
    mv_inds = raw_mission.topic == 'observations/state'
    if np.sum(mv_inds) > 0:
        mv = raw_mission[mv_inds][MISSION_BASE_COLS]
        mv.rename(columns=COLS_MAPPING, inplace=True)
        mv['action'] = 'move'
        df = pd.concat((df, mv))

    # add base columns if they are not there
    for col_names in MISSION_BASE_COLS:
        if col_names not in raw_mission.columns:
            raw_mission[col_names] = np.nan

    # lookup rubble collapse
    df = pd.concat((df, get_rubble_collapse(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup successful rubble removals and add
    df = pd.concat((df, get_rubble_removes(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup successful victim triages and add
    df = pd.concat((df, get_triages_minimal(raw_mission, MISSION_BASE_COLS, COLS_MAPPING, 
                                            VICTIM_TYPE_MAP)))

    # lookup successful victim pickups/placements and add
    # df = pd.concat((df, get_victim_actions(raw_mission, MISSION_BASE_COLS, COLS_MAPPING,
    #                                        VICTIM_TYPE_MAP)))
    df = pd.concat((df, get_victim_pickup(raw_mission, MISSION_BASE_COLS, COLS_MAPPING,
                                           VICTIM_TYPE_MAP)))
    df = pd.concat((df, get_victim_dropoff(raw_mission, MISSION_BASE_COLS, COLS_MAPPING,
                                           VICTIM_TYPE_MAP)))

    # lookup markers placed
    df = pd.concat((df, get_markers_placed(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup signals detected
    df = pd.concat((df, get_signals(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # lookup signals detected
    df = pd.concat((df, get_door_event(raw_mission, MISSION_BASE_COLS, COLS_MAPPING)))

    # add mission metadata
    df.mission_map = mission_map

    return df

def get_roleswitches(raw_mission: pd.DataFrame, base_cols: List[str], cols_mapping: Dict[str, str],
                     initial_roles=None) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
              initial_roles is either None or a Dict[str, str] from player_id to
                role types (as listed in ROLE_NAMES_MAP.values())
    EFFECTS: returns Dataframe with all role switches and expected data
             matches output format of boil
    """
    ROLE_NAMES_MAP = {'Engineering_Specialist': 'rubbler',
                      'Medical_Specialist': 'medic',
                      'Transport_Specialist': 'scout'}

    roleswitches = raw_mission[raw_mission.topic == 'observations/events/player/role_selected']
    roleswitches = roleswitches[base_cols + ['data.new_role', 'data.prev_role']]
    roleswitches.rename(columns=cols_mapping, inplace=True)
    roleswitches.rename(columns={'data.new_role': 'current_role', 'data.prev_role': 'action_data'},
                        inplace=True)
    roleswitches['action'] = 'switch_role'

    roleswitches.current_role = roleswitches.current_role.map(ROLE_NAMES_MAP)
    roleswitches.action_data = roleswitches.action_data.map(ROLE_NAMES_MAP)

    if initial_roles is not None:
        # create rows for initial role selections
        startingroles = pd.DataFrame({'action': ['switch_role']*len(initial_roles),
                                      # coindexed, see https://stackoverflow.com/questions/835092
                                      'player_id': list(initial_roles.keys()),
                                      'current_role': list(initial_roles.values()),
                                      'time': [0]*len(initial_roles)})  # mission start
        startingroles.index = [raw_mission.iloc[0].name] * len(startingroles)

        roleswitches = pd.concat((startingroles, roleswitches))

    return roleswitches


def get_roles_premission(raw_mission: pd.DataFrame) -> Optional[Dict[str, str]]:
    """
    REQUIRES: add_timing(raw_mission) has NOT been called, i.e.
              raw_mission = pd.json_normalize(pd.read_csv('raw_mission_file.metadata'))
    EFFECTS:  Extracts, for each player, the last role selected before mission start.
              Returns a dict from player id to the role they chose.
    """
    ROLE_NAMES_MAP = {'Engineering_Specialist': 'rubbler',
                      'Medical_Specialist': 'medic',
                      'Transport_Specialist': 'scout'}

    start_row = raw_mission[raw_mission['data.mission_state'] == 'Start'].tail(1).iloc[0]
    if len(raw_mission[raw_mission['data.mission_state'] == 'Start']) != 1:
        print('Warning: multiple Start mission events. Using the last one')
    start_row_idx = start_row.name

    roleswitches = raw_mission.loc[:start_row_idx][raw_mission.loc[:start_row_idx]\
                              .topic == 'observations/events/player/role_selected']

    if len(roleswitches) == 0:
        # guess no-one selected a role before mission start
        return None

    player_id_colname = 'data.playername' if 'data.playername' in raw_mission.columns \
                                          else 'data.participant_id'
    lastpicks = roleswitches.groupby(player_id_colname)[[player_id_colname, 'data.new_role']].tail(1)

    # construct dict
    lastpicks.index = lastpicks[player_id_colname]
    lastpicks = lastpicks.to_dict()['data.new_role']
    lastpicks = { p_id: ROLE_NAMES_MAP[role] for p_id, role in lastpicks.items() }

    assert(len(lastpicks) <= 3)

    return lastpicks


def get_roles_final(raw_mission: pd.DataFrame) -> Optional[Dict[str, str]]:
    """
    REQUIRES: add_timing(raw_mission) has NOT been called, i.e.
              raw_mission = pd.json_normalize(pd.read_csv('raw_mission_file.metadata'))
    EFFECTS:  Extracts, for each player, the last role selected.
              Returns a dict from player id to the role they chose.
    """
    ROLE_NAMES_MAP = {'Engineering_Specialist': 'rubbler',
                      'Medical_Specialist': 'medic',
                      'Transport_Specialist': 'scout'}

    roleswitches = raw_mission[raw_mission .topic == 'observations/events/player/role_selected']

    if len(roleswitches) == 0:
        # guess no-one selected a role before mission start
        return None

    player_id_colname = 'data.playername' if 'data.playername' in raw_mission.columns \
                                          else 'data.participant_id'
    lastpicks = roleswitches.groupby(player_id_colname)[[player_id_colname, 'data.new_role']].tail(1)

    # construct dict
    lastpicks.index = lastpicks[player_id_colname]
    lastpicks = lastpicks.to_dict()['data.new_role']
    lastpicks = { p_id: ROLE_NAMES_MAP[role] for p_id, role in lastpicks.items() }

    assert(len(lastpicks) <= 3)

    return lastpicks


def get_tooldepletions(raw_mission: pd.DataFrame, base_cols: List[str],
                       cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns DataFrame with all tool depletions (i.e. when tool cannot
              be used anymore and needs to be replenished). Matches output format
              of boil
    """
    TOOL_NAMES_MAP = {'MEDKIT': 'medic',
                      'HAMMER': 'rubbler',
                      'STRETCHER': 'scout',
                      'STRETCHER_OCCUPIED': 'scout'}

    tooldepletions = raw_mission[raw_mission.topic == 'observations/events/player/tool_depleted']
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//
    # MessageSpecs/ToolDepleted/tool_depleted_event_message.md
    tooldepletions = tooldepletions[base_cols + ['data.tool_type']]
    tooldepletions.rename(columns=cols_mapping, inplace=True)
    tooldepletions.rename(columns={'data.tool_type': 'action_data'}, inplace=True)
    tooldepletions['action'] = 'tool_depleted'

    tooldepletions.action_data = tooldepletions.action_data.map(TOOL_NAMES_MAP)

    return tooldepletions


def get_freezes(raw_mission: pd.DataFrame, base_cols: List[str],
                cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns all moments when players trigger a freeze block (become frozen)
              and when another player rescues them. In output format of boil
    """
    FREEZE_STATE_MAP = {'FROZEN': 'get_frozen', 'UNFROZEN': 'unfreeze'}
    # go here for message spec
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/
    # PlayerFrozenStateChange/player_frozen_state_change_event_message.md

    medic_colname = 'data.medic_playername' if 'data.playername' in base_cols \
                                            else 'data.medic_participant_id'

    freezes = raw_mission[raw_mission.topic == 'observations/events/player/freeze']

    if len(freezes) == 0:
        return pd.DataFrame()

    freezes = freezes[base_cols + ['data.state_changed_to', medic_colname]]
    freezes.rename(columns=cols_mapping, inplace=True)

    # want to replace player "getting unfrozen" events with medic "unfreezing player" actions...
    freezes.rename(columns={'data.state_changed_to': 'action'}, inplace=True)
    # put frozen player id in action_data column if they're getting unfrozen
    freezes['action_data'] = freezes.apply(lambda r: r['player_id'] if r.action == 'UNFROZEN'
                                           else np.nan, axis=1)
    freezes.action = freezes.action.apply(lambda x: FREEZE_STATE_MAP[x])
    # replace player_id with player performing the action
    freezes.player_id = freezes.apply(lambda r: r[medic_colname] if r.action == 'unfreeze'
                                      else r.player_id, axis=1)
    # remove location data for unfreeze actions; this needs to be overwritten with medic
    # coordinates later
    freezes.loc[freezes.action == 'unfreeze', ['x', 'z', 'y', 'yaw']] = np.nan, np.nan, np.nan, \
                                                                        np.nan
    freezes.drop(columns=medic_colname, inplace=True)

    # TODO: really check this...
    return freezes


def get_triages(raw_mission: pd.DataFrame, base_cols: List[str], cols_mapping: Dict[str, str],
                victim_type_map: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  returns all successful victim triages, output matches output format of boil
              Also includes scoring data, since score only changes when victims are triaged.
    """
    # go here for message spec
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Triage
    # /triage_event_message.md

    triages = raw_mission[raw_mission.topic == 'observations/events/player/triage']
    
    if len(triages) == 0:
        return pd.DataFrame()

    triages = triages[triages['data.triage_state'] == 'SUCCESSFUL']
    triages = triages[base_cols + ['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id',
                                   'data.scoreboard.TeamScore']]

    triages.rename(columns=cols_mapping, inplace=True)
    triages['action'] = 'triage'

    def package_triage_actiondata(r: pd.Series, victim_type_map: Dict[str, str]) -> tuple:
        victim_info = (victim_type_map[r['data.type']], r['data.victim_x'], r['data.victim_z'], 
                       r['data.victim_id'])
        return victim_info

    triages['action_data'] = triages.apply(package_triage_actiondata, axis=1,
                                           victim_type_map=victim_type_map)

    triages.drop(columns=['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id'], inplace=True)
    # medic role specified later in boil

    # get score data
    score_col_idx = list(triages.columns).index('score')
    def assign_score(score_row: pd.Series, triagedf: pd.DataFrame) -> None:
        score = score_row['data.scoreboard.TeamScore']
        triage_idx = triagedf[triagedf.time <= score_row.time].iloc[-1].name
        triagedf.loc[triage_idx, 'score'] = score
        return
    scores = raw_mission.loc[raw_mission.topic == 'observations/events/scoreboard',
                             ['time', 'data.scoreboard.TeamScore']]
    scores.apply(assign_score, triagedf=triages, axis=1)

    return triages


def get_triages_minimal(raw_mission: pd.DataFrame, base_cols: List[str], cols_mapping: Dict[str, str],
                victim_type_map: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  returns all successful victim triages, output matches output format of boil
              Also includes scoring data, since score only changes when victims are triaged.
    """
    # go here for message spec
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Triage
    # /triage_event_message.md

    triages = raw_mission[raw_mission.topic == 'observations/events/player/triage']
    if len(triages) == 0:
        return pd.DataFrame()

    triages = triages[triages['data.triage_state'] == 'SUCCESSFUL']
    if len(triages) == 0:
        return pd.DataFrame()

    triages = triages[base_cols + ['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id']]

    triages.rename(columns=cols_mapping, inplace=True)
    triages['action'] = 'triage'

    def package_triage_actiondata(r: pd.Series) -> tuple:
        victim_info = (r['data.type'], r['data.victim_x'], r['data.victim_z'], 
                       r['data.victim_id'])
        # print(f"DEBUG package_triage_actiondata:, {victim_info}")
        return victim_info

    triages['action_data'] = triages.apply(package_triage_actiondata, axis=1)

    triages.drop(columns=['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id'], inplace=True)
    # medic role specified later in boil

    return triages


def get_markers_placed(raw_mission: pd.DataFrame, base_cols: List[str],
                         cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  returns all marker placement events, output matches output format of boil
    """
    # go here for message spec
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MarkerPlaced
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MarkerRemoved
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MarkerDestroyed

    markers_placed = raw_mission[raw_mission.topic == 'observations/events/player/marker_placed']

    if len(markers_placed) == 0:
        return pd.DataFrame()

    markers_placed = markers_placed[base_cols + ['data.type', 'data.marker_x',
                                                 'data.marker_z', 'data.marker_y']]
    markers_placed.rename(columns=cols_mapping, inplace=True)
    markers_placed['action'] = 'marker_placed'

    def package_marker_actiondata(r: pd.Series) -> tuple:
        marker_info = (r['data.type'], r['data.marker_x'], r['data.marker_z'], r['data.marker_y'])
        return marker_info

    markers_placed['action_data'] = markers_placed.apply(package_marker_actiondata, axis=1)

    markers_placed.drop(columns=['data.type', 'data.marker_x', 
                                 'data.marker_z', 'data.marker_y'], inplace=True)

    return markers_placed


def get_signals(raw_mission: pd.DataFrame, base_cols: List[str],
                cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  returns all signal detection events, output matches output format of boil
    """

    signals = raw_mission[raw_mission.topic == "observations/events/player/signal"]

    if len(signals) == 0:
        return pd.DataFrame()

    signals = signals[base_cols + ['data.roomname', 'data.message']]
    signals.rename(columns=cols_mapping, inplace=True)
    signals['action'] = 'signal_detected'

    def package_signal_actiondata(r: pd.Series) -> tuple:
        signal_info = (r['data.roomname'], r['data.message'].replace(' ', '_'))
        return signal_info

    signals['action_data'] = signals.apply(package_signal_actiondata, axis=1)

    signals.drop(columns=['data.roomname', 'data.message'], inplace=True)

    return signals


def get_door_event(raw_mission: pd.DataFrame, base_cols: List[str],
                cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  returns all door events, output matches output format of boil
    """

    door = raw_mission[raw_mission.topic == "observations/events/player/door"]

    if len(door) == 0:
        return pd.DataFrame()

    door = door[base_cols + ['data.door_x', 'data.door_z', 'data.door_y']]
    door.rename(columns=cols_mapping, inplace=True)
    door['action'] = 'door_open'

    def package_door_actiondata(r: pd.Series) -> tuple:
        door_info = (r['data.door_x'], r['data.door_z'], r['data.door_y'])
        return door_info

    door['action_data'] = door.apply(package_door_actiondata, axis=1)

    door.drop(columns=['data.door_x', 'data.door_z', 'data.door_y'], inplace=True)

    return door


def get_rubble_removes(raw_mission: pd.DataFrame, base_cols: List[str],
                       cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns dataframe in boil output format of all successful rubble remove actions
    """

    rubble_removes = raw_mission[raw_mission.topic == 'observations/events/player/rubble_destroyed']

    if len(rubble_removes) == 0:
        return pd.DataFrame()

    rubble_removes = rubble_removes[base_cols + ['data.rubble_x', 'data.rubble_z', 'data.rubble_y']]
    rubble_removes.rename(columns=cols_mapping, inplace=True)
    rubble_removes['action'] = 'remove_rubble'

    def package_rubble_actiondata(r: pd.Series) -> tuple:
        rubble_info = (r['data.rubble_x'], r['data.rubble_z'], r['data.rubble_y'])
        return rubble_info

    rubble_removes['action_data'] = rubble_removes.apply(package_rubble_actiondata, axis=1)

    rubble_removes.drop(columns=['data.rubble_x', 'data.rubble_z', 'data.rubble_y'], inplace=True)
    # rubbler role specified later in boil

    return rubble_removes


def get_rubble_collapse(raw_mission: pd.DataFrame, base_cols: List[str],
                       cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns dataframe in boil output format of all instance of rubble collapse triggered
    """

    rubble_collapse = raw_mission[raw_mission.topic == 'observations/events/player/rubble_collapse']

    if len(rubble_collapse) == 0:
        return pd.DataFrame()

    rubble_collapse = rubble_collapse[base_cols + ['data.fromBlock_x', 'data.fromBlock_z', 'data.fromBlock_y']]
    rubble_collapse.rename(columns=cols_mapping, inplace=True)
    rubble_collapse['action'] = 'trigger_rubble_collapse'

    def package_rubble_actiondata(r: pd.Series) -> tuple:
        rubble_info = (r['data.fromBlock_x'], r['data.fromBlock_z'], r['data.fromBlock_y'])
        return rubble_info

    rubble_collapse['action_data'] = rubble_collapse.apply(package_rubble_actiondata, axis=1)

    rubble_collapse.drop(columns=['data.fromBlock_x', 'data.fromBlock_z', 'data.fromBlock_y'], inplace=True)
    # rubbler role specified later in boil

    return rubble_collapse


def get_victim_pickup(raw_mission: pd.DataFrame, base_cols: List[str], cols_mapping: Dict[str, str],
                      victim_type_map: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns dataframe in boil output format with all successful victim pickups.
    """

    v_pickups = raw_mission[raw_mission.topic == 'observations/events/player/victim_picked_up']
    if len(v_pickups) == 0:
        return pd.DataFrame()

    v_pickups = v_pickups[base_cols + ['data.victim_x', 'data.victim_z', 'data.type', 'data.victim_id']]
    v_pickups.rename(columns=cols_mapping, inplace=True)
    v_pickups['action'] = 'pickup_victim'

    def package_scout_actiondata(r: pd.Series, victim_type_map: Dict[str, str]) -> tuple:
        info = (victim_type_map[r['data.type']], r['data.victim_x'], r['data.victim_z'], r['data.victim_id'])
        return info

    v_pickups['action_data'] = v_pickups.apply(package_scout_actiondata, axis=1,
                                               victim_type_map=victim_type_map)

    v_pickups.drop(columns=['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id'], inplace=True)
 
    return v_pickups


def get_victim_dropoff(raw_mission: pd.DataFrame, base_cols: List[str], cols_mapping: Dict[str, str],
                      victim_type_map: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns dataframe in boil output format with all successful victim dropoffs.
    """

    v_dropoffs = raw_mission[raw_mission.topic == 'observations/events/player/victim_placed']
    if len(v_dropoffs) == 0:
        return pd.DataFrame()

    v_dropoffs = v_dropoffs[base_cols + ['data.victim_x', 'data.victim_z', 'data.type', 'data.victim_id']]
    v_dropoffs.rename(columns=cols_mapping, inplace=True)
    v_dropoffs['action'] = 'place_victim'

    def package_scout_actiondata(r: pd.Series, victim_type_map: Dict[str, str]) -> tuple:
        info = (victim_type_map[r['data.type']], r['data.victim_x'], r['data.victim_z'], r['data.victim_id'])
        return info

    v_dropoffs['action_data'] = v_dropoffs.apply(package_scout_actiondata, axis=1,
                                               victim_type_map=victim_type_map)
 
    v_dropoffs.drop(columns=['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id'], inplace=True)
    
    return v_dropoffs


def get_victim_actions(raw_mission: pd.DataFrame, base_cols: List[str], cols_mapping: Dict[str, str],
                      victim_type_map: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Returns dataframe in boil output format with all successful victim pickups
              and victim places.
    """

    # go here for pickup victim message spec
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/VictimPickedUp/
    # victim_picked_up_event_message.md
    v_pickups = raw_mission[raw_mission.topic == 'observations/events/player/victim_picked_up']
    if len(v_pickups) > 0:
        v_pickups = v_pickups[base_cols + ['data.victim_x', 'data.victim_z', 'data.type', 'data.victim_id']]
        v_pickups.rename(columns=cols_mapping, inplace=True)
        v_pickups['action'] = 'pickup_victim'

    # go here for drop off victim message spec
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/VictimPlaced/
    # victim_placed_event_message.md
    v_dropoffs = raw_mission[raw_mission.topic == 'observations/events/player/victim_placed']
    if len(v_dropoffs) > 0:
        v_dropoffs = v_dropoffs[base_cols + ['data.victim_x', 'data.victim_z', 'data.type', 'data.victim_id']]
        v_dropoffs.rename(columns=cols_mapping, inplace=True)
        v_dropoffs['action'] = 'place_victim'

    def package_scout_actiondata(r: pd.Series, victim_type_map: Dict[str, str]) -> tuple:
        info = (victim_type_map[r['data.type']], r['data.victim_x'], r['data.victim_z'], r['data.victim_id'])
        return info

    # rewriting verbosely to make more readable
    if len(v_pickups) > 0 and len(v_dropoffs) == 0:
        v_pickups['action_data'] = v_pickups.apply(package_scout_actiondata, axis=1,
                                                           victim_type_map=victim_type_map)
    elif len(v_pickups) > 0 and len(v_dropoffs) > 0:
        v_pickups['action_data'] = v_pickups.apply(package_scout_actiondata, axis=1,
                                                           victim_type_map=victim_type_map)
        v_dropoffs['action_data'] = v_dropoffs.apply(package_scout_actiondata, axis=1,
                                                             victim_type_map=victim_type_map)
    elif len(v_pickups) == 0 and len(v_dropoffs) == 0:
        return pd.DataFrame()
    else:
        # something wrong, because there were no scout pickups
        # but there were scout drop offs
        print('scout may have dropped off a victim without picking up one')
        # raise ValueError('scout may have dropped off a victim without picking up one')

    # scout role specified later in boil

    v_pickups.drop(columns=['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id'], inplace=True)
    v_dropoffs.drop(columns=['data.type', 'data.victim_x', 'data.victim_z', 'data.victim_id'], inplace=True)
 
    return pd.concat((v_pickups, v_dropoffs))


def parse_fov(raw_mission: pd.DataFrame, cols_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    REQUIRES: raw_mission is input to boil
    EFFECTS:  Parses FOV data. Produces a dataframe in boil output format, with
              action == "observe" and action_data a list of tuples, e.g.
                ('regular_victim', x, y, z, victim_id)
                ('critical_victim', x, y, z, victim_id)
                ('rubble', x, y, z, block_id, cluster_id)
              A tuple for a victim/rubble entity is only listed THE FIRST TIME
              it appears in the FoV data (i.e. the first time the agent perceives it)
    """

    observations = raw_mission[raw_mission.topic == 'agent/pygl_fov/player/3d/summary']
    if len(observations) == 0:
        print('Cannot find FOV data!')

    observations = observations[['data.playername', 'data.x', 'data.y', 'data.z', 'data.yaw',
                                 'time', 'data.blocks']]
    observations.rename(columns=cols_mapping, inplace=True)
    observations['action'] = 'observe'

    # parse data.blocks column
    # see spec here:
    # https://gitlab.com/artificialsocialintelligence/study3/-/blob/master/MessageSpecs/PyGLFoVAgent/fov.md
    def parse_blocks(r: pd.Series) -> pd.DataFrame:
        """
        REQUIRES: r['data.blocks']
        EFFECTS:  Returns a dataframe in boil format with
                  a single block observation in each row.
                  Only 'gravel' (rubble) and victim observations
                  are included
        """
        # TODO: include saved victims?
        IMPORTANT_ENTITIES = {'gravel', 'block_victim_1', 'block_victim_proximity'}
        PIXEL_THRESHOLD = 200

        b = pd.json_normalize(r['data.blocks'])
        b = b[(b['type'].isin(IMPORTANT_ENTITIES)) & (b.number_pixels > PIXEL_THRESHOLD)]

        pd.concat((b[['type', 'location']], observations.iloc[2002].drop(columns=['data.blocks'])),
                  axis=1)  # TODO not correct

    # TODO
    raise NotImplementedError


def check_yaws(df: pd.DataFrame, toomany_warning=2) -> pd.DataFrame:
    """
    REQUIRES: df is preprocessed mission file
              df.index.name is not in df.columns
    MODIFIES: df
    EFFECTS:  Checks if any Minecraft yaw values are above 360 or below -360.
              If more than toomany_warning rows have spurious yaw values,
              raises an error so user can take a deeper look.
              Returns df with the spurious yaw row removed, if it exists.
    """

    spurious_mask = (df.yaw < -360) | (df.yaw > 360)
    spurious = df[spurious_mask]
    if len(spurious) == 0:
        return df
    elif len(spurious) <= toomany_warning:
        # remove this row
        print(f'Removing {len(spurious)} rows from trial '
              f'{df.iloc[0].trial_num}: {spurious.T}')
        if df.index.name is None:
            # this may have been erased when player starting roles were padded before mission start
            df.index.name = '@timestamp'

        # fancy stuff needed because there are duplicate timestamp-based indices
        df_index_col = df.index.name
        df_i = df.reset_index()
        spurious_i = df_i[(df_i.yaw < -360) | (df_i.yaw > 360)].index
        df = df_i.drop(index=spurious_i)
        df.index = df[df_index_col]
        df.drop(columns=df_index_col, inplace=True)
        return df
    else:
        raise ValueError(f'Too many rows with spurious yaw values. '
                         f'Need to take a deeper look at trial {df.iloc[0].trial_num}')


def check_yaws_script(dry_run=True):
    # run this to check yaw values of all files in preprocessed_data folder.
    data_dir = '/projects/f_ps848_1/ASIST/TA3-data/study-2-2021-07/preprocessed_v3'
    missions = [ m for m in os.listdir(data_dir)
                 if m.startswith('study2_preprocessed_T') and m.endswith('.csv') ]
    for mission_filename in missions:
        mission_df = pd.read_csv(data_dir+'/'+mission_filename, index_col=0)
        mission_df = check_yaws(mission_df)
        if not dry_run:
            print(f'saving {mission_filename}')
            mission_df.to_csv(data_dir+'/'+mission_filename)

    return


def check_roles(df: pd.DataFrame) -> bool:
    """
    REQUIRES: df is in boil output format (columns)
              df is sorted by Timestamp index
    EFFECTS:  Asserts that all actions are taken by appropriate roles
    """

    def assert_valid_action(r: pd.Series) -> bool:
        VALID_ACTIONS = {'medic': {'triage'},
                         'rubbler': {'remove_rubble'},
                         'scout': {}}
        if r.action in {'move', 'switch_role', 'tool_depleted', 'get_frozen',
                        'observe', 'marker_placed', 'trigger_rubble_collapse',
                        'pickup_victim', 'place_victim'}:
            # actions available to any role
            return True
        return r.action in VALID_ACTIONS[r.current_role]

    # TODO: assert scout doesn't place a victim without having picked one up first
    # Scout can only pick up and hold one victim at a time

    valid_entries = df.apply(assert_valid_action, axis=1)
    is_valid = valid_entries.all()

    return is_valid


def get_init_rubble_info(mission: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: raw_mission as input
    EFFECTS:  Returns dataframe for rubbles: block_id, x, y, z, status, cluster_id
        block_id is an int from 0 to len(rubble)
        status can be 0 (removed), 1 (present)
        cluster_id is initialized to -1
    """

    rubble_data = mission[mission.topic == 'ground_truth/mission/blockages_list']
    rubble_data = rubble_data.iloc[0]['data.mission_blockage_list']
    rubble = pd.json_normalize(rubble_data)

    # rename for config format
    # rubble.drop(columns=['room_name', 'feature_type', 'block_type'], inplace=True)
    rubble.index.name = 'block_id'
    rubble['status'] = 1  # present

    # update 7/22/21
    # drop y coordinate (changes during game), use status to mean how many rubble
    # blocks remaining at (x, z)
    rubble = rubble.groupby(['x', 'z']).status.sum().reset_index()

    assign_rubble_clusters(rubble)

    return rubble


def assign_rubble_clusters(rubble: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: rubble has columns [x, z, y, status] and index name is block_id
              each value in index is unique integer
              all (x, z) are valid Minecraft coordinates
    MODIFIES: rubble
    EFFECTS:  Using x and z columns as spatial coordinates, assigns each block
              to a rubble cluster id (integer) and puts this in a new column cluster_id.
              A pair of blocks are assigned the same cluster_id iff their (x, z)
              coordinates are next to each other (not diagonally)
    """

    # Note: O(n^2) solution. Only need to run once per map type
    rubble['cluster_id'] = -1  # unassigned

    def gen_neighbors(x: int, z: int) -> List[Tuple[int, int]]:
        neighbors = [(x-1, z), (x, z), (x+1, z), (x, z-1), (x, z+1)]
        # don't need to check for valid idx's
        return neighbors

    def select_neighbors(n: List[Tuple[int, int]]) -> pd.Series:
        mask = ((rubble.x == n[0][0]) & (rubble.z == n[0][1]))
        for x, z in n[1:]:
            mask = mask | ((rubble.x == x) & (rubble.z == z))
        return rubble[mask]

    new_cluster_id = 0
    for _, rub in rubble.iterrows():  # oof
        neighbors = gen_neighbors(rub.x, rub.z)
        clustermates = select_neighbors(neighbors)

        # check for adjacent clusters
        adjacent_clusters = clustermates.cluster_id.unique()
        if (adjacent_clusters != -1).any():
            # add found adjacent clusters to current cluster
            adjacent_clusters = adjacent_clusters[adjacent_clusters != -1]
            clustermates = pd.concat([clustermates,
                                      rubble[rubble.cluster_id.isin(adjacent_clusters)]])

        # skip already assigned
        if rub.cluster_id != -1:
            current = rub.cluster_id
        else:
            current = new_cluster_id
            new_cluster_id += 1

        # assign to same cluster
        rubble.loc[clustermates.index, 'cluster_id'] = current

    return rubble

def get_init_victims_info(mission: pd.DataFrame) -> pd.DataFrame:
    """
    REQUIRES: raw_mission as input
    EFFECTS:  Returns dataframe for victims: victim_id, x, y, z, victim_type, status
        victim_id is an int from 0 to len(victims)
        victim_type can be "unknown", "normal", "critical";
        status can be 0 (unsaved), 1 (saved), 2 (held)
    OUTPUT:
    NOTES: transported from notebook, not tested
    """
    def rename_victim_block(s):
        if s == "block_victim_1":
            return 'A'
        elif s == "block_victim_1b":
            return 'B'
        elif s == "block_victim_proximity":
            return 'C'

    victims_data = mission[mission.topic == 'ground_truth/mission/victims_list']
    victims_data = victims_data.iloc[0]['data.mission_victim_list']

    victims = pd.json_normalize(victims_data)

    # rename for config format
    victims.rename(columns={'unique_id': 'victim_id', 'block_type': 'victim_type'},
                   inplace=True)
    victims.index = victims.victim_id
    victims.drop(columns=['victim_id'], inplace=True)
    victims.victim_type = victims.victim_type.apply(lambda r: rename_victim_block(r))
    victims['status'] = 0  # unsaved

    return victims


def get_kmaps(df):
    """
    REQUIRES: df = pd.read_excel("SaturnA_1.5_r2j0e1_sum_gyr_all-names_shadow.xlsx", sheet_name="region14")
              SaturnA can be SaturnB;
              sheet_name can be region14, region24, region34, region54, region64
    EFFECTS:  Computes the static, initial victim and rubble knowledge maps
              as well as the RGB file players see, all in numpy format
    OUTPUT:   The 3 numpy maps, the victim and rubble knowledge maps
              are already saved in folder "knowledge_maps"
    """

    saturn_rgba_kmap = np.zeros([73,139,4])
    saturn_victim_kmap = np.zeros([73,139]) # walls and outside are 0 by default
    saturn_rubble_kmap = np.zeros([73,139]) # walls and outside are 0 by default
    for index, data in df.iterrows():
        i = data.row - 5
        j = data.col - 3
        color = data.bgColor
        a = data.alpha
        if color == '#999999':
            saturn_rgba_kmap[i,j,:3] = 0
        elif color == '#4C4C4C':
            saturn_rgba_kmap[i,j,:3] = 0.5
            saturn_victim_kmap[i,j] = 2 # unobserved
            saturn_rubble_kmap[i,j] = 2 # unobserved
        elif color == '#FF0000':
            saturn_rgba_kmap[i,j,0] = 1
            saturn_victim_kmap[i,j] = a # potential victim, ranges [0,1]
        elif color == '#0000FF':
            saturn_rgba_kmap[i,j,2] = 1
            saturn_rubble_kmap[i,j] = 1 # potential rubble
        saturn_rgba_kmap[i,j,3] = a

    return saturn_victim_kmap, saturn_rubble_kmap, saturn_rgba_kmap


def lookup_trial_info(mission_file: str, metadata: pd.DataFrame) -> Tuple[int, int, str, str, int]:
    """
    REQUIRES: mission_file is just filename, not a path
    EFFECTS:  Looks up and returns trial_num, team_id, planning_cond, mission_map (SaturnA or B),
              trial_order (whether this is the first or second trial). and density maps for this
    """

    try:
        trial_info = metadata[metadata.file_name == mission_file].iloc[0]
    except IndexError:
        raise ValueError(f'Mission {mission_file} not found in metadata')

    map_name = trial_info.map_name
    if len(map_name) > 7:
        # truncate "_Vers-#"
        map_name = map_name[:7]

    result = (trial_info.trial_id, trial_info.team_id, trial_info.teaming_cond,
              map_name, trial_info.trial_order)

    return result


def preprocess_single(mission_path: str, metadata: pd.DataFrame, save_dir=None) -> pd.DataFrame:
    """
    REQUIRES: mission_file is valid path to raw .metadata mission file from study 2 experiments
              metadata has columns:
                file_name, trial_id, team_id, teaming_cond, map_name, trial_order
              Trial used Saturn 1.5 or 1.6 maps (they are the same)
              save_dir is None or
    MODIFIES: ./preprocessed_data/
    EFFECTS:  Preprocesses mission_file.
    """
    mission = read_file(mission_path)
    mission_filename = mission_path.split('/')[-1]
    trial_num, team_id, planning_cond, mission_map, trial_order = lookup_trial_info(mission_filename,
                                                                                    metadata)
    map_knowledge_conds = extract_map_knowledge_conds(mission)
    initial_roles = get_roles_final(mission)

    # if not verify_map(mission, mission_map):
    #     raise ValueError('rubble or victims do not match ground truth files')

    mission = add_timing(mission)

    preprocessed = boil(mission, trial_num, team_id, trial_order, planning_cond,
                        mission_map, map_knowledge_conds, initial_roles=initial_roles)

    if save_dir is not None:
        save_to = 'study3_preprocessed_T'+str(trial_num)+'.csv'
        save_path = save_dir + '/' + save_to
        print('Saving to:', save_path)
        preprocessed.to_csv(save_path)

    return preprocessed


def preprocess_dir(dir_path: str, metadata_path: str, save_path: str) -> None:
    """
    REQUIRES: dir_path valid path to directory (no trailing /)
              metadata_path valid path to a csv
              save_path valid path to directory (no trailing /)
    MODIFIES: save_path
    EFFECTS:  Preprocesses all valid mission files in dir_path and saves resulting
              files to save_path.
    """

    metadata = pd.read_csv(metadata_path, index_col=0)
    all_files = os.listdir(dir_path)

    EXCLUSIONS = {}

    # prune irrelevant files
    mission_files = [ f for f in all_files if f.endswith('.metadata') and f.startswith('NotHSRData')
                                              and f not in EXCLUSIONS ]

    # don't repeat files we've already preprocessed
    def check_if_done(raw_filename: str, done_files: Set[str]) -> bool:
        trial_num, _, _, _, _ = lookup_trial_info(raw_filename, metadata)
        preprocessed_filename = f'study3_preprocessed_T{trial_num}.csv'
        return preprocessed_filename in done_files

    mission_files = [ f for f in mission_files if not check_if_done(f, set(os.listdir(save_path))) ]

    for mission_file in mission_files:
        print('Preprocessing:', mission_file)
        preprocess_single(dir_path+'/'+mission_file, metadata, save_dir=save_path)

    return


def main(data_path: str):
    """
    REQUIRES: mission_file is path to raw .metadata mission file from study 3 experiments.
    """

    print('Preprocessing files from:', data_path)

    save_path = 'preprocessed_data'
    metadata_path = 'subj_data/meta_file.csv'

    preprocess_dir(data_path, metadata_path, save_path)

    return 0


if __name__ == '__main__':
    main(sys.argv[1])
