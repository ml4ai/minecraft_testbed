# -*- coding: utf-8 -*-
"""
.. module:: shapes
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of shapes in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of types of shapes used in Minecraft.  Shapes are block properties
for stairs in Minecraft, and can take on eof the following values::

    straight
    inner_left
    inner_right
    outer_left
    outer_right

Information about items is available at `Official Minecraft Stairs Wiki`_.

.. _Official Minecraft Stairs Wiki: https://minecraft.gamepedia.com/Stairs
"""


from enum import IntEnum, unique

@unique
class Shape(IntEnum):
	"""
    Enumeration of shapes available in Minecraft.  Shape values are attributes
    used by stairs.

    The Shape enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	outer_left = 0
	outer_right = 1
	inner_left = 2
	inner_right = 3
	straight = 4
