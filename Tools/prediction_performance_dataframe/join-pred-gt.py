from argparse import ArgumentParser
from os.path import join
import pandas as pd
import json
import os

def main():
    parser = ArgumentParser(description='get prediction messages')
    parser.add_argument('-g', '--input_gt_file', type=str, required=True, help='path to ground truth dataframe')
    parser.add_argument('-p', '--input_pred_file', type=str, required=True, help='path to prediction dataframe')
    args = parser.parse_args()

    if not os.path.exists(args.input_gt_file) or not os.path.exists(args.input_pred_file):
        print('File does not exist')
        return    

    prediction = pd.read_csv(args.input_pred_file)
    groundtruth = pd.read_csv(args.input_gt_file)    
    
    concat = pd.merge(prediction, groundtruth, on=['Trial ID', 'Block Location: X', 'Block Location: Z'], how='inner')

    concat.loc[concat['Door ID_x'].str[:2] == 'c_'] = concat[concat['Door ID_x'] == concat['Door ID_y']]
    concat = concat.rename(columns={'Door ID_y': 'Door ID'})
    del concat['Door ID_x']

    concat.loc[concat['Start Elapsed Time_y'].notna()] = concat[(concat['Start Elapsed Time_x'] //1000) == (concat['Start Elapsed Time_y'] //1000)]
    concat = concat.rename(columns={'Start Elapsed Time_x': 'Start Elapsed Time'})
    del concat['Start Elapsed Time_y']

    concat.loc[concat['Subject_x'].notna()] = concat[concat['Subject_x'] == concat['Subject_y']]
    concat = concat.rename(columns={'Subject_x': 'Subject'})
    concat['Subject'] = concat['Subject_y']
    del concat['Subject_y']

    concat = concat[concat['Predicted Property'].str[:2] == concat['Measure']]

    concat.loc[concat['Ground Truth'].str.isnumeric(), ['Measurement']] = pd.to_numeric(concat['Ground Truth'], errors='coerce') - pd.to_numeric(concat['Prediction'], errors='coerce')
    concat.loc[~concat['Ground Truth'].str.isnumeric(), ['Measurement']] = (concat['Ground Truth'] == concat['Prediction']).astype(int)

    concat.to_csv('combined_output.csv', index=False)
    print('combined prediction and ground truth saved to combined_output.csv')  

if __name__ == '__main__':
    main()