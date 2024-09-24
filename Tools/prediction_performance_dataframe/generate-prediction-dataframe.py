from argparse import ArgumentParser
from os.path import join
import pandas as pd
import json
import os

def main():
    parser = ArgumentParser(description='get prediction messages')
    parser.add_argument('-d', '--input_dir', type=str, required=True, help='path to dir containing prediction messages')
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print('File does not exist')
        return    
    dfs = pd.DataFrame(columns=['Source', 'Subject Type', 'Subject', 'Trial ID',\
                                        'Start Elapsed Time', 'Predicted Property', 'Prediction', 'Prediction ID',\
                                        'Block Location: X', 'Block Location: Z', 'Door ID'])
    for root, dirs, files in os.walk(args.input_dir):
        for file in files:
            
            source = 'N/A'
            subject_type = 'N/A'
            subject = 'N/A'
            trial_id = 'N/A'
            default_start = 'N/A'
            start = 'N/A'
            predicted_property = 'N/A'
            prediction = ['N/A']
            prediction_id = 'N/A'
            block_x = 'N/A'
            block_z = 'N/A'
            door_id = 'N/A'


            with open(os.path.join(root, file)) as f:
                print('Scanning', file)
                f2 = []
                for line in f:
                    f2.append(line)
                f.seek(0)
                for line in f:
                    prediction_msg = json.loads(line)
                    if 'msg' not in prediction_msg.keys():
                        continue
                    for k, v in prediction_msg['msg'].items():

                        if k == 'trial_id':
                            trial_id = v
                            if trial_id == '123e4567-e89b-12d3-a456-426655440000':
                                for l2 in f2:
                                    p2 = json.loads(l2)
                                    for k2, v2 in p2['msg'].items():
                                        if k2 == 'trial_id':
                                            if v2 != '123e4567-e89b-12d3-a456-426655440000':

                                                trial_id = v2

                        if k == 'source':
                            source = v
                    for k, v in prediction_msg['data'].items():
                        if k == 'group':
                            for i, j in v.items():
                                if i == 'start_elapsed_time':
                                    # seconds = j / 1000
                                    # minute = seconds // 60
                                    # rem = seconds % 60
                                    # rem = rem / 60
                                    # start = round(minute + rem, 1)
                                    # default_start = round(minute + rem, 1)
                                    start = j
                                    default_start = j
                        if k == 'predictions':
                            if 'State'.lower() in prediction_msg['msg']['sub_type'].lower():
                                for pred in v:
                                    for key, val in pred.items():
                                        if key == 'unique_id':
                                            prediction_id = val
                                        if key == 'start_elapsed_time':
                                            if val:
                                                # j = val
                                                # seconds = j / 1000
                                                # minute = seconds // 60
                                                # rem = seconds % 60
                                                # rem = rem / 60
                                                # start = round(minute + rem, 1)
                                                start = val

                                        if key == 'subject_type':
                                            subject_type = val
                                        if key == 'subject':
                                            subject = val
                                        if key == 'predicted_property':
                                            predicted_property = val
                                        if key == 'prediction':
                                            prediction = val
                                    dfs = dfs.append({'Source': source, 'Subject Type': subject_type, 'Subject': subject, 'Trial ID': trial_id, \
                                                        'Start Elapsed Time': start, 'Predicted Property': predicted_property, \
                                                        'Block Location: X': block_x, 'Block Location: Z': block_z, 'Door ID': door_id,\
                                                        'Prediction': prediction, 'Prediction ID': prediction_id}, ignore_index=True)
                                    subject_type = 'N/A'
                                    subject = 'N/A'
                                    start = default_start
                                    predicted_property = 'N/A'
                                    prediction = ['N/A']
                                    prediction_id = 'N/A'

                            elif 'Action'.lower() in prediction_msg['msg']['sub_type'].lower():
                                for pred in v:
                                    for key, val in pred.items():
                                        if key == 'unique_id':
                                            prediction_id = val
                                        if key == 'start_elapsed_time':
                                            if val:
                                                # j = val
                                                # seconds = j / 1000
                                                # minute = seconds // 60
                                                # rem = seconds % 60
                                                # rem = rem / 60
                                                # start = round(minute + rem, 1)
                                                start = val
                                        if key == 'subject_type':
                                            subject_type = 'val'
                                        if key == 'subject':
                                            subject = val
                                        if key == 'predicted_property':
                                            predicted_property = val
                                        if key == 'action':
                                            if 'not' in val:
                                                prediction = False
                                            else:
                                                prediction = True
                                        if key == 'using':
                                            if isinstance(val, str):
                                                jsonval = json.loads(val)
                                                val = jsonval
                                            if isinstance(val, dict):
                                                for k, v in val.items():

                                                    if k == 'location':
                                                        if isinstance(v, list):
                                                            block_x = v[0]
                                                            block_z = v[2]
                                                        else:
                                                            block_x = v['x']
                                                            block_z = v['z']
                                                            if prediction_msg['msg']['source'] == 'SIFTAsistant':
                                                                block_x = block_x - 1

                                        if key == 'object':
                                            door_id = val
                                    dfs = dfs.append({'Source': source, 'Subject Type': subject_type, 'Subject': subject, 'Trial ID': trial_id, \
                                                        'Start Elapsed Time': start, 'Predicted Property': predicted_property, \
                                                        'Block Location: X': block_x, 'Block Location: Z': block_z, 'Door ID': door_id,\
                                                        'Prediction': prediction, 'Prediction ID': prediction_id}, ignore_index=True)
                                    subject_type = 'N/A'
                                    subject = 'N/A'
                                    start = default_start
                                    predicted_property = 'N/A'
                                    prediction = ['N/A']
                                    prediction_id = 'N/A'
                                    block_x = 'N/A'
                                    block_z = 'N/A'
                                    door_id = 'N/A'



    # d = {'Team': team, 'Trial': trial_number}
    # df = pd.DataFrame(data=d)
    dfs.to_csv('prediction_output.csv', index=False)
    print('predictions saved to prediction_output.csv') 

if __name__ == '__main__':
    main()