# Datetime in py
import datetime
import time

class PlayerTimes:
	def __init__(self):
		self.checkInTime = None
		self.checkOutTime = None
		self.times = []
	
	def setCheckInTime(self):
		self.checkInTime = datetime.datetime.now()

	
	def setCheckOutTime(self):
		if self.checkInTime:
			self.checkOutTime = datetime.datetime.now()
			# when we set checkout time, we get time delta, and then reset
			self.getTimeDelta()
		else:
			print("Check in time not set")


	def getTimeDelta(self):
		if self.checkInTime and self.checkOutTime:
			time_delta = self.checkOutTime - self.checkInTime
			secs = time_delta.seconds
			print(f"Time delta is a total of {secs} secs")
			self.times.append(secs)
			# reset to None
			self.checkInTime = None
			self.checkOutTime = None
	
	def printTimes(self):
		print(self.times)


# worked 
pt = PlayerTimes()
pt.setCheckInTime()
print("Sleeping for 10s")
time.sleep(10)
pt.setCheckOutTime()

pt.setCheckInTime()
print("Sleeping for 2s")
time.sleep(2)
pt.setCheckOutTime()

pt.printTimes()

