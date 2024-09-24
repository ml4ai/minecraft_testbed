"""
perspective.py

The Perspective class establishes and maintains all components associated with
the perspective / camera in OpenGL.  In particular, the class stores the
field of view and size of the window to render to.

The main purpose of keeping the perspective classes separate from the FOV class
is to allow for creation of the OpenGL context based on available / installed
libraries.  At the moment, GLFW is the preferred context, while GLUT is used as
a backup context.
"""

from OpenGL import GL, GLU

# OpenGL requires some context (window) in order to generate images
try:
	from .context.glfw import OpenGLContext
except:
	from .context.glut import OpenGLContext

import numpy as np


class Perspective:
	"""
	The perspective class is responsible for maintaining components related to
	the perspective model in OpenGL, and inform the FOV when any of these
	components change.  Specifically, instances of the class need to keep 
	track of the position and orientation of the perspective, the vertical
	angle of the field of view, and the size of the window (if possible).
	"""

	class PlayerState:
		"""
		The PlayerState class is a simple wrapper encapsulating the effect of
		the player's current movement state (e.g., running, walking, etc.) has
		on the perspective of the FoV
		"""

		def __init__(self, viewHeight, fovy):
			"""
			Create a new PlayerState with the associated perspective parameters

			Args:
				viewHeight - the vertical offset of the perspective from the
				             player's position
				fovy       - the y-axis field of view (in degrees) of the
				             perspective
			"""

			self.viewHeight = viewHeight
			self.fovy = fovy


	# Static instances of player state, reflecting player movement modes:
	#   WALKING:    When the player is walking or standing still
	#   SPRINTING:  When the player is sprinting.
	#   SNEAKING:   When the player is sneaking / crouching
	#
	# NOTE:  Currently, values for viewHeight and FOV are estimated based on 
	#        the following sources:
	#        https://minecraft.gamepedia.com/Player
	#        
	#        In the Player wiki page, height is given as 1.8 for walking and 
	#        running, and 1.5 for sneaking.  However, eye height is also noted
	#        as being at a height of 1.62 for walking.  
	PlayerState.WALKING = PlayerState(1.8, 70)
	PlayerState.SPRINTING = PlayerState(1.8, 70)
	PlayerState.SNEAKING = PlayerState(1.5, 70)


	def __init__(self, position=(0,0,0), orientation=(0,0,0),
		               playerState=PlayerState.WALKING, 
		               window_size=(600,400), 
		               zNear=0.1, zFar=100.0):
		"""
		Create the perspective with the provided parameters.

		Args:
		    position    - the location (x,y,z) of the perspective
		    orientation - the orientation (pitch, yaw, roll) of the perspective
		    playerState - the player's motion state, an instance of PlayerState
		    window_size - the size of the window to render (wicth, height)
		    zNear       - distance to the near clipping plane
		    zFar        - distance to the far clipping plane
		"""

		self.position = position
		self.orientation = orientation
		self.playerState = playerState
		self.window_size = window_size
		self.zNear = zNear
		self.zFar = zFar

		# GLU uses the aspect ratio of the window when setting the projection
		# matrix
		self.aspect = float(self.window_size[0])/float(self.window_size[1])

		# Create the needed context
		self.context = OpenGLContext(self.window_size)

		# Observers
		self.observers = set()


	def register(self, observer):
		"""
		Add an observer to the set of observers of this object.

		Args:
			observer - object to be notified when the feeder contents change.
		"""

		self.observers.add(observer)


	def deregister(self, observer):
		"""
		Remove the observer from the set of observers of this object.

		Args:
			observer - object in the observers registry to be removed.
		"""

		if observer in self.observers:
			self.observers.remove(observer)


	def __notify(self):
		"""
		Inform observers that the perspective has changed.
		"""

		for observer in self.observers:
			observer.updatePerspective()


	def setup(self):
		"""
		Set the OpenGL projection and model matrices to reflect the position
		and orientation of the perspective
		"""

		# Unpack for simplicity
		x,y,z = self.position
		pitch,yaw,roll = self.orientation

		# Increase the y position by the current playerState viewHeight
		y += self.playerState.viewHeight
		# Increase the x position by the thickness of the avatar's head
		x += 0.0

		# Set the projection matrix
		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glLoadIdentity()
		GLU.gluPerspective(self.playerState.fovy, self.aspect, self.zNear, self.zFar)

		# Move the scene by the inverse of the perspective position and
		# orientation (OpenGL doesn't have a "camera", rather, the model
		# is intiially transformed by the inverse of the "camrea" prior to 
		# placing things in the environment).
		# NOTE:  The yaw in Minecraft seems to be 180 degrees different than
		#        of what is in OpenGL.  Hence, we add 180 degrees.
		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glLoadIdentity()
		GL.glRotatef(pitch, 1.0, 0.0, 0.0)
		GL.glRotatef(yaw+180, 0.0, 1.0, 0.0)
		GL.glRotatef(roll, 0.0, 0.0, 1.0)
		GL.glTranslatef(-x, -y, -z)


	def set_pose(self, position, orientation):
		"""
		Set the position and orientation of the perspective

		Args:
		    position    - (x,y,z) of the updated perspective 
		    orientation - (pitch,yaw,roll) of the updated perpective
		"""

		self.position = position
		self.orientation = orientation


	def set_position(self, position):
		"""
		Set the position of the perspective

		Args:
		    position    - (x,y,z) of the updated perspective 
		"""

		self.set_pose(position, self.orientation)


	def set_orientation(self, orientation):
		"""
		Set the orientation of the perspective

		Args:
		    orientation - (pitch,yaw,roll) of the updated perpective
		"""

		self.set_pose(self.position, orientation)


	def getImage(self):
		"""
		Extract the image generated by the OpenGL rendering

		Returns:
			A 3D numpy array containing the RGB values of each pixel
		"""

		# Read the pixels out in RGB format, with 8 bits per channel
		GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
		data = GL.glReadPixels(0, 0, self.window_size[0], self.window_size[1], 
			                   GL.GL_RGB, GL.GL_UNSIGNED_BYTE)

		# Extract the RGB data into an numpy array, and reshape appropriately
		rgbArray = np.frombuffer(data, np.ubyte)
		rgbArray.shape = self.window_size[1], self.window_size[0], 3
		rgbArray = np.swapaxes(rgbArray, 0, 1)
		rgbArray = np.flip(rgbArray, axis=1)

		return rgbArray


	def getViewRay(self):
		"""
		Return a normalized vector representing the direction of the view
		"""

		# Convert pitch and yaw to radians
		pitch = self.orientation[0]*np.pi/180.0
		yaw = (self.orientation[1]+180.0)*np.pi/180.0

		# Yaw determines the x-z direction, pitch the y direction
		x = np.cos(yaw)*np.cos(pitch)
		z = np.sin(yaw)*np.cos(pitch)
		y = np.sin(pitch)

		return np.array[(x,y,z)]


	def getUp(self):
		"""
		Return the up and right vectors
		"""

		# Convert pitch and yaw to radians
		pitch = self.orientation[0]*np.pi/180.0
		yaw = (self.orientation[1]+180.0)*np.pi/180.0

		# 
		x = -np.cos(yaw)*np.sin(pitch)
		z = -np.sin(yaw)*np.sin(pitch)
		y = np.cos(pitch)

		return np.array[(x,y,z)]



	def computeFrustrum(self):
		"""
		Compute the frustrum
		"""

		viewRay = self.getViewRay()

		Hnear = 2.0 * np.tan(self.playerState.fovy*np.pi/360.0) * self.zNear
		Wnear = Hnear * self.aspect

		Hfar = 2.0 * np.tan(self.playerState.fovy*np.pi/360.0)* self.zFar
		Wfar = Hfar * self.aspect

		# Calculate the up and right vectors
		up = self.getUp()
		right = np.cross(viewRay, up)


		# Calculate the corner points
		p = np.array(self.position)

		fc = p + viewRay * self.zFar
		nc = p + viewRay * self.zNear

		ftl = fc + (up*Hfar/2) - (right*Wfar/2)
		ftr = fc + (up*Hfar/2) + (right*Wfar/2)
		fbl = fc - (up*Hfar/2) - (right*Wfar/2)
		fbr = fc - (up*Hfar/2) + (right*Wfar/2)

		ntl = nc + (up*Hnear/2) - (right*Wnear/2)
		ntr = nc + (up*Hnear/2) + (right*Wnear/2)
		nbl = nc - (up*Hnear/2) - (right*Wnear/2)		
		nbr = nc - (up*Hnear/2) + (right*Wnear/2)

		# Calculate vectors for the right, left, top, and bottom of the frustrum
		aRight = (nc + right * Wnear / 2) - p 
		aLeft = (nc - right * Wnear / 2) - p
		aTop = (nc + up * Hnear / 2) - p
		aBottom = (nc - up * Hnear / 2) - p 

		# What are the point and normals defining each plane?
		nearPlane = (nc, viewRay)
		farPlane = (fc, -viewRay)

