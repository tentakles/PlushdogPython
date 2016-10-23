import pygame, sys
from pygame.locals import *

class PydogPlayer:
	def __init__(self):
		self.maxFrameTime = 1
		self.frameTime = 0
	
		self.maxBarkTime=self.maxFrameTime * 16 # two complete cycles of animation
		self.barkTime=self.maxBarkTime

		self.maxFrames = 3
		self.aniFrame = 0
		self.aniFront = []
		self.aniBack = []
		self.aniLeft = []
		self.aniRight = []	
		self.aniBark = []
		self.direction=''
		
		self.maxMoveCounterY = 20
		self.moveCounterY = 0
		self.maxMoveCounterX = 32
		self.moveCounterX = 0
		self.moveCounterXStep= 4
		self.moveCounterYStep= 3

		self.aniFront.append(pygame.image.load('data/dog/fram1.gif'))
		self.aniFront.append(pygame.image.load('data/dog/fram2.gif'))
		self.aniFront.append(pygame.image.load('data/dog/fram3.gif'))
		self.aniFront.append(pygame.image.load('data/dog/fram4.gif'))
		
		self.aniBack.append(pygame.image.load('data/dog/bak1.gif'))
		self.aniBack.append(pygame.image.load('data/dog/bak2.gif'))
		self.aniBack.append(pygame.image.load('data/dog/bak3.gif'))
		self.aniBack.append(pygame.image.load('data/dog/bak4.gif'))
		
		self.aniLeft.append(pygame.image.load('data/dog/vsida1.gif'))
		self.aniLeft.append(pygame.image.load('data/dog/vsida2.gif'))
		self.aniLeft.append(pygame.image.load('data/dog/vsida3.gif'))
		self.aniLeft.append(pygame.image.load('data/dog/vsida4.gif'))
		
		self.aniRight.append(pygame.image.load('data/dog/hsida1.gif'))
		self.aniRight.append(pygame.image.load('data/dog/hsida2.gif'))
		self.aniRight.append(pygame.image.load('data/dog/hsida3.gif'))
		self.aniRight.append(pygame.image.load('data/dog/hsida4.gif'))

		self.aniBark.append(pygame.image.load('data/dog/bark1.gif'))
		self.aniBark.append(pygame.image.load('data/dog/bark2.gif'))
		self.aniBark.append(pygame.image.load('data/dog/bark3.gif'))
		self.aniBark.append(pygame.image.load('data/dog/bark4.gif'))

		self.aniCurrent = self.aniFront

	def isMoving(self):
		return self.moveCounterX > 0 or self.moveCounterY > 0 or  self.barkTime < self.maxBarkTime

	def stopAnimation(self):
		self.moveCounterX=0
		self.moveCounterY=0
		self.barkTime=self.maxBarkTime
		self.aniCurrent = self.aniFront
		self.aniFrame=0
		self.frameTime = 0
	
	def setAni(self,ani):
		self.direction = ani
		if ani is 'DOWN':
			self.y=self.y+1
			self.aniCurrent = self.aniFront
			self.moveCounterY = self.maxMoveCounterY
		elif ani is 'UP':
			self.y=self.y-1
			self.aniCurrent = self.aniBack
			self.moveCounterY = self.maxMoveCounterY
		elif ani is 'LEFT':
			self.x = self.x-1
			self.aniCurrent = self.aniLeft
			self.moveCounterX = self.maxMoveCounterX
		elif ani is 'RIGHT':
			self.x = self.x+1
			self.aniCurrent = self.aniRight
			self.moveCounterX = self.maxMoveCounterX
		elif ani is 'BARK':
			self.aniCurrent = self.aniBark
			self.barkTime=0
			self.moveCounter = 0
		self.aniFrame = 0
		self.frameTime = 0
				
	def getFrame(self):
	
		if not self.isMoving():
			return self.aniCurrent[0]
	
		if self.moveCounterX > 0:
			self.moveCounterX-=self.moveCounterXStep
		if self.moveCounterY > 0:
			self.moveCounterY-=self.moveCounterYStep
		if self.aniCurrent is self.aniBark:
			if self.barkTime is self.maxBarkTime:
				self.aniCurrent = self.aniFront
			else:
				self.barkTime += 1
		frame  = self.aniCurrent[self.aniFrame]
		if self.frameTime is self.maxFrameTime:
			self.frameTime = 0
			self.aniFrame += 1
			if self.aniFrame > self.maxFrames:
				self.aniFrame = 0
		else:
			self.frameTime += 1
		return frame