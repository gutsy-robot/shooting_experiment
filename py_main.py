from SIMKit import RobotScript, Event
import PyPR2
import time
import commands
import iksresolver
import rospy
from std_msgs.msg import String



iksResolver = None




def main():
  
	global iksResolver
  	iksResolver = iksresolver.IKSResolver()

	time.sleep(10)
	PyPR2.openGripper(1)
	time.sleep(10)
	PyPR2.closeGripper(1)
