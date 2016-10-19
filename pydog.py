import pygame, sys, random
from pygame.locals import *
from pygame import *
from code.PydogLevel import PydogLevel
from code.PydogPlayer import PydogPlayer
pygame.init()
WIDTH = 640
HEIGHT = 480
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)

titleScreenImg = pygame.image.load('data\other\intro.jpg')
floor =  pygame.image.load('data/other/floor.gif')
obstacle =  pygame.image.load('data/other/obstacle.gif')
device =  pygame.image.load('data/other/device6.gif')
goal =  pygame.image.load('data/other/button.gif')
icon =  pygame.image.load('data/other/icon.gif')

sound_dog1 =  pygame.mixer.Sound('data/sound/dog.ogg')
sound_dog2 =  pygame.mixer.Sound('data/sound/dog2.ogg')
sound_place =  pygame.mixer.Sound('data/sound/laser.ogg')
sound_win =  pygame.mixer.Sound('data/sound/triumph.ogg')
sound_fail =  pygame.mixer.Sound('data/sound/fail.ogg')

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

y_offset = 50 #todo calculcate this to center
x_offset = 10 # todo implement and calculate this to center
floor_height=20
floor_width=32
levelIndex = 0

mute = False

pydogLevel = PydogLevel()
player = PydogPlayer()

pygame.display.set_icon(icon)
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))

alphaSurface = Surface((WIDTH, HEIGHT)) # The custom-surface of the size of the screen.
alphaSurface.fill((0,0,0)) # Fill it with whole white before the main-loop.
alphaSurface.set_alpha(0) # Set alpha to 0 before the main-loop.

OBJECT_BLOCK ='#'
OBJECT_PLAYER ='@'
OBJECT_GOAL ='.'
OBJECT_BOX ='$'
OBJECT_MOVING_BOX ='X'
OBJECT_EMPTY =' '
OBJECT_GOAL_AND_BOX ='Z'

pygame.key.set_repeat (100, 250)

fontObj = pygame.font.Font('freesansbold.ttf', 16)

def main():
	titleScreen()

def win(level):
	for row,line in enumerate(level):	
		for col,type in enumerate(line):
			if type is OBJECT_GOAL:
				return False
	return True
	
def playSound(sound,mute):
	if mute is False:
		pygame.mixer.stop()
		sound.play()

def isOkStep(level,x,y,xNext,yNext,levelOrg):
	if player.isMoving():
		return False
	obj = level[y][x]
	if obj is OBJECT_BLOCK:
		return False
	if obj is OBJECT_EMPTY or obj is OBJECT_PLAYER or obj is OBJECT_GOAL:
		return True
	if obj is OBJECT_BOX:
			objNext = level[yNext][xNext]
			if objNext is OBJECT_GOAL or objNext is OBJECT_EMPTY:
				replaceWith = OBJECT_EMPTY	
				if objNext is OBJECT_GOAL and levelOrg[y][x] is not OBJECT_GOAL:
					playSound(sound_place,mute)
				if levelOrg[y][x] is OBJECT_GOAL:
					replaceWith = OBJECT_GOAL
					
				level[y][x] = replaceWith
				level[yNext][xNext] = OBJECT_MOVING_BOX
				
				return True
	return False
		
def placePlayer(level, player):
	for row,line in enumerate(level):	
		for col,type in enumerate(line):
			if type is OBJECT_PLAYER:				
					player.x=col
					player.y=row
					break	

def gameLoop():
	
	global levelIndex
	global y_offset
	global player
	global mute
	setupLevel = True
	nextLevel = False
	showInstructions = False
	chooseLevel = False	
	numSteps = 0

	while True: 
		if setupLevel is True:
				level = pydogLevel.getLevel(levelIndex)
				levelOrg = pydogLevel.getLevel(levelIndex)
				placePlayer(level,player)
				setupLevel = False
				player.stopAnimation()
				alpha = 0
				alphaSurface.set_alpha(0) 	
				pygame.display.set_caption("plush dog's sokoban. Level: " + str(levelIndex+1))
	
				numSteps = 0

		if win(level) and not nextLevel:
			playSound(sound_win,mute)
			levelIndex +=1
			nextLevel = True
			
			textRenders =[]	
			textSurfaceObj = fontObj.render('Level '+str(levelIndex)+ ' cleared in ' +str(numSteps)+ ' steps!  Press ENTER to continue.', True, WHITE, BLACK)
			textRectObj = textSurfaceObj.get_rect()
			textRectObj.center = (WIDTH/2, HEIGHT/2)
			textRenders.append((textSurfaceObj,textRectObj))
			
		for h in xrange(0,HEIGHT,floor_height):
			for w in xrange(0,WIDTH,floor_width):
				DISPLAYSURF.blit(floor, (w,h))

		for row,line in enumerate(level):	
			for col,type in enumerate(line):
				if type is OBJECT_GOAL:
						DISPLAYSURF.blit(goal, (col*floor_width,row*floor_height-20 + y_offset))
				if type is OBJECT_BLOCK:
						DISPLAYSURF.blit(obstacle, (col*floor_width,row*floor_height - 30+ y_offset))
		
		playerX = player.x*floor_width 		
		if player.direction is 'LEFT':
			playerX+= player.moveCounterX
		if player.direction is 'RIGHT':
			playerX-= player.moveCounterX
		playerY = player.y*floor_height-64 + y_offset
		if player.direction is 'UP':
			playerY+= player.moveCounterY
		if player.direction is 'DOWN':
			playerY-= player.moveCounterY
		
		for row,line in enumerate(level):	
			if player.y is row:
				DISPLAYSURF.blit(player.getFrame(), (playerX,playerY))

			for col,type in enumerate(line):
				if type is OBJECT_MOVING_BOX:
					boxX = col*floor_width
					boxY = row*floor_height-60+ y_offset
					if levelOrg[row][col] is OBJECT_GOAL:
						DISPLAYSURF.blit(goal, (boxX,boxY+40))
					if player.direction is 'LEFT':
						boxX+= player.moveCounterX
					if player.direction is 'RIGHT':
						boxX-= player.moveCounterX
					if player.direction is 'UP':
						boxY+= player.moveCounterY
					if player.direction is 'DOWN':
						boxY-= player.moveCounterY
					DISPLAYSURF.blit(device, (boxX,boxY))
					if(not player.isMoving()):
						level[row][col] = OBJECT_BOX
							
				if type is OBJECT_BOX:
						DISPLAYSURF.blit(device, (col*floor_width,row*floor_height-60+ y_offset))
	
		if nextLevel or showInstructions or chooseLevel:
			DISPLAYSURF.blit(alphaSurface,(0,0))
			if alpha < 255:
				alpha += 8 
				alphaSurface.set_alpha(alpha) 
			else:
				for tr in textRenders:
					DISPLAYSURF.blit(tr[0], tr[1])

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w or event.key == pygame.K_UP: #move up
					if isOkStep(level,player.x,player.y-1,player.x,player.y-2,levelOrg):
						player.setAni('UP')
						numSteps +=1
				elif event.key == pygame.K_s or event.key == pygame.K_DOWN: #move down
					if isOkStep(level,player.x,player.y+1,player.x,player.y+2,levelOrg):
						player.setAni('DOWN')
						numSteps +=1
				elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: #move right
					if isOkStep(level,player.x+1,player.y,player.x+2,player.y,levelOrg):
						player.setAni('RIGHT')
						numSteps +=1
				elif event.key == pygame.K_a or event.key == pygame.K_LEFT: #move left
					if isOkStep(level,player.x-1,player.y,player.x-2,player.y,levelOrg):
						player.setAni('LEFT')
						numSteps +=1
				elif event.key == pygame.K_c: #mute	
					mute = not mute
				elif event.key == pygame.K_b: #bark			
					player.setAni('BARK')
					playSound(random.choice([sound_dog1, sound_dog2]),mute)
				elif event.key == pygame.K_SPACE: #restart
					setupLevel = True
					playSound(sound_fail,mute)
				elif event.key == pygame.K_x: #next level
					levelIndex +=1
					setupLevel = True
				elif event.key == pygame.K_z: #previous level
					if levelIndex > 0:
						levelIndex -=1
						setupLevel = True
				elif event.key == pygame.K_ESCAPE: #go to menu
					return
				elif event.key == pygame.K_RETURN: #go to next
					nextLevel = False
					setupLevel = True
				elif event.key == pygame.K_v: #go to next
				
					texts  =[]
					texts.append("Instructions: Your goal is to help plush dog finish every level")
					texts.append("by placing all objects on the red dots.")
					texts.append("Try not jamming the objects in to a corner,")
					texts.append("there is no way to get them out of there!")
					texts.append("")
					texts.append("User interface:")
					texts.append("arrows: moves the dog")
					texts.append("esc: ends the game")
					texts.append("space: restarts level")
					texts.append("z: skip one level ahead")
					texts.append("x: choose level")
					texts.append("b: dog barks")
					texts.append("v: toggle instructions on/off")
					texts.append("c: toggle sound on/off")

					textRenders =[]
					
					margin=20
					marginx2 = margin*2
					textOffset=20
					for i,text in enumerate(texts):
						y = margin + (textOffset * i)
						textRenders.append(  (fontObj.render(text,True, WHITE, BLACK),Rect(margin,y,WIDTH-marginx2,100))   )

					alpha= 0
					alphaSurface.set_alpha(0) 	
						
					showInstructions = not showInstructions

			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		fpsClock.tick(FPS)
	
def titleScreen():
	pygame.display.set_caption("plush dog's sokoban ")
	
	while True: # main game loop	
		DISPLAYSURF.blit(titleScreenImg, (0,0))

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					gameLoop()
					pygame.display.set_caption("plush dog's sokoban ")
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		fpsClock.tick(FPS)

if __name__ == '__main__':
	main()

	

