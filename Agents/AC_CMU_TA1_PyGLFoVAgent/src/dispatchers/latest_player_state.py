from .base_dispatcher import BaseDispatcher

from MinecraftBridge.messages import PlayerState

class LatestPlayerStateDispatcher(BaseDispatcher):
	"""
	"""

	def __init__(self):

		BaseDispatcher.__init__(self)


	def next(self):

		# If nothing is in the list, then return nothing
		if len(self) == 0:
			return None

		# Return the item at the head of the list
		item = self.items[0]
		self.items = self.items[1:]

		return item


	def add(self, item):

		# We want to only allow a single instance of a PlayerState message for
		# each participant.  If the item is a PlayerState message, then remove
		# any other PlayerState message from the list with the same
		# participant_id
		if isinstance(item, PlayerState):
			self.items = [x for x in self.items if not isinstance(x, PlayerState) or x.participant_id != item.participant_id]

		# Add the item to the tail of the list (as the BaseDispatcher does)
		BaseDispatcher.add(self, item)




