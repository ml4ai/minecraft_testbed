## Introduction
This is a simplified version of the Doll/MIT basemap code that just generates the basemap JSON file and no images and no extra folders/files.  It also adds the MineCraft 'data' parameter to each block that contains MineCraft metadata about each block.  For instance for levers it specifies which face the lever is on and if it is active or not. See the MineCraft wiki for info on what each bit in the data's integer value means for each block: 

* doors - https://minecraft.gamepedia.com/Door#Block_data 
* levers - https://minecraft.gamepedia.com/Lever#Block_data

It relies on mca files `./testbed/Local/CLEANMAPS/`. For each world, __Falcon/Sparky__ etc, it consumes region files and corresponding MIN/MAX coordinates to produce mission map in json format.

## Engineering Notes
The contents of the resulting JSON file are in the following format: 
#### JSON Description
```
{
  "doors": [
    [
      [
        -2028,
        61,
        151
      ],
      [
        -2028,
        60,
        151
      ],
      "wooden_door",
      9,
      0
    ],
    [
      [
        -2042,
        61,
        159
      ],
      [
        -2042,
        60,
        159
      ],
      [
        -2042,
        61,
        158
      ],
      [
        -2042,
        60,
        158
      ],
      "dark_oak_door",
      8,
      2,
      9,
      2
    ],
    ...
  ],
  "levers": [
    [
      [
        -2035,
        61,
        184
      ],
      "lever",
      2
    ],
    ...
  ],
  "data": [
    [
      [
        -2020,
        62,
        153
      ],
      "barrier",
      0
    ],
    [
      [
        -2073,
        61,
        151
      ],
      "stained_hardened_clay",
      4
    ],
    [
      [
        -2097,
        61,
        167
      ],
      "water",
      8
    ],
    ...
  ],
}
```
The first door example is a single door.  It contains the location of two MineCraft blocks which specify the top and bottom blocks of the door.  It then has the block_type followed by the data values for the first door block and then the second.  The second door example is a double door.  Again the location of each MineCraft block for the door is specified, one door then the other, then the block_type, and finally the data for each door block in the same order in which they are provided.  The levers and data blocks have a similar format with the location of the MineCraft block first, followed by the block_type, and finally the data value associated with the block.

Note: the doors and levers have been copied, and grouped in the case of doors, to the `doors` and `levers` lists, but still exist as individual blocks in the `data` list.

#### Ranges Format
The ranges for a map are now just the cube which bounds the area to be processed.  The code is able to look at the whole Minecraft world and just process the parts in the specified ranges.
```
    # rngs = (x_low, x_high, z_low, z_high, y_low, y_high)
    ranges = (-2240,  -2068,   -82,    130,    60,     62)
```

## Requirements
 * A python 3.7 or greater python environment.
 * A `requirement.txt` file is provided to initialize your python environment. 
 * An `asist_testbed` environment value is required for the code to run and should point to the location where the ASIST testbed is installed so that the MineCraft world files can be located. 

## Operation

### Native Host
Just call the python script with the name of the folder in Local/CLEAN_MAPS that you want to process

`./testbed_to_basemap.py Saturn_2.0_3D`

## Issues

Occasionally and on MacOS, if the command fails with `OSError: [Errno 24] Too many open files`, increase 
the limit with the command `ulimit -n 4096`. Note this sets the value for the current shell instance only.

## Questions, comments and feedback
Email: rcarff@ihmc.us or find me on Slack!
