"""
OpenGL context using GLFW as the backend.  This is the currently preferred
context, as it is more modern, and is easier to create windows that are hidden.
"""

import glfw
import logging

from OpenGL import GL

class OpenGLContext:
	"""
	An OpenGL context using GLFW as the backend.
	"""

	def __init__(self, screen_size):
		"""
		Create a context with the given screen size
		"""

		# Store the screen size, and grab a handle to the logger
		self.screen_size = screen_size
		self.logger = logging.getLogger(__name__)

		# Trying to use glfw instead of glut
		if not glfw.init():
			self.logger.error("%s: Unable to initialize GLFW", self)
			return

		# Set window hint NOT visible
		glfw.window_hint(glfw.VISIBLE, False)

		# Create a windowed mode window and its OpenGL context
		window = glfw.create_window(self.screen_size[0], self.screen_size[1], "hidden", None, None)

		if not window:
			self.logger.error("%s: Unable to create a GLFW window.", self)
			glfw.terminate()
			return

		# Make the window's context current
		glfw.make_context_current(window)

		# Set up OpenGL rendering 
		GL.glClearColor(0.0, 0.0, 0.0, 1.0)		# Background color is black
		GL.glClearDepth(1.0)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glDisable(GL.GL_BLEND)
		GL.glDepthFunc(GL.GL_LEQUAL)
		GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

		self.logger.info("%s: Using GLFW Backend", self)
		self.logger.info("%s:   OpenGL Vendor String: %s", self, GL.glGetString(GL.GL_VENDOR))
		self.logger.info("%s:   OpenGL Renderer String: %s", self, GL.glGetString(GL.GL_RENDERER))
		self.logger.info("%s:   OpenGL Version String: %s", self, GL.glGetString(GL.GL_VERSION))
		self.logger.info("%s:   OpenGL SL Version String: %s", self, GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION))


	def __str__(self):
		"""
		String representation of this class
		"""

		return "[OpenGLContext <GLFW>]"


	def getBackendInfo(self):
		"""
		Returns a dictionary of info on the GL backend

		Returns
		-------
		Dictionary with backend info
		"""

		return { "backend": "GLFW",
		         "vendor": GL.glGetString(GL.GL_VENDOR),
		         "renderer": GL.glGetString(GL.GL_RENDERER),
		         "version": GL.glGetString(GL.GL_VERSION),
		         "sl_version": GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
		       }