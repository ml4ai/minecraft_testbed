Usage
=====

`MinecraftElements` is intended to serve as a simple enumeration and namespace
for elements related to Minecraft (e.g., types of blocks).  The enumerations
use Python's `enum` module, allowing for flexible representation of elements
(i.e., as strings, objects, or integers)::

    import MinecraftElements

    someStoneBlock = MinecraftElements.Block.stone

Alternatively, specific (or all) components can be imported, if namespacing
won't be an issue::

    from MinecraftElements import *
    someStoneBlock = Block.stone

Enumerated values can also be instantiated using the string name of the element
through the use of the `__getitem__` method::

    from MinecraftElements import Block
    someStoneBlock = Block["stone"]

As the string names match those used in Malmo's `Types` schema, this should
simplify conversion between data collected from Malmo to an enumeration.

Finally, enumerations can be treated as integer objects.  This is useful for 
incorporating with certain types of data structures, e.g., numpy arrays::

    from MinecraftElements import Block
    import numpy as np

    blockArray = np.array([Block.stone, Block.air, Block.stone], dtype=np.uint8)

Note that all enumerated values are non-negative, and less than 236, allowing
for compatible representation using 8-bit unsigned bytes.