# -*- coding: utf-8 -*-
"""
.. module:: items
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of items in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of items available in Minecraft.  

Information about items is available at `Official Minecraft Item Wiki`_.

.. _Official Minecraft Item Wiki: https://minecraft.fandom.com/wiki/Item
"""

from enum import IntEnum, unique

@unique
class Item(IntEnum):
	"""
    Enumeration of items available in Minecraft.

    The Item enumeration extends IntEnum, so that individual elements can be
    treated as one would treat any other int.

	NOTE: Malmo lists two instances of 'bucket' in it's schema; only one
	      instance of 'bucket' is implemented in this enumeration.
	"""

	iron_shovel = 0
	iron_pickaxe = 1
	iron_axe = 2
	flint_and_steel = 3
	apple = 4
	bow = 5
	arrow = 6
	coal = 7
	diamond = 8
	iron_ingot = 9
	gold_ingot = 10
	iron_sword = 11
	wooden_sword = 12
	wooden_shovel = 13
	wooden_pickaxe = 14
	wooden_axe = 15
	stone_sword = 16
	stone_shovel = 17
	stone_pickaxe = 18
	stone_axe = 19
	diamond_sword = 20
	diamond_shovel = 21
	diamond_pickaxe = 22
	diamond_axe = 23
	stick = 24
	bowl = 25
	mushroom_stew = 26
	golden_sword = 27
	golden_shovel = 28
	golden_pickaxe = 29
	golden_axe = 30
	string = 31
	feather = 32
	gunpowder = 33
	wooden_hoe = 34
	stone_hoe = 35
	iron_hoe = 36
	diamond_hoe = 37
	golden_hoe = 38
	wheat_seeds = 39
	wheat = 40
	bread = 41
	leather_helmet = 42
	leather_chestplate = 43
	leather_leggings = 44
	leather_boots = 45
	chainmail_helmet = 46
	chainmail_chestplate = 47
	chainmail_leggings = 48
	chainmail_boots = 49
	iron_helmet = 50
	iron_chestplate = 51
	iron_leggings = 52
	iron_boots = 53
	diamond_helmet = 54
	diamond_chestplate = 55
	diamond_leggings = 56
	diamond_boots = 57
	golden_helmet = 58
	golden_chestplate = 59
	golden_leggings = 60
	golden_boots = 61
	flint = 62
	porkchop = 63
	cooked_porkchop = 64
	painting = 65
	golden_apple = 66
	sign = 67
	wooden_door = 68
	bucket = 69
	water_bucket = 70
	lava_bucket = 71
	minecart = 72
	saddle = 73
	iron_door = 74
	redstone = 75
	snowball = 76
	boat = 77
	leather = 78
	milk_bucket = 79
	brick = 80
	clay_ball = 81
	reeds = 82
	paper = 83
	book = 84
	slime_ball = 85
	chest_minecart = 86
	furnace_minecart = 87
	egg = 88
	compass = 89
	fishing_rod = 90
	clock = 91
	glowstone_dust = 92
	fish = 93
	cooked_fish = 94
	dye = 95
	bone = 96
	sugar = 97
	cake = 98
	bed = 99
	repeater = 100
	cookie = 101
	filled_map = 102
	shears = 103
	melon = 104
	pumpkin_seeds = 105
	melon_seeds = 106
	beef = 107
	cooked_beef = 108
	chicken = 109
	cooked_chicken = 110
	rotten_flesh = 111
	ender_pearl = 112
	blaze_rod = 113
	ghast_tear = 114
	gold_nugget = 115
	nether_wart = 116
	potion = 117
	glass_bottle = 118
	spider_eye = 119
	fermented_spider_eye = 120
	blaze_powder = 121
	magma_cream = 122
	brewing_stand = 123
	cauldron = 124
	ender_eye = 125
	speckled_melon = 126
	spawn_egg = 127
	experience_bottle = 128
	fire_charge = 129
	writable_book = 130
	written_book = 131
	emerald = 132
	item_frame = 133
	flower_pot = 134
	carrot = 135
	potato = 136
	baked_potato = 137
	poisonous_potato = 138
	map = 139
	golden_carrot = 140
	skull = 141
	carrot_on_a_stick = 142
	nether_star = 143
	pumpkin_pie = 144
	fireworks = 145
	firework_charge = 146
	enchanted_book = 147
	comparator = 148
	netherbrick = 149
	quartz = 150
	tnt_minecart = 151
	hopper_minecart = 152
	prismarine_shard = 153
	prismarine_crystals = 154
	rabbit = 155
	cooked_rabbit = 156
	rabbit_stew = 157
	rabbit_foot = 158
	rabbit_hide = 159
	armor_stand = 160
	iron_horse_armor = 161
	golden_horse_armor = 162
	diamond_horse_armor = 163
	lead = 164
	name_tag = 165
	command_block_minecart = 166
	mutton = 167
	cooked_mutton = 168
	banner = 169
	spruce_door = 170
	birch_door = 171
	jungle_door = 172
	acacia_door = 173
	dark_oak_door = 174
	chorus_fruit = 175
	chorus_fruit_popped = 176
	beetroot = 177
	beetroot_seeds = 178
	beetroot_soup = 179
	dragon_breath = 180
	splash_potion = 181
	spectral_arrow = 182
	tipped_arrow = 183
	lingering_potion = 184
	shield = 185
	elytra = 186
	spruce_boat = 187
	birch_boat = 188
	jungle_boat = 189
	acacia_boat = 190
	dark_oak_boat = 191
	totem_of_undying = 192
	shulker_shell = 193
	iron_nugget = 194
	record_13 = 195
	record_cat = 196
	record_blocks = 197
	record_chirp = 198
	record_far = 199
	record_mall = 200
	record_mellohi = 201
	record_stal = 202
	record_strad = 203
	record_ward = 204
	record_11 = 205
	record_wait = 206
	