class PydogLevel:
	def __init__(self):
		self.lines = [line.rstrip('\n') for line in open('data/level.data')]

	def getLevel(self, index):
		result=[]		
		currentIndex = 0
	
		for val in self.lines:		
			if index is currentIndex:
				if '#' in val:
					result.append(list(val))
				if len(val)<2:
					break
			if len(val)<2:
					currentIndex+=1
			
		#for val in result:	
		#	print val
			
		return result