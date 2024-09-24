# -*- coding: utf-8 -*-
"""
.. module:: facing
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of facing properties in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of the facing property of blocks available in Minecraft.  

The actual values that can be used are dependent on the type of block 
described, but consist of one of the following::

	down
	up
	north
	northwest
	northeast
	north-northwest
	north-northeast
	south
	southwest
	southeast
	south-southwest
	south-southeast
	west
	west-northwest
	west-southwest
	east
	east-northeast
	east-southeast
	up_x
	up_z
	down_x
	down_z  Information

Information about block facing is available at `Official Minecraft Block State Wiki`_.

.. _Official Minecraft Block State Wiki: https://minecraft.gamepedia.com/Block_states
"""

from enum import IntEnum, unique

@unique
class Facing(IntEnum):
	"""
    Enumeration of facings available in Minecraft.

    The Facing enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	DOWN = 0
	UP = 1
	NORTH = 2
	SOUTH = 3
	WEST = 4
	EAST = 5
	UP_X = 6
	DOWN_X = 7
	UP_Z = 8
	DOWN_Z = 9
	SOUTH_SOUTHWEST = 10
	SOUTHWEST = 11
	WEST_SOUTHWEST = 12
	WEST_NORTHWEST = 13
	NORTHWEST = 14
	NORTH_NORTHWEST = 15
	NORTH_NORTHEAST = 16
	NORTHEAST = 17
	EAST_NORTHEAST = 18
	EAST_SOUTHEAST = 19
	SOUTHEAST = 20
	SOUTH_SOUTHEAST = 21
