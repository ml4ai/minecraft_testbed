"""
actions.py
"""

from enum import IntEnum, unique
from .blocks import Block



@unique
class Action(IntEnum):
    """
    Enumeration of actions in Minecraft.

    This IntEnum is designed to be compatible with MiniGrid.
    """

    left = 0
    right = 1
    forward = 2
    toggle = 5
    done = 6


    @staticmethod
    def num_actions():
        return len(list(map(int, Action)))
