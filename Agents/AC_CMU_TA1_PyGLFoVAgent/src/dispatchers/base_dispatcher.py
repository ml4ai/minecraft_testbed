# -*- coding: utf-8 -*-
"""
.. module:: base_dispatcher.py
   :platform: Linux, Windows, OSX
   :synopsis: Definition of the core functionality required by all message
              dispatchers.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""


class BaseDispatcher:
	"""
	A simple class for defining core functionality required by all Dispatcher
	classes.  Each Dispatcher class needs to implement the following method:

    __len__ - returns the number of items in the collection
    add     - add a new item into the collection
    next    - retrieve the next item in the collection
    empty   - clear out all items in the collection
	"""

	def __init__(self):
		"""
		Initialize the BaseDispatcher components
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