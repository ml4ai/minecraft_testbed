# -*- coding: utf-8 -*-
"""
.. module:: woods
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of woods in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of wood types available in Minecraft.  

The wood types available in Minecraft consist of the following::

    oak
    spruce
    birch
    jungle
    acacia
    dark_oak

Information about wood types is available at `Official Minecraft Wood Wiki`_.

.. _Official Minecraft Wood Wiki: https://minecraft.gamepedia.com/Wood
"""


from enum import IntEnum, unique

@unique
class Wood(IntEnum):
	"""
    Enumeration of wood types available in Minecraft.

    The Wood enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	# Enumerated list of wood types in Minecraft / Malmo
	oak = 0
	spruce = 1
	birch = 2
	jungle = 3
	acacia = 4
	dark_oak = 5
