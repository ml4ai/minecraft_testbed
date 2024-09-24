"""
`________  ___    ___ ________  ___       ________ ________  ___      ___ 
|\   __  \|\  \  /  /|\   ____\|\  \     |\  _____\ \   __  \|\  \    /  /|
\ \  \|\  \ \  \/  / | \  \___|\ \  \    \ \  \__/\  \  \|\  \ \  \  /  / /
 \ \   ____\ \    / / \ \  \  __\ \  \    \ \   __\ \ \  \ \  \ \  \/  / / 
  \ \  \___|\/  /  /   \ \  \|\  \ \  \____\ \  \_|  \ \  \_\  \ \    / /  
   \ \__\ __/  / /      \ \_______\ \_______\ \__\    \ \_______\ \__/ /   
    \|__||\___/ /        \|_______|\|_______|\|__|     \|_______|\|__|/    
         \|___|/                                                          
                                                                          
                                                                          
This module calculates the blocks that are viewable in a player's Field of View
in Minecraft.  The module reconstructs (to a reasonable approximation) of the
rendering pipeline of Minecraft using OpenGL, and uses the resulting generated
images to determine the pixel-level occupancy of blocks passed to the renderer.

This module has several (potential) use cases, including:

-- Determining the set of blocks observable by the player in Minecraft
-- Determining which block is rendered on a per-pixel basis
-- Generating saliency maps of the player's field of view
-- Determining the number of pixels associated with a specific / each block
-- If eye-tracking is available, determining which block(s) the human is
   visually attending to.
"""

__all__ = ["Block", "BlockFeeder", "FOV", "Perspective", "MinecraftElements", "CompositeBlockFeeder", "StaticVboStore", "SimpleVertexStore", "CompositeVertexStore", "BlockColorMapper", "PlayerVboStore"]

__author__ = "Dana Hughes"
__email__ = "danahugh@andrew.cmu.edu"
__url__ = "https://gitlab.com/cmu_asist/pygl_fov"
__version__ = "0.3.6"


from .block_feeder import BlockFeeder
from .composite_block_feeder import CompositeBlockFeeder
from .block import Block
from .fov import FOV
from .perspective import Perspective

from .vertex_store import StaticVboStore
from .vertex_store import SimpleVertexStore
from .vertex_store import PlayerVboStore
from .composite_vertex_store import CompositeVertexStore
from .id_color_mapper import BlockColorMapper


import MinecraftElements
