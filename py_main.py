from SIMKit import RobotScript, Event
import PyPR2
import time
import commands
import iksresolver
import rospy
from std_msgs.msg import String
import detection
import door_block


iksResolver = None


csvFile = "/home/demoshare/sid_stuff/aggressiveBehaviourExperiment/test1_"+str(time.time())+".csv"
#csvFileCounter = 1

def main():
  
	global iksResolver, csvFile,csvFileCounter
  	iksResolver = iksresolver.IKSResolver()

'''
  	while csvLength(csvFile) > 0:
  		counter +=1
  		csvFile = "/home/demoshare/sid_stuff/aggresiveBehaviourExperiment/test"+str(csvFileCounter)+".csv"
'''

  	#PyPR2.registerHumanDetectTracking(door_block.onHumanDetected,door_block.onHumanTracking)

def csvLength(csv):
		
		with open(csv,"r") as f:
			reader = csv.reader(f,delimiter = ',')
			data = list(reader)
			row_count = len(data)
			return row_count