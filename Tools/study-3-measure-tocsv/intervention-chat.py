from argparse import ArgumentParser
from os.path import join
from datetime import datetime
import pandas as pd
import numpy as np
import copy
import json
import math
import os

def main():
    parser = ArgumentParser(description='get stats from trial data')
    parser.add_argument('-d', '--input_dir', type=str, required=True, help='path to dir containing metadata files')
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print('File does not exist')
        return    

    for root, dirs, files in os.walk(args.input_dir):

        # table column headers
        dfs = pd.DataFrame(columns=['Trial', 'Team', 'Scenario', 'Timestamp', 'ASI', 'Intervention Message', 'Intervention Recipient','Speech Message', 'Medic', 'Transporter', 'Engineer', 'Explanation'])
        for file in files:
            print(file)
            if file.split('.')[-1] == 'metadata':

                #intervention count
                intervention_message_count = 0
                
                roles = {}
                players = {}
                # if file name is standard format get trial number and asi from filename
                tidx = [index for index, s in enumerate(file.split('.')[0].split('_')) if 'Trial-' in s][0]
                trial_number = file.split('.')[0].split('_')[tidx].split('Trial-')[-1]
                aidx = [index for index, s in enumerate(file.split('.')[0].split('_')) if 'CondBtwn-' in s][0]
                asi = file.split('.')[0].split('_')[aidx].split('CondBtwn-')[-1]

                if trial_number == 'Training':
                    continue
                # filename in T000449_ASI-UAZ-TA1.metadata format
                # trial_number = file.split('.')[0].split('_')[0] # i 
                # agent = file.split('.')[0].split('_')[-1]
                if 'ASI-CMU' in asi:
                    asi = 'ASI-CMURI-TA1'
                print('Trial:', trial_number, 'ASI:', asi)
                with open(os.path.join(root, file), encoding="utf8") as f:
                    mission_started = False
                    mission_start = ''
                    scenario = ''
                    team = ''

                    roles.clear()

                    for line in f:
                        message = json.loads(line)

                        if 'topic' in message.keys() and message['topic'] == 'trial':
                            if message['msg']['sub_type'].lower() == 'start':
                                scenario = message['data']['experiment_mission']
                                team = message['data']['experiment_name']


                        # get mission start time
                        if 'topic' in message.keys() and message['topic'] == 'observations/events/mission':
                            if message['data']['mission_state'] == 'Start':
                                mission_start = datetime.strptime(message['msg']['timestamp'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
                                mission_started = True

                        if 'topic' in message.keys() and message['topic'] == 'observations/events/player/role_selected':
                            players[message['data']['playername']] = message['data']['new_role']
                            roles[message['data']['participant_id']] = message['data']['new_role']



                        #################################
                        #           Speech             #
                        #################################                       

                        if 'topic' in message.keys() and message['topic'] == 'agent/asr/final':
                            if message['msg']['sub_type'] == 'asr:transcription':
                                
                                m = 0
                                e = 0
                                t = 0
                                
                                if players.get(message['data']['participant_id']):
                                    if players[message['data']['participant_id']] == 'Medical_Specialist':
                                        m = 1
                                    if players[message['data']['participant_id']] == 'Transport_Specialist':
                                        t = 1
                                    if players[message['data']['participant_id']] == 'Engineering_Specialist':
                                        e = 1

                                dfs = dfs.append({'Trial': trial_number, 'Team': team, 'Scenario': scenario, 'Timestamp': message['header']['timestamp'], 'ASI': asi, \
                                    'Intervention Message': {}, 'Intervention Recipient': {}, 'Speech Message': message['data']['text'], \
                                    'Medic': m, 'Transporter': t, 'Engineer': e, 'Explanation': {}}, ignore_index=True)


                        #################################
                        #           Advisor             #
                        #################################                       

                        if 'topic' in message.keys() and message['topic'].startswith('agent/intervention/') and message['topic'].endswith('/chat') :
                            if message['msg']['sub_type'] == 'Intervention:Chat':
                                s = message['data']['content'].replace('\n', '')
                                # intervention_message_count = intervention_message_count + 1
                                # print(intervention_message_count, message['msg']['source'], 'message')

                                m = 0
                                e = 0
                                t = 0
                                
                                for participant in message['data']['receivers']:
                                    if roles.get(participant):
                                        if roles[participant] == 'Medical_Specialist':
                                            m = 1
                                        if roles[participant] == 'Transport_Specialist':
                                            t = 1
                                        if roles[participant] == 'Engineering_Specialist':
                                            e = 1

                                dfs = dfs.append({'Trial': trial_number, 'Team': team, 'Scenario': scenario, 'Timestamp': message['header']['timestamp'], 'ASI': asi, \
                                    'Intervention Message': s, 'Intervention Recipient': message['data']['receivers'], 'Speech Message': {}, \
                                    'Medic': m, 'Transporter': t, 'Engineer': e, 'Explanation': message['data']['explanation']}, ignore_index=True)

                      
    dfs.to_csv('intervention_output.csv', index=False)
    print('file saved') 

if __name__ == '__main__':
    main()