"""
fov.py

Implements shadow casting, currently
with diamond walls. Used by BeliefUpdater in prob_map.py
to compute uncertainty maps and updates.

Modified original code from https://www.albertford.com/shadowcasting/.

CoDaS Lab, 6/11/21
"""

import math
from fractions import Fraction
from map_s3 import Map


MARKED_VISIBLE = 8  # must be above 5


class Quadrant:
    def __init__(self, cardinal, origin):
        self.north = 0
        self.east = 1
        self.south = 2
        self.west = 3

        self.cardinal = cardinal
        self.ox, self.oy = origin

    def transform(self, tile):
        row, col = tile
        # the row controls the naming of the directions
        if self.cardinal == self.north:
            return self.ox + col, self.oy - row
        if self.cardinal == self.south:
            return self.ox + col, self.oy + row
        if self.cardinal == self.east:
            return self.ox + row, self.oy + col
        if self.cardinal == self.west:
            return self.ox - row, self.oy + col


class Row:
    """
    EFFECTS: Controls the number of tiles in a "row,"
    not the direction of the row.
    The direction is controlled by quadrant.transform.
    """

    def __init__(self, depth, start_slope, end_slope):
        self.depth = depth
        self.start_slope = start_slope
        self.end_slope = end_slope

    def tiles(self):
        min_col = round_ties_up(self.depth * self.start_slope)
        max_col = round_ties_down(self.depth * self.end_slope)
        # DEBUG
        # print("Row.tile: min_col is {}; max_col is {}".format(min_col, max_col))
        for col in range(min_col, max_col + 1):
            yield (self.depth, col)

    def advance(self):
        # DEBUG
        # print("row advanced!")
        return Row(
            # FIXME: does this depth increment respect dimensions of topo_map?
            self.depth + 1,
            self.start_slope,
            self.end_slope)


def compute_fov(origin, yaw, topo_map, fov_map, square_walls=True):
    """
    INPUTS:
    origin: agent's location in (x,y): +x is increasing col; +y is decreasing row.
    yaw: degree (0 to 360) with following convention:
            0 degree = -y = increasing row = south.
            Increasing degree turns counter-clockwise in (x,y) coord.
    topo_map: the topography matrix, used to determine is_blocking,
            should include rubble and victims.
    fov_map: a copy of the topography matrix, updated to record seen tiles.
            Seen tiles include walls, etc.
    MODIFIES: fov_map
    OUTPUTS: updated fov_map.
    NOTEs:
    There are 3 coordinate systems:
        Minecraft (x,z), topograhy matrix (row,col), and topography matrix (x,y).
    Be careful to translate agent's location from Minecraft (x,z) to
        topograhy matrix (row,col), then to topography matrix (x,y).
    tile is in (row,col).
    """

    MIN_X = 0
    MAX_X = 138
    MIN_Y = 0
    MAX_Y = 74

    def is_blocking(x, y, topo_map):
        # x is col, y is row
        if x <= MIN_X or x >= MAX_X or y <= MIN_Y or y >= MAX_Y:
            return True
        if topo_map[y,x] == Map.OPEN_SPACE:
            return False
        else:
            return True

    def mark_visible(x, y, fov_map):
        # x is col, y is row
        if x >= MIN_X and x <= MAX_X and y >= MIN_Y and y <= MAX_Y:
            fov_map[y,x] = MARKED_VISIBLE

    def reveal(tile):
        x, y = quadrant.transform(tile)
        mark_visible(x, y, fov_map)

    def is_wall(tile):
        if tile is None:
            return False
        x, y = quadrant.transform(tile)
        return is_blocking(x, y, topo_map)

    def is_floor(tile):
        if tile is None:
            return False
        x, y = quadrant.transform(tile)
        return not is_blocking(x, y, topo_map)

    def scan(row, use_square_walls=False):
        prev_tile = None
        for ind, tile in enumerate(row.tiles()):
            if is_wall(tile) or is_symmetric(row, tile):
                reveal(tile)
            if use_square_walls and is_floor(tile) and ind == 0:
                # this is to deal with the "origin=(60,50) and yaw=335" see-through issue
                _row, _col = tile
                fake_prev_tile = (_row, _col - 1)
                if is_wall(fake_prev_tile):
                    row.start_slope = slope_start_for_square_wall(fake_prev_tile)
            if is_wall(prev_tile) and is_floor(tile):
                row.start_slope = slope_start_for_square_wall(tile) if use_square_walls \
                    else slope(tile)
            if is_floor(prev_tile) and is_wall(tile):
                next_row = row.advance()
                next_row.end_slope = slope_end_for_square_wall(tile) if use_square_walls \
                    else slope(tile)
                scan(next_row, use_square_walls=use_square_walls)
            prev_tile = tile
        if is_floor(prev_tile):
            scan(row.advance(), use_square_walls=use_square_walls)

    def angle_in_quadrant(a):
        if (a >= 315) or (a < 45):
            return 2  # south
        elif (a >= 45) and (a < 135):
            return 1  # east
        elif (a >= 135) and (a < 225):
            return 0  # north
        elif (a >= 225) and (a < 315):
            return 3  # west

    def slope_in_quadrant(a, quad):
        """
        OUTPUTS: slope (Fraction) of angle a in the quad
        """
        if (a < 0) or (a > 360):
            raise ValueError('Angle out of bound [0,360].')

        if quad == 0:  # north
            if a >= 180:
                theta = a - 180
                direction = -1
            else:
                theta = 180 - a
                direction = 1
        elif quad == 1:  # east
            if a >= 90:
                theta = a - 90
                direction = -1
            else:
                theta = 90 - a
                direction = 1
        elif quad == 2:  # south
            if a >= 315:
                theta = 360 - a
                direction = -1
            else:
                theta = a
                direction = 1
        elif quad == 3:  # west
            if a >= 270:
                theta = a - 270
                direction = 1
            else:
                theta = 270 - a
                direction = -1
        else:
            raise ValueError(f'Quad number not valid: {quad}')

        opp = math.tan(theta / 180 * math.pi)
        # DEBUG
        # print("Output of slope_in_quadrant", Fraction(direction*opp))
        return Fraction(direction * opp)

    def slope_quad_larger_bound(quad):
        """
        Returns the slope of the quad boundary at the larger angle
        """
        if not quad in [0, 1, 2, 3]:
            raise ValueError('Quadrant not in 0 (north), 1 (east), 2 (south), or 3 (west).')
        if quad == 0:
            return Fraction(-1)
        elif quad == 1:
            return Fraction(-1)
        elif quad == 2:
            return Fraction(1)
        elif quad == 3:
            return Fraction(1)

    def slope_quad_smaller_bound(quad):
        """
        Returns the slope of the quad boundary at the smaller angle
        """
        if quad not in {0, 1, 2, 3}:
            raise ValueError('Quadrant not in 0 (north), 1 (east), 2 (south), or 3 (west).')
        if quad == 0:
            return Fraction(1)
        elif quad == 1:
            return Fraction(1)
        elif quad == 2:
            return Fraction(-1)
        elif quad == 3:
            return Fraction(-1)

    def fov_slopes_quadrants(yaw, view_width=70.0):
        """
        OUTPUTS: 2 lists
        (1): list of quadrant indices (ints) involved, at most 2 quadrants,
             and must be adjacent quadrants
        (2): a list of [smaller_slopes, larger slopes] (list of Fractions)
             ordered by the list of quadrants
        NOTES:
        start_ is always associated with the smaller angle;
        final_ is always asscociated with the larget angle.
        """
        if (yaw < 0) or (yaw > 360):
            raise ValueError('Yaw out of bound [0,360].')
        if (view_width <= 0) or (view_width >= 90):
            raise ValueError('View width out of bound (0,90) degree.')

        half_width = view_width / 2.0

        if (yaw >= half_width) and (yaw < (360 - half_width)):
            start_angle = yaw - half_width
            final_angle = yaw + half_width
            start_quad = angle_in_quadrant(start_angle)
            final_quad = angle_in_quadrant(final_angle)
            # DEBUG
            # print("start quad {}, final quad {}".format(start_quad, final_quad))
            if start_quad == final_quad:
                start_slope = slope_in_quadrant(start_angle, start_quad)
                final_slope = slope_in_quadrant(final_angle, final_quad)
                slopes = [start_slope, final_slope]
                slopes.sort()
                return [start_quad], [slopes]
            else:
                start_slope1 = slope_in_quadrant(start_angle, start_quad)
                final_slope1 = slope_quad_larger_bound(start_quad)
                start_slope2 = slope_quad_smaller_bound(final_quad)
                final_slope2 = slope_in_quadrant(final_angle, final_quad)
                slopes1 = [start_slope1, final_slope1]
                slopes2 = [start_slope2, final_slope2]
                slopes1.sort()
                slopes2.sort()
                return [start_quad, final_quad], [slopes1, slopes2]
        else:
            quad = 2  # yaw and view_width completely in south
            if yaw >= (360 - half_width):
                start_angle = half_width - (360 - yaw)
                final_angle = yaw - half_width
            else:
                start_angle = yaw + half_width
                final_angle = 360 - (half_width - yaw)
            start_slope = slope_in_quadrant(start_angle, quad)
            final_slope = slope_in_quadrant(final_angle, quad)
            slopes = [start_slope, final_slope]
            slopes.sort()
            # DEBUG
            # print("slopes", slopes)
            return [quad], [slopes]

    mark_visible(*origin, fov_map)
    quads, slope_pairs = fov_slopes_quadrants(yaw, view_width=70.0)
    # DEBUG
    # print("quads:", quads)
    # print("list of slope pairs:", slope_pairs)
    for ind in range(len(quads)):
        quadrant = Quadrant(quads[ind], origin)
        # first_row = Row(1, Fraction(-1), Fraction(1))
        first_row = Row(1, slope_pairs[ind][0], slope_pairs[ind][1])
        scan(first_row, use_square_walls=square_walls)


def slope(tile):
    row_depth, col = tile
    return Fraction(2 * col - 1, 2 * row_depth)


def slope_start_for_square_wall(tile):
    # written for square walls
    row_depth, col = tile
    if col >= 0:
        # return Fraction(col + 1/2, row_depth - 1/2)
        return Fraction(2*col + 1, 2*row_depth - 1)
    else:
        return Fraction(2*col + 1, 2*row_depth + 1)


def slope_end_for_square_wall(tile):
    # written for square walls
    row_depth, col = tile
    if col <= 0:
        return Fraction(2*col - 1, 2*row_depth - 1)
    else:  # col > row_depth:
        return Fraction(2*col - 1, 2*row_depth + 1)


def is_symmetric(row, tile):
    # Equivalent to checking if col of tile is
    # inside range in row.
    # Unrelated to direction, just about Row.
    row_depth, col = tile
    return row.depth * row.start_slope <= col <= row.depth * row.end_slope


def round_ties_up(n):
    return math.floor(n + 0.5)


def round_ties_down(n):
    return math.ceil(n - 0.5)


def scan_iterative(row):
    rows = [row]
    while rows:
        row = rows.pop()
        prev_tile = None
        for tile in row.tiles():
            if compute_fov.is_wall(tile) or is_symmetric(row, tile):
                compute_fov.reveal(tile)
            if compute_fov.is_wall(prev_tile) and compute_fov.is_floor(tile):
                row.start_slope = slope(tile)
            if compute_fov.is_floor(prev_tile) and compute_fov.is_wall(tile):
                next_row = row.next()
                next_row.end_slope = slope(tile)
                rows.append(next_row)
            prev_tile = tile
        if compute_fov.is_floor(prev_tile):
            rows.append(row.next())
