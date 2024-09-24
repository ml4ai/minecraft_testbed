# -*- coding: utf-8 -*-
"""
.. module:: monster_eggs
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of monster eggs in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of types of monster eggs available in Minecraft.  MonsterEgg types
match stone types, and can take one of the following values::

    cobblestone
    stone_brick
    mossy_brick
    cracked_brick
    chiseled_brick

Information about items is available at `Official Minecraft Monster Egg Wiki`_.

.. _Official Minecraft Monster Egg Wiki: https://minecraft.gamepedia.com/Infested_Block
"""


from enum import IntEnum, unique

@unique
class MonsterEgg(IntEnum):
	"""
    Enumeration of monster eggs available in Minecraft.  MonsterEggs are blocks
    that release a monster when destroyed.

    The MonsterEgg enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	cobblestone = 0
	stone_brick = 1
	mossy_brick = 2
	cracked_brick = 3
	chiseled_brick = 4