# -*- coding: utf-8 -*-
"""
.. module:: colors
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of colors in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of the colors available in Minecraft.  The colors in
Minecraft consist of the following::
    
    white
    orange
    magenta
    light_blue
    yellow
    lime
    pink
    gray
    silver
    cyan
    purple
    blue
    brown
    green
    red
    black

Information about individual colors is available at `Official Minecraft Dye Wiki`_.

.. _Official Minecraft Dye Wiki: https://minecraft.gamepedia.com/Dye#Colors
"""


from enum import IntEnum, unique



@unique
class Color(IntEnum):
    """
    Enumeration of colors available in Minecraft.

    The Color enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
    """
    UNKNOWN = 0
    WHITE = 1
    ORANGE = 2
    MAGENTA = 3
    LIGHT_BLUE = 4
    YELLOW = 5
    LIME = 6
    PINK = 7
    GRAY = 8
    SILVER = 9
    CYAN = 10
    PURPLE = 11
    BLUE = 12
    BROWN = 13
    GREEN = 14
    RED = 15
    BLACK = 16
