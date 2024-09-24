# PyGL Field of View

This module is designed to generate a machine legible version of the player's
Field of View in Minecraft.  The module is designed to be used as either a
component for agents, or as a stand-alone agent connected to the testbed
message bus (MQTT).

## Requirements

This module requires that the packages below are installed.  OpenGL drivers are
available for all major platforms, and the required python modules can be 
installed using `pip`.

* Python 3.5 or later
* OpenGL
* GLU
* GLFW (preferred) or GLUT (pygame may also be an option)
* PyOpenGL
* numpy

See `documentation\INSTALL.md` for details on installing the above packages.

Additionally, this module assumes that the `MinecraftElements` package is
installed.  The repo for this package is located at https://gitlab.com/cmu_asisi/MinecraftElements

## Usage

