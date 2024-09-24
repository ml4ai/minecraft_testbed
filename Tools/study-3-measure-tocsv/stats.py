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

    threat_rooms = {'Saturn_A': ['A4', 'B8', 'C2', 'D3', 'H1A', 'J4', 'K2', 'M3'],
                    'Saturn_B': ['A3', 'C3', 'C6', 'F4', 'D4', 'I3A', 'K1', 'L3'],
                    'Saturn_C': ['A4', 'B9', 'C1', 'D2', 'G2', 'I1', 'K4', 'M1'],
                    'Saturn_D': ['A3', 'C2', 'C7', 'D3', 'E5', 'I4', 'J4', 'L1']}

    if not os.path.exists(args.input_dir):
        print('File does not exist')
        return    

    for root, dirs, files in os.walk(args.input_dir):

        # table column headers
        dfs = pd.DataFrame(columns=['Trial', 'AC', 'ASI', 'Measure ID', 'Measure Value', 'Event', 'Elapsed Milliseconds', 'Additional Data'])
        for file in files:
            print(file)
            if file.split('.')[-1] == 'metadata':
                # array for survey responses tracking
                mission_1_measure_6_question_1 = [] #QID811_1, 
                mission_1_measure_6_question_2 = [] #QID811_6, 
                mission_1_measure_7_question_1 = [] #QID811_7, 
                mission_1_measure_7_question_2 = [] #QID811_8, 

                mission_2_measure_6_question_1 = [] #, QID817_1
                mission_2_measure_6_question_2 = [] #, QID817_6
                mission_2_measure_7_question_1 = [] #, QID817_7
                mission_2_measure_7_question_2 = [] #, QID817_8

                #intervention count
                intervention_message_count = 0

                #max beliefdiff avg
                avg_belief_diff = []

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

                    for line in f:
                        message = json.loads(line)

                        if 'topic' in message.keys() and message['topic'] == 'trial':
                            if message['msg']['sub_type'].lower() == 'start':
                                scenario = message['data']['experiment_mission'][:8]


                        # get mission start time
                        if 'topic' in message.keys() and message['topic'] == 'observations/events/mission':
                            if message['data']['mission_state'] == 'Start':
                                mission_start = datetime.strptime(message['msg']['timestamp'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
                                mission_started = True

                        #################################
                        #           APTIMA AC           #
                        #################################

                        if 'topic' in message.keys() and message['topic'] == 'agent/measures/AC_Aptima_TA3_measures':
                            # remove any measures from before the replay was ran or non terminal values
                            if 'replay_parent_id' in message['msg'].keys() or message['data']['event_properties']['qualifying_event_sub_type'] != 'stop':
                                continue
                            # print(trial_number, message['data']['measure_data'][0]['measure_id'], message['data']['measure_data'][0]['measure_value'], message['data']['event_properties']['qualifying_event_sub_type']) \
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'AC_Aptima_TA3_measures', 'ASI': asi, \
                            'Measure Value': message['data']['measure_data'][0]['measure_value'], \
                            'Measure ID': message['data']['measure_data'][0]['measure_id'], \
                            'Event': message['data']['event_properties']['qualifying_event_sub_type'],\
                            'Elapsed Milliseconds': message['data']['elapsed_milliseconds'],\
                            'Additional Data': message['data']['measure_data'][0]['additional_data']}, ignore_index=True)

                        #################################
                        #          CMU TED AC           #
                        #################################
                        
                        if 'topic' in message.keys() and message['topic'] == 'agent/ac/ac_cmu_ta2_ted/ted':
                            if ((dfs['Measure ID'] == 'CMU TED: Collective effort') & (dfs['Trial'] == trial_number)).any() :
                                dfs.loc[(dfs['Measure ID'] == 'CMU TED: Collective effort') & (dfs['Trial'] == trial_number), 'Measure Value'] = message['data']['process_effort_agg']
                                
                            if ((dfs['Measure ID'] == 'CMU TED: Appropriate skill use') & (dfs['Trial'] == trial_number)).any():
                                dfs.loc[(dfs['Measure ID'] == 'CMU TED: Appropriate skill use') & (dfs['Trial'] == trial_number), 'Measure Value'] = message['data']['process_skill_use_agg']
                                
                            if ((dfs['Measure ID'] == 'CMU TED: Appropriate Use of Strategy') & (dfs['Trial'] == trial_number)).any():
                                dfs.loc[(dfs['Measure ID'] == 'CMU TED: Appropriate Use of Strategy') & (dfs['Trial'] == trial_number), 'Measure Value'] = message['data']['process_workload_burnt_agg']
                                continue

                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_ted', 'ASI': asi, \
                            'Measure Value': message['data']['process_effort_agg'], \
                            'Measure ID': 'CMU TED: Collective effort', \
                            'Event': 'Terminal',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_ted', 'ASI': asi, \
                            'Measure Value': message['data']['process_skill_use_agg'], \
                            'Measure ID': 'CMU TED: Appropriate skill use', \
                            'Event': 'Terminal',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_ted', 'ASI': asi, \
                            'Measure Value': message['data']['process_workload_burnt_agg'], \
                            'Measure ID': 'CMU TED: Appropriate Use of Strategy', \
                            'Event': 'Terminal',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)

                        #################################
                        #           BEARD AC            #
                        #################################

                        if 'topic' in message.keys() and message['topic'] == 'agent/ac/ac_cmu_ta2_beard/beard':
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_beard', 'ASI': asi, \
                            'Measure Value': message['data']['team']['walking_skill_mean'], \
                            'Measure ID': 'CMU TA2 BEARD: minecraft skill: walking - Mean', \
                            'Event': 'Initial',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_beard', 'ASI': asi, \
                            'Measure Value': message['data']['team']['walking_skill_sd'], \
                            'Measure ID': 'CMU TA2 BEARD: minecraft skill: walking - SD', \
                            'Event': 'Initial',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_beard', 'ASI': asi, \
                            'Measure Value': message['data']['team']['sbsod_mean'], \
                            'Measure ID': 'CMU TA2 BEARD: spatial ability - Mean', \
                            'Event': 'Initial',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)
                            dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_cmu_ta2_beard', 'ASI': asi, \
                            'Measure Value': message['data']['team']['sbsod_sd'], \
                            'Measure ID': 'CMU TA2 BEARD: spatial ability - SD', \
                            'Event': 'Initial',\
                            'Elapsed Milliseconds': 'N/A',\
                            'Additional Data': {}}, ignore_index=True)

                        #################################
                        #           RUTGERS AC          #
                        #################################

                        if 'topic' in message.keys() and message['topic'] == 'agent/ac/threat_room_communication':
                            new = True

                            nearest_room = message['data']['nearest_room']
                            intersection = [x for x in set(nearest_room) if x in threat_rooms[scenario]]
                            measure = round(len(intersection) / len(threat_rooms[scenario]), 4)

                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'Rutgers: Threat room communication AC' and dfs.loc[index, 'Trial'] == trial_number:
                                    dfs.at[index, 'Additional Data'] = message['data']
                                    dfs.at[index, 'Measure Value'] = measure
                                    new = False
                            if new:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'AC_Rutgers_TA2_Utility', 'ASI': asi, \
                                'Measure Value': measure, \
                                'Measure ID': 'Rutgers: Threat room communication AC', \
                                'Event': 'Terminal',\
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)

                        if 'topic' in message.keys() and message['topic'] == 'agent/ac/victim_type_communication':
                            new = True
                            ab_victims = 20
                            victim_match = [x for x in list(set(message['data']['victims_match_marker_block'])) if x]
                            measure = round(len(victim_match) / ab_victims, 4)
                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'Rutgers: Victim type communication AC' and dfs.loc[index, 'Trial'] == trial_number:
                                    dfs.at[index, 'Additional Data'] = message['data']
                                    dfs.at[index, 'Measure Value'] = measure
                                    new = False
                            if new:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'AC_Rutgers_TA2_Utility', 'ASI': asi, \
                                'Measure Value': measure, \
                                'Measure ID': 'Rutgers: Victim type communication AC', \
                                'Event': 'Terminal',\
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)

                        if 'topic' in message.keys() and message['topic'] == 'agent/ac/belief_diff':
                            new = True

                            red_indiv = message['data']['RED_indiv'][-1]
                            blue_indiv = message['data']['BLUE_indiv'][-1]
                            green_indiv = message['data']['GREEN_indiv'][-1]

                            red_marker = message['data']['RED_marker'][-1]
                            blue_marker = message['data']['BLUE_marker'][-1]
                            green_marker = message['data']['GREEN_marker'][-1]
                            
                            shared = message['data']['shared'][-1]
                            red = get_non_zero_value((red_marker - red_indiv) , (shared - red_indiv))
                            blue = get_non_zero_value((blue_marker - blue_indiv) , (shared - blue_indiv))
                            green = get_non_zero_value((green_marker - green_indiv) , (shared - green_indiv))

                            max_val = max(red, green, blue)

                            avg_belief_diff.append(max_val)
                            measure = np.around(np.mean(avg_belief_diff), 4)

                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'Rutgers: Belief difference AC' and dfs.loc[index, 'Trial'] == trial_number:
                                    dfs.at[index, 'Additional Data'] = message['data']
                                    dfs.at[index, 'Measure Value'] = measure
                                    new = False
                            if new:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'AC_Rutgers_TA2_Utility', 'ASI': asi, \
                                'Measure Value': measure, \
                                'Measure ID': 'Rutgers: Belief difference AC', \
                                'Event': 'Terminal',\
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)

                        #################################
                        #           CORNELL AC          #
                        #################################
                        # Team goal alignment???

                        if 'topic' in message.keys() and message['topic'] == 'agent/ac/goal_alignment':
                            new = True

                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'Cornell: Goal alignment' and dfs.loc[index, 'Trial'] == trial_number:
                                    dfs.at[index, 'Measure Value'] = message['data']['Team']['goal_alignment_overall']
                                    dfs.at[index, 'Additional Data'] = message['data']
                                    new = False
                            if new:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'AC_CORNELL_TA2_TEAMTRUST', 'ASI': asi, \
                                'Measure Value': message['data']['Team']['goal_alignment_overall'], \
                                'Measure ID': 'Cornell: Goal alignment', \
                                'Event': 'Terminal',\
                                'Elapsed Milliseconds': message['data']['elapsed_ms'],\
                                'Additional Data': message['data']}, ignore_index=True)

                        #################################
                        #           GELP AC             #
                        #################################        

                        if 'topic' in message.keys() and message['topic'] == 'agent/gelp':
                            new = True

                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'Gallup: GELP' and dfs.loc[index, 'Trial'] == trial_number:
                                    #print(message['data'])

                                    dfs.at[index, 'Measure Value'] = message['data']['gelp_results'][0]['gelp_overall']
                                    dfs.at[index, 'Additional Data'] = message['data']
                                    new = False
                            if new:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_gallup_ta2_gelp', 'ASI': asi, \
                                'Measure Value': message['data']['gelp_results'][0]['gelp_overall'], \
                                'Measure ID': 'Gallup: GELP', \
                                'Event': 'Terminal',\
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)

                        #################################
                        #           UCF AC              #
                        #################################                       

                        if 'topic' in message.keys() and message['topic'] == 'agent/ac_ucf_ta2_playerprofiler/playerprofile':
                            new = True
                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'UCF: TaskPotential' and dfs.loc[index, 'Trial'] == trial_number:
                                    dfs.at[index, 'Additional Data'] = message['data']
                                    dfs.at[index, 'Measure Value'] = message['data']['task-potential-state-averages-list'][-5:]
                                    new = False
                            if new and 'task-potential-state-averages-list' in message['data'].keys():
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_ucf_ta2_playerprofiler', 'ASI': asi, \
                                'Measure Value': message['data']['task-potential-state-averages-list'][-5:], \
                                'Measure ID': 'UCF: TaskPotential', \
                                'Event': 'Terminal',\
                                # use timestamp for now
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)
                            new_team = True
                            new_task = True
                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'UCF: Player Profiler team-potential-category' and dfs.loc[index, 'Trial'] == trial_number:
                                    new_team = False
                                if dfs.loc[index, 'Measure ID'] == 'UCF: Player Profiler task-potential-category' and dfs.loc[index, 'Trial'] == trial_number:
                                    new_task = False
                            if new_team:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_ucf_ta2_playerprofiler', 'ASI': asi, \
                                'Measure Value': message['data']['team-potential-category'], \
                                'Measure ID': 'UCF: Player Profiler team-potential-category', \
                                'Event': 'Initial',\
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)
                            if new_task:
                                dfs = dfs.append({'Trial': trial_number, 'AC': 'ac_ucf_ta2_playerprofiler', 'ASI': asi, \
                                'Measure Value': message['data']['task-potential-category'], \
                                'Measure ID': 'UCF: Player Profiler task-potential-category', \
                                'Event': 'Initial',\
                                'Elapsed Milliseconds': 'N/A',\
                                'Additional Data': message['data']}, ignore_index=True)

                        #################################
                        #           Qualtrics           #
                        #################################                       

                        if 'topic' in message.keys() and message['topic'] == 'status/asistdataingester/surveyresponse':
                            # print(message['data']['values'].get('surveyname'))
                            if message['data']['values'].get('surveyname') and (('Mission1Reflection' in message['data']['values'].get('surveyname')) or ('Mission2Reflection' in message['data']['values'].get('surveyname'))):
                                for k, v in message['data']['values'].items():
                                    if k == 'QID811_1':
                                        mission_1_measure_6_question_1.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})
                                    if k == 'QID811_6':
                                        mission_1_measure_6_question_2.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})   
                                    if k == 'QID811_7':
                                        mission_1_measure_7_question_1.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})
                                    if k == 'QID811_8':
                                        mission_1_measure_7_question_2.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})
                                    if k == 'QID817_1':
                                        mission_2_measure_6_question_1.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})
                                    if k == 'QID817_6':
                                        mission_2_measure_6_question_2.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})                
                                    if k == 'QID817_7':
                                        mission_2_measure_7_question_1.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})
                                    if k == 'QID817_8':
                                        mission_2_measure_7_question_2.append({'pid': message['data']['values']['participantid'], 'score': v, 'question': k})

                            m6 = mission_1_measure_6_question_1 + mission_1_measure_6_question_2 + mission_2_measure_6_question_1 + mission_2_measure_6_question_2
                            m7 = mission_1_measure_7_question_1 + mission_1_measure_7_question_2 + mission_2_measure_7_question_1 + mission_2_measure_7_question_2
                            

                            m6_avg = 0
                            if len(m6) > 0:
                                m6_avg = sum(s['score'] for s in m6) /len(m6)

                            m7_avg = 0
                            if len(m7) > 0:
                                m7_avg = sum(s['score'] for s in m7) /len(m7)

                            new_m6 = True
                            new_m7 = True


                            for index in dfs.index:
                                if dfs.loc[index, 'Measure ID'] == 'ASI-M6: Perceived Utility of ASI' and dfs.loc[index, 'Trial'] == trial_number:
                                    #print(message['data'])

                                    dfs.at[index, 'Measure Value'] = format(m6_avg, '.4f')
                                    dfs.at[index, 'Additional Data'] = m6
                                    new_m6 = False
                                if dfs.loc[index, 'Measure ID'] == 'ASI-M7: Trust in ASI' and dfs.loc[index, 'Trial'] == trial_number:
                                    #print(message['data'])

                                    dfs.at[index, 'Measure Value'] = format(m7_avg, '.4f')
                                    dfs.at[index, 'Additional Data'] = m7
                                    new_m7 = False

                            if new_m6 and m6_avg != 0 and asi.lower() != 'none':

                                dfs = dfs.append({'Trial': trial_number, 'AC': 'N/A', 'ASI': asi, \
                                    'Measure Value': format(m6_avg, '.4f'), \
                                    'Measure ID': 'ASI-M6: Perceived Utility of ASI', \
                                    'Event': 'N/A',\
                                    'Elapsed Milliseconds': 'N/A',\
                                    'Additional Data': m6}, ignore_index=True)
                            if new_m7 and m7_avg != 0 and asi.lower() != 'none':

                                dfs = dfs.append({'Trial': trial_number, 'AC': 'N/A', 'ASI': asi, \
                                    'Measure Value': format(m7_avg, '.4f'), \
                                    'Measure ID': 'ASI-M7: Trust in ASI', \
                                    'Event': 'N/A',\
                                    'Elapsed Milliseconds': 'N/A',\
                                    'Additional Data': m7}, ignore_index=True)      


                        #################################
                        #           Advisor             #
                        #################################                       

                        if 'topic' in message.keys() and message['topic'].startswith('agent/intervention/') and message['topic'].endswith('/chat') :
                            if message['msg']['sub_type'] == 'Intervention:Chat':
                                intervention_message_count = intervention_message_count + 1
                                #print(intervention_message_count, message['msg']['source'], 'message')

                                new = True

                                for index in dfs.index:
                                    if dfs.loc[index, 'Measure ID'] == 'ASI-M8: Interventions' and dfs.loc[index, 'Trial'] == trial_number:
                                        #print(message['data'])

                                        dfs.at[index, 'Measure Value'] = intervention_message_count
                                        dfs.at[index, 'Additional Data'] = {}
                                        new = False

                                if new:

                                    dfs = dfs.append({'Trial': trial_number, 'AC': 'N/A', 'ASI': asi, \
                                        'Measure Value': intervention_message_count, \
                                        'Measure ID': 'ASI-M8: Interventions', \
                                        'Event': 'N/A',\
                                        'Elapsed Milliseconds': 'N/A',\
                                        'Additional Data': {}}, ignore_index=True)

                      
    dfs.to_csv('measure_output.csv', index=False)
    print('file saved') 

def get_non_zero_value(val1, val2):
    return val1 / val2 if val2 else 0

if __name__ == '__main__':
    main()