# Map Blocks

## Introduction

The Asist mod allows for a MapBlocks.csv, placed in the server mods directory to define a set of blocks to load into the map when the server is initially started.

## File Format

The MapBlocks.csv file is a standard csv file containing a header row with 6 columns.

- LocationXYZ - the coordinates of the block in the world separated by spaces
- BlockType - the minecraft internal name of the block
- Command - If the BlockType is "command_block", this is a single line minecraft command to run when the command block is triggered
- CommandOptions - Conditional, Unconditional, AlwaysActive, or NeedsRedstone. Separate multiple options with |
- RoomName -The name of the room this block is in. Required for victim blocks
- FeatureType - The type of map feature this block is associated with

## Example file

``` csv
LocationXYZ,BlockType,Command,CommandOptions,RoomName,FeatureType
-2125 52 175, stone,,,,
-2125 53 175, stone,,,,
-2124 52 175, grass,,,,
-2123 52 175, dirt,,,,
-2121 52 175, cobblestone,,,,
-2121 52 176, cobblestone,,,,
-2120 52 175, command_block,summon minecraft:zombie ~ ~2 ~,,,
-2118 52 175, command_block,summon minecraft:creeper ~ ~2 ~,,,
-2088 60 146, block_victim_1,,,Security Office,
```
