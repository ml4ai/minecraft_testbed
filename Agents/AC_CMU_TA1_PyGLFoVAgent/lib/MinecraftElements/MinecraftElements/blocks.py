# -*- coding: utf-8 -*-
"""
.. module:: blocks
   :platform: Linux, Windows, OSX
   :synopsis: Enumerations of block types in Minecraft

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Enumeration of the blocks available in Minecraft.  Enumerated names and values
are such that they match the namespace ID and numeric ID utilized by Minecraft.
Information about individual blocks is available in the 
`Official Minecraft Block Wiki`_.

Additional ASIST-related block types (e.g., block_victim_1, marker_block, etc.)
are also included.  While enumerations for Minecraft specific blocks correspond
to the numeric ID of the blocks used by Minecraft, the same does not hold true
for ASIST-related block types.  As such, any numeric ID below 256 should be
considered an original Minecraft block, while those with value 256 and above 
are ASIST-related blocks.

Finally, an `UNKNOWN` block type is also included.  This block type allows for
graceful handling of blocks whose string values are not currently part of the
Block enumeration

.. _Official Minecraft Block Wiki: https://minecraft.gamepedia.com/Block
"""

from enum import IntEnum, unique

@unique
class Block(IntEnum):
	"""
	Enumeration of block types available in Minecraft and ASIST-related blocks.

	The Block enumeration extends IntEnum, so that individual elements can be
	treated as one would treat any other int.  Additionally, Block enumerations
	are unique.
	"""

	air = 0
	stone = 1
	grass = 2
	dirt = 3
	cobblestone = 4
	planks = 5
	sapling = 6
	bedrock = 7
	flowing_water = 8
	water = 9
	flowing_lava = 10
	lava = 11
	sand = 12
	gravel = 13
	gold_ore = 14
	iron_ore = 15
	coal_ore = 16
	log = 17
	leaves = 18
	sponge = 19
	glass = 20
	lapis_ore = 21
	lapis_block = 22
	dispenser = 23
	sandstone = 24
	noteblock = 25
	bed = 26
	golden_rail = 27
	detector_rail = 28
	sticky_piston = 29
	web = 30
	tallgrass = 31
	deadbush = 32
	piston = 33
	piston_head = 34
	wool = 35
	piston_extension = 36
	yellow_flower = 37
	red_flower = 38
	brown_mushroom = 39
	red_mushroom = 40
	gold_block = 41
	iron_block = 42
	double_stone_slab = 43
	stone_slab = 44
	brick_block = 45
	tnt = 46
	bookshelf = 47
	mossy_cobblestone = 48
	obsidian = 49
	torch = 50
	fire = 51
	mob_spawner = 52
	oak_stairs = 53
	chest = 54
	redstone_wire = 55
	diamond_ore = 56
	diamond_block = 57
	crafting_table = 58
	wheat = 59
	farmland = 60
	furnace = 61
	lit_furnace = 62
	standing_sign = 63
	wooden_door = 64
	ladder = 65
	rail = 66
	stone_stairs = 67
	wall_sign = 68
	lever = 69
	stone_pressure_plate = 70
	iron_door = 71
	wooden_pressure_plate = 72
	redstone_ore = 73
	lit_redstone_ore = 74
	unlit_redstone_torch = 75
	redstone_torch = 76
	stone_button = 77
	snow_layer = 78
	ice = 79
	snow = 80
	cactus = 81
	clay = 82
	reeds = 83
	jukebox = 84
	fence = 85
	pumpkin = 86
	netherrack = 87
	soul_sand = 88
	glowstone = 89
	portal = 90
	lit_pumpkin = 91
	cake = 92
	unpowered_repeater = 93
	powered_repeater = 94
	stained_glass = 95
	trapdoor = 96
	monster_egg = 97
	stonebrick = 98
	brown_mushroom_block = 99
	red_mushroom_block = 100
	iron_bars = 101
	glass_pane = 102
	melon_block = 103
	pumpkin_stem = 104
	melon_stem = 105
	vine = 106
	fence_gate = 107
	brick_stairs = 108
	stone_brick_stairs = 109
	mycelium = 110
	waterlily = 111
	nether_brick = 112
	nether_brick_fence = 113
	nether_brick_stairs = 114
	nether_wart = 115
	enchanting_table = 116
	brewing_stand = 117
	cauldron = 118
	end_portal = 119
	end_portal_frame = 120
	end_stone = 121
	dragon_egg = 122
	redstone_lamp = 123
	lit_redstone_lamp = 124
	double_wooden_slab = 125
	wooden_slab = 126
	cocoa = 127
	sandstone_stairs = 128
	emerald_ore = 129
	ender_chest = 130
	tripwire_hook = 131
	tripwire = 132
	emerald_block = 133
	spruce_stairs = 134
	birch_stairs = 135
	jungle_stairs = 136
	command_block = 137
	beacon = 138
	cobblestone_wall = 139
	flower_pot = 140
	carrots = 141
	potatoes = 142
	wooden_button = 143
	skull = 144
	anvil = 145
	trapped_chest = 146
	light_weighted_pressure_plate = 147
	heavy_weighted_pressure_plate = 148
	unpowered_comparator = 149
	powered_comparator = 150
	daylight_detector = 151
	redstone_block = 152
	quartz_ore = 153
	hopper = 154
	quartz_block = 155
	quartz_stairs = 156
	activator_rail = 157
	dropper = 158
	stained_hardened_clay = 159
	stained_glass_pane = 160
	leaves2 = 161
	log2 = 162
	acacia_stairs = 163
	dark_oak_stairs = 164
	slime = 165
	barrier = 166
	iron_trapdoor = 167
	prismarine = 168
	sea_lantern = 169
	hay_block = 170
	carpet = 171
	hardened_clay = 172
	coal_block = 173
	packed_ice = 174
	double_plant = 175
	standing_banner = 176
	wall_banner = 177
	daylight_detector_inverted = 178
	red_sandstone = 179
	red_sandstone_stairs = 180
	double_stone_slab2 = 181
	stone_slab2 = 182
	spruce_fence_gate = 183
	birch_fence_gate = 184
	jungle_fence_gate = 185
	dark_oak_fence_gate = 186
	acacia_fence_gate = 187
	spruce_fence = 188
	birch_fence = 189
	jungle_fence = 190
	dark_oak_fence = 191
	acacia_fence = 192
	spruce_door = 193
	birch_door = 194
	jungle_door = 195
	acacia_door = 196
	dark_oak_door = 197
	end_rod = 198
	chorus_plant = 199
	chorus_flower = 200
	purpur_block = 201
	purpur_pillar = 202
	purpur_stairs = 203
	purpur_double_slab = 204
	purpur_slab = 205
	end_bricks = 206
	beetroots = 207
	grass_path = 208
	end_gateway = 209
	repeating_command_block = 210
	chain_command_block = 211
	frosted_ice = 212
	magma = 213
	nether_wart_block = 214
	red_nether_brick = 215
	bone_block = 216
	structure_void = 217
	observer = 218
	white_shulker_box = 219
	orange_shulker_box = 220
	magenta_shulker_box = 221
	light_blue_shulker_box = 222
	yellow_shulker_box = 223
	lime_shulker_box = 224
	pink_shulker_box = 225
	gray_shulker_box = 226
	silver_shulker_box = 227
	cyan_shulker_box = 228
	purple_shulker_box = 229
	blue_shulker_box = 230
	brown_shulker_box = 231
	green_shulker_box = 232
	red_shulker_box = 233
	black_shulker_box = 234
	white_glazed_terracotta = 235
	orange_glazed_terracotta = 236
	magenta_glazed_terracotta = 237
	light_blue_glazed_terracotta = 238
	yellow_glazed_terracotta = 239
	lime_glazed_terracotta = 240
	pink_glazed_terracotta = 241
	gray_glazed_terracotta = 242
	light_gray_glazed_terracotta = 243
	cyan_glazed_terracotta = 244
	purple_glazed_terracotta = 245
	blue_glazed_terracotta = 246
	brown_glazed_terracotta = 247
	green_glazed_terracotta = 248
	red_glazed_terracotta = 249
	black_glazed_terracotta = 250
	concrete = 251
	concrete_powder = 252
	structure_block = 255

	#### ASIST-Related blocks ###

	# Victim Blocks
	block_victim_1 = 256
	block_victim_1b = 257
	block_victim_2 = 258
	block_victim_saved = 259
	block_victim_expired = 260
	block_victim_proximity = 261
	block_victim_saved_a = 262
	block_victim_saved_b = 263
	block_victim_saved_c = 264

	# Marker Blocks
	marker_block = 265
	block_freeze_player = 266
	block_threat_sign = 267
	block_marker_1_red = 268
	block_marker_2_red = 269
	block_marker_3_red = 270
	block_marker_4_red = 271
	block_marker_5_red = 272
	block_marker_6_red = 273
	block_marker_1_green = 274
	block_marker_2_green = 275
	block_marker_3_green = 276
	block_marker_4_green = 277
	block_marker_5_green = 278
	block_marker_6_green = 279
	block_marker_1_blue = 280
	block_marker_2_blue = 281
	block_marker_3_blue = 282
	block_marker_4_blue = 283
	block_marker_5_blue = 284
	block_marker_6_blue = 285

	block_marker_blue_abrasion = 286
	block_marker_blue_bonedamage = 287
	block_marker_blue_critical = 288
	block_marker_blue_criticalvictim = 289
	block_marker_blue_regularvictim = 290
	block_marker_blue_rubble = 291
	block_marker_blue_threat = 292
	block_marker_blue_wildcard = 293

	block_marker_green_abrasion = 294
	block_marker_green_bonedamage = 295
	block_marker_green_critical = 296
	block_marker_green_criticalvictim = 297
	block_marker_green_regularvictim = 298
	block_marker_green_rubble = 299
	block_marker_green_threat = 300
	block_marker_green_wildcard = 301
	
	block_marker_red_abrasion = 302
	block_marker_red_bonedamage = 303
	block_marker_red_critical = 304
	block_marker_red_criticalvictim = 305
	block_marker_red_regularvictim = 306
	block_marker_red_rubble = 307
	block_marker_red_threat = 308
	block_marker_red_wildcard = 309

	# Role Blocks
	block_role_hs = 310
	block_role_med = 311
	block_role_ss = 312
	block_role_engineer = 313
	block_role_medic = 314
	block_role_transporter = 315

	# Miscellaneous Blocks
	perturbation_opening = 316
	player = 317
	UNKNOWN = 318

	blue_novictim = 319
	green_novictim = 320
	red_novictim = 321

	blue_sos = 322
	green_sos = 323
	red_sos = 324

	MarkerBlock1 = 325
	MarkerBlock2 = 326
	MarkerBlock3 = 327
	MarkerBlock4 = 328
	MarkerBlock5 = 329
	MarkerBlock6 = 330

	red_regularvictim = 331
	red_criticalvictim = 332
	red_abrasion = 333
	red_bonedamage = 334
	red_critical = 335
	red_rubble = 336
	red_threat = 337
	red_wildcard = 338

	green_regularvictim = 339
	green_criticalvictim = 340
	green_abrasion = 341
	green_bonedamage = 342
	green_critical = 343
	green_rubble = 344
	green_threat = 345
	green_wildcard = 346

	blue_regularvictim = 347
	blue_criticalvictim = 348
	blue_abrasion = 349
	blue_bonedamage = 350
	blue_critical = 351
	blue_rubble = 352
	blue_threat = 353
	blue_wildcard = 354

	MarkerBlockred = 355
	MarkerBlockblue = 356
	MarkerBlockgreen = 357

	# This block type is to indicate an *UNKNOWN* regular victim.  This is
	# needed for the FoV agent to be able to report blocks without leaking info
	# on the type of vicitm
	block_victim_regular = 358


	@staticmethod
	def victims():
		"""
		Returns set of all victim blocks.
		"""
		return {
			*Block.injured_victims(),
			*Block.triaged_victims(),
			Block.block_victim_expired,
		}


	@staticmethod
	def injured_victims():
		"""
		Returns set of all injured victim blocks.
		"""
		return {
			Block.block_victim_1,
			Block.block_victim_1b,
			Block.block_victim_2,
			Block.block_victim_proximity, # deprecated
			Block.block_victim_regular
		}


	@staticmethod
	def triaged_victims():
		"""
		Returns set of all triaged victim blocks.
		"""
		return {
			Block.block_victim_saved_a,
			Block.block_victim_saved_b,
			Block.block_victim_saved_c,
			Block.block_victim_saved, # deprecated
		}


	@staticmethod
	def markers():
		"""
		Returns set of all marker blocks.
		"""
		return {
			Block.marker_block,
			Block.block_freeze_player,
			Block.block_threat_sign,
			Block.block_marker_1_red,
			Block.block_marker_2_red,
			Block.block_marker_3_red,
			Block.block_marker_4_red,
			Block.block_marker_5_red,
			Block.block_marker_6_red,
			Block.block_marker_1_green,
			Block.block_marker_2_green,
			Block.block_marker_3_green,
			Block.block_marker_4_green,
			Block.block_marker_5_green,
			Block.block_marker_6_green,
			Block.block_marker_1_blue,
			Block.block_marker_2_blue,
			Block.block_marker_3_blue,
			Block.block_marker_4_blue,
			Block.block_marker_5_blue,
			Block.block_marker_6_blue,

			Block.block_marker_blue_abrasion,
			Block.block_marker_blue_bonedamage,
			Block.block_marker_blue_critical,
			Block.block_marker_blue_criticalvictim,
			Block.block_marker_blue_regularvictim,
			Block.block_marker_blue_rubble,
			Block.block_marker_blue_threat,
			Block.block_marker_blue_wildcard,

			Block.block_marker_green_abrasion,
			Block.block_marker_green_bonedamage,
			Block.block_marker_green_critical,
			Block.block_marker_green_criticalvictim,
			Block.block_marker_green_regularvictim,
			Block.block_marker_green_rubble,
			Block.block_marker_green_threat,
			Block.block_marker_green_wildcard,

			Block.block_marker_red_abrasion,
			Block.block_marker_red_bonedamage,
			Block.block_marker_red_critical,
			Block.block_marker_red_criticalvictim,
			Block.block_marker_red_regularvictim,
			Block.block_marker_red_rubble,
			Block.block_marker_red_threat,
			Block.block_marker_red_wildcard,

			Block.blue_novictim,
			Block.green_novictim,
			Block.red_novictim,

			Block.blue_sos,
			Block.green_sos,
			Block.red_sos,

			Block.MarkerBlock1,
			Block.MarkerBlock2,
			Block.MarkerBlock3,
			Block.MarkerBlock4,
			Block.MarkerBlock5,
			Block.MarkerBlock6,

			Block.red_regularvictim,
			Block.red_criticalvictim,
			Block.red_abrasion,
			Block.red_bonedamage,
			Block.red_critical,
			Block.red_rubble,
			Block.red_threat,
			Block.red_wildcard,

			Block.green_regularvictim,
			Block.green_criticalvictim,
			Block.green_abrasion,
			Block.green_bonedamage,
			Block.green_critical,
			Block.green_rubble,
			Block.green_threat,
			Block.green_wildcard,

			Block.blue_regularvictim,
			Block.blue_criticalvictim,
			Block.blue_abrasion,
			Block.blue_bonedamage,
			Block.blue_critical,
			Block.blue_rubble,
			Block.blue_threat,
			Block.blue_wildcard,

			Block.MarkerBlockred,
			Block.MarkerBlockblue,
			Block.MarkerBlockgreen,
		}


	@staticmethod
	def doors():
		"""
		Returns set of all door blocks.
		"""
		return {
			Block.wooden_door, 
			Block.iron_door, 
			Block.trapdoor,
			Block.iron_trapdoor, 
			Block.spruce_door, 
			Block.birch_door,
			Block.jungle_door, 
			Block.acacia_door, 
			Block.dark_oak_door,
      }	
