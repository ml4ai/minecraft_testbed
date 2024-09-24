"""
profiling.py

Short script to profile (test performance of)
infer_knowledge_cond.py. Should help me get it
to run faster.

Sean Anderson, 3/8/22
CoDaS Lab
"""

import cProfile
import pandas as pd
import json
from rutgers_ac import preprocess_ac, rubble_victim_init_info, \
                       preprocess_ac_news
from belief import update_victims_seen


def main():
    # load messages
    p = "filename = 'subj_data/study-3_spiral-3_pilot_NotHSRData_TrialMessages_Trial-T000448_" \
        "Team-TM000074_Member-na_CondBtwn-ASI-UAZ-TA1_CondWin-na_Vers-1.metadata'\n" \
    "with open(filename) as f:\n" \
    "    data_list = f.readlines()\n" \
    "topic_msg_list = [json.loads(l) for l in data_list]\n" \
    "mission_raw = pd.json_normalize(topic_msg_list)\n" \
    "BASE_MSG_N = 4000\n" \
    "mission_raw_base = mission_raw[:BASE_MSG_N]\n" \
    "mission_news = mission_raw[BASE_MSG_N:]\n" \
    "mission_df, mission_map, start_time = preprocess_ac(mission_raw_base)\n"
    #rubble_df, victims_df = rubble_victim_init_info(mission_raw_base)
    # =========================================

    # preprocess and append new messages
    #news = preprocess_ac_news(mission_news, mission_map, start_time)
    #mission_df = pd.concat((mission_df, news))

    s = "news = preprocess_ac_news(mission_news, mission_map, start_time)\n" \
        "rubble_df, victims_df = rubble_victim_init_info(mission_raw_base)\n" \
        "victim_df, tiles_seen = update_victims_seen(news, rubble_df, victims_df)"
    c = cProfile.run(p + s, sort='cumtime')
    print(c)

    return 0


if __name__ == '__main__':
    main()
