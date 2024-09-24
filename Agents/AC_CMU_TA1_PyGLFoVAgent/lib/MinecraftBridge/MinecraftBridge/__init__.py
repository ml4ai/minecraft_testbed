# -*- coding: utf-8 -*-
"""
.. module:: MinecraftBridge
   :platform: Linux, Windows, OSX
   :synopsis: MinecraftBridge module

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Package containing messages and bridges to message sources for interfacing 
with Minecraft::

       __  ____                            ______  ____       _     __         
      /  |/  (_)___  ___  ______________ _/ __/ /_/ __ )_____(_)___/ /___ ____ 
     / /|_/ / / __ \/ _ \/ ___/ ___/ __ `/ /_/ __/ __  / ___/ / __  / __ `/ _ \
    / /  / / / / / /  __/ /__/ /  / /_/ / __/ /_/ /_/ / /  / / /_/ / /_/ /  __/
   /_/  /_/_/_/ /_/\___/\___/_/   \__,_/_/  \__/_____/_/  /_/\__,_/\__, /\___/ 
                                                               /____/       

The purpose of this module is to simplify interfacing to various sources of 
observations from Minecraft (e.g., Malmo, MQTT, File Readers, etc.) and provide
a common representation of messages received from Minecraft, and interface to
subscribe to specific observations and publish messages back to the Minecraft
bridge.
"""

__author__ = "Dana Hughes"
__email__ = "danahugh@andrew.cmu.edu"
__url__ = "https://gitlab.com/cmu_asist/MinecraftBridge"
__version__ = "1.3.6"
