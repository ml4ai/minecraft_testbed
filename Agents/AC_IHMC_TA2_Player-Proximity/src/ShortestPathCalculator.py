import os
import numpy as np
import time
import threading
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
from ASISTTools import ASISTTools


class ShortestPathCalculator(object):

    def __init__(self, map_name, semantic_map, basemap):
        self.map_name = map_name
        self.semantic_map = semantic_map
        self.graph = None
        self.movementGrid = None
        self.pointIndicies = [[]]
        self.xRange = [99999, -99999]
        self.zRange = [99999, -99999]
        self.minX = self.xRange[0]
        self.minZ = self.zRange[0]
        self.width = 0
        self.height = 0
        self.set_basemap(basemap)
        if not self.load_dist_matrix():
            self.dist_matrix_map = None
            self.compute_dist_matrix()
        self.loc_connections_map = {}
        self.connection_centers = {}

    # Given two points p1[x,y] and p2[x,y], determine the shortest path in blocks from p1 to p2
    def shortest_dist(self, p1, p2):
        if self.dist_matrix_map is None:
            return None

        # use the grid to compute the distance.
        ip1 = self.pointIndicies[p1[0]-self.minX][p1[1]-self.minZ]
        ip2 = self.pointIndicies[p2[0]-self.minX][p2[1]-self.minZ]

        dist = self.dist_matrix_map[ip1][ip2] / 100.0
        if dist == np.Infinity or dist < 0:
            dist = None
        return dist

    # Return the shortest distance to the location's connections from the given point.
    def shortest_distance_to_location(self, p1, loc_id):
        if p1 is None or loc_id is None:
            return None
        if loc_id not in self.loc_connections_map.keys():
            self.loc_connections_map[loc_id] = self.semantic_map.get_connections_to_location(loc_id, use_updated_map=False)
        loc_connections = self.loc_connections_map[loc_id]
        shortest_dist = 99999
        for conn in loc_connections:
            dist = self.shortest_distance_to_connection(p1, conn)
            if dist is not None and dist < shortest_dist:
                shortest_dist = dist
        if shortest_dist >= 99999:
            return None
        return shortest_dist

    # Return the shortest distance to the connection from the given point.
    def shortest_distance_to_connection(self, p1, conn_id):
        shortest_dist = None
        if conn_id not in self.connection_centers.keys():
            connection = self.semantic_map.get_connection(conn_id, use_updated_map=False)
            if connection is None:
                self.connection_centers[conn_id] = [0, 0]
            else:
                conn_center = self.semantic_map.get_bounds_center(connection['bounds'])
                conn_center[0] = int(np.floor(conn_center[0]))
                conn_center[1] = int(np.floor(conn_center[1]))
                self.connection_centers[conn_id] = conn_center
        conn_center = self.connection_centers[conn_id]
        if conn_center[0] == 0 and conn_center[1] == 0:
            return shortest_dist
        return self.shortest_dist(p1, conn_center)

    def load_dist_matrix(self):
        if self.map_name is not None and os.path.exists(self.map_name + ".npz"):
            start_time = time.perf_counter()
            data = np.load(self.map_name + ".npz")
            if data is not None and 'dmm' in data.keys():
                self.dist_matrix_map = data['dmm']
                ASISTTools.get_logger().info("Finished loading dist_matrix_map in " + str(time.perf_counter() - start_time) + " seconds.")
                return True
            ASISTTools.get_logger().info("Failed loading dist_matrix_map in " + str(time.perf_counter() - start_time) + " seconds.")
        return False

    def compute_dist_matrix(self):
        # now compute the shortest path graphs for the movement grid
        # print('  - building the graph...')
        # graph = [[0 for i in range(self.width*self.height)] for j in range(self.width*self.height)]
        graph = np.zeros((self.width*self.height, self.width*self.height), dtype=np.uint8)
        # print('  - populating the graph...')
        for x in range(self.width):
            for z in range(self.height):
                pt1 = self.pointIndicies[x][z]
                # print('    checking [' + str(pt1) + '] (' + str(x) + ', ' + str(z) + ')')
                if self.movementGrid[x][z] != 0:
                    # print('    - Skipping it!!')
                    continue
                a = False
                b = False
                if x+1 < self.width and self.movementGrid[x+1][z] == 0:
                    # print('    - FOUND path to right : [' + str(self.pointIndicies[x+1][z]) + '] (' + str(x+1) + ', ' + str(z) + ')')
                    graph[pt1][self.pointIndicies[x+1][z]] = 100
                    # graph[self.pointIndicies[x+1][z]][pt1] = 100
                    a = True
                # else:
                #     print('    - no path to right : [' + str(self.pointIndicies[x+1][z]) + '] (' + str(x+1) + ', ' + str(z) + ')')

                if z+1 >= self.height:
                    # print ('    - last row so not checking down.')
                    continue
                if self.movementGrid[x][z+1] == 0:
                    # print('    - FOUND path down to : [' + str(self.pointIndicies[x][z+1]) + '] (' + str(x) + ', ' + str(z+1) + ')')
                    graph[pt1][self.pointIndicies[x][z+1]] = 100
                    # graph[self.pointIndicies[x][z+1]][pt1] = 100
                    b = True
                # else:
                #     print('    - no path down to : [' + str(self.pointIndicies[x][z+1]) + '] (' + str(x) + ', ' + str(z+1) + ')')

                # allow for diagonal movement when possible
                if (a or b) and self.movementGrid[x+1][z+1] == 0:
                    graph[pt1][self.pointIndicies[x+1][z+1]] = 130
                    # graph[self.pointIndicies[x+1][z+1]][pt1] = 130

        # print(graph)

        # print('  - Compressing the graph...')
        graph = csr_matrix(graph)
        self.graph = graph
        # print(graph)

        threading.Thread(target=self.repopulate_dist_matrix).start()

    def repopulate_dist_matrix(self):
        # pre-populate the distance matrices
        self.dist_matrix_map = None
        ASISTTools.get_logger().info("Pre populating Distance Matrices...")
        start_time = time.perf_counter()
        self.dist_matrix_map = shortest_path(csgraph=self.graph,
                                             directed=False,
                                             return_predecessors=False)
        ASISTTools.get_logger().info("Finished Pre populating Distance Matrices in: " + str(time.perf_counter() - start_time) + " seconds.")

        if self.map_name is not None:
            start_time = time.perf_counter()
            np.savez_compressed(self.map_name, dmm=self.dist_matrix_map)
            ASISTTools.get_logger().info("Finished saving Distance Matrices in: " + str(time.perf_counter() - start_time) + " seconds.")

    def update_min_max_range(self, x, z):
        if self.xRange[0] > x:
            self.xRange[0] = x
        elif self.xRange[1] < x:
            self.xRange[1] = x

        if self.zRange[0] > z:
            self.zRange[0] = z
        elif self.zRange[1] < z:
            self.zRange[1] = z

        self.minX = self.xRange[0]
        self.minZ = self.zRange[0]
        self.width = self.xRange[1] - self.xRange[0] + 1
        self.height = self.zRange[1] - self.zRange[0] + 1

    def set_basemap(self, basemap):
        self.xRange = [99999, -99999]
        self.zRange = [99999, -99999]

        walls = {}
        for data in basemap['data']:
            if data[1] in ['wall_sign', 'wall_banner', 'lever', 'water', 'flower_pot', 'barrier',
                           'tripwire_hook', 'redstone_torch', 'ladder', 'cake', 'brewing_stand'] or \
               data[1].endswith('_button') or data[1].endswith('_door') or \
               data[0][1] == 62:
                continue

            x = data[0][0]
            z = data[0][2]
            y = data[0][1]
            key = str(x) + ',' + str(z)
            if key not in walls.keys():
                walls[key] = [x, z, 0]
                self.update_min_max_range(x, z)
            walls[key][2] += y - 59        # 1 = block at height 1, 2 = block at height 2, 3 = block at height 1 and 2

        walls = list(walls.values())

        # setup the initial world grids based
        self.movementGrid = [[0 for i in range(self.height)] for j in range(self.width)]

        # use the semantic map to cut out areas which are not places the players can reach.
        if self.semantic_map is not None:
            for x in range(self.width):
                for z in range(self.height):
                    if len(self.semantic_map.get_locations_containing(x+self.minX, z+self.minZ, False)) == 0 and \
                       len(self.semantic_map.get_connections_containing(x+self.minX, z+self.minZ, False)) == 0:
                        self.movementGrid[x][z] = 3

        for wall in walls:
            if wall[0] < self.xRange[0] or wall[0] > self.xRange[1] or \
               wall[1] < self.zRange[0] or wall[1] > self.zRange[1]:
                continue
            self.movementGrid[wall[0]-self.minX][wall[1]-self.minZ] = 1          # cannot move here

        self.pointIndicies = [[0 for i in range(self.height)] for j in range(self.width)]
        cntr = 0
        for x in range(self.width):
            for z in range(self.height):
                self.pointIndicies[x][z] = cntr
                cntr = cntr + 1
