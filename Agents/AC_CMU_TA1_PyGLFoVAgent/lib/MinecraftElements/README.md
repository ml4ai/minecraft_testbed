# MinecraftElements

The MinecraftElements module consists of a collection of enumerations of 
Minecraft elements.  Enumerations are defined for most types of element (e.g.,
blocks, items, etc.)

This module is primarily designed to be used as a helper for other projects, 
and defines little in terms of functionality.  However, by maintaining a single
module, any dependent code will essentially be using a global enumeration of 
elements.  In addition to the standard benefits of using enumerated values, this
should help ensure that modules can interface easily without having to map
enumerated (or worse, hardcoded) values of available Minecraft elements.


## Requirements

This package may be used with Python version 3.5 and later.


## Enumeration Formats

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
Project Malmo in the Types schema (see [Project Malmo Types Schema][malmo_types_schema]).  Each file
contains a docstring with further details on the specific element.

Each enumeration extends Python's IntEnum, allowing enumerated elements to be 
treated as if they were integer values.  Additionally, enumerated values are
unique, so that there is a one-to-one mapping between enumerations and the 
corresponding values (i.e., no aliasing).


## Installation

This module can be installed as a package using `pip`.  Assuming `pip` is
installed, the package can be installed (for users) from the root folder by

    pip install --user -e . 

Once installed, the module can be imported from arbitrary locations.


## Documentation
Documentation for this module can be built using [Sphinx][sphinx_documentation], which is also installed with [pip][pip_documentation].  The source and build files for the documentation is in the `docs` folder.


### Requirements

Note that build targets may require additional dependencies to be installed.  For building a PDF of the documentation using Latex, basic Latex dependencies need to be installed.  On Ubuntu-based systems, this can be done by installing the following packages using `aptitude`

    apt-get install texlive-latex-recommended
    texlive-latex-extra texlive-fonts-recommended


### Building Documentation

To build a PDF of the *MinecraftElements Manual*, from the `docs` folder, run the build command with the latexpdf target::

    cd docs
    make latexpdf

This will create a `build` subfolder, and `latex` subfolder within build.  The final pdf file, `MinecraftElements_Manual.pdf` will be written to the `latex` subfolder, which can be moved to the root directory easily.  In Linux or OSX, this is done with::

    mv build/latex/MinecraftElements_Manual.pdf ..

While in Windows, this would be done by::

    move build\latex\MinecraftElements_Manual.pdf ..


## Usage

`MinecraftElements` is intended to serve as a simple enumeration and namespace
for elements related to Minecraft (e.g., types of blocks).  The enumerations
use Python's `enum` module, allowing for flexible representation of elements
(i.e., as strings, objects, or integers)

    import MinecraftElements

    someStoneBlock = MinecraftElements.Block.stone

Alternatively, specific (or all) components can be imported, if namespacing
won't be an issue

    from MinecraftElements import *
    someStoneBlock = Block.stone

Enumerated values can also be instantiated using the string name of the element
through the use of the `__getitem__` method:

    from MinecraftElements import Block
    someStoneBlock = Block["stone"]

As the string names match those used in Malmo's `Types` schema, this should
simplify conversion between data collected from Malmo to an enumeration.

Enumerations also provide static methods that return sets of specific enum groupings.  
This is particularly useful for checking membership:

    >>> from MinecraftElements import Block
    >>> my_block = Block.wooden_door
    >>> my_block in Block.doors()
    True
    >>> my_block in Block.victims()
    False

Finally, enumerations can be treated as integer objects.  This is useful for 
incorporating with certain types of data structures, e.g., numpy arrays:

    from MinecraftElements import Block
    import numpy as np

    blockArray = np.array([Block.stone, Block.air, Block.stone], dtype=np.uint8)

Note that all enumerated values are non-negative, and less than 236, allowing
for compatible representation using 8-bit unsigned bytes.


## TODO

* Add documentation on building Sphinx documents to README and Sphinx document.


## CHANGELOG

* 11 Feb 2022

  * Added static methods to Blocks and Marker_Blocks enum classes to return groups of blocks

* 29 June 2021

  * Updated Python docstrings to work with Sphinx.

  * Added Sphinx Documentation.

[malmo_types_schema]: https://github.com/microsoft/malmo/blob/master/Schemas/Types.xsd

[working_with_submodules]: https://github.blog/2016-02-01-working-with-submodules/

[pip_documentation]: https://pip.pypa.io/en/stable/

[sphinx_documentation]: https://www.sphinx-doc.org/en/master/
