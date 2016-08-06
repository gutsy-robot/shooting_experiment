from SIMKit import RobotScript, Event
import PyPR2


class commands:
	def __init__(self,sc):
		self.script= sc
	

	def play(self):
		self.script.play()


		
