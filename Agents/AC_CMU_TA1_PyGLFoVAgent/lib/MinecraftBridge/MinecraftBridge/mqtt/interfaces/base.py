from ...utils import Loggable
from abc import ABC



class MinecraftInterface(ABC, Loggable):
	"""
	Abstract base class for Minecraft interfaces as
	wrappers around a MinecraftBridge object.
	"""

	def __init__(self, bridge):
		"""
		Arguments
		---------
			bridge: MinecraftBridge.BaseBridge or MinecraftInterface instance
		"""
		self._bridge = bridge._unwrapped


	def __str__(self):
		"""
		Provide a string representation of the object.
		"""
		bridge_str = str(self._bridge).strip('[]')
		return f"[{self.__class__.__name__} @ {bridge_str}]"


	@property
	def _unwrapped(self):
		"""
		Internal property that returns the underlying bridge.
		"""
		return self._bridge

