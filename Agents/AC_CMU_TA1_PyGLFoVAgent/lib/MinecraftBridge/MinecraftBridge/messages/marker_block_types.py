# -*- coding: utf-8 -*-
"""
.. module:: marker_block_types
   :platform: Linux, Windows, OSX
   :synopsis: Enumeration of Marker Blocks used by ASIST mod.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of Marker Block Types used by the ASIST mod.
"""

import enum

class MarkerBlockType(enum.Enum):
	"""
	Enumeration of the marker block types used in the ASIST mod of Minecraft.
	"""

	'''
	# Deprecated from study 2
	MarkerBlock1 = "Marker Block 1"
	MarkerBlock2 = "Marker Block 2"
	MarkerBlock3 = "Marker Block 3"
	MarkerBlock4 = "Marker Block 4"
	MarkerBlock5 = "Marker Block 5"
	MarkerBlock6 = "Marker Block 6"
	'''

	red_regularvictim = 'red_regularvictim'
	red_criticalvictim = 'red_criticalvictim'
	red_abrasion = 'red_abrasion'
	red_bonedamage = 'red_bonedamage'
	red_critical = 'red_critical'
	red_rubble = 'red_rubble'
	red_threat = 'red_threat'
	red_wildcard = 'red_wildcard'

	green_regularvictim = 'green_regularvictim'
	green_criticalvictim = 'green_criticalvictim'
	green_abrasion = 'green_abrasion'
	green_bonedamage = 'green_bonedamage'
	green_critical = 'green_critical'
	green_rubble = 'green_rubble'
	green_threat = 'green_threat'
	green_wildcard = 'green_wildcard'

	blue_regularvictim = 'blue_regularvictim'
	blue_criticalvictim = 'blue_criticalvictim'
	blue_abrasion = 'blue_abrasion'
	blue_bonedamage = 'blue_bonedamage'
	blue_critical = 'blue_critical'
	blue_rubble = 'blue_rubble'
	blue_threat = 'blue_threat'
	blue_wildcard = 'blue_wildcard'

	MarkerBlockred = 'red_wildcard'
	MarkerBlockgreen = 'green_wildcard'
	MarkerBlockblue = "blue_wildcard"