class Player:

	def __init__(self,name,number):
		self.name = name
		self.number = number

		# Stat sheet

		# TwoPointers
		self.twoPointer = 0
		self.twoPointerMade = 0
		# ThreePointers
		self.threePointer = 0
		self.threePointerMade = 0
		# Freethrows
		self.freeThrow = 0
		self.freeThrowMade = 0
		# Rebounds
		self.offensiveRebound = 0
		self.defensiveRebound = 0
		# Block / Steals
		self.block = 0
		self.steal = 0
		# Assist / turnOver
		self.assist = 0
		self.turnOver = 0
		# foul/ playTime
		self.foul = 0



	def shotTwoPointer(self,status):
		# when made, we add to twoPointerMade
		if status == "Made":
			self.twoPointerMade += 1
		self.twoPointer += 1



	def shotThreePointer(self,status):
		# when made, we add to twoPointerMade
		if status == "Made":
			self.threePointerMade += 1
		self.threePointer += 1


	def shotfreeThrow(self,status):
		# when made, we add to twoPointerMade
		if status == "Made":
			self.freeThrowMade += 1
		self.freeThrow += 1

	def getRebound(self,status):
		if status == "Offensive":
			self.offensiveRebound +=1	
		elif status == "Defensive":
			self.defensiveRebound +=1


	def getBlock(self):
		self.block +=1



	def getSteal(self):
		self.steal +=1


	def getAssist(self):
		self.assist +=1


	def getFoul(self):
		self.foul +=1


	def setPlayTime(self,playTime):
		self.playTime = playTime	




