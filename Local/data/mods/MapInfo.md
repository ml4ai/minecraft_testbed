# Map Info

## Introduction

The Asist mod allows for a MapInfo.csv, placed in the server mods directory to define additional map features needed by the Asist mod. This includes the location of doorways for example.

## File Format

The MapInfo.csv file is a standard csv file containing a header row with 4 columns.

- LocationXYZ - the coordinates of the block in the world separated by spaces
- FeatureType - the name of the map feature being identified. For example, a doorway.
- FeatureSubType - an optional feature sub-type for holding more detailed information
- RoomName -The name of the room this feature is associated with

## Example file

``` csv
LocationXYZ,FeatureType,FeatureSubType,RoomName
-2087 60 152, doorway,,Security Office
-2082 60 152, doorway,,Open Break Area
-2081 60 152, doorway,,Open Break Area
-2080 60 152, doorway,,Open Break Area
-2079 60 152, doorway,,Open Break Area
-2075 60 152, doorway,,Executive Suite 1
```
