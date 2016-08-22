import time 
from SIMKit import RobotScript, Event

import positions



left_home = {'l_wrist_roll_joint': -1.4839826438312786, 'l_forearm_roll_joint': 0.09411721046856195, 'l_elbow_flex_joint': -1.6020058990083763, 'l_shoulder_lift_joint': 0.9999119910946541, 'l_upper_arm_roll_joint': 0.050311863150738656, 'l_wrist_flex_joint': -0.09739164174443621, 'l_shoulder_pan_joint': 0.7000872541366616}


right_home = {'r_elbow_flex_joint': -1.904287144377182, 'r_shoulder_lift_joint': 0.996697384016685, 'r_upper_arm_roll_joint': 0.0316294531242729, 'r_wrist_roll_joint': -1.4867103184375225, 'r_shoulder_pan_joint': -0.6982633085548079, 'r_forearm_roll_joint': 0.10296781477199769, 'r_wrist_flex_joint': -0.08803722392302316}



right_pose1 = {'r_elbow_flex_joint': -1.604287144377182, 'r_shoulder_lift_joint': 0.996697384016685, 'r_upper_arm_roll_joint': 0.0316294531242729, 'r_wrist_roll_joint': -1.4867103184375225, 'r_shoulder_pan_joint': 0.0008, 'r_forearm_roll_joint': 0.10296781477199769, 'r_wrist_flex_joint': -0.08803722392302316}


left_pose1 = {'l_wrist_roll_joint': -0.08643262131220664, 'l_forearm_roll_joint': -1.734371360951705, 'l_elbow_flex_joint': -1.683367038805919, 'l_shoulder_lift_joint': 1.2484518751755418, 'l_upper_arm_roll_joint': 1.7890392454794153, 'l_wrist_flex_joint': -0.09656497226254357, 'l_shoulder_pan_joint': 0.060213981375445536}


right_pose2 = {'r_elbow_flex_joint': -1.6043222303905127, 'r_shoulder_lift_joint': 1.2964171965757678, 'r_upper_arm_roll_joint': 0.0316294531242729, 'r_wrist_roll_joint': -1.4867103184375225, 'r_shoulder_pan_joint': -2.1347862674993, 'r_forearm_roll_joint': 0.10296781477199769, 'r_wrist_flex_joint': -0.08803722392302316}


left_pose2 = {'l_wrist_roll_joint': -0.08643262131220619, 'l_forearm_roll_joint': -1.734371360951705, 'l_elbow_flex_joint': -1.683367038805919, 'l_shoulder_lift_joint': 1.1879665051558568, 'l_upper_arm_roll_joint': 1.4078758231981956, 'l_wrist_flex_joint': -0.10091586427250354, 'l_shoulder_pan_joint': -0.3637704597881797}


right_pose3 = {'r_elbow_flex_joint': -1.2138756217891382, 'r_shoulder_lift_joint': 0.7701521799429554, 'r_upper_arm_roll_joint': -0.5948768535028726, 'r_wrist_roll_joint': -2.8705115222051223, 'r_shoulder_pan_joint': -2.1347862674993, 'r_forearm_roll_joint': 1.76069178551421, 'r_wrist_flex_joint': -0.4688708015547729}

left_pose3 = {'l_wrist_roll_joint': -0.08643262131220619, 'l_forearm_roll_joint': -1.734371360951705, 'l_elbow_flex_joint': -1.683367038805919, 'l_shoulder_lift_joint': 1.1879665051558568, 'l_upper_arm_roll_joint': 1.4078758231981956, 'l_wrist_flex_joint': -0.10091586427250354, 'l_shoulder_pan_joint': -0.3637704597881797}

left_home_position = {'l_wrist_roll_joint': -0.0007893761161641422, 'l_forearm_roll_joint': -5.784708695053728e-05, 'l_elbow_flex_joint': -0.1483631860063741, 'l_shoulder_lift_joint': 0.0356638539879416, 'l_upper_arm_roll_joint': 0.15967385473500117, 'l_wrist_flex_joint': -0.07863929718151064, 'l_shoulder_pan_joint': 0.0035887617206241673}

right_home_position={'r_elbow_flex_joint': 0.0, 'r_shoulder_lift_joint': 0.0, 'r_upper_arm_roll_joint': 0.0, 'r_wrist_roll_joint': 0.0, 'r_shoulder_pan_joint': 0.0, 'r_forearm_roll_joint': 0.0, 'r_wrist_flex_joint': 0.0}

def launch():
	PyPR2.moveTorsoBy(0.2,7)
	time.sleep(10)
	
	PyPR2.moveArmWithJointPos(**right_home)
	PyPR2.moveArmWithJointPos(**left_home)
	time.sleep(4)
	PyPR2.say("Hi, Gutsy is ready to get Clicked")
	PyPR2.tuckBothArms()
	time.sleep(4)
	PyPR2.say("are you ready?")
	time.sleep(15)
	PyPR2.moveArmWithJointPos(**right_pose1)
	PyPR2.moveArmWithJointPos(**left_pose1)
	time.sleep(3)
	PyPR2.say(" lets intro duce our selves")
	PyPR2.openGripper(2)
	PyPR2.say("Hand shake ?")
	time.sleep(3)
	PyPR2.setGripperPosition(2,0.03)	
	time.sleep(4)
	PyPR2.moveArmWithJointPos(**right_pose3)
	PyPR2.moveArmWithJointPos(**left_pose3)	
	time.sleep(3)
	PyPR2.say("What's outside, lets find out")
	time.sleep(6)
	PyPR2.moveHeadTo(-1.50,0.2,False)
	PyPR2.closeGripper(2)
	time.sleep(2)
	PyPR2.openGripper(2)
	PyPR2.say("Give me a ball")
	time.sleep(4)
	PyPR2.closeGripper(2)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**left_home_positon)
	time.sleep(2)
	PyPR2.openGripper(2)
	time.sleep(3)
	gun_launch()






def gun_launch():

	PyPR2.moveArmWithJointPos(**right_home_position)
	PyPR2.moveArmWithJointPos(**left_home_position)
	time.sleep(3)
	PyPR2.say("Give me a Gun!!")
	PyPR.openGripper(2)
	time.sleep(5)
	PyPR2.closeGripper(2)
	PyPR2.moveArmWithJointPos(**right_success)
	PyPR2.moveArmWithJointPos(**left_success)
	
	


	
	
