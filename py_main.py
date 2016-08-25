from SIMKit import RobotScript, Event
import PyPR2
import time
import commands
import iksresolver
import rospy
from std_msgs.msg import String
import detection


iksResolver = None




def main():
  
	global iksResolver
  	iksResolver = iksresolver.IKSResolver()

	

