"""
A simple endpoint wrapper that maintains timing information on how long an 
endpoint takes to execute.  Primarily for debugging purposes.
"""

import numpy as np
import time

class EndpointTiming:
	"""
	A simple endpoint for timing other endpoints.
	"""

	def __init__(self, endpoint):
		"""
		Wrap the passed endpoint with timing

		Args:
			endpoint - the endpoint to time
		"""

		self.endpoint = endpoint

		# Maintain a list of execution times
		self.execution_times = []


	def reset(self):
		"""
		Erase all the current execution times
		"""

		self.execution_times = []


	def __call__(self, pixelMap):
		"""
		Call the base endpoint, capturing timestamps of the start and end
		of the call
		"""

		start_time = time.perf_counter()
		results = self.endpoint(pixelMap)
		end_time = time.perf_counter()

		# Add how long it took to calculate the endpoint to the current list
		self.execution_times.append(end_time-start_time)


	def getTimingStatistics(self):
		"""
		Return the mean and standard deviation of the execution times of the 
		wrapped enpoint
		"""

		return np.mean(self.execution_times), np.std(self.execution_times)