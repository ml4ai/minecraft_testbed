# -*- coding: utf-8 -*-
"""
.. module:: hinge
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of hinge properties in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of block hinge properties available in Minecraft.  The hinge 
property is used by door blocks, and can take on one of the value of `left` 
or `right`.

Information about hinge properties is available at `Official Minecraft Block State Wiki`_.

.. _Official Minecraft Block State Wiki: https://minecraft.gamepedia.com/Block_states
"""

from enum import IntEnum, unique

@unique
class Hinge(IntEnum):
	"""
    Enumeration of hinging available in Minecraft.  Hinges are attributes of
    door blocks, and can take the value of 'left' or 'right'.

    The Hinge enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	left = 0
	right = 1
	