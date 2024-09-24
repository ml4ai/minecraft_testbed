import imp
import logging
import threading
import time
import warnings
from threading import Timer
from typing import Dict

import numpy as np
import pandas as pd
from asistagenthelper import ASISTAgentHelper

import belief as bf
from data_parsing_s3 import Mission
from map_s3 import Map

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
# from .RawConnection import RawConnection, RawMessage
import data_parsing_s3 as dp3
import preprocess_s3 as pp3
from parsing_prep import preprocess_ac


def on_message(topic, header, msg, data, mqtt_message):
    # logger.info("Received a message on the topic: " + topic)
    # Now handle the message based on the topic.  Refer to Message Specs for the contents of header, msg, and data
    if topic == "trial" and msg["sub_type"] == "start":
        logger.info(" - Trial Started with Mission set to: " + data["experiment_mission"])
    if topic == "trial" and msg["sub_type"] == "stop":
        logger.info(" - Trial Stopeed with Mission set to: " + data["experiment_mission"])


LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(
    logging.Formatter("%(asctime)s | %(name)s | %(lineno)d | %(levelname)s — %(message)s")
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(LOG_HANDLER)


def preprocess_ac(mission):
    
    trial = mission[mission.topic == "trial"]
    mission_map = trial[trial["msg.sub_type"] == "start"]["data.experiment_mission"].to_list()[0]

    preprocessed = pp3.boil_minimal(mission, mission_map)

    return preprocessed, mission_map


def rubble_victim_init_info(mission):
    # get rubble info
    if (mission.topic == 'ground_truth/mission/blockages_list').any():
        rubble_df = pp3.get_init_rubble_info(mission)
    else:
        rubble_df = pd.DataFrame()

    # get victims info
    if (mission.topic == 'ground_truth/mission/victims_list').any():
        victims_df = pp3.get_init_victims_info(mission)
    else:
        victims_df = pd.DataFrame()
    return rubble_df, victims_df


def preprocess_ac_news(new_lines, mission_map):

    preprocessed_news = pp3.boil_minimal(new_lines, mission_map)

    return preprocessed_news


def get_player_callsign(mission):

    player_callsign_dict = {}
    trial = mission[mission.topic == 'trial']            
    for info in trial['data.client_info'].iloc[0]:
        player_callsign_dict[info['playername']] = info['callsign']

    return player_callsign_dict


def test_belief(news: pd.DataFrame, rubble_df: pd.DataFrame, victim_df: pd.DataFrame):
    """
    REQUIRES:
              news only has "move" actions
    """
    # simple script to test ongoing work in belief.py
    print(rubble_df)
    print(victim_df)
    print(news)

    victim_df, tiles_seen = bf.update_victims_seen(news, rubble_df, victims_df)

    # visualize results
    print(victim_df)
    for player in news.player_id.unique():
        plt.matshow(tiles_seen[player])
        plt.show()

    return 0


def threat_room_known(t, marked_room_id, threat_r):
    return marked_room_id in threat_r[threat_r.time_added <= t].room_name.to_list()


def critical_victim_coordination(mission: Mission, player_callsign: Dict):
    # get all entrances and exists
    m = mission.mission.drop(columns=["current_role", "action_data", "score"])
    m = m[(m.action == 'move')].copy()
    m = m[m.z <= (m3.Map.FOV_Z_MAX-0.5)]
    m = m.sort_values("time")
    m['location'] = m.apply(lambda row: mission.find_room(row.x, row.z), axis=1)
    m = m.fillna('not_room')

    # get one player's entrances and exits
    for player in mission.players:
        player_mv = m[m.player_id == player].copy()
        if player_callsign[player] == 'Red':
            red_ee = mission.get_near_critical_time(player_mv)
        elif player_callsign[player] == 'Green':
            green_ee = mission.get_near_critical_time(player_mv)
        elif player_callsign[player] == 'Blue':
            blue_ee = mission.get_near_critical_time(player_mv)

    # get critical victim coordination
    saw_times = red_ee.near_critical.to_list() + \
                blue_ee.near_critical.to_list() + \
                green_ee.near_critical.to_list()
    saw_times = np.sort(saw_times)
    saw_times = saw_times[~np.isnan(saw_times)]

    ee = pd.concat((red_ee, blue_ee, green_ee))

    # cvc stands for critical victim coordination
    cvc = pd.DataFrame(columns=['room_id', 'player_saw', 'saw_time', 'exit_time',
                                'wait_time', 'teammate_enter', 'over_threshold'])

    for saw_time in saw_times:
        room = ee[ee.near_critical == saw_time].location.item()
        player_saw = ee[ee.near_critical == saw_time].player_id.item()
        enter_time = ee[ee.near_critical == saw_time].time.item()
        exit_time = ee[ee.near_critical == saw_time].exit.item()

        # check if saw_time is doubled
        # if saw_time < the exit time after the coordination in the recorded room, it is doubled
        saw_time_new = True
        visited = cvc[cvc.room_id == room]
        if len(visited) > 0:
            last_exit_time = visited.exit_time.to_numpy()[-1]
            if saw_time < last_exit_time:
                saw_time_new = False

        if saw_time_new:
            teammate_df = ee[(ee.location == room) & (ee.player_id != player_saw) & 
                            (ee.time <= exit_time) & (ee.exit >= enter_time)]
            if len(teammate_df) == 0:
                wait_time = exit_time - saw_time
                teammate = np.nan
            elif len(teammate_df) == 1 or len(teammate_df) == 2:
                wait_time = max(0, teammate_df.iloc[0].time - saw_time)
                teammate = teammate_df.iloc[0].player_id
            else:
                print("logic loophole")
            cvc = cvc.append({'room_id':room, 'player_saw':player_saw,
                            'saw_time':saw_time, 'exit_time':exit_time,
                            'wait_time':wait_time, 'teammate_enter':teammate}, ignore_index=True)

    cvc['over_threshold'] = np.where(cvc.wait_time > 5, True, False)
    cvc = cvc.drop(columns=['exit_time'])
    return cvc

class PlayerUtility(ASISTAgentHelper):
    def __init__(self, on_message_handler):
        super().__init__(on_message_handler)
        self.__rubble_destroy_queue = set()
        self.__rubble_collapse_queue = set()
        self.__rubble_threshold_time = 10
        self.__topic_message_list = list()
        self.mission_raw = pd.DataFrame()
        self.__agent_publish_loop_thread = None
        self.topic_track = set()
        self.msg_processed_idx = 0
        self.preprocess_calculation = False
        self.time_in_seconds = 0
        self.__agent_publish_loop_thread = None
        self.__agent_publish_running = False
        self.is_actual_mission = False
        self._ASISTAgentHelper__message_bus.onMessage = self.__on_utility_message

    def __check_rubble_destroy(self, rubble_id):
        if rubble_id not in self.__rubble_destroy_queue:
            self.mission_raw = pd.json_normalize(
                self.__topic_message_list[self.msg_processed_idx :]
            )
            try:
                self.time_in_seconds = self.mission_raw.iloc[-1]["data.elapsed_milliseconds"] /1000
                logger.info(f"Time elapsed: {self.time_in_seconds}")
                news = preprocess_ac_news(self.mission_raw, self.mission_map)
                self.mission_df = pd.concat([self.mission_df, news])
                self.msg_processed_idx = len(self.__topic_message_list)
                self.mission = dp3.Mission(self.mission_df, self.rubble_df, self.victims_df)
                self.__publish_threat_coord(rubble_id)
            except Exception as e:
                logger.info(f"Error in check_rubble_destroy")
                logger.info(f"(in check_rubble_destroy) self.mission_raw shape: {self.mission_raw.shape}")

    def __wait_rubble_destroy(self, rubble_id):
        t = Timer(self.__rubble_threshold_time, self.__check_rubble_destroy, [rubble_id])
        t.start()

    @staticmethod
    def __get_rubble_id(msg_data, event):
        if event == "rubble_collapse":
            return " ".join(
                [str(msg_data["data"]["fromBlock_x"]), str(msg_data["data"]["fromBlock_z"])]
            )
        else:
            return " ".join([str(msg_data["data"]["rubble_x"]), str(msg_data["data"]["rubble_z"])])

    def __get_threat_coord(self):
        data_dic = {}
        try:
            r_log = self.mission.rubble_log.copy()
            threat_r = r_log[(r_log.time_added > 0)]
            ac_threat_r = threat_r[['room_name', 'time_added', 'player_triggered', 'wait_time']]
            ac_threat_r = ac_threat_r.rename(columns={'room_name':'room_id',
                                                    'time_added':'threat_activation_time',
                                                    'player_triggered':'threat_activation_player',
                                                    'wait_time':'wait_time'})
            data_dic = ac_threat_r.to_dict(orient='list')
            data_dic["threshold:"] = self.__rubble_threshold_time
        except Exception:
            logger.error("Error processing the threat_r", exc_info=True)
        return data_dic

    def ___update_base_data(self):
        pass
        # self.mission_raw = pd.json_normalize(
        #     self.__topic_message_list[self.msg_processed_idx :]
        # )
        # self.time_in_seconds = self.mission_raw.iloc[-1]["data.elapsed_milliseconds"] /1000
        # logger.info(f"Time elapsed: {self.time_in_seconds}")
        # news = preprocess_ac_news(self.mission_raw, self.mission_map)
        # self.mission_df = pd.concat([self.mission_df, news])
        # self.msg_processed_idx = len(self.__topic_message_list)
        # self.mission = dp3.Mission(self.mission_df, self.rubble_df, self.victims_df)


    def __get_belief_diff(self):
        self.mission_raw = pd.json_normalize(
            self.__topic_message_list[self.msg_processed_idx :]
        )
        try:
            self.time_in_seconds = self.mission_raw.iloc[-1]["data.elapsed_milliseconds"] /1000
            logger.info(f"Time elapsed: {self.time_in_seconds}")
            news = preprocess_ac_news(self.mission_raw, self.mission_map)
            self.mission_df = pd.concat([self.mission_df, news])
            self.msg_processed_idx = len(self.__topic_message_list)
            self.mission = dp3.Mission(self.mission_df, self.rubble_df, self.victims_df)
            ac_bf = bf.BeliefDiff(self.mission, self.time_in_seconds, self.player_callsign)
            cols = ac_bf.entropy_df.columns != 'room_id'
            try:
                ac_bf.entropy_df.loc[:, cols] = ac_bf.entropy_df.loc[:, cols].round(3)
            except Exception as e:
                logger.info(f"astype conversion error {e}. The dataframe may have incompatible values like NaN")

            ent_df = ac_bf.entropy_df
            ent_df = ent_df.rename(columns={'room_id':'room_id',
                                            'shared':'shared',
                                            'RED_indiv':'RED_indiv',
                                            'BLUE_indiv':'BLUE_indiv',
                                            'GRENN_indiv':'GREEN_indiv',
                                            'RED_marker':'RED_marker',
                                            'BLUE_marker':'BLUE_marker',
                                            'GREEN_marker':'GREEN_marker'})
            return ent_df.to_dict(orient='list')
        except Exception as e:
            logger.info("Time in seconds is not available for belief diff message")
            logger.info(f"(in get_belief_diff) self.mission_raw shape: {self.mission_raw.shape}")
            logger.info(f"type of error in get_belief_diff: {type(e)}")
            return str(e)

    def __publish_belief_diff(self):
        if self.preprocess_calculation is True and self.time_in_seconds > 0:
            logger.info("Getting data belief diff")
            data_dic = self.__get_belief_diff()
            if isinstance(data_dic, dict):
                data_dic["time_in_seconds"] = self.time_in_seconds
                self.send_msg(
                    "agent/ac/belief_diff",
                    "agent",
                    "AC:belief_diff",
                    0.1,
                    data=data_dic,
                    msg_version="0.1",
                )
                logger.info("Published belief diff")
            else:
                logger.info(f"content of data_dic error: {data_dic}")

    def __publish_threat_coord(self, rubble_id):
        logger.info("Getting data threat room coordination")
        self.__rubble_destroy_queue.add(rubble_id)
        data_dic = self.__get_threat_coord()
        data_dic["time_in_seconds"] = self.time_in_seconds
        self.send_msg(
            "agent/ac/threat_room_coordination",
            "agent",
            "AC:threat_room_coordination",
            0.2,
            data=data_dic,
            msg_version="0.1",
        )
        logger.info("Published threat room coordination")


    def run_belief_diff_publish_loop(self):
        logger.info("Starting Belief Diff Publish Loop: " + self.agent_name)
        self.__agent_publish_running = True

        while self.__agent_publish_running:
            time.sleep(30)
            self.__publish_belief_diff()
        # self.__agent_publish_loop_thread = None

    def start_belief_diff_publish_loop_thread(self):
        if self.__agent_publish_loop_thread is not None:
            return
        self.__agent_publish_loop_thread = threading.Thread(target=self.run_belief_diff_publish_loop)
        self.__agent_publish_loop_thread.start()

    def stop_belief_diff_publish_loop_thread(self):
        self.__agent_publish_running = False

    def __get_critical_victim_coord(self):
        pass


    def __publish_critical_victim_coord(self):
        data_dic = self.__get_critical_victim_coord()
        data_dic["time_in_seconds"] = self.time_in_seconds
        logger.info("publishing critical victim coordination")
        self.send_msg(
            "agent/ac/critical_victim_coordination",
            "agent",
            "AC:critical_victim_coordination",
            0.1,
            data=data_dic,
            msg_version="0.1",
        )

    def __is_near_critical_victim(self, x, z):
        self.mission.victims_ground_truth
        v_gt = self.mission.victims_ground_truth.copy()
        v_c = v_gt[v_gt.victim_type == 'C']
        if np.sum((v_c.x - x)**2 + (v_c.z - z)**2 < 9) > 0:
            return True
        else:
            return False


    def __on_utility_message(self, message):
        self._ASISTAgentHelper__on_message(message)
        try:
            topic = message.key
            msg_data = message.jsondata
            msg_data["topic"] = topic

            if topic == "trial" and msg_data["msg"]["sub_type"] == "stop":
                self.is_actual_mission = False

            if topic == "trial" and msg_data["msg"]["sub_type"] == "start" and\
               msg_data["data"]["experiment_mission"] != "Hands-on Training":
                self.is_actual_mission = True
                self.__topic_message_list = list()
                self.preprocess_calculation = False
                self.mission_raw = pd.DataFrame()
                self.__rubble_destroy_queue = set()
                self.__rubble_collapse_queue = set()
                self.topic_track = set()
                self.msg_processed_idx = 0
                self.preprocess_calculation = False
                self.time_in_seconds = 0
                self.stop_belief_diff_publish_loop_thread()
                self.__agent_publish_loop_thread = None
                self.__agent_publish_running  = False
                self.start_belief_diff_publish_loop_thread()
            self.__topic_message_list.append(msg_data)

            if self.is_actual_mission:
                if self.preprocess_calculation is False:
                    if topic in {
                        "trial",
                        "ground_truth/mission/blockages_list",
                        "ground_truth/mission/victims_list",
                        "observations/state",
                    }:
                        self.topic_track.add(topic)
                        if len(self.topic_track) == 4:
                            self.msg_processed_idx = len(self.__topic_message_list)
                            self.mission_raw = pd.json_normalize(
                                self.__topic_message_list[: self.msg_processed_idx]
                            )
                            self.mission_df, self.mission_map = preprocess_ac(self.mission_raw)
                            self.player_callsign = get_player_callsign(self.mission_raw)
                            self.rubble_df, self.victims_df = rubble_victim_init_info(self.mission_raw)
                            self.preprocess_calculation = True
                            self.mission = dp3.Mission(self.mission_df, self.rubble_df, self.victims_df)
                    # logger.info(msg_data)
                if topic in {
                    "observations/events/player/rubble_collapse",
                    "observations/events/player/rubble_destroyed",
                    "observations/events/player/marker_placed",
                } and self.preprocess_calculation is True:
                    self.mission_raw = pd.json_normalize(
                        self.__topic_message_list[self.msg_processed_idx :]
                    )
                    self.time_in_seconds = self.mission_raw.iloc[-1]["data.elapsed_milliseconds"] /1000
                    logger.info(f"Time elapsed: {self.time_in_seconds}")
                    news = preprocess_ac_news(self.mission_raw, self.mission_map)
                    self.mission_df = pd.concat([self.mission_df, news])
                    self.msg_processed_idx = len(self.__topic_message_list)
                    self.mission = dp3.Mission(self.mission_df, self.rubble_df, self.victims_df)

                    if topic == "observations/events/player/rubble_collapse":
                        rubble_id = self.__get_rubble_id(msg_data, "rubble_collapse")
                        self.__rubble_collapse_queue.add(rubble_id)
                        # self.__rubble_destroy_queue.add(rubble_id)
                        self.__wait_rubble_destroy(rubble_id)
                    elif topic == "observations/events/player/rubble_destroyed":
                        rubble_id = self.__get_rubble_id(
                            msg_data, "rubble_destroy"
                        )  # remove id from the queue
                        if rubble_id in self.__rubble_collapse_queue:
                            self.__publish_threat_coord(rubble_id)
                        else:
                            logger.info(f"Rubble id: {rubble_id} destroyed that was not collapsed.")
                    elif topic == "observations/events/player/marker_placed":
                        logger.info(f"Topic:  {topic}")
                        logger.info(f"MSG_DATA: {msg_data['data']['type']}")
                        if msg_data["data"]["type"] in {"blue_threat", "red_threat", "green_threat"}:
                            self.__publish_threat_room_communication()
                        elif msg_data["data"]["type"] in {
                            "blue_abrasion",
                            "red_abrasion",
                            "green_abrasion",
                            "blue_bonedamage",
                            "red_bonedamage",
                            "green_bonedamage"
                        }:
                            self.__publish_victim_type()
                # elif topic == "observations/state" and self.preprocess_calculation is True:
                #     x_coord = msg_data["data"]["x"]
                #     z_coord = msg_data["data"]["z"]
                #     if msg_data["data"]["z"] <= (Map.FOV_Z_MAX-0.5):
                #         near_victim = self.__is_near_critical_victim(msg_data["data"]['x'], msg_data["data"]["z"])
                #         if near_victim is True:
                #             self.__publish_critical_victim_coord()
        except Exception:
            logger.error("Error processing the message on utility", exc_info=True)

    def __publish_threat_room_communication(self):
        data_dic = self.__get_threat_room_communication()
        data_dic["time_in_seconds"] = self.time_in_seconds
        logger.info("publishing threat room communication")
        self.send_msg(
            "agent/ac/threat_room_communication",
            "agent",
            "AC:threat_room_communication",
            0.2,
            data=data_dic,
            msg_version="0.1",
        )

    def __get_threat_room_communication(self):
        logger.info("Getting data threat room communication")
        r_log = self.mission.rubble_log
        threat_r = r_log[(r_log.time_added > 0)]
        threat_m = self.mission.markers_log.copy()
        threat_m['type'] = threat_m.apply(lambda row: row.type.split('_')[1], axis=1)
        threat_m = threat_m[threat_m.type == 'threat'].copy()

        threat_m['nearest_room'] = threat_m.apply(lambda row: self.mission.nearest_plate(row.x, row.z),
                                                axis=1)
        threat_m['threat_room_seen'] = threat_m.apply(lambda x:
                                        threat_room_known(x.time, x.nearest_room, threat_r), axis=1)

        ac_threat_m = threat_m[['player_id','time','nearest_room','threat_room_seen']]
        ac_threat_m = ac_threat_m.rename(columns={'player_id':'player_placed',
                                                'time':'time_placed',
                                                'nearest_room':'nearest_room',
                                                'threat_room_seen':'is_observed_threat_room'})

        return ac_threat_m.to_dict(orient='list')
    logger.info("Published threat room communication")

    def __get_victim_type(self):
        DIST_THRESHOLD = 2
        markers_dict = {'abrasion': 'A', 'bonedamage': 'B'} # 'criticalvictim': 'C'
        markers = self.mission.markers_log.copy()
        markers['type'] = markers.apply(lambda row: row.type.split('_')[1], axis=1)
        markers = markers[markers.type.isin(markers_dict.keys())]
        markers['type'] = markers.apply(lambda row: markers_dict[row.type], axis=1)

        markers['vicitm_type_in_vicinity'] = ''
        markers['matched_vicitm_id_in_vicinity'] = ''
        markers['vicitm_type_in_vicinity'] = markers['vicitm_type_in_vicinity'].astype(object)
        markers['matched_vicitm_id_in_vicinity'] = markers['matched_vicitm_id_in_vicinity'].astype(object)
        # when operating on streaming data, there would be no for loop
        for ind, marker in markers.iterrows():
            t = marker['time']
            v = self.mission.get_victims_info_minimal(t)
            v = v.reset_index('victim_id')

            in_vicinity = ((v.x - marker['x'])**2 + (v.z - marker['z'])**2) <= DIST_THRESHOLD**2
            victim_type_in_vicinity = v[in_vicinity].victim_type.to_list()
            markers.at[ind, 'vicitm_type_in_vicinity'] = ','.join(victim_type_in_vicinity)

            marker_match_type = (v.victim_type == marker['type'])
            matched_victim_id_in_vicinity = v[in_vicinity & marker_match_type].victim_id.to_list()
            markers.at[ind, 'matched_vicitm_id_in_vicinity'] = ','.join(str(int(mviiv)) 
                                                                        for mviiv in matched_victim_id_in_vicinity)


        ac_markers = markers[['player_id','time','type','vicitm_type_in_vicinity',
                            'matched_vicitm_id_in_vicinity']]
        ac_markers = ac_markers.rename(columns={'player_id':'player_placed',
                                                'time':'time_placed',
                                                'type':'marker_block_type',
                                                'victim_type_in_vicinity':'victim_type_in_vicinity',
                                    'matched_vicitm_id_in_vicinity':'victims_match_marker_block'})

        data_dic = ac_markers.to_dict(orient='list')
        data_dic["vicinity_threshold_in_blocks"] = DIST_THRESHOLD
        return data_dic

    def __publish_victim_type(self):
        logger.info("Getting victim type communication")
        data_dic = self.__get_victim_type()
        data_dic["time_in_seconds"] = self.time_in_seconds
        self.send_msg(
            "agent/ac/victim_type_communication",
            "agent",
            "AC:victim_type_communication",
            0.2,
            data=data_dic,
            msg_version="0.1",
        )
        logger.info("Published victim type communication")
