"""
OpenGL context using pygame
"""
"""
import pygame

from OpenGL import GL

class OpenGLContext:
	"""
	An OpenGL context using GLFW
	"""

	def __init__(self, screen_size):
		"""
		"""

		pygame.init()

		self.screen_size = screen_size

		self.screen = pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF, 32)


		# Set up OpenGL rendering 
		GL.glViewport(0, 0, screen_size[0], screen_size[1])
		GL.glClearColor(0.0, 0.0, 0.0, 1.0)
		GL.glClearDepth(1.0)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glDisable(GL.GL_BLEND)
		GL.glDepthFunc(GL.GL_LEQUAL)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
"""