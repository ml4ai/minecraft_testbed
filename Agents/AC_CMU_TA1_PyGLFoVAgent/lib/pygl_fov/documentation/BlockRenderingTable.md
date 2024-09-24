# Block Rendering

Block are rendered according to the best estimate of their size (in meters) in Minecraft.
Several block types share a common rendering function.  For example, all unit blocks use
the 'renderUnitBlock' function.

The table below lists all block types identified in the Types.xsd schema in Malmo, the
size of the block, the transparency of the block type (e.g., air = transparent, stone = 
not transparent, glass pane = partially transparent), and the function used to render the
block.  Blocks without entries are not currently implemented.


| Block Type                    | Size (x) | Size (y) | Size (z) | Transparent | Rendering Function  | Facing | Half | Shape | Other   |
|-------------------------------|:--------:|:--------:|:--------:|:-----------:|---------------------|:------:|:----:|:-----:|:-------:|
| air                           | 1.0      | 1.0      | 1.0      | Yes         | renderNothing       |        |      |       |         |
| stone                         | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| grass                         | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| dirt                          | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| cobblestone                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| planks                        | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| sapling                       |          |          |          |             |                     |        |      |       |         |
| bedrock                       | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| flowing_water                 |          |          |          |             |                     |        |      |       |         |
| water                         |          |          |          | Partially   | renderWater         |        |      |       |         |
| flowing_lava                  |          |          |          |             |                     |        |      |       |         |
| lava                          |          |          |          |             |                     |        |      |       |         |
| sand                          | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| gravel                        | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| gold_ore                      | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| iron_ore                      | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| coal_ore                      | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| log                           | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| leaves                        |          |          |          |             | renderUnitBlock     |        |      |       |         |
| sponge                        |          |          |          |             |                     |        |      |       |         |
| glass                         |          |          |          | Yes         | renderUnitBlock     |        |      |       |         |
| lapis_ore                     | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| lapis_block                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| dispenser                     | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| sandstone                     | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| noteblock                     |          |          |          |             |                     |        |      |       |         |
| bed                           |          |          |          |             |                     |        |      |       |         |
| golden_rail                   |          |          |          |             |                     |        |      |       |         |
| detector_rail                 |          |          |          |             |                     |        |      |       |         |
| sticky_piston                 |          |          |          |             |                     |        |      |       |         |
| web                           |          |          |          |             |                     |        |      |       |         |
| tallgrass                     |          |          |          |             |                     |        |      |       |         |
| deadbush                      |          |          |          |             |                     |        |      |       |         |
| piston                        |          |          |          |             |                     |        |      |       |         |
| piston_head                   |          |          |          |             |                     |        |      |       |         |
| wool                          | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| piston_extension              |          |          |          |             |                     |        |      |       |         |
| yellow_flower                 |          |          |          |             |                     |        |      |       |         |
| red_flower                    |          |          |          |             |                     |        |      |       |         |
| brown_mushroom                |          |          |          |             |                     |        |      |       |         |
| red_mushroom                  |          |          |          |             |                     |        |      |       |         |
| gold_block                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| iron_block                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| double_stone_slab             | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| stone_slab                    |          |          |          |             | renderSlab          |        |  X   |       |         |
| brick_block                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| tnt                           | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| bookshelf                     | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| mossy_cobblestone             | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| obsidian                      | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| torch                         |          |          |          | No          | renderTorch         |   X    |      |       |         |
| fire                          |          |          |          | See Notes   | renderFire          |        |      |       |         |
| mob_spawner                   |          |          |          |             |                     |        |      |       |         |
| oak_stairs                    |          |          |          | No          | renderStairs        |   X    |  X   |   X   |         |
| chest                         | 0.9375   | 0.875    | 0.9375   | No          | renderChest         |        |      |       |         |
| redstone_wire                 |          |          |          |             |                     |        |      |       |         |
| diamond_ore                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| diamond_block                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| crafting_table                | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| wheat                         |          |          |          | No          |                     |        |      |       |         |
| farmland                      |          |          |          | No          |                     |        |      |       |         |
| furnace                       | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| lit_furnace                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| standing_sign                 |          |          |          | No          |                     |        |      |       |         |
| wooden_door                   |          |          |          | No          | renderDoor          |   X    |  X   |   X   | open    |
| ladder                        |          |          |          | No          | renderLadder        |   X    |      |       |         |
| rail                          |          |          |          | No          |                     |        |      |       |         |
| stone_stairs                  |          |          |          | No          | renderStairs        |   X    |  X   |   X   |         |
| wall_sign                     |          |          |          | No          | renderWallSign      |   X    |      |       |         |
| lever                         |          |          |          | No          | renderLever         |   X    |      |       |         |
| stone_pressure_plate          |          |          |          | No          | renderPressurePlate |        |      |       |         |
| iron_door                     |          |          |          | No          | renderDoor          |   X    |  X   |   X   | open    |
| wooden_pressure_plate         |          |          |          | No          | renderPressurePlate |        |      |       |         |
| redstone_ore                  | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| lit_redstone_ore              | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| unlit_redstone_torch          |          |          |          | No          | renderTorch         |   X    |      |       |         |
| redstone_torch                |          |          |          | No          | renderTorch         |   X    |      |       |         |
| stone_button                  |          |          |          | No          | renderButton        |   X    |      |       | powered |
| snow_layer                    |          |          |          | No          | renderSnowLayer     |        |      |       | layers  |
| ice                           | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| snow                          |          |          |          | No          | renderUnitBlock     |        |      |       |         |
| cactus                        |          |          |          | No          | renderCactus        |        |      |       |         |
| clay                          | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| reeds                         |          |          |          | No          |                     |        |      |       |         |
| jukebox                       |          |          |          | No          |                     |        |      |       |         |
| fence                         |          |          |          | No          | renderFence         |   X    |      |       |         |
| pumpkin                       | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| netherrack                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| soul_sand                     | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| glowstone                     | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| portal                        |          |          |          | No          |                     |        |      |       |         |
| lit_pumpkin                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| cake                          |          |          |          | No          |                     |        |      |       |         |
| unpowered_repeater            |          |          |          | No          |                     |        |      |       |         |
| powered_repeater              |          |          |          | No          |                     |        |      |       |         |
| stained_glass                 |          |          |          | Yes         | renderUnitBlock     |        |      |       |         |
| trapdoor                      |          |          |          | No          | renderTrapdoor      |   X    |  X   |       | opened  |
| monster_egg                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| stonebrick                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| brown_mushroom_block          | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| red_mushroom_block            | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| iron_bars                     |          |          |          | No          | renderBars          |   X    |      |       |         |
| glass_pane                    |          |          |          | Yes         | renderGlassPane     |        |      |       |         |
| melon_block                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| pumpkin_stem                  |          |          |          | No          |                     |        |      |       |         |
| melon_stem                    |          |          |          | No          |                     |        |      |       |         |
| vine                          |          |          |          | No          |                     |        |      |       |         |
| fence_gate                    |          |          |          | No          | renderFenceGate     |   X    |      |       | opened  |
| brick_stairs                  |          |          |          | No          | renderStairs        |   X    |  X   |   X   |         |
| stone_brick_stairs            |          |          |          | No          | renderStairs        |   X    |  X   |   X   |         |
| mycelium                      |          |          |          | No          |                     |        |      |       |         |
| waterlily                     |          |          |          | No          |                     |        |      |       |         |
| nether_brick                  | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| nether_brick_fence            |          |          |          | No          | renderFence         |   X    |      |       |         |
| nether_brick_stairs           |          |          |          | No          | renderStairs        |   X    |  X   |   X   |         |
| nether_wart                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock     |        |      |       |         |
| enchanting_table              |          |          |          | No          | renderEnchantingTable |     |      |       |         |
| brewing_stand                 |          |          |          | No          |                    |        |      |       |         |
| cauldron                      |          |          |          | No          | renderCauldron     |        |      |       |         |
| end_portal                    |          |          |          | No          |                    |        |      |       |         |
| end_portal_frame              |          |          |          | No          | renderEndPortalFrame |      |      |       |         |
| end_stone                     |          |          |          | No          |                    |        |      |       |         |
| dragon_egg                    |          |          |          | No          |                    |        |      |       |         |
| redstone_lamp                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| lit_redstone_lamp             | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| double_wooden_slab            | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| wooden_slab                   |          |          |          | No          | renderSlab         |        |  X   |       |         |
| cocoa                         |          |          |          | No          |                    |        |      |       |         |
| sandstone_stairs              |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| emerald_ore                   | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| ender_chest                   | 0.9375   | 0.875    | 0.9375   | No          | renderChest        |        |      |       |         |
| tripwire_hook                 |          |          |          | No          | renderTripwireHook |   X    |      |       |         |
| tripwire                      |          |          |          | No          |                    |        |      |       |         |
| emerald_block                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| spruce_stairs                 |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| birch_stairs                  |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| jungle_stairs                 |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| command_block                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| beacon                        |          |          |          | No          |                    |        |      |       |         |
| cobblestone_wall              |          |          |          | No          | renderWall         |        |      |       | N/S/E/W |
| flower_pot                    |          |          |          | No          | renderFlowerPot    |        |      |       |         |
| carrots                       |          |          |          | No          |                    |        |      |       |         |
| potatoes                      |          |          |          | No          |                    |        |      |       |         |
| wooden_button                 |          |          |          | No          | renderButton       |   X    |      |       | powered |
| skull                         |          |          |          | No          |                    |        |      |       |         |
| anvil                         |          |          |          | No          | renderAnvil        |   X    |      |       |         |
| trapped_chest                 | 0.9375   | 0.875    | 0.9375   | No          | renderChest        |        |      |       |         |
| light_weighted_pressure_plate |          |          |          | No          | renderPressurePlate|        |      |       |         |
| heavy_weighted_pressure_plate |          |          |          | No          | renderPressurePlate|        |      |       |         |
| unpowered_comparator          |          |          |          | No          |                    |        |      |       |         |
| powered_comparator            |          |          |          | No          |                    |        |      |       |         |
| daylight_detector             |          |          |          | No          |                    |        |      |       |         |
| redstone_block                | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| quartz_ore                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| hopper                        |          |          |          | No          | renderHopper       |   X    |      |       |         |
| quartz_block                  | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| quartz_stairs                 |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| activator_rail                |          |          |          | No          |                    |        |      |       |         |
| dropper                       | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| stained_hardened_clay         | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| stained_glass_pane            |          |          |          | No          | renderGlassPane    |        |      |       | N/S/E/W |
| leaves2                       | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| log2                          | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| acacia_stairs                 |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| dark_oak_stairs               |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| slime                         | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| barrier                       |          |          |          | No          |                    |        |      |       |         |
| iron_trapdoor                 |          |          |          | No          | renderTrapdoor     |   X    |  X   |       |         |
| prismarine                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| sea_lantern                   |          |          |          | No          |                    |        |      |       |         |
| hay_block                     |          |          |          | No          |                    |        |      |       |         |
| carpet                        |          |          |          | No          |                    |        |      |       |         |
| hardened_clay                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| coal_block                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| packed_ice                    |          |          |          | No          |                    |        |      |       |         |
| double_plant                  |          |          |          | No          |                    |        |      |       |         |
| standing_banner               |          |          |          | No          |                    |        |      |       |         |
| wall_banner                   |          |          |          | No          |                    |        |      |       |         |
| daylight_detector_inverted    |          |          |          | No          |                    |        |      |       |         |
| red_sandstone                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| red_sandstone_stairs          |          |          |          | No          | renderStairs       |   X    |  X   |  X    |         |
| double_stone_slab2            |          |          |          | No          | renderUnitBlock    |        |      |       |         |
| stone_slab2                   |          |          |          | No          | renderSlab         |        |  X   |       |         |
| spruce_fence_gate             |          |          |          | No          | renderFenceGate    |   X    |      |       | opened  |
| birch_fence_gate              |          |          |          | No          | renderFenceGate    |   X    |      |       | opened  |
| jungle_fence_gate             |          |          |          | No          | renderFenceGate    |   X    |      |       | opened  |
| dark_oak_fence_gate           |          |          |          | No          | renderFenceGate    |   X    |      |       | opened  |
| acacia_fence_gate             |          |          |          | No          | renderFenceGate    |   X    |      |       | opened  |
| spruce_fence                  |          |          |          | No          | renderFence        |        |      |       | N/S/E/W |
| birch_fence                   |          |          |          | No          | renderFence        |        |      |       | N/S/E/W |
| jungle_fence                  |          |          |          | No          | renderFence        |        |      |       | N/S/E/W |
| dark_oak_fence                |          |          |          | No          | renderFence        |        |      |       | N/S/E/W |
| acacia_fence                  |          |          |          | No          | renderFence        |        |      |       | N/S/E/W |
| spruce_door                   |          |          |          | No          | renderDoor         |   X    |  X   |       | opened, hinge |
| birch_door                    |          |          |          | No          | renderDoor         |   X    |  X   |       | opened, hinge |
| jungle_door                   |          |          |          | No          | renderDoor         |   X    |  X   |       | opened, hinge |
| acacia_door                   |          |          |          | No          | renderDoor         |   X    |  X   |       | opened, hinge |
| dark_oak_door                 |          |          |          | No          | renderDoor         |   X    |  X   |       | opened, hinge |
| end_rod                       |          |          |          | No          |                    |        |      |       |         |
| chorus_plant                  |          |          |          | No          |                    |        |      |       |         |
| chorus_flower                 |          |          |          | No          |                    |        |      |       |         |
| purpur_block                  | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| purpur_pillar                 | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| purpur_stairs                 |          |          |          | No          | renderStairs       |   X    |  X   |   X   |         |
| purpur_double_slab            | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| purpur_slab                   |          |          |          | No          | renderSlab         |   X    |  X   |   X   |         |
| end_bricks                    |          |          |          | No          |                    |        |      |       |         |
| beetroots                     |          |          |          | No          |                    |        |      |       |         |
| grass_path                    |          |          |          | No          |                    |        |      |       |         |
| end_gateway                   |          |          |          | No          |                    |        |      |       |         |
| repeating_command_block       | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| chain_command_block           |          |          |          | No          |                    |        |      |       |         |
| frosted_ice                   |          |          |          | No          |                    |        |      |       |         |
| magma                         |          |          |          | No          |                    |        |      |       |         |
| nether_wart_block             | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| red_nether_brick              | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| bone_block                    | 1.0      | 1.0      | 1.0      | No          | renderUnitBlock    |        |      |       |         |
| structure_void                |          |          |          | No          |                    |        |      |       |         |
| observer                      |          |          |          | No          |                    |        |      |       |         |
| white_shulker_box             |          |          |          | No          |                    |        |      |       |         |
| orange_shulker_box            |          |          |          | No          |                    |        |      |       |         |
| magenta_shulker_box           |          |          |          | No          |                    |        |      |       |         |
| light_blue_shulker_box        |          |          |          | No          |                    |        |      |       |         |
| yellow_shulker_box            |          |          |          | No          |                    |        |      |       |         |
| lime_shulker_box              |          |          |          | No          |                    |        |      |       |         |
| pink_shulker_box              |          |          |          | No          |                    |        |      |       |         |
| gray_shulker_box              |          |          |          | No          |                    |        |      |       |         |
| silver_shulker_box            |          |          |          | No          |                    |        |      |       |         |
| cyan_shulker_box              |          |          |          | No          |                    |        |      |       |         |
| purple_shulker_box            |          |          |          | No          |                    |        |      |       |         |
| blue_shulker_box              |          |          |          | No          |                    |        |      |       |         |
| brown_shulker_box             |          |          |          | No          |                    |        |      |       |         |
| green_shulker_box             |          |          |          | No          |                    |        |      |       |         |
| red_shulker_box               |          |          |          | No          |                    |        |      |       |         |
| black_shulker_box             |          |          |          | No          |                    |        |      |       |         |
| structure_block               |          |          |          | No          |                    |        |      |       |         |