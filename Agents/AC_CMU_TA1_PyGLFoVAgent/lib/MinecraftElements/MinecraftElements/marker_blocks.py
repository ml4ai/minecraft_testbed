# -*- coding: utf-8 -*-
"""
.. module:: marker_blocks
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of marker block types used in the asistmod

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of the marker block types available in the ASIST Mod
"""

from enum import IntEnum, unique
from .blocks import Block

@unique
class MarkerBlock(IntEnum):
    """
    Enumeration of marker block types in the ASIST Mod.

    The MarkerBlock enumeration extends IntEnum, so that individual elements 
    can be treated as one would treat any other int.
    """

    blue_novictim = Block.blue_novictim
    green_novictim = Block.green_novictim
    red_novictim = Block.red_novictim
 
    blue_sos = Block.blue_sos
    green_sos = Block.green_sos
    red_sos = Block.red_sos
  
    UNKNOWN = Block.UNKNOWN

    MarkerBlock1 = Block.MarkerBlock1
    MarkerBlock2 = Block.MarkerBlock2
    MarkerBlock3 = Block.MarkerBlock3
    MarkerBlock4 = Block.MarkerBlock4
    MarkerBlock5 = Block.MarkerBlock5
    MarkerBlock6 = Block.MarkerBlock6

    red_regularvictim = Block.red_regularvictim
    red_criticalvictim = Block.red_criticalvictim
    red_abrasion = Block.red_abrasion
    red_bonedamage = Block.red_bonedamage
    red_critical = Block.red_critical
    red_rubble = Block.red_rubble
    red_threat = Block.red_threat
    red_wildcard = Block.red_wildcard

    green_regularvictim = Block.green_regularvictim
    green_criticalvictim = Block.green_criticalvictim
    green_abrasion = Block.green_abrasion
    green_bonedamage = Block.green_bonedamage
    green_critical = Block.green_critical
    green_rubble = Block.green_rubble
    green_threat = Block.green_threat
    green_wildcard = Block.green_wildcard

    blue_regularvictim = Block.blue_regularvictim
    blue_criticalvictim = Block.blue_criticalvictim
    blue_abrasion = Block.blue_abrasion
    blue_bonedamage = Block.blue_bonedamage
    blue_critical = Block.blue_critical
    blue_rubble = Block.blue_rubble
    blue_threat = Block.blue_threat
    blue_wildcard = Block.blue_wildcard

    MarkerBlockred = Block.MarkerBlockred
    MarkerBlockblue = Block.MarkerBlockblue
    MarkerBlockgreen = Block.MarkerBlockgreen

    marker_block = Block.marker_block
    block_marker_1_red = Block.block_marker_1_red
    block_marker_2_red = Block.block_marker_2_red
    block_marker_3_red = Block.block_marker_3_red
    block_marker_4_red = Block.block_marker_4_red
    block_marker_5_red = Block.block_marker_5_red
    block_marker_6_red = Block.block_marker_6_red
    block_marker_1_green = Block.block_marker_1_green
    block_marker_2_green = Block.block_marker_2_green
    block_marker_3_green = Block.block_marker_3_green
    block_marker_4_green = Block.block_marker_4_green
    block_marker_5_green = Block.block_marker_5_green
    block_marker_6_green = Block.block_marker_6_green
    block_marker_1_blue = Block.block_marker_1_blue
    block_marker_2_blue = Block.block_marker_2_blue
    block_marker_3_blue = Block.block_marker_3_blue
    block_marker_4_blue = Block.block_marker_4_blue
    block_marker_5_blue = Block.block_marker_5_blue
    block_marker_6_blue = Block.block_marker_6_blue
 
    block_marker_blue_abrasion = Block.block_marker_blue_abrasion
    block_marker_blue_bonedamage = Block.block_marker_blue_bonedamage
    block_marker_blue_critical = Block.block_marker_blue_critical
    block_marker_blue_criticalvictim = Block.block_marker_blue_criticalvictim
    block_marker_blue_regularvictim = Block.block_marker_blue_regularvictim
    block_marker_blue_rubble = Block.block_marker_blue_rubble
    block_marker_blue_threat = Block.block_marker_blue_threat
    block_marker_blue_wildcard = Block.block_marker_blue_wildcard

    block_marker_green_abrasion = Block.block_marker_green_abrasion
    block_marker_green_bonedamage = Block.block_marker_green_bonedamage
    block_marker_green_critical = Block.block_marker_green_critical
    block_marker_green_criticalvictim = Block.block_marker_green_criticalvictim
    block_marker_green_regularvictim = Block.block_marker_green_regularvictim
    block_marker_green_rubble = Block.block_marker_green_rubble
    block_marker_green_threat = Block.block_marker_green_threat
    block_marker_green_wildcard = Block.block_marker_green_wildcard

    block_marker_red_abrasion = Block.block_marker_red_abrasion
    block_marker_red_bonedamage = Block.block_marker_red_bonedamage
    block_marker_red_critical = Block.block_marker_red_critical
    block_marker_red_criticalvictim = Block.block_marker_red_criticalvictim
    block_marker_red_regularvictim = Block.block_marker_red_regularvictim
    block_marker_red_rubble = Block.block_marker_red_rubble
    block_marker_red_threat = Block.block_marker_red_threat
    block_marker_red_wildcard = Block.block_marker_red_wildcard


    @staticmethod
    def victims():
        """
        Returns set of all marker blocks indicating victims.
        """
        return {
            MarkerBlock.red_regularvictim,
            MarkerBlock.red_criticalvictim,
            MarkerBlock.red_abrasion,
            MarkerBlock.red_bonedamage,
            MarkerBlock.red_critical,

            MarkerBlock.green_regularvictim,
            MarkerBlock.green_criticalvictim,
            MarkerBlock.green_abrasion,
            MarkerBlock.green_bonedamage,
            MarkerBlock.green_critical,

            MarkerBlock.blue_regularvictim,
            MarkerBlock.blue_criticalvictim,
            MarkerBlock.blue_abrasion,
            MarkerBlock.blue_bonedamage,
            MarkerBlock.blue_critical,

            MarkerBlock.block_marker_red_abrasion,
            MarkerBlock.block_marker_red_bonedamage,
            MarkerBlock.block_marker_red_critical,
            MarkerBlock.block_marker_red_criticalvictim,
            MarkerBlock.block_marker_red_regularvictim,

            MarkerBlock.block_marker_green_abrasion,
            MarkerBlock.block_marker_green_bonedamage,
            MarkerBlock.block_marker_green_critical,
            MarkerBlock.block_marker_green_criticalvictim,
            MarkerBlock.block_marker_green_regularvictim,

            MarkerBlock.block_marker_blue_abrasion,
            MarkerBlock.block_marker_blue_bonedamage,
            MarkerBlock.block_marker_blue_critical,
            MarkerBlock.block_marker_blue_criticalvictim,
            MarkerBlock.block_marker_blue_regularvictim,
        }


    @staticmethod
    def threats():
        """
        Returns set of all marker blocks indicating threat rooms.
        """
        return {
            MarkerBlock.red_threat,
            MarkerBlock.green_threat,
            MarkerBlock.blue_threat,
            MarkerBlock.block_marker_red_threat,
            MarkerBlock.block_marker_green_threat,
            MarkerBlock.block_marker_blue_threat,
        }
