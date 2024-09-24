"""
This module contains a set of classes for storing and rendering OpenGL vertices
"""

from .static_vbo_store import StaticVboStore
from .simple_vertex_store import SimpleVertexStore
from .player_vbo_store import PlayerVboStore

__all__ = ["StaticVboStore", "SimpleVertexStore", "PlayerVboStore"]