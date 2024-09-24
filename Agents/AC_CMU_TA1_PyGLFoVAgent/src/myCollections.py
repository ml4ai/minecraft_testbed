"""
collections.py

A set of classes for allowing workers to store and process messages as they 
become available.  Collection defines the majority of functionality.  Each 
concrete subclass of Collection defines the order which messages are accessed.

Each Collection class implements the following methods:

    __len__ - returns the number of items in the collection
    add     - add a new item into the collection
    next    - retrieve the next item in the collection
    empty   - clear out all items in the collection

Each concrete subclass implements a version of next:

    Stack     - Last-In, First-Out (LIFO) data structure.  The most recent
                messages are published first, followed with any previously
                unpublished messages.  Ensures that all messages are published,
                but not necessarily in order of being received.
    Queue     - First-In, First-Out (FIFO) data structure.  Publishes messages
                in the order they are received.  Ensures that all messages are
                published in the order they're generated, but may result in 
                messages being published much later than they are generated.
    Singleton - Single-item data structure.  Publishes the most recent message
                received.  If a backlog of messages are created, then they are
                simply ignored.  Does not guarantee that all messages will be
                published, but will publish messages as close as possible to
                when they are received.

Author: Dana Hughes
email:  danahugh@andrew.cmu.edu
"""

__author__ = 'danahugh'


class Collection:
	"""
	A simple class for defining collections.  The purpose is to simply extend
	to create Stack or Queue classes
	"""

	def __init__(self):
		"""
		Create a Collection
		"""

		# Internal storage of items
		self.items = []


	def __len__(self):
		"""
		Number of items in the Queue
		"""

		return len(self.items)


	def next(self):
		"""
		Get the next item in the collection, or None if nothing available

		Return:
			An item based on the concrete implementation, None if the collection
			is empty.		
		"""

		# This will be class specific
		raise NotImplementedError


	def add(self, item):
		"""
		Add an item to the collection

		Args:
			item - the item to add to the collection.
		"""

		self.items.append(item)


	def empty(self):
		"""
		Clear out the items in the collection
		"""

		self.items = []



class Stack(Collection):
	"""
	A Stack (LIFO) implementation of Collection
	"""

	def __init__(self):
		"""
		Create the stack
		"""

		Collection.__init__(self)


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



class Queue(Collection):
	"""
	A Queue (FIFO) implementation of Collection
	"""

	def __init__(self):
		"""
		Create the stack
		"""

		Collection.__init__(self)


	def next(self):
		"""
		Return the oldest item on the stack
		"""

		# If nothing is in the list, then return nothing
		if len(self) == 0:
			return None

		# Stack returns the last item added to the list (tail)
		item = self.items[0]
		self.items = self.items[1:]

		return item



class Singleton(Collection):
	"""
	A single item implementation will only allow a single item to be stored at
	any given time.  If there is an unprocessed item, then added items will be
	ignored.
	"""

	def __init__(self):
		"""
		Create the Singleton implementation of Collection
		"""

		Collection.__init__(self)


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


