class PydogLevel:
	def __init__(self):
		self.lines = [line.rstrip('\n') for line in open('data/level.data')]

	def numLevels(self):
		currentIndex = 0
		for val in self.lines:		
			if len(val)<2:
				currentIndex+=1
		return currentIndex
			
	def getLevel(self, index):
		result=[]		
		currentIndex = 0
		for i,val in enumerate(self.lines):	
			if index == currentIndex:		
				if '#' in val:
					result.append(list(val))
				if len(val)<2:
					break
			if len(val)<2:
				currentIndex+=1

		return result