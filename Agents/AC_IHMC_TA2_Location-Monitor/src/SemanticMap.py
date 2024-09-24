"""
SemanticMap Utilities Class

Author: Roger Carff (rcarff@ihmc.org)
"""
import os
import json
import math
import numpy as np
from skimage.filters import threshold_mean
from skimage.measure import find_contours
from skimage.transform import rescale
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class SemanticMap(object):
    def __init__(self, semantic_map_filename=None):
        self.semantic_map = {}
        self.updates = {}
        self.updated_semantic_map = {}
        self.load_semantic_map(semantic_map_filename)

    def load_semantic_map(self, semantic_map_filename):
        if semantic_map_filename is not None and os.path.exists(semantic_map_filename):
            with open(semantic_map_filename) as json_file:
                self.set_semantic_map(json.load(json_file))

    def set_semantic_map(self, semantic_map_json):
        self.semantic_map = semantic_map_json
        self.updated_semantic_map = json.loads(json.dumps(semantic_map_json))  # clone the semantic map
        self.updates = {}
        self.dps, self.distances, self.predecessors = self.compute_distances()

    def get_updates(self):
        return self.updates

    def get_semantic_map(self):
        return self.semantic_map

    def get_updated_semantic_map(self):
        return self.updated_semantic_map

    def get_locations_with_types(self, types=[], use_updated_map=True):
        locations = self.updated_semantic_map['locations'] if use_updated_map else self.semantic_map['locations']
        response = {}
        for loc in locations:
            if loc['type'] in types:
                response[loc['id']] = loc

        return response

    def get_location(self, loc_id, use_updated_map=True):
        locations = self.updated_semantic_map['locations'] if use_updated_map else self.semantic_map['locations']
        for loc in locations:
            if loc['id'] == loc_id:
                return loc

        return None

    def get_locations_containing(self, x, z, use_updated_map=True):
        locations = self.updated_semantic_map['locations'] if use_updated_map else self.semantic_map['locations']
        return SemanticMap.get_containing(locations, x, z)

    def get_connections_containing(self, x, z, use_updated_map=True):
        connections = self.updated_semantic_map['connections'] if use_updated_map else self.semantic_map['connections']
        return SemanticMap.get_containing(connections, x, z)

    def get_all_connections(self, use_updated_map=True):
        connections = self.updated_semantic_map['connections'] if use_updated_map else self.semantic_map['connections']
        return connections

    def get_objects_containing(self, x, z, use_updated_map=True):
        objs = self.updated_semantic_map['objects'] if use_updated_map else self.semantic_map['objects']
        return SemanticMap.get_containing(objs, x, z)

    @staticmethod
    def compute_distance(x1, y1, x2, y2):
        return math.hypot(x2-x1, y2-y1)


    def get_num_non_critical_victims(self, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "decision_points" in sm['extensions']['ihmc_simasist'].keys():
           return 0

        num = 0
        dps = sm['extensions']['ihmc_simasist']['decision_points']
        for dp in dps:
            if 'victims' in dp.keys() and 'non_critical' in dp['victims'].keys():
                num += dp['victims']['non_critical']

        return num


    def get_num_critical_victims(self, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "decision_points" in sm['extensions']['ihmc_simasist'].keys():
           return 0

        num = 0
        dps = sm['extensions']['ihmc_simasist']['decision_points']
        for dp in dps:
            if 'victims' in dp.keys() and 'critical' in dp['victims'].keys():
                num += dp['victims']['critical']

        return num


    def get_decision_point_id_list(self, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "decision_points" in sm['extensions']['ihmc_simasist'].keys():
           return []

        ret_dps = []
        dps = sm['extensions']['ihmc_simasist']['decision_points']
        for dp in dps:
            if not dp['id'] in ret_dps:
                ret_dps.append(dp['id'])

        ret_dps.sort()
        return ret_dps

    def get_decision_points_in_location(self, loc_id, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "decision_points" in sm['extensions']['ihmc_simasist'].keys():
           return []

        ret_dps = []
        dps = sm['extensions']['ihmc_simasist']['decision_points']
        for dp in dps:
            if dp['area_id'] == loc_id:
                ret_dps.append(dp)

        return ret_dps

    def get_objects_intersecting(self, bounds, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not 'objects' in sm.keys():
            return []
        objs = []
        if bounds['type'] == 'point':
            for obj in sm['objects']:
                if SemanticMap.semantic_bounds_contains(obj['bounds'], bounds['coordinates'][0]['x'], bounds['coordinates'][0]['z']):
                    objs.append(obj)
        else:
            fsm_bnds = SemanticMap.from_semantic_bounds(bounds)
            for obj in sm['objects']:
                if SemanticMap.bounds_intersect(SemanticMap.from_semantic_bounds(obj['bounds']), \
                                                fsm_bnds):
                    objs.append(obj)

        return objs

    def get_connection(self, connection_id, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not 'connections' in sm.keys():
            return None

        for connection in sm['connections']:
            if connection['id'] == connection_id:
                return connection

        return None

    def get_decision_point(self, decision_point_id, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "decision_points" in sm['extensions']['ihmc_simasist'].keys():
           return None

        dps = sm['extensions']['ihmc_simasist']['decision_points']
        for dp in dps:
            if dp['id'] == decision_point_id:
                return dp

        return None

    def get_accessable_decision_points (self, from_decision_point, use_updated_map=True):
        if from_decision_point is None:
            return []
        accessable_dps = [from_decision_point]
        paths = self.get_paths_from(from_decision_point, use_updated_map)
        for path in paths:
            if 'obstacles' in path.keys():
                continue
            dp_to_id = path['loc_id_1'] if path['loc_id_1'] != from_decision_point['id'] \
                  else path['loc_id_2']
            dp = self.get_decision_point (dp_to_id, use_updated_map)
            if not dp is None and not dp in accessable_dps:
                accessable_dps.append(dp)

        return accessable_dps

    def get_closest_decision_point(self, x, z, from_decision_point_list=None, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "decision_points" in sm['extensions']['ihmc_simasist'].keys():
           return None

        areaId = None
        dist = 999999.99
        closest_dp = None

        if from_decision_point_list is None or len(from_decision_point_list) <= 0:
            # print("** Looking for closest DP using ALL dps!!!")
            dps = sm['extensions']['ihmc_simasist']['decision_points']
        else:
            dps = from_decision_point_list

            # see which location the point is in and do not choose a dp in another area if there is a from list.
            locs = self.get_locations_containing(x, z, use_updated_map=use_updated_map)
            for loc in locs:
                if not loc['name'].lower().startswith('part of '):
                    areaId = loc['id']
                    break
            # if no area id, use the first in the list provided
            if areaId is None:
                areaId = dps[0]['area_id']

        for dp in dps:
            # print('compute distance between (' + str(x) + ", " + str(z) + ') and ')
            # print (dp)

            this_dist = SemanticMap.compute_distance(x, z, dp['bounds']['coordinates'][0]['x'], dp['bounds']['coordinates'][0]['z'])
            if this_dist < dist and (areaId is None or areaId == dp['area_id']):
                dist = this_dist
                closest_dp = dp

        if closest_dp is None and not areaId is None and not from_decision_point_list is None:
            print('No Closest Point!! ' + areaId + ' for (' + str(x) + ', ' + str(z) + ') from ' + dps[0]['id'] + ' ' + dps[0]['area_id'] + ' trying ALL DPs')
            closest_dp, dist = self.get_closest_decision_point(x, z, from_decision_point_list=None, use_updated_map=use_updated_map)
            if closest_dp is None:
                print('2 No Closest Point!! ' + areaId + ' for (' + str(x) + ', ' + str(z) + ') from ' + dps[0]['id'] + ' ' + dps[0]['area_id'] + ' trying ALL DPs')
                for dp in dps:
                    this_dist = SemanticMap.compute_distance(x, z, dp['bounds']['coordinates'][0]['x'], dp['bounds']['coordinates'][0]['z'])
                    print('  : distance to (' + str(dp['bounds']['coordinates'][0]['x']) + ", " + str(dp['bounds']['coordinates'][0]['z']) + ') in ' + dp['id'] + ' [' + dp['area_id'] + '] is ' + str(this_dist))

        return closest_dp, dist

    def get_path_for_connection(self, con_id, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "paths" in sm['extensions']['ihmc_simasist'].keys():
           return []

        for path in sm['extensions']['ihmc_simasist']['paths']:
            if 'connection_id' in path.keys() and path['connection_id'] == con_id:
                return path

        return None

    def get_paths (self, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "paths" in sm['extensions']['ihmc_simasist'].keys():
           return []

        return sm['extensions']['ihmc_simasist']['paths']

    def get_path(self, path_id, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "paths" in sm['extensions']['ihmc_simasist'].keys():
           return None

        paths = sm['extensions']['ihmc_simasist']['paths']
        for path in paths:
            if path['id'] == path_id:
                return path

        return None


    def get_paths_from (self, decision_point, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "paths" in sm['extensions']['ihmc_simasist'].keys():
           return []

        connected_paths = []
        paths = sm['extensions']['ihmc_simasist']['paths']
        for path in paths:
            if path['loc_id_1'] == decision_point['id']:
                connected_paths.append(path)
            elif path['loc_id_2'] == decision_point['id']:
                if not 'bidirectional' in path.keys() or path['bidirectional']:
                    connected_paths.append(path)

        return connected_paths

    def get_path_between (self, decision_point_1, decision_point_2, use_updated_map=True):
        sm = self.updated_semantic_map if use_updated_map else self.semantic_map
        if not "extensions" in sm.keys() or \
           not "ihmc_simasist" in sm['extensions'].keys() or \
           not "paths" in sm['extensions']['ihmc_simasist'].keys():
           return None

        paths = sm['extensions']['ihmc_simasist']['paths']
        for path in paths:
            if path['loc_id_1'] == decision_point_1['id'] and path['loc_id_2'] == decision_point_2['id']: 
                return path
            elif path['loc_id_1'] == decision_point_2['id'] and path['loc_id_2'] == decision_point_1['id']:
                if not 'bidirectional' in path.keys() or path['bidirectional']:
                   return path

        return None


    # given a mission_victim_list in JSON format as specified by the Testbed Message,
    # add the victim objects to the update message and to the updated semantic map
    def add_victims(self, victims_list):
        victims = []
        if len(victims_list) <= 0:
            return

        vg = 0
        vy = 0

        for victim in victims_list:
            obj = {
                'id': 'victim',
                'type': 'victim',
                'bounds': {
                    'type': 'block',
                    'coordinates': [{'x': int(victim['x']), 'z': int(victim['z'])}]
                }
            }
            if victim['block_type'] == 'block_victim_1':
                vg = vg + 1
                obj['id'] = 'vg' + str(vg)
                obj['type'] = 'green_victim'
            else:
                vy = vy + 1
                obj['id'] = 'vy' + str(vy)
                obj['type'] = 'yellow_victim'
            victims.append(obj)

        if len(victims) > 0:
            if 'additions' not in self.updates.keys():
                self.updates['additions'] = {}
            if 'objects' not in self.updates['additions']:
                self.updates['additions']['objects'] = []

            # remove any numpy objects
            victims = json.loads(json.dumps(victims, cls=NpEncoder))

            self.updates['additions']['objects'].extend(victims)
            self.updated_semantic_map['objects'].extend(victims)

    # given a mission_blockage_list in JSON format as specified by the Testbed Message,
    # add any changes to the update message and to the updated semantic map
    def apply_blockages_list(self, blockages_list):
        compressed = self.compress_blockages(blockages_list)

        for blockage in (x for x in compressed if x['type'] == 'blockage'):
            intersectedLocations = []
            intersectedConnections = []
            if 'locations' in self.updated_semantic_map.keys():
                # Find all locations intersecting this blockage
                intersectedLocations = self.get_intersecting_locations(blockage['bounds'])
                intersectedConnections = self.get_intersecting_connections(blockage['bounds'])

            for location in intersectedLocations:
                # break up the location into smaller pieces
                bounds = self.breakup_bounds_with_bounds(location['bounds'], blockage['bounds'])
                # if there are no pieces, then delete the location!!
                if len(bounds) == 0:
                    self.delete_location(location)
                # if there is only one piece, update this location's bounds
                if len(bounds) == 1:
                    self.update_location_bounds(location, bounds[0])
                # if there is more than one, create locations for each and set this location as their parent
                elif len(bounds) > 1:
                    self.update_location_children(location, bounds)

            for connection in intersectedConnections:
                boundsList = self.breakup_bounds_with_bounds(connection['bounds'], blockage['bounds'])
                if len(boundsList) == 0:
                    self.delete_connection(connection)
                else:
                    c_id = self.generate_connection_id(boundsList[0])
                    # if there is only one bounds and it has the same id then nothing has changed.
                    if not (len(boundsList) == 1 and c_id == connection['id']):
                        self.delete_connection(connection)
                        for bounds in boundsList:
                            c_id = self.generate_connection_id(bounds)
                            connection = {'id': c_id,
                                        'type': 'opening',
                                        'bounds': bounds,
                                        'connected_locations': []
                                        }
                            if 'locations' in self.updated_semantic_map.keys():
                                # Find all locations touching this connection
                                connection['connected_locations'] = self.get_connected_bounds(bounds)

                            if 'additions' not in self.updates.keys():
                                self.updates['additions'] = {}
                            if 'connections' not in self.updates['additions']:
                                self.updates['additions']['connections'] = []

                            self.updates['additions']['connections'].append(connection)

                            self.updated_semantic_map['connections'].append(connection)

        for opening in (x for x in compressed if x['type'] == 'opening'):
            bounds = self.to_semantic_bounds(opening['bounds'])
            c_id = self.generate_connection_id(opening['bounds'])
            connection = {'id': c_id,
                            'type': 'opening',
                            'bounds': bounds,
                            'connected_locations': []
                            }
            if 'locations' in self.updated_semantic_map.keys():
                # Find all locations touching this connection
                connection['connected_locations'] = self.get_connected_bounds(opening['bounds'])

            if 'additions' not in self.updates.keys():
                self.updates['additions'] = {}
            if 'connections' not in self.updates['additions']:
                self.updates['additions']['connections'] = []

            self.updates['additions']['connections'].append(connection)

            self.updated_semantic_map['connections'].append(connection)

        # remove any numpy objects
        self.updates = json.loads(json.dumps(self.updates, cls=NpEncoder))
        self.updated_semantic_map = json.loads(json.dumps(self.updated_semantic_map, cls=NpEncoder))


    # look at the bounds and return true if the bounds intersect.
    @staticmethod
    def bounds_intersect(b1, b2):

        x_overlap = max(0, min(b1[0]+b1[2], b2[0]+b2[2]) - max(b1[0], b2[0]))
        z_overlap = max(0, min(b1[1]+b1[3], b2[1]+b2[3]) - max(b1[1], b2[1]))

        if x_overlap * z_overlap > 0:
            return True

        return False

    # look at the bounds and return true if the bounds intersect or if any edges are touching.
    # I do not consider bounds intersecting if it is just at the corners.
    @staticmethod
    def bounds_touching(b1, b2):
        x_overlap = max(0, min(b1[0]+b1[2], b2[0]+b2[2]) - max(b1[0], b2[0]))
        z_overlap = max(0, min(b1[1]+b1[3], b2[1]+b2[3]) - max(b1[1], b2[1]))

        if x_overlap * z_overlap > 0:
            return True

        # check for any touching on the x sides.
        if x_overlap > 0 and (b1[1] == b2[1] + b2[3] or b2[1] == b1[1] + b1[3]):
            return True

        # check for any touching on the z sides.
        if z_overlap > 0 and (b1[0] == b2[0] + b2[2] or b2[0] == b1[0] + b1[2]):
            return True

        return False

    @staticmethod
    def compute_bounds_touching(b1, b2):
        x_overlap = max(0, min(b1[0]+b1[2], b2[0]+b2[2]) - max(b1[0], b2[0]))
        z_overlap = max(0, min(b1[1]+b1[3], b2[1]+b2[3]) - max(b1[1], b2[1]))

        # ignore this for now.  This means they are intersecting not touching!!
        if x_overlap * z_overlap > 0:
            return None

        # check for any touching on the x sides.
        if x_overlap > 0:
            z = None
            if b1[1] == b2[1] + b2[3]:
                z = b1[1]
            elif b2[1] == b1[1] + b1[3]:
                z = b2[1]
            if z is not None:
                x = b2[0] if b2[0] > b1[0] else b1[0]
                return [x, z, x_overlap, 0]

        # check for any touching on the z sides.
        if z_overlap > 0:
            x = None
            if b1[0] == b2[0] + b2[2]:
                x = b1[0]
            elif b2[0] == b1[0] + b1[2]:
                x = b2[0]
            if x is not None:
                z = b2[1] if b2[1] > b1[1] else b1[1]
                return [x, z, 0, z_overlap]

        return None

    # This creates the smallest rectangle which includes the provided rectangles
    #
    # ** It does not create a polygon which is what it should do in the future!!!
    @staticmethod
    def merge_bounds(b1, b2):
        x1 = min(b1[0], b2[0])
        z1 = min(b1[1], b2[1])
        x2 = max(b1[0] + b1[2], b2[0] + b2[2])
        z2 = max(b1[1] + b1[3], b2[1] + b2[3])

        return [x1, z1, x2-x1, z2-z1]

    # go through the blockages and compute the bounds of the blockages/openings
    # by finding all blocks that are touching the bounds.
    #
    # ** For now this assumes that they are given in an order which is sequential
    @staticmethod
    def get_blockage_bounds(start_blockage, blockages):
        bounds = [start_blockage['x'], start_blockage['z'], 1, 1]

        for key in blockages:
            blockage = blockages[key]
            if blockage['processed'] or blockage['num_blocks'] < 2:
                continue

            bounds_2 = [blockage['x'], blockage['z'], 1, 1]
            if SemanticMap.bounds_touching(bounds, bounds_2):
                bounds = SemanticMap.merge_bounds(bounds, bounds_2)
                blockage['processed'] = True

        return bounds

    # Compress blockages and openings based on the number of blocks in a column and
    # the blocks which are touching/intersecting.
    @staticmethod
    def compress_blockages(blockages_and_openings):
        blockages = {}
        for blockage in blockages_and_openings:
            key = str(blockage['x']) + ',' + str(blockage['z'])
            if key not in blockages:
                blockages[key] = {'type': blockage['block_type'],
                                  'num_blocks': 0,
                                  'x': blockage['x'],
                                  'z': blockage['z'],
                                  'processed': False}
            blockages[key]['num_blocks'] = blockages[key]['num_blocks'] + 1

        compressed = []
        for key in blockages:
            blockage = blockages[key]
            if blockage['processed'] or blockage['num_blocks'] < 2:
                continue

            # get the blockage group which is all blocks which have not been
            # processed of the same type that are touching.
            blockage_bounds = SemanticMap.get_blockage_bounds(blockage, blockages)
            blockage['processed'] = True
            compressed.append({'type': 'opening' if blockage['type'] == 'air' else 'blockage',
                               'bounds': blockage_bounds})

        return compressed

    @staticmethod
    def get_bounds_center(semantic_bounds):
        coords = SemanticMap.from_semantic_bounds(semantic_bounds)
        pt = [0, 0]
        pt[0] = coords[0] + (coords[2] / 2)
        pt[1] = coords[1] + (coords[3] / 2)

        return pt

    @staticmethod
    def from_semantic_bounds(semantic_bounds):
        if semantic_bounds['type'] == 'rectangle' or semantic_bounds['type'] == 'line':
            coords = semantic_bounds['coordinates']
            return [coords[0]['x'], coords[0]['z'], coords[1]['x']-coords[0]['x'], coords[1]['z']-coords[0]['z']]
        if semantic_bounds['type'] == 'block':
            coords = semantic_bounds['coordinates']
            return [coords[0]['x'], coords[0]['z'], 1, 1]
        if semantic_bounds['type'] == 'point':
            coords = semantic_bounds['coordinates']
            return [coords[0]['x'], coords[0]['z'], 0, 0]

        return [0, 0, 0, 0]

    def get_intersecting_locations(self, bounds):
        intersecting_locations = []
        for location in self.updated_semantic_map['locations']:
            if 'bounds' not in location.keys():
                continue

            if SemanticMap.bounds_intersect(bounds, SemanticMap.from_semantic_bounds(location['bounds'])):
                intersecting_locations.append(location)

        return intersecting_locations

    def get_intersecting_connections(self, bounds):
        intersecting_connecitons = []
        for connection in self.updated_semantic_map['connections']:
            if 'bounds' not in connection.keys():
                continue

            if SemanticMap.bounds_intersect(bounds, SemanticMap.from_semantic_bounds(connection['bounds'])):
                intersecting_connecitons.append(connection)

        return intersecting_connecitons

    def get_connected_bounds(self, bounds):
        connected_locations = []
        for location in self.updated_semantic_map['locations']:
            if 'bounds' not in location.keys():
                continue

            if SemanticMap.bounds_touching(bounds, SemanticMap.from_semantic_bounds(location['bounds'])):
                connected_locations.append(location['id'])

        return connected_locations

    @staticmethod
    def to_semantic_bounds(bounds):
        bounds_type = 'rectangle' if bounds[2] != 0 and bounds[3] != 0 else 'line'
        semantic_bounds = {
            'type': bounds_type,
            'coordinates': [
                {'x': bounds[0], 'z': bounds[1]},
                {'x': bounds[0] + bounds[2], 'z': bounds[1] + bounds[3]}
            ]
        }

        return semantic_bounds

    # refactored from https://github.com/CodeVirtuoso/gridmancer/blob/master/gridmancer.js
    @staticmethod
    def compute_rectangles(grid):
        bounds = grid.shape

        building_mode_x = False
        grid_max_x = bounds[0]-1
        grid_max_y = bounds[1]-1
        rectangles = []
        tile_size = 1
        tiles_width = 0
        start_x = 0

        # Parse the logical grid, from left to right, bottom to top
        for y in range(0, bounds[1]):
            for x in range(0, bounds[0]):
                # When available field is found, if we're not currently building a rectangle, start one.
                # Add a horizontal tile to the current rectangle.
                if not grid[x, y]:
                    if not building_mode_x:
                        start_x = x
                        tiles_width = 0
                        building_mode_x = True
                    tiles_width += 1
                else:
                    # If we were building a rectangle horizontally, and just hit the wall,
                    # now try building it out vertically as much as we can.
                    if building_mode_x:
                        start_y = y
                        # current_x = start_x
                        current_y = start_y
                        tiles_height = 1
                        building_mode_x = False
                        building_mode_y = True
                        left_side_open = False
                        right_side_open = False

                        while building_mode_y:
                            current_y += 1
                            # Check if there's an available field on the left side
                            if start_x > 0 and current_y < grid_max_y:
                                if not grid[start_x - 1, current_y]:
                                    left_side_open = True

                            # Check if there's an available field on the right side
                            if start_x + tiles_width < grid_max_x and current_y < grid_max_y:
                                if not grid[start_x + tiles_width, current_y]:
                                    right_side_open = True

                            # Check if we've reached the crossroad
                            if left_side_open and right_side_open:
                                building_mode_y = False
                            else:
                                # If we're not at the crossroad, see if can we build
                                # up our rectangle for one more level
                                for current_x in range(start_x, start_x + tiles_width):
                                    if current_x >= grid_max_x or current_y >= grid_max_y or grid[current_x, current_y]:
                                        building_mode_y = False
                                if building_mode_y:
                                    tiles_height += 1

                        # Update our binary map, by marking fields of our new rectangle as taken
                        for takenY in range(start_y, start_y + tiles_height):
                            for takenX in range(start_x, start_x + tiles_width):
                                if takenX < grid_max_x and takenY < grid_max_y:
                                    grid[takenX, takenY] = True

                        rect = [[start_x * tile_size, start_y * tile_size],
                                [start_x * tile_size + tiles_width * tile_size, start_y * tile_size],
                                [start_x * tile_size + tiles_width * tile_size,
                                 start_y * tile_size + tiles_height * tile_size],
                                [start_x * tile_size, start_y * tile_size + tiles_height * tile_size],
                                [start_x * tile_size, start_y * tile_size]]

                        # add the rectangle
                        rectangles.append(np.asarray(rect))

        return rectangles

    @staticmethod
    def compute_contours(img):
        scale = 10
        img_scale = rescale(img, scale, order=0)
        thresh = threshold_mean(img_scale)
        img_scale = img_scale < thresh

        # skip 'open' contours
        contours = find_contours(img_scale, 0.5, fully_connected='high')

        if len(contours) <= 0 or (contours[0][0][0] != contours[0][-1][0] and contours[0][0][1] != contours[0][-1][1]):
            return []

        rectangles = SemanticMap.compute_rectangles(img_scale)
        for rect in rectangles:
            for point in rect:
                point[0] /= scale
                point[1] /= scale

        return rectangles

    @staticmethod
    def breakup_bounds_with_bounds(bounds1, bounds2):
        bounds = SemanticMap.from_semantic_bounds(bounds1)
        img = np.ones((bounds[2] + 2, bounds[3] + 2), np.int32)
        # fill the first bounds with 0's
        for x in range(1, bounds[2]+1):
            for y in range(1, bounds[3]+1):
                img[x, y] = 0

        # add the bounds used for breaking the first bounds up
        start_x = round(bounds2[0]-bounds[0])
        start_y = round(bounds2[1]-bounds[1])
        for x in range(1+start_x, start_x+round(bounds2[2])+1):
            for y in range(1+start_y, start_y+round(bounds2[3])+1):
                img[x, y] = 1

        lc = SemanticMap.compute_contours(img == 0)
        rects = []
        for rect in lc:
            bnds = [9999, 9999, -9999, -9999]
            for point in rect:
                point[0] += bounds[0] - 1
                point[1] += bounds[1] - 1
                bnds[0] = min(bnds[0], point[0])
                bnds[1] = min(bnds[1], point[1])
                bnds[2] = max(bnds[2], point[0])
                bnds[3] = max(bnds[3], point[1])
            bnds[2] = bnds[2] - bnds[0]
            bnds[3] = bnds[3] - bnds[1]
            rects.append(bnds)
        return rects

    def delete_connection(self, connection):
        if 'deletions' not in self.updates.keys():
            self.updates['deletions'] = {}
        if 'connections' not in self.updates['deletions'].keys():
            self.updates['deletions']['connections'] = []
            
        self.updates['deletions']['connections'].append(connection['id'])
        self.updated_semantic_map['connections'].remove(connection)

    def delete_location(self, location):
        if 'deletions' not in self.updates.keys():
            self.updates['deletions'] = {}

        if 'locations' not in self.updates['deletions'].keys():
            self.updates['deletions']['locations'] = []
        self.updates['deletions']['locations'].append(location['id'])

        # remove the location from the semantic map
        self.updated_semantic_map['locations'].remove(location)

        # now see if any connections need to be removed or modified
        connections_to_remove = []
        for connection in self.updated_semantic_map['connections']:
            if location['id'] in connection['connected_locations']:
                connection['connected_locations'].remove(location['id'])
                if len(connection['connected_locations']) < 2:
                    connections_to_remove.append(connection)
                    if 'connections' not in self.updates['deletions'].keys():
                        self.updates['deletions']['connections'] = []
                    self.updates['deletions']['connections'].append(connection['id'])
                else:
                    if 'modifications' not in self.updates.keys():
                        self.updates['modifications'] = {}
                    if 'connections' not in self.updates['modifications'].keys():
                        self.updates['modifications']['connections'] = []
                    self.updates['modifications']['connections'].append({
                        'id': connection['id'],
                        'connected_locations': connection['connected_locations']
                    })

        for connection in connections_to_remove:
            self.delete_connection(connection)

    def update_location_bounds(self, location, bounds):
        if 'modifications' not in self.updates.keys():
            self.updates['modifications'] = {}

        location['bounds'] = SemanticMap.to_semantic_bounds(bounds)
        if 'locations' not in self.updates['modifications'].keys():
            self.updates['modifications']['locations'] = []
        self.updates['modifications']['locations'].append({'id': location['id'], 'bounds': location['bounds']})

        # now see if any connections need to be removed or modified
        connections_to_remove = []
        for connection in self.updated_semantic_map['connections']:
            if location['id'] in connection['connected_locations']:
                conn_bounds = SemanticMap.from_semantic_bounds(connection['bounds'])
                if not SemanticMap.bounds_touching(bounds, conn_bounds):
                    connection['connected_locations'].remove(location['id'])
                    if len(connection['connected_locations']) < 2:
                        connections_to_remove.append(connection)
                        if 'deletions' not in self.updates.keys():
                            self.updates['deletions'] = {}
                        if 'connections' not in self.updates['deletions'].keys():
                            self.updates['deletions']['connections'] = []
                        self.updates['deletions']['connections'].append(connection['id'])
                    else:
                        if 'connections' not in self.updates['modifications'].keys():
                            self.updates['modifications']['connections'] = []
                        self.updates['modifications']['connections'].append({
                            'id': connection['id'],
                            'connected_locations': connection['connected_locations']
                        })

        for connection in connections_to_remove:
            self.updated_semantic_map['connections'].remove(connection)

    @staticmethod
    def create_connection_between(loc1, loc2):
        b1 = SemanticMap.from_semantic_bounds(loc1['bounds'])
        b2 = SemanticMap.from_semantic_bounds(loc2['bounds'])
        conn_bounds = SemanticMap.compute_bounds_touching(b1, b2)
        if conn_bounds is None:
            return None

        return {
            'id': SemanticMap.generate_connection_id(conn_bounds),
            'type': 'extension',
            'bounds': SemanticMap.to_semantic_bounds(conn_bounds),
            'connected_locations': [loc1['id'], loc2['id']],
        }

    def update_location_children(self, location, bounds_list):
        new_locations = []
        location['child_locations'] = []
        counter = 0
        # first create new locations for the bounds objects
        for bounds in bounds_list:
            counter = counter + 1
            loc_id = location['id'] + "_" + str(counter)
            location['child_locations'].append(loc_id)
            new_locations.append({'id': loc_id,
                                  'name': 'Part of ' + location['id'],
                                  'type': location['type'],
                                  'bounds': SemanticMap.to_semantic_bounds(bounds)})
        location.pop('bounds')

        if 'modifications' not in self.updates.keys():
            self.updates['modifications'] = {}
        if 'locations' not in self.updates['modifications'].keys():
            self.updates['modifications']['locations'] = []
        self.updates['modifications']['locations'].append({
            'id': location['id'],
            'bounds': None,
            'child_locations': location['child_locations']
        })
        if 'additions' not in self.updates.keys():
            self.updates['additions'] = {}
        if 'locations' not in self.updates['additions'].keys():
            self.updates['additions']['locations'] = []
        for child in new_locations:
            self.updated_semantic_map['locations'].append(child)
            self.updates['additions']['locations'].append(child)

        # now create any new connections between the locations
        for i in range(len(new_locations)):
            for j in range(i+1, len(new_locations)):
                connection = SemanticMap.create_connection_between(new_locations[i], new_locations[j])
                if connection is not None:
                    if 'connections' not in self.updates['additions'].keys():
                        self.updates['additions']['connections'] = []
                    self.updates['additions']['connections'].append(connection)
                    self.updated_semantic_map['connections'].append(connection)

        # now update any connections that were associated with the original location
        # now see if any connections need to be removed or modified
        connections_to_remove = []
        for connection in self.updated_semantic_map['connections']:
            if location['id'] in connection['connected_locations']:
                # remove the original location
                connection['connected_locations'].remove(location['id'])
                conn_bounds = SemanticMap.from_semantic_bounds(connection['bounds'])

                # add any child locations that are touching it
                for child in new_locations:
                    if SemanticMap.bounds_touching(SemanticMap.from_semantic_bounds(child['bounds']), conn_bounds):
                        connection['connected_locations'].append(child['id'])

                if len(connection['connected_locations']) < 2:
                    connections_to_remove.append(connection)
                    if 'deletions' not in self.updates.keys():
                        self.updates['deletions'] = {}
                    if 'connections' not in self.updates['deletions'].keys():
                        self.updates['deletions']['connections'] = []
                    self.updates['deletions']['connections'].append(connection['id'])
                else:
                    if 'connections' not in self.updates['modifications'].keys():
                        self.updates['modifications']['connections'] = []
                    self.updates['modifications']['connections'].append({
                        'id': connection['id'],
                        'connected_locations': connection['connected_locations']
                    })

        for connection in connections_to_remove:
            self.updated_semantic_map['connections'].remove(connection)

    @staticmethod
    def generate_connection_id(bounds):
        return 'c_' \
               + str(int(bounds[0]+2201)) + '_' \
               + str(int(bounds[1]-75)) + '_' \
               + str(int(bounds[0]+bounds[2]+2201)) + '_' \
               + str(int(bounds[1]+bounds[3]-75))

    @staticmethod
    def semantic_bounds_contains(bounds, x, z):
        if bounds['type'] == 'rectangle':
            if bounds['coordinates'][0]['x'] <= x <= bounds['coordinates'][1]['x'] and \
                    bounds['coordinates'][0]['z'] <= z <= bounds['coordinates'][1]['z']:
                return True
        elif bounds['type'] == 'block':
            if bounds['coordinates'][0]['x'] <= x <= bounds['coordinates'][0]['x']+1 and \
                    bounds['coordinates'][0]['z'] <= z <= bounds['coordinates'][0]['z']+1:
                return True
        elif bounds['type'] == 'line':
            if bounds['coordinates'][0]['x'] == bounds['coordinates'][1]['x'] and \
                    bounds['coordinates'][0]['x']-0.2 <= x <= bounds['coordinates'][1]['x']+0.2 and \
                    bounds['coordinates'][0]['z'] <= z <= bounds['coordinates'][1]['z']:
                return True
            elif bounds['coordinates'][0]['z'] == bounds['coordinates'][1]['z'] and \
                    bounds['coordinates'][0]['z']-0.2 <= z <= bounds['coordinates'][1]['z']+0.2 and \
                    bounds['coordinates'][0]['x'] <= x <= bounds['coordinates'][1]['x']:
                return True

        return False

    @staticmethod
    def get_object_parent(object_list, obj):
        for possible_parent in object_list:
            if 'child_locations' in possible_parent.keys() and obj['id'] in possible_parent['child_locations']:
                return possible_parent
        return None

    @staticmethod
    def get_containing(objects_list, x, z):
        objects = []

        # print('get objects containing: ' + str(x) + ', ' + str(z) + ' from:')
        # print(objects_list)

        for obj in objects_list:
            if 'bounds' in obj.keys() and SemanticMap.semantic_bounds_contains(obj['bounds'], x, z):
                parent = SemanticMap.get_object_parent(objects_list, obj)
                while parent is not None:
                    if parent not in objects:
                        objects.append(parent)
                    parent = SemanticMap.get_object_parent(objects_list, parent)
                if obj not in objects:
                    objects.append(obj)

        return objects

    def compute_distances(self):
        # get a list of all decision point id's
        dps = self.get_decision_point_id_list(False)

        if dps is None or len(dps) <= 0:
            return None, None, None
        
        graph = [[0 for i in range(len(dps))] for j in range(len(dps))]

        # now go through the paths and input the distances
        paths = self.get_paths(False)
        for path in paths:
            blocked = False
            if "obstacles" in path.keys():
                # there are obstacles, see if the path is blocked!!
                for obstacle in path['obstacles']:
                    if "amount" in obstacle.keys() and obstacle["amount"] > 0:
                        blocked = True
                        break
            if blocked:
                continue

            index_1 = dps.index(path['loc_id_1'])
            index_2 = dps.index(path['loc_id_2'])
            graph[index_1][index_2] = path['distance'] if 'distance' in path.keys() else 1
            if not 'bidirectional' in path.keys() or path['bidirectional']:
                graph[index_2][index_1] = graph[index_1][index_2]

        graph = csr_matrix(graph)
        distances, predecessors = shortest_path(csgraph=graph, return_predecessors=True)
        return dps, distances, predecessors

    def get_shortest_path(self, x1, z1, x2, z2):
        if self.dps is None:
            return None, None, None, None
        
        start_dp, start_dp_dist = self.get_closest_decision_point(x1, z1, use_updated_map=False)
        end_dp, end_dp_dist = self.get_closest_decision_point(x2, z2, use_updated_map=False)

        start_dp_index = self.dps.index(start_dp['id'])
        end_dp_index = self.dps.index(end_dp['id'])

        dist = self.distances[start_dp_index][end_dp_index]

        path_indices = [self.dps[end_dp_index]]

        next_index = end_dp_index
        while next_index != -9999 and next_index != start_dp_index:
            next_index = self.predecessors[start_dp_index][next_index]
            path_indices.insert(0, self.dps[next_index])

        if next_index == -9999:
            dist = -9999
            path_indices = []

        return dist, start_dp_dist, end_dp_dist, path_indices
