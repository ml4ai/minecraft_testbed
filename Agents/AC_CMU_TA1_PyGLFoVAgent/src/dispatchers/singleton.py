from .base_dispatcher import BaseDispatcher

class Singleton(BaseDispatcher):
	"""
	A single item implementation will only allow a single item to be stored at
	any given time.  If there is an unprocessed item, then added items will be
	ignored.
	"""

	def __init__(self):
		"""
		Create the Singleton implementation of Collection
		"""

		BaseDispatcher.__init__(self)


	def next(self):
		"""
		Return the content of collection
		"""

		# If nothing in the list, return nothing
		if len(self) == 0:
			return None

		# Singleton returns the content of the list.  Since only a single item
		# is present, the items list will be empty
		item = self.items[0]
		self.empty()

		return item


