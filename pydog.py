import pygame, sys, random
from pygame.locals import *
from pygame import *
from code.PydogLevel import PydogLevel
from code.PydogPlayer import PydogPlayer

class PyDogGame(object):		
	def run(self):
		self.titleScreen()

	def __init__(self, screen_size):	
		pygame.init()
		self.WIDTH = screen_size[0]
		self.HEIGHT = screen_size[1]
		self.BLACK = ( 0, 0, 0)
		self.WHITE = (255, 255, 255)

		self.titleScreenImg = pygame.image.load('data\other\intro.jpg')
		self.floor =  pygame.image.load('data/other/floor.gif')
		self.obstacle =  pygame.image.load('data/other/obstacle.gif')
		self.device =  pygame.image.load('data/other/device6.gif')
		self.goal =  pygame.image.load('data/other/button.gif')
		self.icon =  pygame.image.load('data/other/icon.gif')
		self.muteIcon =  pygame.image.load('data/other/mute.gif')

		self.sound_dog1 =  pygame.mixer.Sound('data/sound/dog.ogg')
		self.sound_dog2 =  pygame.mixer.Sound('data/sound/dog2.ogg')
		self.sound_place =  pygame.mixer.Sound('data/sound/laser.ogg')
		self.sound_win =  pygame.mixer.Sound('data/sound/triumph.ogg')
		self.sound_fail =  pygame.mixer.Sound('data/sound/fail.ogg')

		self.mutePosX = 20
		self.mutePosY = 20
		
		self.FPS = 30 # frames per second setting
		self.fpsClock = pygame.time.Clock()

		self.y_offset = 50 #todo calculcate this to center
		self.x_offset = 10 # todo implement and calculate this to center
		self.floor_height=20
		self.floor_width=32
		self.levelIndex = 0

		self.mute = False

		self.pydogLevel = PydogLevel()
		self.player = PydogPlayer()

		self.DISPLAYSURF = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

		self.OBJECT_BLOCK ='#'
		self.OBJECT_PLAYER ='@'
		self.OBJECT_GOAL ='.'
		self.OBJECT_BOX ='$'
		self.OBJECT_MOVING_BOX ='X'
		self.OBJECT_EMPTY =' '
		self.OBJECT_GOAL_AND_BOX ='Z'
		
		pygame.display.set_icon(self.icon)
		pygame.key.set_repeat (100, 250)

		self.fontObj = pygame.font.Font('freesansbold.ttf', 16)
		self.fontObjLarge = pygame.font.Font('freesansbold.ttf', 24)

	def win(self,level):
		for row,line in enumerate(level):	
			for col,type in enumerate(line):
				if type is self.OBJECT_GOAL:
					return False
		return True
	
	def playSound(self,sound):
		if self.mute is False:
			pygame.mixer.stop()
			sound.play()

	def isOkStep(self,level,x,y,xNext,yNext,levelOrg):
		if self.player.isMoving():
			return False
		obj = level[y][x]
		if obj is self.OBJECT_BLOCK:
			return False
		if obj is self.OBJECT_EMPTY or obj is self.OBJECT_PLAYER or obj is self.OBJECT_GOAL:
			return True
		if obj is self.OBJECT_BOX:
				objNext = level[yNext][xNext]
				if objNext is self.OBJECT_GOAL or objNext is self.OBJECT_EMPTY:
					replaceWith = self.OBJECT_EMPTY	
					if objNext is self.OBJECT_GOAL and levelOrg[y][x] is not self.OBJECT_GOAL:
						self.playSound(self.sound_place)
					if levelOrg[y][x] is self.OBJECT_GOAL:
						replaceWith = self.OBJECT_GOAL
						
					level[y][x] = replaceWith
					level[yNext][xNext] = self.OBJECT_MOVING_BOX
					
					return True
		return False
		
	def placePlayer(self,level, player):
		for row,line in enumerate(level):	
			for col,type in enumerate(line):
				if type is self.OBJECT_PLAYER:				
						player.x=col
						player.y=row
						break	

	def gameLoop(self):
		setupLevel = True
		showInstructions = False
		chooseLevel = False	
		numSteps = 0

		while True: 
			if setupLevel is True:
				level = self.pydogLevel.getLevel(self.levelIndex)
				levelOrg = self.pydogLevel.getLevel(self.levelIndex)
				self.placePlayer(level,self.player)			
				self.player.stopAnimation()
				pygame.display.set_caption("plush dog's sokoban. Level: " + str(self.levelIndex+1))
				numSteps = 0
				setupLevel = False

			if self.win(level) and not self.player.isMoving():
				self.playSound(self.sound_win)
				self.levelIndex +=1
				if self.levelIndex >= self.pydogLevel.numLevels():
					self.lastLevelScreen()
					self.levelIndex=0
					return

				setupLevel = True
				self.nextLevelScreen('Level '+str(self.levelIndex)+ ' cleared in ' +str(numSteps)+ ' steps!  Press SPACE to continue.')

			for h in xrange(0,self.HEIGHT,self.floor_height):
				for w in xrange(0,self.WIDTH,self.floor_width):
					self.DISPLAYSURF.blit(self.floor, (w,h))

			for row,line in enumerate(level):	
				for col,type in enumerate(line):
					if type is self.OBJECT_GOAL:
							self.DISPLAYSURF.blit(self.goal, (col*self.floor_width,row*self.floor_height-20 + self.y_offset))
					if type is self.OBJECT_BLOCK:
							self.DISPLAYSURF.blit(self.obstacle, (col*self.floor_width,row*self.floor_height - 30+ self.y_offset))
			
			playerX = self.player.x*self.floor_width 		
			if self.player.direction is 'LEFT':
				playerX+= self.player.moveCounterX
			if self.player.direction is 'RIGHT':
				playerX-= self.player.moveCounterX
			playerY = self.player.y*self.floor_height-64 + self.y_offset
			if self.player.direction is 'UP':
				playerY+= self.player.moveCounterY
			if self.player.direction is 'DOWN':
				playerY-= self.player.moveCounterY
			
			for row,line in enumerate(level):	
				if self.player.y is row:
					self.DISPLAYSURF.blit(self.player.getFrame(), (playerX,playerY))

				for col,type in enumerate(line):
					if type is self.OBJECT_MOVING_BOX:
						boxX = col*self.floor_width
						boxY = row*self.floor_height-60+ self.y_offset
						if levelOrg[row][col] is self.OBJECT_GOAL:
							self.DISPLAYSURF.blit(self.goal, (boxX,boxY+40))
						if self.player.direction is 'LEFT':
							boxX+= self.player.moveCounterX
						if self.player.direction is 'RIGHT':
							boxX-= self.player.moveCounterX
						if self.player.direction is 'UP':
							boxY+= self.player.moveCounterY
						if self.player.direction is 'DOWN':
							boxY-= self.player.moveCounterY
						self.DISPLAYSURF.blit(self.device, (boxX,boxY))
						if(not self.player.isMoving()):
							level[row][col] = self.OBJECT_BOX
								
					if type is self.OBJECT_BOX:
							self.DISPLAYSURF.blit(self.device, (col*self.floor_width,row*self.floor_height-60+ self.y_offset))

			if self.mute:
				self.DISPLAYSURF.blit(self.muteIcon, (self.mutePosX,self.mutePosY))
							
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w or event.key == pygame.K_UP: #move up
						if self.isOkStep(level,self.player.x,self.player.y-1,self.player.x,self.player.y-2,levelOrg):
							self.player.setAni('UP')
							numSteps +=1
					elif event.key == pygame.K_s or event.key == pygame.K_DOWN: #move down
						if self.isOkStep(level,self.player.x,self.player.y+1,self.player.x,self.player.y+2,levelOrg):
							self.player.setAni('DOWN')
							numSteps +=1
					elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: #move right
						if self.isOkStep(level,self.player.x+1,self.player.y,self.player.x+2,self.player.y,levelOrg):
							self.player.setAni('RIGHT')
							numSteps +=1
					elif event.key == pygame.K_a or event.key == pygame.K_LEFT: #move left
						if self.isOkStep(level,self.player.x-1,self.player.y,self.player.x-2,self.player.y,levelOrg):
							self.player.setAni('LEFT')
							numSteps +=1
					elif event.key == pygame.K_c: #mute	
						self.mute = not self.mute
						pygame.mixer.stop()
					elif event.key == pygame.K_b: #bark			
						self.player.setAni('BARK')
						self.playSound(random.choice([self.sound_dog1, self.sound_dog2]))
					elif event.key == pygame.K_SPACE: #restart
						setupLevel = True
						self.playSound(self.sound_fail)
					elif event.key == pygame.K_z: #next level
						self.levelIndex +=1
						setupLevel = True
					elif event.key == pygame.K_x: #choose level				
						self.selectLevelScreen()
						setupLevel = True
					elif event.key == pygame.K_ESCAPE: #go to menu
						return
					elif event.key == pygame.K_v: #go instructions			
						self.helpScreen()

				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.update()
			self.fpsClock.tick(self.FPS)

	def textMode(self,textRenders):
		alphaMaxLevel = 255
		alphaIncrement = 8
		alpha=0
		alphaSurface = Surface((self.WIDTH, self.HEIGHT))
		alphaSurface.fill((0,0,0))
		alphaSurface.set_alpha(alpha) 
		bgImage =self.DISPLAYSURF.copy()

		while True: 
			self.DISPLAYSURF.blit(bgImage, (0,0))
			self.DISPLAYSURF.blit(alphaSurface,(0,0))

			if alpha < alphaMaxLevel:
				alpha += alphaIncrement
				alphaSurface.set_alpha(alpha) 
			else:
				for tr in textRenders:
					self.DISPLAYSURF.blit(tr[0], tr[1])

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						return
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()
			self.fpsClock.tick(self.FPS)
		
	def helpScreen(self):
		texts  =["Instructions: Your goal is to help plush dog finish every level",
		"by placing all objects on the red dots.",
		"Try not jamming the objects in to a corner,",
		"there is no way to get them out of there!",
		"",
		"User interface:",
		" arrows: moves the dog",
		" esc: ends the game",
		" space: restarts level",
		" z: skip one level ahead",
		" x: choose level",
		" b: dog barks",
		" v: show instructions",
		" c: toggle sound on/off",
		"",
		"Press SPACE to continue!"]
		
		textRenders =[]
		margin=50
		marginx2 = margin*2
		textOffset=20
		for i,text in enumerate(texts):
			y = margin + (textOffset * i)
			textRenders.append(  (self.fontObj.render(text,True, self.WHITE, self.BLACK),Rect(margin,y,self.WIDTH-marginx2,100))   )

		self.textMode(textRenders)
		
	def lastLevelScreen(self):
		texts = ["Last level reached.","If you played through all levels, congratulations!","Press SPACE to return to title screen."]
	
		textRenders =[]
		margin=50
		marginx2 = margin*2
		textOffset=20
		for i,text in enumerate(texts):
			y = margin + (textOffset * i)
			textRenders.append(  (self.fontObj.render(text,True, self.WHITE, self.BLACK),Rect(margin,y,self.WIDTH-marginx2,100))   )

		self.textMode(textRenders)

	def selectLevelScreen(self):
		alphaMaxLevel = 255
		alphaIncrement = 8
		alpha=0
		alphaSurface = Surface((self.WIDTH, self.HEIGHT))
		alphaSurface.fill((0,0,0))
		alphaSurface.set_alpha(alpha) 
		bgImage =self.DISPLAYSURF.copy()
		
		maxLevel = self.pydogLevel.numLevels()
		
		texts = [('Choose level with arrow keys. Press SPACE to enter level!',self.fontObj),
		('',self.fontObj),
		('Level:',self.fontObj),
		(str(self.levelIndex+1),self.fontObjLarge)]
		
		textRenders =[]	
		textOffset = 20

		for i,text in enumerate(texts):
			y = textOffset * i
			textSurfaceObj = text[1].render(text[0],True, self.WHITE, self.BLACK)
			textRectObj = textSurfaceObj.get_rect()
			yValue = (self.HEIGHT/2) + y -50
			textRectObj.center = (self.WIDTH/2, yValue)
			textRenders.append((textSurfaceObj,textRectObj))

		while True:
			self.DISPLAYSURF.blit(bgImage, (0,0))
			self.DISPLAYSURF.blit(alphaSurface,(0,0))

			if alpha < alphaMaxLevel:
				alpha += alphaIncrement
				alphaSurface.set_alpha(alpha) 
			else:
				for tr in textRenders:
					self.DISPLAYSURF.blit(tr[0], tr[1])
	
			render = self.fontObjLarge.render(str(self.levelIndex+1),True, self.WHITE, self.BLACK)
			rect = render.get_rect()
			rect.center = (self.WIDTH/2, yValue)
			textRenders[len(textRenders)-1] = (render,rect)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						if self.levelIndex+1 < maxLevel:
							self.levelIndex +=1		
							self.pydogLevel.getLevel(self.levelIndex)
					if event.key == pygame.K_DOWN:
						if self.levelIndex>0:
							self.levelIndex -=1				
					if event.key == pygame.K_LEFT:
						if self.levelIndex-10 >= 0:
							self.levelIndex -=10				
					if event.key == pygame.K_RIGHT:
						if self.levelIndex+10 < maxLevel:
							self.levelIndex +=10
					if event.key == pygame.K_SPACE:
						return
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()
			self.fpsClock.tick(self.FPS)
		
	def nextLevelScreen(self,text):
		textRenders =[]	
		textSurfaceObj = self.fontObj.render(text, True, self.WHITE, self.BLACK)
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (self.WIDTH/2, self.HEIGHT/2)
		textRenders.append((textSurfaceObj,textRectObj))
		self.textMode(textRenders)

	def titleScreen(self):
		pygame.display.set_caption("plush dog's sokoban ")
		
		while True:	
			self.DISPLAYSURF.blit(self.titleScreenImg, (0,0))

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.gameLoop()
						pygame.display.set_caption("plush dog's sokoban ")
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()
			self.fpsClock.tick(self.FPS)


if __name__ == "__main__":
    game = PyDogGame((640, 480))
    game.run()


