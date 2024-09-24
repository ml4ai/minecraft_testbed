"""
A list of helper functions to convert the nibble defining the data values for a
block to a dictionary with string keys mapping to cooresponding value types.
Where applicable, the data value type will be an enumerated MinecraftElement,
e.g., MinecraftElements.Facing.DOWN instead of "down".

The properties and data value nibble will be block specific.

This file also defines the dictionary "propertiesLibrary", which maps block
types (MinecraftElements.Block) to corresponding property functions.

The list of block propoerties and mapped type include:

    facing   - MinecraftElements.Facing
    half     - MinecraftElements.Half
    hinge    - MinecraftElements.Hinge
    shape    - MinecraftElements.Shape
    power    - integer [0 - 15]
    layers   - integer [0 - 7]
    attached - boolean
    enabled  - boolean
    powered  - boolean
    open     - boolean

References
    https://minecraft.gamepedia.com/Java_Edition_data_value
"""

import MinecraftElements


def getPropertiesNothing(nibble):
	"""
	Generate an empty dictionary of properties.  Useful for block types that
	have no useful properties (e.g., stone)

	Returns:
		Empty Property Dictionary
	"""

	return {}


def getPropertiesButton(nibble):
	"""
	Generate a dictionary for buttons.

	Returns:
		Property dictionary with following keys:
		facing
		powered
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.DOWN,
			   1: MinecraftElements.Facing.EAST,
			   2: MinecraftElements.Facing.WEST,
			   3: MinecraftElements.Facing.SOUTH,
			   4: MinecraftElements.Facing.NORTH,
			   5: MinecraftElements.Facing.UP 
			 }

	properties['facing'] = FACING[nibble & 0x07]
	properties['powered'] = True if (nibble & 0x08) != 0 else False

	return properties


def getPropertiesDoor(nibble):
	"""
	Generate a dictionary for doors.  The properties returned depend on whether
	the door is an upper or lower half.

	Returns:
		Property dictionary with a subset of the following keys:
		half
		facing
		open
		hinge
		powered
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.EAST,
			   1: MinecraftElements.Facing.SOUTH,
			   2: MinecraftElements.Facing.WEST,
			   3: MinecraftElements.Facing.NORTH,
			 }

	# The 0x08 bit indicates if it's an upper or lower part of the door
	# Note that properties are different for upper and lower doors
	properties['half'] = MinecraftElements.Half.upper if (nibble & 0x08) == 8 else MinecraftElements.Half.lower

	if properties['half'] == MinecraftElements.Half.lower:
		properties['facing'] = FACING[nibble & 0x03]
		properties['open'] = True if (nibble & 0x04) == 8 else False

	else:
		properties['hinge'] = [MinecraftElements.Hinge.left, MinecraftElements.Hinge.right][nibble & 0x01]
		properties['powered'] = True if (nibble & 0x02) == 4 else False

	return properties


def getPropertiesFence(nibble):
	"""
	Generate a dictionary for fences.  Currently, the function returns an empty
	dictionary, as the properties of the fence are based on neighboring blocks,
	not the block data nibble.

	Returns:
		Empty property dictionary.
	"""

	properties = {}

	return properties



def getPropertiesGate(nibble):
	"""
	Generate a dictionary for gates.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
		open
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.SOUTH,
			   1: MinecraftElements.Facing.WEST,
			   2: MinecraftElements.Facing.NORTH,
			   3: MinecraftElements.Facing.EAST,
			 }

	properties['facing'] = FACING[nibble & 0x03]
	properties['open'] = True if (nibble & 0x04) == 4 else False

	return properties


def getPropertiesStairs(nibble):
	"""
	Generate a dictionary for stairs.  The properties include an entry for 
	"shape" mapped to MinecraftElements.Shape.straight.  This value is actually
	based on the presence of surrounding stair blocks, and should be modified.
	Inclusion of the property is to ensure completeness.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
		half
		shape
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.EAST,
	           1: MinecraftElements.Facing.WEST,
	           2: MinecraftElements.Facing.SOUTH,
	           3: MinecraftElements.Facing.NORTH
	         }

	properties['facing'] = FACING[nibble & 0x03]
	properties['half'] = MinecraftElements.Half.top if (nibble & 0x04) == 4 else MinecraftElements.Half.bottom

	# For now, let the shape of the stairs be straight.  Need to change this
	# in post-processing
	properties['shape'] = MinecraftElements.Shape.straight

	return properties


def getPropertiesPressurePlate(nibble):
	"""
	Generate a dictionary for pressure plates.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		powered
	"""

	properties = {}

	properties["powered"] = True if (nibble & 0x01) == 1 else False

	return properties



def getPropertiesWeightedPressurePlate(nibble):
	"""
	Generate a dictionary for weighted pressure plates.  Weighted pressure
	plates are defined by a "power" property, which takes a value from 0 to 15.
	The properties included in this funciton include a "powered" property, to
	align its properties with pressure plates, and is true if the power
	property is non-zero.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		power
		powered
	"""

	properties = {}

	properties["power"] = nibble

	# This is added to be able to make a weighted pressure plate behave as a
	# pressur plate.
	properties["powered"] = properties["power"] > 0

	return properties


def getPropertiesSign(nibble):
	"""
	Generate a dictionary for signs.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.SOUTH,
	           1: MinecraftElements.Facing.SOUTH_SOUTHWEST,
	           2: MinecraftElements.Facing.SOUTHWEST,
	           3: MinecraftElements.Facing.WEST_SOUTHWEST,
	           4: MinecraftElements.Facing.WEST,
	           5: MinecraftElements.Facing.WEST_NORTHWEST,
	           6: MinecraftElements.Facing.NORTHWEST,
	           7: MinecraftElements.Facing.NORTH_NORTHWEST,
	           8: MinecraftElements.Facing.NORTH,
	           9: MinecraftElements.Facing.NORTH_NORTHEAST,
	           10: MinecraftElements.Facing.NORTHEAST,
	           11: MinecraftElements.Facing.EAST_NORTHEAST,
	           12: MinecraftElements.Facing.EAST,
	           13: MinecraftElements.Facing.EAST_SOUTHEAST,
	           14: MinecraftElements.Facing.SOUTHEAST,
	           15: MinecraftElements.Facing.SOUTH_SOUTHEAST
			 }

	properties["facing"] = FACING[nibble]

	return properties


def getPropertiesWallSign(nibble):
	"""
	Generate a dictionary for wall signs.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
	"""

	properties = {}

	FACING = { 2: MinecraftElements.Facing.NORTH,
			   3: MinecraftElements.Facing.SOUTH,
			   4: MinecraftElements.Facing.WEST,
			   5: MinecraftElements.Facing.EAST
			 }

	properties["facing"] = FACING[nibble & 0x07]

	return properties


def getPropertiesTrapdoor(nibble):
	"""
	Generate a dictionary for trap doors.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
		half
		open
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.SOUTH,
			   1: MinecraftElements.Facing.NORTH,
			   2: MinecraftElements.Facing.EAST,
			   3: MinecraftElements.Facing.WEST
			 }

	properties["facing"] = FACING[nibble & 0x03]
	properties["half"] = MinecraftElements.Half.top if (nibble & 0x04) == 4 else MinecraftElements.Half.bottom
	properties["open"] = (nibble & 0x08) == 8

	return properties


def getPropertiesSlab(nibble):
	"""
	Generate a dictionary for slabs.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		half
	"""

	properties = {}

	properties["half"] = MinecraftElements.Half.top if (nibble & 0x8) == 8 else MinecraftElements.Half.bottom

	return properties



def getPropertiesTorch(nibble):
	"""
	Generate a dictionary for torches.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
	"""

	properties = {}

	FACING = { 1: MinecraftElements.Facing.EAST,
			   2: MinecraftElements.Facing.WEST,
			   3: MinecraftElements.Facing.SOUTH,
			   4: MinecraftElements.Facing.NORTH,
			   5: MinecraftElements.Facing.UP
			 }

	properties["facing"] = FACING[nibble & 0x07]

	return properties


def getPropertiesSnowLayer(nibble):
	"""
	Generate a dictionary for snow.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		layers
	"""

	properties = {}

	properties["layers"] = nibble & 0x07

	return properties


def getPropertiesLadder(nibble):
	"""
	Generate a dictionary for ladders.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
	"""

	properties = {}

	FACING = { 2: MinecraftElements.Facing.NORTH,
			   3: MinecraftElements.Facing.SOUTH,
			   4: MinecraftElements.Facing.WEST,
			   5: MinecraftElements.Facing.EAST
	         }

	properties["facing"] = FACING[nibble & 0x07]

	return properties


def getPropertiesLever(nibble):
	"""
	Generate a dictionary for levers.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
		powered
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.DOWN_X,
			   1: MinecraftElements.Facing.EAST,
			   2: MinecraftElements.Facing.WEST,
			   3: MinecraftElements.Facing.SOUTH,
			   4: MinecraftElements.Facing.NORTH,
			   5: MinecraftElements.Facing.UP_Z,
			   6: MinecraftElements.Facing.UP_X,
			   7: MinecraftElements.Facing.DOWN_Z
		     }

	properties["facing"] = FACING[nibble & 0x07]
	properties["powered"] = True if (nibble & 0x08) == 8 else False

	return properties


def getPropertiesBars(nibble):
	"""
	Generate a dictionary for iron bars.  This function returns an empty
	dictionary, as the properties of bars are dependent on neighboring blocks.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Empty property dictionary
	"""

	properties = {}

	return properties


def getPropertiesGlassPane(nibble):
	"""
	Generate a dictionary for glass panes.  This function returns an empty
	dictionary, as the properties of glass paness are dependent on neighboring 
	blocks.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Empty property dictionary
	"""

	properties = {}

	return properties


def getPropertiesTripwireHook(nibble):
	"""
	Generate a dictionary for tripwire hooks.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
		attached
		powered
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.SOUTH,
	           1: MinecraftElements.Facing.WEST,
	           2: MinecraftElements.Facing.NORTH,
	           3: MinecraftElements.Facing.EAST
	         }

	properties["facing"] = FACING[nibble & 0x03]
	properties["attached"] = True if (nibble & 0x04) == 4 else False
	properties["powered"] = True if (nibble & 0x08) == 8 else False

	return properties



def getPropertiesWall(nibble):
	"""
	Generate a dictionary for walls.  This function returns an empty 
	dictionary, as the properties of walls are dependent on neighboring blocks.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Empty property dictionary
	"""

	properties = {}

	return properties


def getPropertiesAnvil(nibble):
	"""
	Generate a dictionary for anvils.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.WEST,
			   1: MinecraftElements.Facing.NORTH,
			   2: MinecraftElements.Facing.EAST,
			   3: MinecraftElements.Facing.SOUTH
	         }
	
	properties["facing"] = FACING[nibble&0x03]

	return properties


def getPropertiesHopper(nibble):
	"""
	Generate a dictionary for hoppers.

	Args:
		nibble - a nibble encoding the block properties.

	Returns:
		Property dictionary with following keys:
		facing
		enabled
	"""

	properties = {}

	FACING = { 0: MinecraftElements.Facing.DOWN,
			   2: MinecraftElements.Facing.NORTH,
			   3: MinecraftElements.Facing.SOUTH,
			   4: MinecraftElements.Facing.WEST,
			   5: MinecraftElements.Facing.EAST
	         }

	properties["enabled"] = True if (nibble&0x08) == 8 else False
	properties["facing"] = FACING[nibble&0x07]

	return properties

"""
NOT_YET_KNOWN is mapped to getPropertiesNothing, to serve as a placeholder
until blocks of certain types have corresponding property functions
implemented.
"""
NOT_YET_KNOWN = getPropertiesNothing

"""
propertiesLibrary maps a block type to a getProperties function
"""
propertiesLibrary = {
	MinecraftElements.Block.air: getPropertiesNothing,
	MinecraftElements.Block.stone: getPropertiesNothing,
	MinecraftElements.Block.grass: getPropertiesNothing,
	MinecraftElements.Block.dirt: getPropertiesNothing,
	MinecraftElements.Block.cobblestone: getPropertiesNothing,
	MinecraftElements.Block.planks: getPropertiesNothing,
	MinecraftElements.Block.sapling: NOT_YET_KNOWN,
	MinecraftElements.Block.bedrock: getPropertiesNothing,
	MinecraftElements.Block.flowing_water: NOT_YET_KNOWN,
	MinecraftElements.Block.water: getPropertiesNothing,
	MinecraftElements.Block.flowing_lava: NOT_YET_KNOWN,
	MinecraftElements.Block.lava: NOT_YET_KNOWN,
	MinecraftElements.Block.sand: getPropertiesNothing,
	MinecraftElements.Block.gravel: getPropertiesNothing,
	MinecraftElements.Block.gold_ore: getPropertiesNothing,
	MinecraftElements.Block.iron_ore: getPropertiesNothing,
	MinecraftElements.Block.coal_ore: getPropertiesNothing,
	MinecraftElements.Block.log: getPropertiesNothing,
	MinecraftElements.Block.leaves: getPropertiesNothing,
	MinecraftElements.Block.sponge: NOT_YET_KNOWN,
	MinecraftElements.Block.glass: getPropertiesNothing,
	MinecraftElements.Block.lapis_ore: getPropertiesNothing,
	MinecraftElements.Block.lapis_block: getPropertiesNothing,
	MinecraftElements.Block.dispenser: getPropertiesNothing,             
	MinecraftElements.Block.sandstone: getPropertiesNothing,
	MinecraftElements.Block.noteblock: NOT_YET_KNOWN,
	MinecraftElements.Block.bed: NOT_YET_KNOWN,
	MinecraftElements.Block.golden_rail: NOT_YET_KNOWN,
	MinecraftElements.Block.detector_rail: NOT_YET_KNOWN,
	MinecraftElements.Block.sticky_piston: NOT_YET_KNOWN,		
	MinecraftElements.Block.web: NOT_YET_KNOWN,
	MinecraftElements.Block.tallgrass: NOT_YET_KNOWN,
	MinecraftElements.Block.deadbush: NOT_YET_KNOWN,
	MinecraftElements.Block.piston: NOT_YET_KNOWN,
	MinecraftElements.Block.piston_head: NOT_YET_KNOWN,
	MinecraftElements.Block.wool: getPropertiesNothing,                      
	MinecraftElements.Block.piston_extension: NOT_YET_KNOWN,
	MinecraftElements.Block.yellow_flower: NOT_YET_KNOWN,
	MinecraftElements.Block.red_flower: NOT_YET_KNOWN,
	MinecraftElements.Block.brown_mushroom: NOT_YET_KNOWN,
	MinecraftElements.Block.red_mushroom: NOT_YET_KNOWN,
	MinecraftElements.Block.gold_block: getPropertiesNothing,
	MinecraftElements.Block.iron_block: getPropertiesNothing,                  
	MinecraftElements.Block.double_stone_slab: getPropertiesNothing,         
	MinecraftElements.Block.stone_slab: getPropertiesSlab,
	MinecraftElements.Block.brick_block: getPropertiesNothing,
	MinecraftElements.Block.tnt: getPropertiesNothing,
	MinecraftElements.Block.bookshelf: getPropertiesNothing,                 
	MinecraftElements.Block.mossy_cobblestone: getPropertiesNothing,
	MinecraftElements.Block.obsidian: getPropertiesNothing,
	MinecraftElements.Block.torch: getPropertiesTorch,
	MinecraftElements.Block.fire: getPropertiesNothing,
	MinecraftElements.Block.mob_spawner: NOT_YET_KNOWN,
	MinecraftElements.Block.oak_stairs: getPropertiesStairs,                   
	MinecraftElements.Block.chest: getPropertiesNothing,							
	MinecraftElements.Block.redstone_wire: NOT_YET_KNOWN,			
	MinecraftElements.Block.diamond_ore: getPropertiesNothing,
	MinecraftElements.Block.diamond_block: getPropertiesNothing,
	MinecraftElements.Block.crafting_table: getPropertiesNothing,            
	MinecraftElements.Block.wheat: NOT_YET_KNOWN,
	MinecraftElements.Block.farmland: NOT_YET_KNOWN,
	MinecraftElements.Block.furnace: getPropertiesNothing,
	MinecraftElements.Block.lit_furnace: getPropertiesNothing,
	MinecraftElements.Block.standing_sign: getPropertiesSign,        	
	MinecraftElements.Block.wooden_door: getPropertiesDoor,
	MinecraftElements.Block.ladder: getPropertiesLadder,                       
	MinecraftElements.Block.rail: NOT_YET_KNOWN,
	MinecraftElements.Block.stone_stairs: getPropertiesStairs,
	MinecraftElements.Block.wall_sign: getPropertiesWallSign,                 
	MinecraftElements.Block.lever: getPropertiesLever,
	MinecraftElements.Block.stone_pressure_plate: getPropertiesPressurePlate,
	MinecraftElements.Block.iron_door: getPropertiesDoor,
	MinecraftElements.Block.wooden_pressure_plate: getPropertiesPressurePlate,
	MinecraftElements.Block.redstone_ore: getPropertiesNothing,
	MinecraftElements.Block.lit_redstone_ore: getPropertiesNothing,
	MinecraftElements.Block.unlit_redstone_torch: getPropertiesTorch,   
	MinecraftElements.Block.redstone_torch: getPropertiesTorch,
	MinecraftElements.Block.stone_button: getPropertiesButton,
	MinecraftElements.Block.snow_layer: getPropertiesSnowLayer,
	MinecraftElements.Block.ice: getPropertiesNothing,
	MinecraftElements.Block.snow: getPropertiesNothing,
	MinecraftElements.Block.cactus: getPropertiesNothing,
	MinecraftElements.Block.clay: getPropertiesNothing,                 
	MinecraftElements.Block.reeds: NOT_YET_KNOWN,
	MinecraftElements.Block.jukebox: NOT_YET_KNOWN,
	MinecraftElements.Block.fence: getPropertiesFence,
	MinecraftElements.Block.pumpkin: getPropertiesNothing,
	MinecraftElements.Block.netherrack: getPropertiesNothing,
	MinecraftElements.Block.soul_sand: getPropertiesNothing,
	MinecraftElements.Block.glowstone: getPropertiesNothing,
	MinecraftElements.Block.portal: NOT_YET_KNOWN,
	MinecraftElements.Block.lit_pumpkin: getPropertiesNothing,
	MinecraftElements.Block.cake: NOT_YET_KNOWN,
	MinecraftElements.Block.unpowered_repeater: NOT_YET_KNOWN,
	MinecraftElements.Block.powered_repeater: NOT_YET_KNOWN,
	MinecraftElements.Block.stained_glass: getPropertiesNothing,
	MinecraftElements.Block.trapdoor: getPropertiesTrapdoor,
	MinecraftElements.Block.monster_egg: getPropertiesNothing,
	MinecraftElements.Block.stonebrick: getPropertiesNothing,
	MinecraftElements.Block.brown_mushroom_block: getPropertiesNothing,
	MinecraftElements.Block.red_mushroom_block: getPropertiesNothing,
	MinecraftElements.Block.iron_bars: getPropertiesBars,
	MinecraftElements.Block.glass_pane: getPropertiesGlassPane,
	MinecraftElements.Block.melon_block: getPropertiesNothing,
	MinecraftElements.Block.pumpkin_stem: NOT_YET_KNOWN,
	MinecraftElements.Block.melon_stem: NOT_YET_KNOWN,
	MinecraftElements.Block.vine: NOT_YET_KNOWN,
	MinecraftElements.Block.fence_gate: getPropertiesGate,
	MinecraftElements.Block.brick_stairs: getPropertiesStairs,
	MinecraftElements.Block.stone_brick_stairs: getPropertiesStairs,
	MinecraftElements.Block.mycelium: NOT_YET_KNOWN,
	MinecraftElements.Block.waterlily: NOT_YET_KNOWN,
	MinecraftElements.Block.nether_brick: getPropertiesNothing,
	MinecraftElements.Block.nether_brick_fence: getPropertiesFence,
	MinecraftElements.Block.nether_brick_stairs: getPropertiesStairs,
	MinecraftElements.Block.nether_wart: getPropertiesNothing,
	MinecraftElements.Block.enchanting_table: getPropertiesNothing,
	MinecraftElements.Block.brewing_stand: NOT_YET_KNOWN,
	MinecraftElements.Block.cauldron: getPropertiesNothing,
	MinecraftElements.Block.end_portal: NOT_YET_KNOWN,
	MinecraftElements.Block.end_portal_frame: getPropertiesNothing,
	MinecraftElements.Block.end_stone: NOT_YET_KNOWN,
	MinecraftElements.Block.dragon_egg: NOT_YET_KNOWN,
	MinecraftElements.Block.redstone_lamp: getPropertiesNothing,
	MinecraftElements.Block.lit_redstone_lamp: getPropertiesNothing,
	MinecraftElements.Block.double_wooden_slab: getPropertiesNothing,
	MinecraftElements.Block.wooden_slab: getPropertiesSlab,
	MinecraftElements.Block.cocoa: NOT_YET_KNOWN,
	MinecraftElements.Block.sandstone_stairs: getPropertiesStairs,
	MinecraftElements.Block.emerald_ore: getPropertiesNothing,
	MinecraftElements.Block.ender_chest: getPropertiesNothing,
	MinecraftElements.Block.tripwire_hook: getPropertiesTripwireHook,
	MinecraftElements.Block.tripwire: NOT_YET_KNOWN,
	MinecraftElements.Block.emerald_block: getPropertiesNothing,
	MinecraftElements.Block.spruce_stairs: getPropertiesStairs,
	MinecraftElements.Block.birch_stairs: getPropertiesStairs,
	MinecraftElements.Block.jungle_stairs: getPropertiesStairs,
	MinecraftElements.Block.command_block: getPropertiesNothing,
	MinecraftElements.Block.beacon: NOT_YET_KNOWN,
	MinecraftElements.Block.cobblestone_wall: getPropertiesWall,
	MinecraftElements.Block.flower_pot: getPropertiesNothing,
	MinecraftElements.Block.carrots: NOT_YET_KNOWN,
	MinecraftElements.Block.potatoes: NOT_YET_KNOWN,
	MinecraftElements.Block.wooden_button: getPropertiesButton,
	MinecraftElements.Block.skull: NOT_YET_KNOWN,
	MinecraftElements.Block.anvil: getPropertiesAnvil,
	MinecraftElements.Block.trapped_chest: getPropertiesNothing,
	MinecraftElements.Block.light_weighted_pressure_plate: getPropertiesWeightedPressurePlate,
	MinecraftElements.Block.heavy_weighted_pressure_plate: getPropertiesWeightedPressurePlate,
	MinecraftElements.Block.unpowered_comparator: NOT_YET_KNOWN,
	MinecraftElements.Block.powered_comparator: NOT_YET_KNOWN,
	MinecraftElements.Block.daylight_detector: NOT_YET_KNOWN,
	MinecraftElements.Block.redstone_block: getPropertiesNothing,
	MinecraftElements.Block.quartz_ore: getPropertiesNothing,
	MinecraftElements.Block.hopper: getPropertiesHopper,
	MinecraftElements.Block.quartz_block: getPropertiesNothing,
	MinecraftElements.Block.quartz_stairs: getPropertiesStairs,
	MinecraftElements.Block.activator_rail: NOT_YET_KNOWN,
	MinecraftElements.Block.dropper: getPropertiesNothing,
	MinecraftElements.Block.stained_hardened_clay: getPropertiesNothing,
	MinecraftElements.Block.stained_glass_pane: getPropertiesGlassPane,
	MinecraftElements.Block.leaves2: getPropertiesNothing,
	MinecraftElements.Block.log2: getPropertiesNothing,
	MinecraftElements.Block.acacia_stairs: getPropertiesStairs,
	MinecraftElements.Block.dark_oak_stairs: getPropertiesStairs,
	MinecraftElements.Block.slime: getPropertiesNothing,
	MinecraftElements.Block.barrier: NOT_YET_KNOWN,
	MinecraftElements.Block.iron_trapdoor: getPropertiesTrapdoor,
	MinecraftElements.Block.prismarine: getPropertiesNothing,
	MinecraftElements.Block.sea_lantern: NOT_YET_KNOWN,
	MinecraftElements.Block.hay_block: NOT_YET_KNOWN,
	MinecraftElements.Block.carpet: NOT_YET_KNOWN,
	MinecraftElements.Block.hardened_clay: getPropertiesNothing,
	MinecraftElements.Block.coal_block: getPropertiesNothing,
	MinecraftElements.Block.packed_ice: NOT_YET_KNOWN,
	MinecraftElements.Block.double_plant: NOT_YET_KNOWN,
	MinecraftElements.Block.standing_banner: NOT_YET_KNOWN,
	MinecraftElements.Block.wall_banner: NOT_YET_KNOWN,
	MinecraftElements.Block.daylight_detector_inverted: NOT_YET_KNOWN,
	MinecraftElements.Block.red_sandstone: getPropertiesNothing,
	MinecraftElements.Block.red_sandstone_stairs: getPropertiesStairs,
	MinecraftElements.Block.double_stone_slab2: getPropertiesNothing,
	MinecraftElements.Block.stone_slab2: getPropertiesSlab,
	MinecraftElements.Block.spruce_fence_gate: getPropertiesGate,
	MinecraftElements.Block.birch_fence_gate: getPropertiesGate,
	MinecraftElements.Block.jungle_fence_gate: getPropertiesGate,
	MinecraftElements.Block.dark_oak_fence_gate: getPropertiesGate,
	MinecraftElements.Block.acacia_fence_gate: getPropertiesGate,
	MinecraftElements.Block.spruce_fence: getPropertiesFence,
	MinecraftElements.Block.birch_fence: getPropertiesFence,
	MinecraftElements.Block.jungle_fence: getPropertiesFence,
	MinecraftElements.Block.dark_oak_fence: getPropertiesFence,
	MinecraftElements.Block.acacia_fence: getPropertiesFence,
	MinecraftElements.Block.spruce_door: getPropertiesDoor,
	MinecraftElements.Block.birch_door: getPropertiesDoor,
	MinecraftElements.Block.jungle_door: getPropertiesDoor,
	MinecraftElements.Block.acacia_door: getPropertiesDoor,
	MinecraftElements.Block.dark_oak_door: getPropertiesDoor,
	MinecraftElements.Block.end_rod: NOT_YET_KNOWN,
	MinecraftElements.Block.chorus_plant: NOT_YET_KNOWN,
	MinecraftElements.Block.chorus_flower: NOT_YET_KNOWN,
	MinecraftElements.Block.purpur_block: NOT_YET_KNOWN,
	MinecraftElements.Block.purpur_pillar: NOT_YET_KNOWN,
	MinecraftElements.Block.purpur_stairs: getPropertiesStairs,
	MinecraftElements.Block.purpur_double_slab: getPropertiesNothing,
	MinecraftElements.Block.purpur_slab: getPropertiesSlab,
	MinecraftElements.Block.end_bricks: NOT_YET_KNOWN,
	MinecraftElements.Block.beetroots: NOT_YET_KNOWN,
	MinecraftElements.Block.grass_path: NOT_YET_KNOWN,
	MinecraftElements.Block.end_gateway: NOT_YET_KNOWN,
	MinecraftElements.Block.repeating_command_block: getPropertiesNothing,
	MinecraftElements.Block.chain_command_block: NOT_YET_KNOWN,
	MinecraftElements.Block.frosted_ice: NOT_YET_KNOWN,
	MinecraftElements.Block.magma: NOT_YET_KNOWN,
	MinecraftElements.Block.nether_wart_block: getPropertiesNothing,
	MinecraftElements.Block.red_nether_brick: getPropertiesNothing,
	MinecraftElements.Block.bone_block: getPropertiesNothing,
	MinecraftElements.Block.structure_void: NOT_YET_KNOWN,
	MinecraftElements.Block.observer: NOT_YET_KNOWN,
	MinecraftElements.Block.white_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.orange_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.magenta_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.light_blue_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.yellow_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.lime_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.pink_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.gray_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.silver_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.cyan_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.purple_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.blue_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.brown_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.green_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.red_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.black_shulker_box: NOT_YET_KNOWN,
	MinecraftElements.Block.white_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.orange_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.magenta_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.light_blue_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.yellow_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.lime_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.pink_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.gray_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.light_gray_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.cyan_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.purple_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.blue_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.brown_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.green_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.red_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.black_glazed_terracotta: NOT_YET_KNOWN,
	MinecraftElements.Block.concrete: NOT_YET_KNOWN,
	MinecraftElements.Block.concrete_powder: NOT_YET_KNOWN,
	MinecraftElements.Block.structure_block: NOT_YET_KNOWN,
}