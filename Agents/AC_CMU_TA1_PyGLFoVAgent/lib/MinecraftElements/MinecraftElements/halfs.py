# -*- coding: utf-8 -*-
"""
.. module:: halfs
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of colors in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of block half properties available in Minecraft.  

The half property for blocks can take on one of the following six values, which
are paired by complement::

	top / bottom
	head / foot
	upper / lower

Information about half properties is available at `Official Minecraft Block State Wiki`_.

.. _Official Minecraft Block State Wiki: https://minecraft.gamepedia.com/Block_states
"""


from enum import IntEnum, unique

@unique
class Half(IntEnum):
	"""
    Enumeration of halves available in Minecraft.  Half values are used as 
    attributes to specific block types (e.g., doors, beds).

    The Half enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	top = 0
	bottom = 1

	head = 2
	foot = 3

	upper = 4
	lower = 5
