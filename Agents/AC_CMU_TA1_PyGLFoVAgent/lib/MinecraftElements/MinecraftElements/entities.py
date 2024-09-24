# -*- coding: utf-8 -*-
"""
.. module:: entities
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of entities in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of the entities available in Minecraft.  Information
about individual entities is available at `Official Minecraft Entity Wiki`_.

.. _Official Minecraft Entity Wiki: https://minecraft.gamepedia.com/Entity
"""

from enum import IntEnum, unique

@unique
class Entity(IntEnum):
	"""
    Enumeration of entities available in Minecraft.

    The Entity enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.
	"""

	ElderGuardian = 0
	WitherSkeleton = 1
	Stray = 2
	Husk = 3
	ZombieVillager = 4
	SkeletonHorse = 5
	ZombieHorse = 6
	EvocationIllager = 7
	VindicationIllager = 8
	Vex = 9
	Creeper = 10
	Skeleton = 11
	Spider = 12
	Giant = 13
	Zombie = 14
	Slime = 15
	Ghast = 16
	PigZombie = 17
	Enderman = 18
	CaveSpider = 19
	Silverfish = 20
	Blaze = 21
	LavaSlime = 22
	EnderDragon = 23
	WitherBoss = 24
	Bat = 25
	Witch = 26
	Endermite = 27
	Guardian = 28
	Shulker = 29
	Donkey = 30
	Mule = 31
	Pig = 32
	Sheep = 33
	Cow = 34
	Chicken = 35
	Squid = 36
	Wolf = 37
	MushroomCow = 38
	SnowMan = 39
	Ozelot = 40
	VillagerGolem = 41
	Horse = 42
	Rabbit = 43
	PolarBear = 44
	Llama = 45
	Villager = 46
	