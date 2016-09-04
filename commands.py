#from magiks.specific_geometries.pr2 import skilled_pr2 as spr
from SIMKit import RobotScript, Event
import PyPR2
import time
#import positions
import sys
import random
import math
import logging


numpy_path      = '/usr/lib/python2.7/dist-packages/'
sympy_path      = '/usr/local/lib/python2.7/dist-packages/'
pyinterval_path = '/usr/local/lib/python2.7/dist-packages/pyinterval-1.0b21-py2.7-linux-x86_64.egg/'
mtpltlib_path   = '/usr/lib/pymodules/python2.7'


sys.path.append(sympy_path)
sys.path.append(numpy_path)
sys.path.append(pyinterval_path)
sys.path.append(mtpltlib_path)
sys.path.append('/home/demoshare/shooting_experiment/Magiks/')



counter =1 
s={'l_wrist_roll_joint': -0.0007893761161641422, 'l_forearm_roll_joint': -5.784708695053728e-05, 'l_elbow_flex_joint': -0.1483631860063741, 'l_shoulder_lift_joint': 0.356638539879416, 'l_upper_arm_roll_joint': 0.15967385473500117, 'l_wrist_flex_joint': -0.07863929718151064, 'l_shoulder_pan_joint': 0.0035887617206241673}
right_shooting = {'r_elbow_flex_joint': -1.5668266161421789, 'r_shoulder_lift_joint': -0.07156730494636866, 'r_upper_arm_roll_joint': -1.1195578453851402, 'r_wrist_roll_joint': -3.1823834614790147, 'r_shoulder_pan_joint': -0.3396092818684876, 'r_forearm_roll_joint': -1.5066273796273486, 'r_wrist_flex_joint': -1.5071675013893124}

right_pullback = {'r_elbow_flex_joint': -1.8827163083810365, 'r_shoulder_lift_joint': -0.1377205348140522, 'r_upper_arm_roll_joint': -1.1378382955913073, 'r_wrist_roll_joint': -2.8935712498579074, 'r_shoulder_pan_joint': -0.395405435349739, 'r_forearm_roll_joint': -1.3948668076388655, 'r_wrist_flex_joint': -1.6445253315659132,'time_to_reach' : 0.2}

left_shooting = {'l_wrist_roll_joint': -2.6133570702164812, 'l_forearm_roll_joint': -1.205012668267126, 'l_elbow_flex_joint': -0.4263229518627475, 'l_shoulder_lift_joint': 0.21368677576185252, 'l_upper_arm_roll_joint': 0.7678997111559798, 'l_wrist_flex_joint': -0.09263466648021362, 'l_shoulder_pan_joint': -0.17482627883160928}

right_pullback_alt = {'r_elbow_flex_joint': -2.119271650781721, 'r_shoulder_lift_joint': -0.15269383620354068, 'r_upper_arm_roll_joint': -0.9991313707813558, 'r_wrist_roll_joint': -2.479583875110267, 'r_shoulder_pan_joint': -0.33853149584284675, 'r_forearm_roll_joint': -1.2974523132141216, 'r_wrist_flex_joint': -1.6922546169151684, 'time_to_reach' : 0.5}

best_pullback = {'r_elbow_flex_joint': -2.119561192204488, 'r_shoulder_lift_joint': -0.25683018654512435, 'r_upper_arm_roll_joint': -0.9635325993272411, 'r_wrist_roll_joint': -2.242225981766941, 'r_shoulder_pan_joint': -0.30528594228269534, 'r_forearm_roll_joint': -1.1978974765722068, 'r_wrist_flex_joint': -1.605912838397527, 'time_to_reach' : 0.01}

right_up = {'r_elbow_flex_joint': -2.0722211695820745, 'r_shoulder_lift_joint': -0.35157650042211364, 'r_upper_arm_roll_joint': -0.7414411648049486, 'r_wrist_roll_joint': -2.2757713591637283, 'r_shoulder_pan_joint': -0.2699677232886195, 'r_forearm_roll_joint': -1.0189764366341232, 'r_wrist_flex_joint': -1.7970475243950452,'time_to_reach' : 0.2}



#previous_pos = 0
CONDITION_TAG=0
movement_tracker = []

def arm_back():
	obj1 = spr.Skilled_PR2()
	obj1.larm_reference = False

	obj2 = spr.Skilled_PR2()
	obj2.larm_reference = True
	
	time.sleep(10)
	obj1.arm_back()
	PyPR2.closeGripper(2)
	#obj2.arm_forward(dx=0.03)


def head_hand_follower(hand_joint_list):
	
	

	n = len(hand_joint_list)
	for i in range(0,n):
		PyPR2.moveArmWithJointPos(**hand_joint_list[i])
		x = PyPR2.getArmPose(False)
		(a,b,c) = x['position']
		PyPR2.pointHeadTo("base_footprint",a,b,c)
		time.sleep(5)


def revolve():
	x = random.randint(10,15)
	i = 0
	for i in range(0,x):
		y = PyPR2.getRobotPose()
		(a,b,c) = y['position']
		PyPR2.moveBodyTo(a,b,1.0,10)

def bow_arrow():
	PyPR2.moveArmWithJointPos(**right_shooting)
	PyPR2.moveArmWithJointPos(**left_shooting)
	time.sleep(10)
	PyPR2.closeGripper(2)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**best_pullback)
	time.sleep(1)
	PyPR2.openGripper(2)
	PyPR2.moveArmWithJointPos(**right_up)
		

def onHumanDetected(objtype, trackid, nameid, status):	
	PyPR2.say("hi")
	
	
	

def onHumanTracking(tracking_objs):		
	focus_obj = tracking_objs[0]
	#PyPR2.moveTorsoBy(0.03,5)
	#if abs(previous_pos - focus_obj['est_pos'][0])< 0.1:	
	#	PyPR2.moveHeadTo(0.2,1.0)
	
	if focus_obj['est_pos'][0]<=4 and focus_obj['est_pos'][0] >3:

			if CONDITION_TAG != 1:
				movement_tracker.append(focus_obj['est_pos'])
				CONDITION_TAG = 1
			
			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      			ofs_x = mid_x - 320
      			ofs_y = mid_y - 240
      			chx = chy = 0.0
      			if math.fabs(ofs_x) > 10:
       				chx = -ofs_x * 90.0 / 640 * 0.01745329252
      			if math.fabs(ofs_y) > 10:
        			chy = ofs_y * 90.0 / 640 * 0.01745329252
      				PyPR2.updateHeadPos( chx, chy )
				#previous_pos = focus_obj['est_pos'][0]
			PyPR2.moveArmWithJointPos(**left_shooting)

	elif focus_obj['est_pos'][0]<=3 and focus_obj['est_pos'][0] >2:
			if CONDITION_TAG != 2:
				movement_tracker.append(focus_obj['est_pos'])
				CONDITION_TAG = 2
			
			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      			ofs_x = mid_x - 320
      			ofs_y = mid_y - 240
      			chx = chy = 0.0
      			if math.fabs(ofs_x) > 10:
       				chx = -ofs_x * 90.0 / 640 * 0.01745329252
      			if math.fabs(ofs_y) > 10:
        			chy = ofs_y * 90.0 / 640 * 0.01745329252
      				PyPR2.updateHeadPos( chx, chy )
			PyPR2.moveArmWithJointPos(**right_shooting)
				#previous_pos = focus_obj['est_pos'][0]		        			
		
	elif focus_obj['est_pos'][0] <2:
			if CONDITION_TAG != 3:
				movement_tracker.append(focus_obj['est_pos'])
				CONDITION_TAG = 3
				
      			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      			ofs_x = mid_x - 320
      			ofs_y = mid_y - 240
      			chx = chy = 0.0
      			if math.fabs(ofs_x) > 10:
       				chx = -ofs_x * 90.0 / 640 * 0.01745329252
      			if math.fabs(ofs_y) > 10:
        			chy = ofs_y * 90.0 / 640 * 0.01745329252
      				PyPR2.updateHeadPos( chx, chy )
			PyPR2.moveArmWithJointPos(**right_pullback_alt)	
				#previous_pos = focus_obj['est_pos'][0]	
	else:
			if CONDITION_TAG != 4:
				movement_tracker.append(focus_obj['est_pos'])
				CONDITION_TAG = 4
			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      			ofs_x = mid_x - 320
      			ofs_y = mid_y - 240
      			chx = chy = 0.0
      			if math.fabs(ofs_x) > 10:
       				chx = -ofs_x * 90.0 / 640 * 0.01745329252
      			if math.fabs(ofs_y) > 10:
        			chy = ofs_y * 90.0 / 640 * 0.01745329252
      				PyPR2.updateHeadPos( chx, chy )			

	   

	
		


