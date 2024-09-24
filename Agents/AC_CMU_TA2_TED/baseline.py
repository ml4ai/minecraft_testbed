#!/usr/bin/env python3
#
# This is the raw code from Fade's Jupyter notebook. It can be used to generate
# a baseline file for testing. This file will contain the expected answers.
# Verify that the online/live agent generates the same outputs when given the
# data via the elkless replayer.

import argparse
import json
import math
import os
import sys

import pandas as pd
pd.options.display.float_format = '{:20,.2f}'.format
import numpy as np


def main(args):
    """Main entry point for script."""
    parser = argparse.ArgumentParser(description=__doc__)
    config = parser.parse_args(args)

    # trial_path = '../../../hsr-study-2/raw/train/HSRData_TrialMessages_Trial-T000417_Team-TM000109_Member-na_CondBtwn-1_CondWin-SaturnA_Vers-2.metadata'
    trial_path = '../../../hsr-study-2/raw/train/HSRData_TrialMessages_Trial-T000457_Team-TM000129_Member-na_CondBtwn-1_CondWin-SaturnB_Vers-4.metadata'
    # Run the script for user chosen time_window/period (specified in sec)
    dt = generateProcessMetrics(trial_path, period=60)

    dt.to_csv('baseline.csv')


# ------------------------------------------------------------

def generateProcessMetrics(trial_path, period=60):
    # Step 1: convert .metadata to sec-by-sec tabulation of key events
    df = processMetadata(trial_path)
    # Step 2: calculate process metrics by player by sec
    dp = calculateRawProcessMetrics(df)
    # Step 3: aggregate process metrics across players (team-level) and period
    #         also generates cumulative values for these metrics
    dt = aggregateProcessMetricsForPeriod(dp, period)
    return dt

def processMetadata(filepath):
    '''takes .metadata and generates sec-by-sec tabulation of key events'''
    print('processMetadata')

    messages = loadMetadata(filepath)
    print(f'loaded {len(messages)} messages')
    print('SCORE')
    df = score(messages)
    print('saveVictim')
    df = pd.merge(df, saveVictim(messages), on=['player','timer'], how='outer')
    print('roleChange')
    df = pd.merge(df, roleChange(messages), on=['player','timer'], how='outer')
    print('useTool')
    df = pd.merge(df, useTool(messages), on=['player','timer'], how='outer')
    print('moveVictim')
    df = pd.merge(df, moveVictim(messages), on=['player','timer'], how='outer')
    print('location')
    df = pd.merge(df, location(messages, df.player.unique()), on=['player','timer'], how='outer')

    print('communications')
    df = pd.merge(df, communications(messages), on=['player','elapsed_sec'], how='outer')

    print('remainder')

    timer_sec = []
    for x in df['timer']:
        if str(x) != 'nan':
            timer_sec.append(int(str(x).split(' ')[0]) * 60 + int(str(x).split(' ')[2]))
        else:
            timer_sec.append(timer_sec[-1])
    df['timer_sec'] = timer_sec
    df['elapsed_seconds'] =  max(df['timer_sec']) - df['timer_sec'] + 1
    df = df.sort_values(['elapsed_sec','score_team']).drop_duplicates().reset_index(drop=True)

    df['score_team'] = df['score_team'].ffill().fillna(0)
    df['score_player'] = df.groupby('player')['score_player'].ffill().fillna(0)
    df['role'] = df.groupby('player')['role'].ffill()
    return df


def loadMetadata(filepath):
    '''converts '.metadata' message stream into json list'''
    print(f'loadMetadata: {filepath}')
    with open(filepath) as f:
        messages = f.readlines()
    return messages


def communications(messages):
    all_events = list(filter(lambda k: 'observations/state' in k, messages))
    starting_timestamp = None
    for i in range(0,len(all_events)):
        d = json.loads(all_events[i])
        if d['data']['elapsed_milliseconds'] >= 0 and d['data']['mission_timer'] != 'Mission Timer not initialized.':
            starting_timestamp = d['data']['timestamp']
            break

    events = list(filter(lambda k: 'agent/asr/final' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_sec', 'elapsed_ms','player',
                                     'start_timestep',
                                     'end_timestep',
                                     'is_final',
                                     'message_text', 'message_occur'])
#     print("starting_timestamp", starting_timestamp)
    for i in range(0,len(events)):
        d = json.loads(events[i])
        if 'start_timestamp' not in d['data']:
            continue
        df.loc[i] = [get_second_time_difference(starting_timestamp, d['data']['start_timestamp']),
                     get_millisecond_time_difference(starting_timestamp, d['data']['start_timestamp']),
                       d['data']['participant_id'],
                       d['data']['start_timestamp'],
                       d['data']['end_timestamp'],
                       d['data']['is_final'],
                       d['data']['text'], 1]
    df = df[df.elapsed_ms > 0]
    df = df.sort_values(by=['elapsed_ms'])
    return df


def score(messages):
    events = list(filter(lambda k: 'observations/events/scoreboard' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)*3),
                            columns=['elapsed_ms','timer','player',
                                     'score_player','score_team'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        players = d['data']['scoreboard'].keys()
        for j, p in enumerate(players):
            if p != 'TeamScore':
                df.loc[3*i+j] = [d['data']['elapsed_milliseconds'],
                               d['data']['mission_timer'],
                               p,
                               d['data']['scoreboard'][p],
                               d['data']['scoreboard']['TeamScore']]
    df = df[df.elapsed_ms > 0]
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms'])


def roleChange(messages):
    events = list(filter(lambda k: 'observations/events/player/role_selected' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_ms','timer','player',
                                     'role'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        try:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['participant_id'],
                         d['data']['new_role']]
        except:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['playername'],
                         d['data']['new_role']]
    df['timer'] = df['timer'].replace('Mission Timer not initialized.', '15 : 3')
    df = df.drop_duplicates(subset=['timer','player'], keep='last')
#     df = df[df.elapsed_ms > 0]
    df.role = df.role.replace({'Hazardous_Material_Specialist':'HMS',
                               'Search_Specialist':'SS',
                               'Medical_Specialist':'MS'})
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms'])


def useTool(messages):
    events = list(filter(lambda k: 'observations/events/player/tool_used' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_ms','timer','player',
                                     'tool_type','tool_target'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        try:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['participant_id'],
                         d['data']['tool_type'],
                         d['data']['target_block_type'].split(":")[1]]
        except:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['playername'],
                         d['data']['tool_type'],
                         d['data']['target_block_type'].split(":")[1]]

    df = df[df.elapsed_ms > 0]
    df = df[df.tool_target != 'air']
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms']).drop_duplicates()


def moveVictim(messages):
    df = pickUpVictim(messages)
    return df.append(placeVictim(messages)).drop_duplicates(subset=['timer','player','moving_victim'], keep=False).reset_index(drop=True)


def pickUpVictim(messages):
    events = list(filter(lambda k: 'observations/events/player/victim_picked_up' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_ms','timer','player',
                                     'moving_victim','moving_state'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        try:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['participant_id'],
                         str(d['data']['victim_id']) + "-" + d['data']['type'],
                         'picked_up']
        except:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['playername'],
                         str(d['data']['victim_id']) + " - " + d['data']['type'][0],
                         'picked_up']

    df = df[df.elapsed_ms > 0]
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms'])


def placeVictim(messages):
    events = list(filter(lambda k: 'observations/events/player/victim_placed' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_ms','timer','player',
                                     'moving_victim','moving_state'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        try:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['participant_id'],
                         str(d['data']['victim_id']) + "-" + d['data']['type'],
                         'placed']
        except:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['playername'],
                         str(d['data']['victim_id']) + " - " + d['data']['type'][0],
                         'placed']

    df = df[df.elapsed_ms > 0]
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms'])


def saveVictim(messages):
    events = list(filter(lambda k: 'observations/events/player/triage' in k, messages))
    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_ms','timer','player',
                                     'saving_victim','saving_state'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        try:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['participant_id'],
                         str(d['data']['victim_id']) + "-" + d['data']['type'],
                         d['data']['triage_state']]
        except:
            df.loc[i] = [d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['playername'],
                         str(d['data']['victim_id']) + " - " + d['data']['type'][0],
                         d['data']['triage_state']]
    df = df[df.elapsed_ms > 0]
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms'])


def location(messages, players):
    all_events = list(filter(lambda k: 'observations/state' in k, messages))
    events = list()

    # filter out end of second events for each player
    for p in players:
        player_events = list(filter(lambda k: p in k, all_events))
        for m in range(0,16):
            for s in range(0,60):
                this_sec = list(filter(lambda k: str(m) + " : " + str(s) in k, player_events))
                if len(this_sec) > 0:
                    events.append(max(this_sec, key=lambda d: json.loads(d)['data']['elapsed_milliseconds']))

    df = pd.DataFrame(index=np.arange(0,len(events)),
                            columns=['elapsed_sec','elapsed_ms','timer','player',
                                     'x','z'])
    for i in range(0,len(events)):
        d = json.loads(events[i])
        try:
            df.loc[i] = [int(d['data']['elapsed_milliseconds']/1000),
                         d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['participant_id'],
                         d['data']['x'],
                         d['data']['z']]
        except:
            df.loc[i] = [int(d['data']['elapsed_milliseconds']/1000),
                         d['data']['elapsed_milliseconds'],
                         d['data']['mission_timer'],
                         d['data']['playername'],
                         d['data']['x'],
                         d['data']['z']]

    df = df[df.elapsed_ms > 0]
    df = df.sort_values(by=['elapsed_ms'])
    return df.drop(columns=['elapsed_ms'])

# ------------------------------------------------------------

def calculateRawProcessMetrics(df):
    '''calculate process metrics by player by sec'''

    #     df['message_occur'] = 1
    df['message_text'] = df.groupby('player')['message_text'].ffill()
    df['message_freq'] = df.groupby('player')['message_occur'].ffill(1).fillna(0)
    df['message_equity'] = df.groupby('player')['message_occur'].ffill(1).fillna(0)

    # INFER ACTION TYPE
    # mark save victims starting triage is in progress or medkit used, ends when points received
    df['victim_count'] = np.nan
    df['victim_count'] = df.groupby('player')['score_player'].diff().fillna(0)/10

    df['action_save_start'] = np.nan
    df.loc[df['saving_state'] == 'IN_PROGRESS', 'action_save_start'] = 1
    df['action_save_start'] = df.groupby('player')['action_save_start'].ffill(limit = 5).fillna(0)

    df['action_save_R'] = np.nan
    df.loc[df['victim_count'] == 1, 'action_save_R'] = 1
    df['action_save_R'] = df.groupby('player')['action_save_R'].bfill(limit = 7).fillna(0)

    df['action_save_C'] = np.nan
    df.loc[df['victim_count'] == 5, 'action_save_C'] = 1
    df['action_save_C'] = df.groupby('player')['action_save_C'].bfill(limit = 14).fillna(0)

    df['action_save_victim'] = np.nan
    df['action_save_victim'] = df['action_save_start'] + df['action_save_R'] + df['action_save_C']
    df.loc[df['tool_type'] == 'MEDKIT', 'action_save_victim'] = 1 # may be overlapping
    df.loc[df['action_save_victim'] > 0, 'action_save_victim'] = 1

    df.loc[df['victim_count'] == 5, 'victim_count'] = 1

    # mark move victims when victim is picked up but not yet placed
    df['action_move_start'] = np.nan
    df.loc[df['moving_state'] == 'picked_up', 'action_move_start'] = df['moving_victim']
    df['action_move_start'] = df.groupby('player')['action_move_start'].ffill().fillna(0)

    df['action_move_end'] = np.nan
    df.loc[df['moving_state'] == 'placed', 'action_move_end'] = df['moving_victim']
    df['action_move_end'] = df.groupby('player')['action_move_end'].ffill().fillna(0)

    df['action_move_victim'] = 0
    df.loc[df['action_move_start'] != df['action_move_end'], 'action_move_victim'] = 1
    df.loc[df['moving_state'] == 'placed', 'action_move_victim'] = 1

    # mark dig rubble is hammer is used to break gravel
    df['action_dig_rubble'] = 0
    df.loc[(df['tool_type'] == 'HAMMER') & (df['tool_target'] == 'gravel'), 'action_dig_rubble'] = 1

    # calculate new positions explored and mark explore action
    df['x'] = df['x'] + 2225
    df['z'] = df['z'] + 11
    df['x'] = df.groupby('player')['x'].ffill()
    df['z'] = df.groupby('player')['z'].ffill()
    df = df.sort_values(['timer_sec','role'], ascending=False)
    visited_positions = []
    coverage_df = pd.DataFrame(columns=['player_position',
                                        'positions_explored',
                                        'positions_explored_cum'])
    for row in df.itertuples():
        try:
            positions_explored = list(set(getFOV(int(row.x),int(row.z))) - set(visited_positions))
            visited_positions = visited_positions + positions_explored
            coverage_df.loc[row.Index] = [[int(row.x),int(row.z)],
                                          len(positions_explored),
                                          len(visited_positions)]
        except ValueError as err:
            # print(err)
            pass

    print(f'writing {len(visited_positions)} positions')
    with open('results/visited-base.json', 'wt') as out:
        json.dump(visited_positions, out)

    df = pd.concat([df, coverage_df], axis=1)
    df['action_explore'] = 0
    df.loc[(df['positions_explored'] > 0), 'action_explore'] = 1

    # mark inaction if player is standing without saving or digging action
    df['dx'] = df.groupby('player')['x'].diff().abs()
    df['dz'] = df.groupby('player')['z'].diff().abs()
        # df['distance_walked'] = np.round(np.sqrt(df.dx.pow(2) + df.dz.pow(2)), 2)

    df['inaction_stand'] = 0
    df.loc[(df.dx < 1) & (df.dz < 1) & (df.action_dig_rubble != 1) & (df.action_save_victim != 1), 'inaction_stand'] = 1

    # PROCESS MEASURES
    df = df.sort_values(['timer_sec','role'], ascending=False).reset_index(drop=True)

    # calculate coverage as new positions/tiles explored
    df['process_coverage'] = df['positions_explored'].dropna().astype(int)

    # calculate skill use as engaging in skill congruent actions
    df['process_skill_use'] = 0
    df.loc[(df['role'] == 'HMS'), 'process_skill_use'] = df['action_dig_rubble'] + df['action_explore']
    df.loc[(df['role'] == 'MS'), 'process_skill_use'] = df['action_save_victim'] + df['action_explore']
    df.loc[(df['role'] == 'SS'), 'process_skill_use'] = df['action_move_victim'] + df['action_explore']
    df.loc[(df['process_skill_use'] > 0), 'process_skill_use'] = 1

    # calculate effort as flip of inaction
    # (correction for edge cases: if skill use == 1, effort == 1)
    df['process_effort'] = 0
    df.loc[(df['inaction_stand'] == 0) | (df['process_skill_use'] == 1), 'process_effort'] = 1

    # cumulative scores
    df['score_team_agg'] = df['score_team'].astype(int)
    df['score_player_agg'] = df['score_player'].astype(int)

    # filter and typecast
    df = df[['timer', 'timer_sec', 'elapsed_sec', 'player', 'message_text','message_freq', 'message_equity', 'role',
             'x' , 'z', 'inaction_stand',
             'process_effort', 'process_skill_use', 'process_coverage',
             'action_save_victim', 'victim_count',
             'score_player_agg', 'score_team_agg']]
    df[df.columns[8:]] = df[df.columns[8:]].astype('float')

    return df.drop_duplicates()


def getFOV(x,z):
    fov = list()
    # 7x7 square with player in the middle (we lose cells in about 10-12% cases with 5x5)
    for i in range(-3,4):
        for j in range(-3,4):
            if z+j <= 72: fov.append((x+i,z+j))
    return fov


# ------------------------------------------------------------
def aggregateProcessMetricsForPeriod(df, period=60):
    '''aggregate process metrics across players (team-level) and period
          also generates cumulative values for these metrics
       takes output dataframe from calculateRawProcessMetrics()'''

    # exception handling for last 3-4 secs (900+ sec all collapsed in last time window)
    df['score_team'] = df['score_team_agg'].diff().fillna(0).astype(int)
    df['period'] = df['elapsed_sec'].sub(1).div(period).astype(int) + 1
    df.loc[df['period'] == df['period'].max(), 'period'] = df['period'].max() - 1

    # aggregate by period
    dm = df.groupby(['period']).agg(
        {'elapsed_sec':'count',
         'process_effort':'sum',
         'process_skill_use':'sum',
         'process_coverage':'sum',
         'action_save_victim':'sum',
         'victim_count':'sum',
         'inaction_stand':'sum',
         'score_team':'sum',
         'score_team_agg':'max',
        'message_freq':'sum',
        'message_equity':'var'})

    # generate cumulatives
    dm['process_skill_use_agg'] = dm['process_skill_use'].cumsum(axis = 0).div(dm['elapsed_sec'].sum())
    dm['process_coverage_agg'] = dm['process_coverage'].cumsum(axis = 0).div(9000)
    dm['process_saving_agg'] = dm['action_save_victim'].cumsum(axis = 0).div(475)

    dm['process_skill_use_rel'] = dm['process_skill_use'] / dm['process_effort']
    dm['process_workload_burnt'] = dm['process_coverage'].div(9000) + dm['action_save_victim'].div(475)
    dm['process_workload_burnt'] = dm['process_workload_burnt'].div(2)
    dm['process_workload_burnt_agg'] = dm['process_workload_burnt'].cumsum(axis = 0)

    dm['process_effort_agg'] = dm['process_effort'].cumsum(axis = 0).div(dm['elapsed_sec'].sum())

    #     dm['message_freq_agg'] = dm['message_freq'].cumsum(axis = 0).div(dm['elapsed_sec'].sum())
    #     dm['message_equity_agg'] = dm['message_occur'].var(axis = 1).div(dm['elapsed_sec'].sum())
    dm['message_consistency_agg'] = [np.var([dm['message_freq'][:i]]) if i>=1 else 0 for i in range(len(dm['message_freq']))]
    #     dm['n_msgs_agg'] = dm['message_text'].cumsum(axis = 0).div(dm['message_text'].sum())

    dm['elapsed_sec'] = dm['elapsed_sec'].div(3).astype(int) # sec in period
    return dm.round(4)

# ------------------------------------------------------------
# Time stuff

from datetime import datetime
def get_millisecond_time_difference(a, b):
    # print("A, b", (a,b))
    time_1 = a.replace("000Z", "").replace("Z", "")
    time_2 = b.replace("000Z", "").replace("Z", "")

    # print("A, b", (time_1,time_2))

    time_1 = datetime.strptime(time_1.split("T")[1].split("Z")[0],"%H:%M:%S.%f") # "2021-06-10T20:13:03.770Z"
    time_2 = datetime.strptime(time_2.split("T")[1].split("Z")[0],"%H:%M:%S.%f")


    delta = time_2 - time_1
    n_ms = int(delta.total_seconds() * 1000)
    return n_ms

def get_second_time_difference(a, b):
    # print("A, b", (a,b))
    time_1 = a.replace("000Z", "").replace("Z", "")
    time_2 = b.replace("000Z", "").replace("Z", "")

    # print("A, b", (time_1,time_2))

    time_1 = datetime.strptime(time_1.split("T")[1].split("Z")[0],"%H:%M:%S.%f") # "2021-06-10T20:13:03.770Z"
    time_2 = datetime.strptime(time_2.split("T")[1].split("Z")[0],"%H:%M:%S.%f")


    delta = time_2 - time_1
    n_ms = int(delta.total_seconds())
    return n_ms

# ------------------------------------------------------------
# This is the magic that runs the main function when this is invoked
# as a script.

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
