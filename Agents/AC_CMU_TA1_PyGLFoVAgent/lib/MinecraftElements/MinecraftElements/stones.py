# -*- coding: utf-8 -*-
"""
.. module:: stones
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of stones in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of stone types available in Minecraft.  

The stone types available in Minecraft consist of the following::

    stone
    granite
    smooth_granite
    diorite
    smooth_diorite
    adensite
    smooth_adensite

Information about stone types is available at `Official Minecraft Stone Wiki`_.

.. _Official Minecraft Stone Wiki: https://minecraft.gamepedia.com/Stone
"""


from enum import IntEnum, unique

@unique
class Stone(IntEnum):
	"""
    Enumeration of stone types available in Minecraft.

    The Stone enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	stone = 0
	granite = 1
	smooth_granite = 2
	diorite = 3
	smooth_diorite = 4
	andesite = 5
	smooth_andesite = 6