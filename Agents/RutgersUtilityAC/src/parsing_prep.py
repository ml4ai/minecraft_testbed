import preprocess_s3 as pp3
import pandas as pd
import numpy as np
import math
import json

TOPOGRAPHY_W = 139
TOPOGRAPHY_H = 76

ROOM_SET = ('A1', 'A2', 'A3', 'A4', 'A4A',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
            'D1', 'D2', 'D3', 'D4',
            'E1', 'E2', 'E3', 'E4', 'E5',
            'F1', 'F2', 'F3', 'F4',
            'G1', 'G2', 'G3',
            'H1', 'H1A', 'H2',
            'I1', 'I2', 'I3', 'I4', 'I1A', 'I2A', 'I3A', 'I4A',
            'J1', 'J2', 'J3', 'J4',
            'K1', 'K2', 'K3', 'K4',
            'L1', 'L2', 'L3',
            'M1', 'M2', 'M3')

def preprocess_ac(mission):
    # victim_list = mission[mission.topic == 'ground_truth/mission/victims_list']['data.mission_victim_list'].to_list()[0]
    # rubble_list = mission[mission.topic == 'ground_truth/mission/blockages_list']['data.mission_blockage_list'].to_list()[0]

    # necessary
    trial = mission[mission.topic == "trial"]
    mission_map = trial[trial["msg.sub_type"] == "start"]["data.experiment_mission"].to_list()[0]

    # not crucial
    trial_num = 0
    team_id = 0
    planning_cond = 0
    trial_order = 0

    # no longer relevant
    map_knowledge_conds = pp3.extract_map_knowledge_conds(mission)

    # players not supposed to change roles after mission starts in study 3
    initial_roles = pp3.get_roles_final(mission)

    mission = pp3.add_timing(mission)

    preprocessed = pp3.boil(mission, trial_num, team_id, trial_order, planning_cond,
                        mission_map, map_knowledge_conds, initial_roles=initial_roles)

    return preprocessed


def get_topography_mat(df):
    "df is trimmed already"
    OPEN_SPACE = 0
    FURNITURE = 2
    WALL = 3
    mat = np.empty(shape=(df.shape))

    if not ((mat.shape[0] == TOPOGRAPHY_H) and (mat.shape[1] == TOPOGRAPHY_W)):
        print("get_topography_map: df slice NOT the right size")

    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            if df.iloc[row, col] == "W":
                mat[row, col] = WALL
            elif df.iloc[row, col] == "F":
                mat[row, col] = FURNITURE
            else:
                mat[row, col] = OPEN_SPACE
    return mat


def check_overlap(mat1, mat2):
    if mat1.shape != mat2.shape:
        print("Check map matrix overlap: Shape mismatch!")
    if np.sum(mat2[mat1!=0]) != 0:
        print("Check map matrix overlap: overlap detected!")
    if np.sum(mat1[mat2!=0]) != 0:
        print("Check map matrix overlap: overlap detected!")


def convert_coords(x: float, z: float) -> (int, int):
    """
    REQUIRES: (x, z) are in Testbed coordinates:
                  x in [-2225, -2087]
                  z in [-11, 63]
    EFFECTS:  Returns corresponding indices for self.topography
              matrix.
    Note that 0->+ left-to-right on x,
              and 0->+ top-to-bottom on z in self.topography.
              x indexes the columns, and z indexes the rows.
              y deals with height and is unused.
    """
    # gleaned from TA3 map excel spreadsheet
    X_ZERO = -2225
    X_MAX = -2087
    Z_ZERO = -11
    Z_MAX = 64  # inclusive

    topography_x = math.floor(x) - X_ZERO
    topography_z = math.floor(z) - Z_ZERO

    return topography_z, topography_x


def get_victim_on_topography(victim_list):
    """
    REQUIRES: victim_list is a list of dictionaries,
              containing, x,y,z,block_type, unique_id, room_name
    EFFECTS:  Returns numpy array marking victim type A, B, and C.
    """
    def victim_block_type_to_num(s):
        VICTIM_A = 'A'
        VICTIM_Β = 'B'
        VICTIM_C = 'C'
        if s == "block_victim_1":
            return VICTIM_A
        elif s == "block_victim_1b":
            return VICTIM_Β
        elif s == "block_victim_proximity":
            return VICTIM_C
        else:
            return 0
    victim_mat = np.zeros([TOPOGRAPHY_H,TOPOGRAPHY_W], dtype='object') # hard coded
    for victim in victim_list:
        row, col = convert_coords(victim["x"], victim["z"])
        victim_mat[row,col] = victim_block_type_to_num(victim["block_type"])

    return victim_df, victim_mat


def get_rubble_on_topography(rubble_list):
    """
    REQUIRES: rubble_list is a list of dictionaries,
              containing, x,y,z, block_type, feature_type, room_name
    EFFECTS:  Returns numpy array marking rubble.
    """
    RUBBLE = 1
    rubble_mat = np.zeros([TOPOGRAPHY_H,TOPOGRAPHY_W])
    for rubble in rubble_list:
        row, col = convert_coords(rubble["x"], rubble["z"])
        rubble_mat[row,col] = RUBBLE
    return rubble_mat


if __name__ == "__main__":

    # load raw_mission
    # filename = 'subj_data/study-3_spiral-3_pilot_NotHSRData_TrialMessages_Trial-T000461_Team-TM000079_Member-na_CondBtwn-ASI-CRA-None_CondWin-na_Vers-1.metadata'
    filename = 'subj_data/study-3_spiral-3_pilot_NotHSRData_TrialMessages_Trial-T000448_Team-TM000074_Member-na_CondBtwn-ASI-UAZ-TA1_CondWin-na_Vers-1.metadata'
    with open(filename, encoding='utf8') as f:
        data_list = f.readlines()
    topic_msg_list = [ json.loads(l) for l in data_list ]
    mission = pd.json_normalize(topic_msg_list)

    # get preprocessed_log data
    preprocess_df = preprocess_ac(mission)
    preprocess_df.to_csv("preprocessed_data/preprocessed_ac.csv")

    # # ONLY NEED TO RE-RUN IF THE MAP LAYOUT CHANGED
    # # get topography numpy (wall, furniture, open_space)
    # # wall
    # wall_room_df = pd.read_csv("walls_rooms_v2.csv")
    # wall_room_df_slice = wall_room_df.iloc[3:, 2:]
    # wall_mat = get_topography_mat(wall_room_df_slice)
    # # furniture
    # df_saturn_a = pd.read_csv('saturn_a_study3.csv')
    # df_saturn_a_slice = df_saturn_a.iloc[3:, 2:]
    # furniture_mat = get_topography_mat(df_saturn_a_slice)
    # # combine
    # check_overlap(wall_mat, furniture_mat)
    # topography_mat = wall_mat + furniture_mat
    # np.save('preprocessed_data/topography.npy', topography_mat)

    # # # ONLY NEED TO RE-RUN IF THE MAP LAYOUT CHANGED
    # # # get room_name.csv
    # # input: "walls_rooms_v2.csv"; output: room_name_s3.npy saved to preprocessed_data/
    # romm_name_np = pp3.preprocessing_semantic_map_region("walls_rooms_v2.csv",
    #                                       "preprocessed_data/room_name_s3.npy")

    # get victims info
    victim_df = pp3.get_init_victims_info(mission)
    victim_df.to_csv("preprocessed_data/victims_list.csv")
    # victim_list = mission[mission.topic == 'ground_truth/mission/victims_list']['data.mission_victim_list'].to_list()[0]
    # victim_mat = get_victim_on_topography(victim_list)
    # np.save('maps/victim_mat.npy', victim_mat)

    # # get rubble info
    rubble_df = pp3.get_init_rubble_info(mission)
    rubble_df.to_csv("preprocessed_data/rubble_list.csv")
    # rubble_list = mission[mission.topic == 'ground_truth/mission/blockages_list']['data.mission_blockage_list'].to_list()[0]
    # rubble_mat = get_rubble_on_topography(rubble_list)
    # np.save('maps/rubble_mat.npy', rubble_mat)
