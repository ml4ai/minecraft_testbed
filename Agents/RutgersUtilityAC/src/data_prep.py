import pandas as pd
import numpy as np
import math
import json

import map_s3 as m3


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


def get_signal_plates(room_stuff_df, wall_room_df):
    room_id = []
    x = []
    z = []
    for row in range(room_stuff_df.shape[0]):
        for col in range(room_stuff_df.shape[1]):
            if room_stuff_df.iloc[row, col] == "P" or room_stuff_df.iloc[row, col] == "p":
                room_id.append(wall_room_df.iloc[row,col])
                x_, z_ = m3.Map._convert_to_minecraft(row, col)
                x.append(x_)
                z.append(z_)
    df = pd.DataFrame({'room_id':room_id, 'x':x, 'z':z})

    # manual correction
    idx = df[(df.x == -2217) & (df.z == -1)].index
    df.loc[idx, 'room_id'] = 'A4A'
    
    return df.sort_values("room_id")


if __name__ == "__main__":

    room_stuff_df = pd.read_csv("maps/saturn_a_study3.csv").iloc[3:, 2:]
    wall_room_df = pd.read_csv("maps/walls_rooms_v1.csv").iloc[3:, 2:]
    wall_room_ext_df = pd.read_csv("maps/walls_rooms_v2.csv").iloc[3:, 2:]

    # get topography numpy (wall, furniture, open_space)
    # wall
    wall_mat = get_topography_mat(wall_room_df)
    # furniture
    furniture_mat = get_topography_mat(room_stuff_df)
    # combine
    check_overlap(wall_mat, furniture_mat)
    topography_mat = wall_mat + furniture_mat
    np.save('preprocessed_data/topography.npy', topography_mat)

    # get room_name_s3.npy
    np.save("preprocessed_data/room_name_s3.npy", wall_room_df.to_numpy())

    # get room_name_ext_s3.npy
    np.save("preprocessed_data/room_name_ext_s3.npy", wall_room_ext_df.to_numpy())

    # get_signal plates
    plate_df = get_signal_plates(room_stuff_df, wall_room_ext_df)
    plate_df.to_csv('preprocessed_data/plate_coord.csv', index=False)

