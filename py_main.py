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

	pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
          hello_str = "hello world %s" % rospy.get_time()
          rospy.loginfo(hello_str)
          pub.publish(hello_str)
          rate.sleep()
