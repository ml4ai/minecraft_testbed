# -*- coding: utf-8 -*-
"""
.. module:: flowers
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of flowers in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of flower types available in Minecraft.  

The flower types available in Minecraft consist of the following::

	dandelion
	poppy
	blue_orchid
	allium
	houstonia
	red_tulip
	orange_tulip
	white_tulip
	pink_tulip
	oxeye_daisy


Information about flowers is available at `Official Minecraft Flower Wiki`_.

.. _Official Minecraft Flower Wiki: https://minecraft.gamepedia.com/Flower
"""


from enum import IntEnum, unique

@unique
class Flower(IntEnum):
	"""
    Enumeration of flowers available in Minecraft.

    The Flower enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	dandelion = 0
	poppy = 1
	blue_orchid = 2
	allium = 3
	houstonia = 4
	red_tulip = 5
	orange_tulip = 6
	white_tulip = 7
	pink_tulip = 8
	oxeye_daisy = 9