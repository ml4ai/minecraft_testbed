Overview
========

The MinecraftElements module consists of a collection of enumerations of 
Minecraft elements.  Enumerations are defined for most types of element (e.g.,
blocks, items, etc.)

This module is primarily designed to be used as a helper for other projects, 
and defines little in terms of functionality.  However, by maintaining a single
module, any dependent code will essentially be using a global enumeration of 
elements.  In addition to the standard benefits of using enumerated values, this
should help ensure that modules can interface easily without having to map
enumerated (or worse, hardcoded) values of available Minecraft elements.


Enumeration Formats
-------------------

Enumerations are provided for the elements listed below.

* Blocks
* Colors
* Entities
* Facing
* Flowers
* Items
* Monster Eggs
* Stones
* Woods

The enumeration for each element type is listed in a python file with the
corresponding name.  Enumerations match the names for elements provided by 
Project Malmo in the Types schema (see `Malmo Types Schema`_).  Each file
contains a docstring with further details on the specific element.

Each enumeration extends Python's IntEnum, allowing enumerated elements to be 
treated as if they were integer values.  Additionally, enumerated values are
unique, so that there is a one-to-one mapping between enumerations and the 
corresponding values (i.e., no aliasing).

.. _Malmo Types Schema: https://github.com/microsoft/malmo/blob/master/Schemas/Types.xsd
