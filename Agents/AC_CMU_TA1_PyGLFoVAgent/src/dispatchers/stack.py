from .base_dispatcher import BaseDispatcher

class Stack(BaseDispatcher):
	"""
	A Stack (LIFO) implementation of a BaseDispatcher
	"""

	def __init__(self):
		"""
		Create the stack
		"""

		BaseDispatcher.__init__(self)


	def next(self):
		"""
		Return the last pushed item on the stack
		"""

		# If nothing is in the list, then return nothing
		if len(self) == 0:
			return None

		# Stack returns the last item added to the list (tail)
		item = self.items[-1]
		self.items = self.items[:-1]

		return item