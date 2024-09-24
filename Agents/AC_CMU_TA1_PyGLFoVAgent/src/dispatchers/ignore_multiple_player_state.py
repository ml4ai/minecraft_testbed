from .base_dispatcher import BaseDispatcher

from MinecraftBridge.messages import PlayerState

class IgnoreMultiplePlayerStateDispatcher(BaseDispatcher):
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
		# each participant.  If the item is a PlayerState message, then check
		# to see if there is another PlayerState message with the same 
		# participant id.  If so, do not add
		if isinstance(item, PlayerState):
			
			for message in self.items:
				if isinstance(message, PlayerState) and message.participant_id == item.participant_id:
					return

		# Add the item to the tail of the list (as the BaseDispatcher does)
		BaseDispatcher.add(self, item)




