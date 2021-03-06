from panda3d.core import Vec3, Point3, NodePath

from math import sin, cos, pi, floor

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import ZUp
from time import sleep

DEG_TO_RAD = pi/180
MOVE_SPEED = 30.0 * 100000
INIT_SCALE = 1.5
MAX_SCALE = 12
SCALE_RATE = 1.5
TRANS_RATE = 1.2
DEG_TO_RAD = pi/180

class SMBall():

	def __init__(self, bWrld, wObj, pObj, playerNP):
		self.playerObj = pObj
		self.player = playerNP
		self.worldBullet = bWrld
		self.worldObj = wObj
		self.rolledOnce = False
		self.rollState = False
		self.ballExists = False
		self.ballModel = loader.loadModel("../res/models/sphere.egg.pz")
		self.ballModel.setScale(INIT_SCALE, INIT_SCALE, INIT_SCALE)
		self.ballNP = NodePath()
		self.ballRBody = NodePath()
		print("Snowball initialized.")
	
	def setRolling(self, roll):
		self.rollState = roll
	
	def isRolling(self):
		return self.rollState

	def getSnowAmount(self):
		result = 0
		size = self.ballModel.getScale().getX()
		if(self.rollState and size > 2.0):
			size = floor(size)
			result += (size * size)
		return result
		
	def exists(self):
		return self.ballExists
	
	def getRigidbody(self):
		return self.ballRBody
		
	def getNodePath(self):
		return self.ballNP
	
	def destroy(self):
		self.ballNP.removeNode()
		self.ballNP = None
		self.ballModel.detachNode()
		self.ballNP = NodePath()
		self.ballExists = False
		self.rollState = False
	
	def respawn(self):
	
		# Drop the ball
		if(self.isRolling()):
			self.setRolling(False)
			self.dropBall()
		
		# Make the ball
		else:
			if(self.rolledOnce):
				self.ballRBody.removeShape(self.ballShape)
				self.ballModel.detachNode()
			
			pos = self.playerObj.getPosition()
			x = pos.getX()
			y = pos.getY()
			z = pos.getZ()
			self.ballModel.setScale(INIT_SCALE, INIT_SCALE, INIT_SCALE)
			self.ballNP = self.playerObj.getNodePath().attachNewNode(self.ballModel.node())
			self.ballNP.setPos(0, 4, -5) # In front and and bit below the yeti.
			self.setRolling(True)
			self.ballExists = False
	
	def dropBall(self):
		self.ballNP.removeNode()
		pos = self.playerObj.getPosition()
		pNP = self.playerObj.getNodePath()
		px = pos.getX()
		py = pos.getY()
		pz = pos.getZ()
		size = self.ballModel.getScale().getX()
		self.ballShape = BulletCylinderShape(size, size * 1.7, ZUp)
		self.ballRBody = BulletRigidBodyNode()
		self.ballRBody.setMass(0)
		self.ballRBody.addShape(self.ballShape)
		rbNP = self.worldObj.attachNewNode(self.ballRBody)
		ph = self.playerObj.getRotation()
		self.ballModel.setPos(0, 0, 0)
		dx = -sin(ph * DEG_TO_RAD) * size * 3
		dy = cos(ph * DEG_TO_RAD) * size * 3
		self.ballModel.reparentTo(rbNP)
		rbNP.setPos(px + dx, py + dy, pz)
		self.worldBullet.attachRigidBody(self.ballRBody)
		self.setRolling(False)
		self.rolledOnce = True
		self.ballExists = True
		print(self.rolledOnce)
	
	def grow(self):
		size = self.ballModel.getScale()
		sx = size.getX()
		if(sx < MAX_SCALE):
			pos = self.ballModel.getPos()
			px = pos.getX()
			py = pos.getY()
			pz = pos.getZ()
			sy = size.getY()
			sz = size.getZ()
			dt = globalClock.getDt()
			self.ballModel.setScale(sx + (SCALE_RATE * dt), sy + (SCALE_RATE * dt), sz + (SCALE_RATE * dt))
			self.ballModel.setPos(px, py + (TRANS_RATE * dt), pz + (TRANS_RATE * dt))

	def getSize(self):
		return self.ballModel.getScale().getX()
	
	def throwBall(self, size, camP, camH):
		self.ballNP.removeNode()
		pos = self.playerObj.getPosition()
		pNP = self.playerObj.getNodePath()
		px = plypos.getX()
		py = plypos.getY()
		pz = plypos.getZ()
		size = self.ballModel.getScale().getX()
		self.ballShape = BulletCylinderShape(size, size * 1.7, ZUp)
		self.ballRBody = BulletRigidBodyNode()
		self.ballRBody.setMass(1)
		self.ballRBody.addShape(self.ballShape)
		rbNP = self.worldObj.attachNewNode(self.ballRBody)
		ph = self.playerObj.getRotation()
		self.ballModel.setPos(0, 0, 0)
		dx = -sin(ph * DEG_TO_RAD) * size * 3
		dy = cos(ph * DEG_TO_RAD) * size * 3
		self.ballModel.reparentTo(rbNP)
		rbNP.setPos(px + dx, py + dy, pz)
		self.worldBullet.attachRigidBody(self.ballRBody)
		self.setRolling(False)
		self.rolledOnce = True
		self.ballExists = True
		xFactor = -sin(camH * DEG_TO_RAD)*cos(camP * DEG_TO_RAD)
		yFactor = cos(camH * DEG_TO_RAD)*cos(camP * DEG_TO_RAD)
		zFactor = sin(camP *DEG_TO_RAD)
		defUpFrc = 200
		defXYFrc = 500
		self.applyForce(Vec3(defXYFrc*xFactor, defXYFrc*yFactor,defUpFrc*zFactor))
		
	
	def setFactor(self, x, y, z):
		self.ballNP.node().setLinearFactor(Vec3(x, y, z))
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Applies a force vector.
	# (Vec3 force)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def applyForce(self, force):
		self.ballNP.node().applyForce(force, PNT)