import os
import json
import time
import numpy as np
from ASISTTools import ASISTTools
from SemanticMap import SemanticMap
from ShortestPathCalculator import ShortestPathCalculator


class ParticipantLocationInfo(object):
    def __init__(self, close_location_distance=30.0, maps_folder='.',
                 maps_map={"DEFAULT": {"semantic_map": "Saturn_2.6_3D_sm_v1.0.json",
                                       "base_map": "Saturn_2.6_3D_bm_v1.0.json",
                                       "dist_map": "Saturn_2.6_3D_dm_v1.0"}},
                 helper=None, output_every_n_sec=0.5):
        self.mission_running = False
        self.client_info = None
        self.player_positions = None
        self.proximity_data = None
        self.semantic_map = None
        self.treatment_areas = {}
        self.map_rooms = {}
        self.basemap = None
        self.path_calculator = None
        self.role_change_location = [-2154, 125]
        self.maps_folder = maps_folder
        self.maps_map = maps_map
        self.close_location_distance = close_location_distance
        self.helper = helper
        self.output_every_n_sec = output_every_n_sec
        self.last_output_time = time.perf_counter()
        self.defaults_set = False

    def set_preloaded_defaults(self, default_info):
        self.semantic_map = default_info.semantic_map
        self.treatment_areas = default_info.treatment_areas
        self.map_rooms = default_info.map_rooms
        self.basemap = default_info.basemap
        self.path_calculator = default_info.path_calculator
        self.defaults_set = True

    def process_message(self, topic, header, msg, data):
        try:
            if topic is None or data is None:
                return self.mission_running

            # See if the message is a trial message and if so, then restart processing messages
            if topic == 'trial' and msg is not None and 'sub_type' in msg.keys():
                if msg['sub_type'] == 'start':
                    # This is the message which tells us which map is being used and all the player info.
                    self.setup_trial_info(data)
                    self.mission_running = True
                else:
                    self.mission_running = False
                    self.client_info = None
                    self.player_positions = None
                    self.proximity_data = None
                return self.mission_running

            if self.client_info is None:
                return self.mission_running

            if topic == 'observations/events/mission':
                # Note mission start/stop
                self.mission_running = True if data['mission_state'].lower().strip() == 'start' else False
                if self.mission_running:
                    self.last_output_time = time.perf_counter()

            elif topic == 'observations/state':
                self.update_player_location(data)
                self.output_if_time(self.helper.get_trial_key(msg))

            elif topic == 'observations/events/player/role_selected':
                self.update_role_selected(data)

        except Exception as ex:
            ASISTTools.get_logger().error(ex)
            ASISTTools.get_logger().error('Error processing topic = ' + topic)

        return self.mission_running

    def setup_trial_info(self, data):
        ASISTTools.get_logger().debug("Setting up the Trial")
        if data is None or 'client_info' not in data.keys():
            ASISTTools.get_logger().debug("Ignoring Trial message because there is no client_info.")
            return

        self.client_info = data['client_info']
        ASISTTools.set_client_info(self.client_info)
        self.player_positions = {}

        # setup the proximity dictionary
        proximity_data = {"elapsed_milliseconds": -1, "participants": {}}
        for client in self.client_info:
            callsign = client['callsign'].lower().strip()
            self.player_positions[callsign] = {"x": self.role_change_location[0],
                                               "z": self.role_change_location[1],
                                               "new_x": self.role_change_location[0],
                                               "new_z": self.role_change_location[1],
                                               "updated": True}
            proximity_data["participants"][callsign] = {"callsign": callsign,
                                                        "participant_id": client['participant_id']
                                                            if 'participant_id' in client.keys() else None,
                                                        "role": "None",
                                                        "current_location": "sga",
                                                        "distance_to_role_change": {"sga": 0.0},
                                                        "distance_to_treatment_areas": {},
                                                        "distance_to_participants": {},
                                                        "distance_to_current_location_exits": {},
                                                        "distance_to_closest_locations": {}}
        self.proximity_data = proximity_data
        ASISTTools.get_logger().debug(self.proximity_data)

        map_name = data['map_name'] if 'map_name' in data.keys() else "MAP_NAME_NOT_SET"
        if map_name not in self.maps_map.keys():
            ASISTTools.get_logger().warn("No mapping for map_name: " + map_name + ".")
            if 'DEFAULT' in self.maps_map.keys():
                ASISTTools.get_logger().warn("  - Using the DEFAULT.")
                map_name = 'DEFAULT'
            else:
                self.client_info = None
                return

        self.load_map_info(map_name)

    def load_map_info(self, map_name):
        default_map = self.maps_map['DEFAULT']
        map_map = self.maps_map[map_name]

        if self.defaults_set and \
           map_map['semantic_map'] == default_map['semantic_map'] and \
           map_map['base_map'] == default_map['base_map']:
            ASISTTools.get_logger().info("Using the preloaded defaults for map: " + map_name)
            return

        dist_map_name = os.path.join(self.maps_folder, map_map['dist_map']) if 'dist_map' in map_map else None

        # load the semantic map associated with this trial
        self.semantic_map = None
        filename = os.path.join(self.maps_folder, map_map["semantic_map"])
        if os.path.exists(filename):
            self.semantic_map = SemanticMap()
            self.semantic_map.load_semantic_map(filename)

        if self.semantic_map is None:
            ASISTTools.get_logger().warn("*** No Semantic map at: " + filename)
            self.client_info = None
            ASISTTools.get_logger().debug("Ignoring Trial message because there is no associated Semantic map for: " + map_name)
            return
        self.treatment_areas = self.semantic_map.get_locations_with_types(["treatment"], use_updated_map=False)
        self.map_rooms = self.semantic_map.get_locations_with_types(["room", "bathroom", "treatment"], use_updated_map=False)

        # load the base map for use by the Map Search tools
        self.basemap = None
        filename = os.path.join(self.maps_folder, map_map["base_map"])
        if os.path.exists(filename):
            with open(filename) as json_file:
                self.basemap = json.load(json_file)

        if self.basemap is None:
            ASISTTools.get_logger().warn("   *** No basemap at: " + filename)
            self.client_info = None
            ASISTTools.get_logger().debug("Ignoring Trial message because there is no associated base map for: " + map_name)
            return

        # Initialize the Map SearchTools
        self.path_calculator = ShortestPathCalculator(dist_map_name, self.semantic_map, self.basemap)

        return

    # get the semantic map location containing this (x, z), if no location
    # contains it return the previous Location.  Also if the (x, z) is not
    # in a location or a connection, then return the previous location, x, and z
    def get_parent_location_at(self, x, z, prevX, prevZ, prevLoc):
        locs = self.semantic_map.get_locations_containing(x, z)
        currentLoc = 'UNKNOWN'
        currentX = x
        currentZ = z
        if locs is None or len(locs) == 0:
            currentLoc = prevLoc
            if prevLoc == 'UNKNOWN':
                ASISTTools.get_logger.debug("No locations at (" + str(x) + ", " + str(z) + ") and previous location is UNKNOWN!!!")
            conns = self.semantic_map.get_connections_containing(x, z)
            if conns is None or len(conns) == 0:
                currentX = prevX
                currentZ = prevZ
        else:
            for loc in locs:
                if not loc['type'].lower().endswith('_part'):  # in ['room', 'bathroom', 'hallway', 'treatment']:
                    currentLoc = loc['id']
                    break

        return currentLoc, currentX, currentZ

    def update_player_location(self, data):
        callsign = ASISTTools.get_player_callsign(data)
        self.proximity_data['elapsed_milliseconds'] = data['elapsed_milliseconds']
        if callsign is None or callsign not in self.proximity_data["participants"].keys():
            return

        player_pos = self.player_positions[callsign]
        x = int(np.floor(data['x']))
        z = int(np.floor(data['z']))

        # see if the player has moved
        if player_pos['x'] != x or player_pos['z'] != z:
            player_pos['updated'] = True
            player_pos['new_x'] = x
            player_pos['new_z'] = z

    def output_if_time(self, trial_key):
        # # do not output anything if the mission has not started.
        if self.proximity_data['elapsed_milliseconds'] < 0:
            return

        # check and see if enough time has passed before sending another message.
        time_now = time.perf_counter()
        if time_now - self.last_output_time < self.output_every_n_sec:
            return

        self.last_output_time = time_now
        time_start = time_now

        for callsign in self.proximity_data["participants"]:
            update_player_loc_time = 0
            player_2_player_dist_time = 0
            exit_calc_time = 0
            closest_location_calc_time = 0
            time_end = time.perf_counter()
            loop_time = time_end - time_start
            time_start = time_end

            player_pos = self.player_positions[callsign]
            # if callsign.lower() == 'red':
            #     ASISTTools.get_logger().info(player_pos)

            if not player_pos['updated']:
                continue
            player_pos['updated'] = False
            try:
                player = self.proximity_data["participants"][callsign]

                new_loc_id, x, z = self.get_parent_location_at(player_pos['new_x'], player_pos['new_z'],
                                                               player_pos['x'], player_pos['z'],
                                                               player['current_location'])
                player_pos['x'] = x
                player_pos['z'] = z
                player['current_location'] = new_loc_id

                time_end = time.perf_counter()
                update_player_loc_time = time_end - time_start
                time_start = time_end

                dist = self.path_calculator.shortest_dist([x, z], self.role_change_location)
                player['distance_to_role_change']['sga'] = dist

                # update the players distance from other players
                player['distance_to_participants'] = {}
                for other_player in self.proximity_data['participants'].values():
                    if other_player['callsign'] == player['callsign']:
                        continue
                    other_player_pos = self.player_positions[other_player['callsign']]
                    dist = self.path_calculator.shortest_dist([x, z], [other_player_pos['x'], other_player_pos['z']])
                    player['distance_to_participants'][other_player['callsign']] = dist
                    other_player['distance_to_participants'][player['callsign']] = dist

                time_end = time.perf_counter()
                player_2_player_dist_time = time_end - time_start
                time_start = time_end

                player['distance_to_current_location_exits'] = {}
                location = self.semantic_map.get_location(player['current_location'], use_updated_map=True)
                # only provide 'exits' for rooms.  Ignore hallways and other types of locations.
                if location['type'] in ['room', 'bathroom', 'treatment']:
                    exits = self.semantic_map.get_connections_to_location(player['current_location'], use_updated_map=False)
                    for exit_id in exits:
                        player['distance_to_current_location_exits'][exit_id] = self.path_calculator.shortest_distance_to_connection([x, z], exit_id)

                time_end = time.perf_counter()
                exit_calc_time = time_end - time_start
                time_start = time_end

                # update distance to treatment areas
                player['distance_to_treatment_areas'] = {}
                for loc_id in self.treatment_areas:
                    player['distance_to_treatment_areas'][loc_id] = self.path_calculator.shortest_distance_to_location([x, z], loc_id)

                player['distance_to_closest_locations'] = {}
                for room in self.map_rooms:
                    if room == player['current_location']:
                        continue
                    dist = self.path_calculator.shortest_distance_to_location([x, z], room)
                    if dist is not None and dist < self.close_location_distance:
                        player['distance_to_closest_locations'][room] = dist

                time_end = time.perf_counter()
                closest_location_calc_time = time_end - time_start
                time_start = time_end

            except Exception as ex:
                ASISTTools.get_logger().error(ex)
                ASISTTools.get_logger().error('Error computing proximity info for : ' + callsign)

            time_end = time.perf_counter()
            ASISTTools.get_logger().debug("  " + callsign + " times:")
            ASISTTools.get_logger().debug("                 loop time: " + str(loop_time))
            ASISTTools.get_logger().debug("         update_player_loc: " + str(update_player_loc_time))
            ASISTTools.get_logger().debug("      player_2_player_dist: " + str(player_2_player_dist_time))
            ASISTTools.get_logger().debug("                 exit_calc: " + str(exit_calc_time))
            ASISTTools.get_logger().debug("     closest_location_calc: " + str(closest_location_calc_time))
            ASISTTools.get_logger().debug("            try/catch exit: " + str((time_end-time_start)))

        time_now = time.perf_counter()

        time_end = time_now
        ASISTTools.get_logger().debug("                 loop time: " + str((time_end-time_start)))

        ASISTTools.get_logger().debug("Output proximity for trial: " + trial_key + " @ " +
                                      str(self.proximity_data['elapsed_milliseconds']/1000) +
                                      " time to process proximity: " + str(time_now - self.last_output_time))
        data = {"elapsed_milliseconds": self.proximity_data['elapsed_milliseconds'], "participants": []}
        for pi in self.proximity_data['participants'].values():
            proximity = {
                "callsign": pi["callsign"],
                "participant_id": pi["participant_id"],
                "role": pi["role"],
                "current_location": pi["current_location"],
                "distance_to_participants": [],
                "distance_to_current_location_exits": [],
                "distance_to_closest_locations": [],
                "distance_to_role_change": [],
                "distance_to_treatment_areas": []
            }
            for key in pi['distance_to_participants']:
                if pi['distance_to_participants'][key] is not None:
                    proximity['distance_to_participants'].append({"id": key, "distance": pi['distance_to_participants'][key]})
            for key in pi['distance_to_current_location_exits']:
                if pi['distance_to_current_location_exits'][key] is not None:
                    proximity['distance_to_current_location_exits'].append({"id": key, "distance": pi['distance_to_current_location_exits'][key]})
            for key in pi['distance_to_closest_locations']:
                if pi['distance_to_closest_locations'][key] is not None:
                    proximity['distance_to_closest_locations'].append({"id": key, "distance": pi['distance_to_closest_locations'][key]})
            for key in pi['distance_to_role_change']:
                if pi['distance_to_role_change'][key] is not None:
                    proximity['distance_to_role_change'].append({"id": key, "distance": pi['distance_to_role_change'][key]})
            for key in pi['distance_to_treatment_areas']:
                if pi['distance_to_treatment_areas'][key] is not None:
                    proximity['distance_to_treatment_areas'].append({"id": key, "distance": pi['distance_to_treatment_areas'][key]})
            data["participants"].append(proximity)

        ASISTTools.get_logger().info(data)

        self.helper.send_msg("observations/events/player/proximity",
                             "event",
                             "Event:proximity", "1.0",
                             trial_key=trial_key,
                             data=data)

    def update_role_selected(self, data):
        callsign = ASISTTools.get_player_callsign(data)
        if callsign is not None and callsign in self.proximity_data["participants"].keys():
            self.proximity_data["participants"][callsign]['role'] = data['new_role']
        return
