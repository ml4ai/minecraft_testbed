"""
OpenGL context using GLUT as the backend.  This is not the preferred context,
but is generally available.
"""

from OpenGL import GL
from OpenGL import GLUT

import logging

import sys

class OpenGLContext:
	"""
	An OpenGL context using GLUT as the backend
	"""

	def __init__(self, screen_size):
		"""
		Create a context with the given screen size
		"""

		# Store the screen size, and grab a handle to the logger
		self.screen_size = screen_size
		self.logger = logging.getLogger(__name__)

		# Initialize OpenGL
		GLUT.glutInit(sys.argv)
		GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_DEPTH)
		GLUT.glutInitWindowSize(self.screen_size[0], self.screen_size[1])
		GLUT.glutInitWindowPosition(0,0)

		self.window = GLUT.glutCreateWindow("dummy")
		GLUT.glutHideWindow()

		GLUT.glutDisplayFunc(self.dummy)

		GL.glClearColor(0.0, 0.0, 0.0, 1.0)
		GL.glClearDepth(1.0)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glDisable(GL.GL_BLEND)
		GL.glDepthFunc(GL.GL_LEQUAL)
		GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

		self.logger.info("%s: Using GLUT Backend", self)
		self.logger.info("%s:   OpenGL Vendor String: %s", self, GL.glGetString(GL.GL_VENDOR))
		self.logger.info("%s:   OpenGL Renderer String: %s", self, GL.glGetString(GL.GL_RENDERER))
		self.logger.info("%s:   OpenGL Version String: %s", self, GL.glGetString(GL.GL_VERSION))
		self.logger.info("%s:   OpenGL SL Version String: %s", self, GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION))

	def __str__(self):
		"""
		String representation of this class
		"""

		return "[OpenGLContext <GLUT>]"

	def dummy(self):
		"""
		A dummy callback display function for GLUT to use
		"""

		pass

	def getBackendInfo(self):
		"""
		Returns a dictionary of info on the GL backend

		Returns
		-------
		Dictionary with backend info
		"""

		return { "backend": "GLUT",
		         "vendor": GL.glGetString(GL.GL_VENDOR),
		         "renderer": GL.glGetString(GL.GL_RENDERER),
		         "version": GL.glGetString(GL.GL_VERSION),
		         "sl_version": GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
		       }