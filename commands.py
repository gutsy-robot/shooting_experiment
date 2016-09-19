from magiks.specific_geometries.pr2 import skilled_pr2 as spr
from SIMKit import RobotScript, Event
import PyPR2
import time
import positions
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




s= positions.s
right_shooting = positions.right_shooting

right_pullback = positions.right_pullback

left_shooting = positions.left_shooting

right_pullback_alt = positions.right_pullback_alt
best_pullback = positions.best_pullback

right_up = positions.right_up
alt_right_shooting = positions.alt_right_shooting

alt_right_release = positions.alt_right_release
alt_right_intermediate = positions.alt_right_intermediate

left_refill = 	positions.left_refill

right_refill = positions.right_refill

right_pick = positions.right_pick
right_pick_further = positions.right_pick_further
left_pick_further= positions.left_pick_further
left_intermediate = positions.left_intermediate
left_last = positions.left_last



l2 = positions.l2

r2 = positions.r2


#a = {'r_elbow_flex_joint': -0.516515105054685, 'r_shoulder_lift_joint': -0.35132271565280027, 'r_upper_arm_roll_joint': 0.4847921924455716, 'r_wrist_roll_joint': -2.8233311186171237, 'r_shoulder_pan_joint': -0.15820960309140264, 'r_forearm_roll_joint': -3.178176804150745, 'r_wrist_flex_joint': -1.7377080510592138}
#b= {'l_wrist_roll_joint': -3.062191134607524, 'l_forearm_roll_joint': -0.8025704843520763, 'l_elbow_flex_joint': -1.6901712622409446, 'l_shoulder_lift_joint': 0.30225766025221656, 'l_upper_arm_roll_joint': 1.1533927137491862, 'l_wrist_flex_joint': -0.08264695215512896, 'l_shoulder_pan_joint': 0.42176973966926046}

#left_current = {'l_wrist_roll_joint': -2.5708187337191086, 'l_forearm_roll_joint': -1.2180861099179523, 'l_elbow_flex_joint': -1.6573083107568838, 'l_shoulder_lift_joint': 0.6408911374393484, 'l_upper_arm_roll_joint': 1.1389607793758965, 'l_wrist_flex_joint': -0.07641030173640845, 'l_shoulder_pan_joint': 0.16094552146418317}




#right_current = {'r_elbow_flex_joint': -0.5144883150953158, 'r_shoulder_lift_joint': -0.16377577113022426, 'r_upper_arm_roll_joint': 0.48463183761920137, 'r_wrist_roll_joint': -2.8072093903002204, 'r_shoulder_pan_joint': -0.4293142418487461, 'r_forearm_roll_joint': -3.3093739973546157, 'r_wrist_flex_joint': -1.7845805453665076}
left_match = positions.left_match


right_match = positions.right_match

left_relax1 = positions.left_relax1

left_relax2 = positions.left_relax2


#previous_pos = 0
CONDITION_TAG = positions.CONDITION_TAG 
movement_tracker = positions.movement_tracker
track_x = positions.track_x
track_y = positions.track_y
diff_min = positions.diff_min

HUMAN_DETECTION_COUNTER = positions.HUMAN_DETECTION_COUNTER


revolve_counter= positions.revolve_counter
torso_position_counter = positions.torso_position_counter
last_action_counter = positions.last_action_counter
sub_action_flag = positions.sub_action_flag


def revolve_cw():
	(a,b)= PyPR2.getHeadPos()
	#PyPR2.say("searching")
	PyPR2.moveHeadTo(a+0.3,0.0)

def revolve_acw():
	(a,b) = PyPR2.getHeadPos()
	#PyPR2.say("searching")
	PyPR2.moveHeadTo(a-0.3,0.0)




def find_human():
	
	global HUMAN_DETECTION_COUNTER,revolve_counter
	while revolve_counter==1 and PyPR2.getHeadPos()[0]<1.5 and HUMAN_DETECTION_COUNTER==0:
			
	
			revolve_cw()
		

	
	while revolve_counter==-1 and PyPR2.getHeadPos()[0]>-1.5 and HUMAN_DETECTION_COUNTER==0:
	
			revolve_acw()

	while PyPR2.getHeadPos()[0] >1.2 and HUMAN_DETECTION_COUNTER==0:

			revolve_counter = -1
			revolve_acw()
			find_human()

		
	while PyPR2.getHeadPos()[0] <-1.2 and HUMAN_DETECTION_COUNTER==0:
		
			revolve_counter = 1
			revolve_cw()
			find_human()


		
	if HUMAN_DETECTION_COUNTER!=0:
		PyPR2.say("Target Detected")

	
		
		
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



def bow_arrow():
	PyPR2.moveArmWithJointPos(**right_shooting)
	PyPR2.moveArmWithJointPos(**left_shooting)
	PyPR2.moveHeadTo(0.0,0.14)
	time.sleep(10)
	PyPR2.closeGripper(2)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**best_pullback)
	PyPR2.moveHeadto(0.0,0.0)
	time.sleep(10)
	PyPR2.openGripper(2)
	PyPR2.moveArmWithJointPos(**right_up)
	
def onHumanDetected(objtype, trackid, nameid, status):	
	global HUMAN_DETECTION_COUNTER,start_time,torso_position_counter
	#PyPR2.say("Target Detect ed")
	#PyPR2.moveTorsoBy(0.1,3)
	#PyPR2.moveBodyTo(0.1,0.0,0.0,4)
	HUMAN_DETECTION_COUNTER+=1
	start_time = time.time()
	if torso_position_counter ==0:
		PyPR2.moveTorsoBy(0.1,3)
		torso_position_counter +=1
	#isStationery()
	
	

def onHumanTracking(tracking_objs):
	
	SHOOTING_TAG = 0
	global start_time,last_action_counter,movement_tracker
	
	
	movement_tracker.append(last_action_counter)
	focus_obj = tracking_objs[0]
	d = math.sqrt(math.pow(focus_obj['est_pos'][0],2)+math.pow(focus_obj['est_pos'][1],2))
	#track_human(focus_obj)
	mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			
	mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
     			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      	ofs_x = mid_x - 320
      	ofs_y = mid_y - 240
      	chx = chy = 0.0
			
      	if math.fabs(ofs_x) > 10:
       		chx = -ofs_x * 90.0 / 640 * 0.01745329252	
				#head_yaw_list.append(chx)
				
      	if math.fabs(ofs_y) > 10:
        	chy = ofs_y * 90.0 / 640 * 0.01745329252
      		PyPR2.updateHeadPos( chx, chy )

	elapsed_time = time.time() - start_time
	track_x.append((focus_obj['est_pos'][0],elapsed_time))
	track_y.append((focus_obj['est_pos'][1],elapsed_time))
	adjust_to_shooting(chy)
	#PyPR2.moveTorsoBy(0.03,5)
	#if abs(previous_pos - focus_obj['est_pos'][0])< 0.1:	
	#	PyPR2.moveHeadTo(0.2,1.0)
	#adjust_to_shooting()
	if d>=4:
		if last_action_counter <4:
			#obj.larm_reference = True	
			#obj.arm_down()
			PyPR2.say("Move Back")
			last_action_counter=4
		elif last_action_counter == 4:		
			PyPR2.moveBodyTo(0.07,0.0,0.0,0.51)
			last_action_counter=4
			
		else:		
			PyPR2.moveArmWithJointPos(**left_shooting)
			last_action_counter=4
	elif d<=4 and d>3:
		if last_action_counter <3:
				PyPR2.say("Move")
				#obj.larm_reference = False
				#obj.arm_right()
				#PyPR2.moveBodyTo(0.01,0.0,0.0,1)
				last_action_counter=3
		elif last_action_counter ==3:
				PyPR2.moveBodyTo(0.07,0.0,0.0,0.51)
				last_action_counter = 3

		else:
				PyPR2.moveArmWithJointPos(**alt_right_shooting)
				PyPR2.moveArmWithJointPos(**left_shooting)
				last_action_counter=3		
				#adjust_to_shooting()
			
			
			
			#PyPR2.moveBodyTo(0.1,0.0,0.0,1)
				#PyPR2.moveBodyTo(0.0,0.0,chx/2.0,2)
				#previous_pos = focus_obj['est_pos'][0]
			#PyPR2.moveArmWithJointPos(**left_shooting)	
			#PyPR2.moveArmWithJointPos(**alt_right_intermediate)	
			#PyPR2.moveBodyTo(0.2,0.0,0.0,1)		
	              
				

	elif d<=3 and d >2:
			
				if last_action_counter <2:
					
					#obj.larm_reference = False
					#obj.arm_right()
					last_action_counter=2
				elif last_action_counter ==2 :
					PyPR2.say("Move Back")	
					last_action_counter =2 
				else:
					PyPR2.moveArmWithJointPos(**alt_right_shooting)
					PyPR2.moveArmWithJointPos(**left_shooting)
					PyPR2.closeGripper(2)
					last_action_counter =2
			

				#previous_pos = focus_obj['est_pos'][0]
				
	                #movement_tracker.append(str(CONDITION_TAG)+":"+str(focus_obj['est_pos']))
	elif focus_obj['est_pos'][0] <2:

			if last_action_counter ==1:
					PyPR2.say("Move")
					last_action_counter=1 
			
			else:
				PyPR2.closeGripper(2)
				PyPR2.moveArmWithJointPos(**best_pullback)
				time.sleep(2)
				PyPR2.openGripper(2)
				PyPR2.moveArmWithJointPos(**right_release)
				last_action_counter=1	
      			
			'''
			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			
	
	                #movement_tracker.append(str(CONDITION_TAG)+":"+str(focus_obj['est_pos']))'''
			#PyPR2.closeGripper(2)
			#time.sleep(2)
			#PyPR2.moveHeadTo(0.0,0.18)
			#PyPR2.moveArmWithJointPos(**best_pullback)
	
	
			#time.sleep(3)
			#PyPR2.moveHeadTo(0.0,0.1)
			#PyPR2.openGripper(2)
			#PyPR2.moveHeadTo(0.0,0.0)
			#PyPR2.moveArmWithJointPos(**alt_right_release)

	
			
	   

	
def reset():
	global CONDITION_TAG, movement_tracker
	movement_tracker = []
	CONDITION_TAG = 0

def onWaitedMeanHumanTracking(tracking_objs):
	#global objects
			
	a = len(tracking_objs)
	mid_x = 0
	mid_y = 0
	for i in range(0,a):
		mid_x += tracking_objs[i]['bound'][0] + tracking_objs[i]['bound'][2] / 2
		mid_y += tracking_objs[i]['bound'][1] + tracking_objs[i]['bound'][3] / 2
		
		ofs_x = mid_x - 320
      		ofs_y = mid_y - 240
      		chx = chy = 0.0
			
 		if math.fabs(ofs_x) > 10:
       			chx = -ofs_x * 90.0 / 640 * 0.01745329252	
				#head_yaw_list.append(chx)
				
      		if math.fabs(ofs_y) > 10:
        		chy = ofs_y * 90.0 / 640 * 0.01745329252
      			PyPR2.updateHeadPos( chx, chy )	
	

def alt_bow_arrow():
	PyPR2.openGripper(2)
	PyPR2.moveHeadTo(0.0,0.15)
	PyPR2.moveArmWithJointPos(**left_shooting)
	PyPR2.openGripper(2)
	time.sleep(2)
	PyPR2.moveHeadTo(0.0,0.0)
	PyPR2.moveArmWithJointPos(**alt_right_intermediate)
	PyPR2.moveHeadTo(0.0,0.3)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**alt_right_shooting)
	time.sleep(5)
	PyPR2.closeGripper(2)
	time.sleep(2)
	PyPR2.moveHeadTo(0.0,0.18)
	PyPR2.moveArmWithJointPos(**best_pullback)
	
	
	time.sleep(5)
	PyPR2.moveHeadTo(0.0,0.1)
	PyPR2.openGripper(2)
	PyPR2.moveHeadTo(0.0,0.0)
	PyPR2.moveArmWithJointPos(**alt_right_release)

	
	#time.sleep(3)
	




def refill():
	PyPR2.moveArmWithJointPos(**left_intermediate)
	PyPR2.moveHeadTo(0.1,0.3)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**right_refill)
	PyPR2.moveHeadTo(-0.7,0.3)
	time.sleep(3)
	PyPR2.moveHeadTo(-0.2,0.3)
	PyPR2.moveArmWithJointPos(**left_refill)
	time.sleep(4)
	PyPR2.moveArmWithJointPos(**right_pick)
	PyPR2.moveHeadTo(-0.2,0.19)
	time.sleep(2)
	PyPR2.closeGripper(2)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**right_pick_further)
	time.sleep(2)
	PyPR2.moveArmWithJointPos(**left_pick_further)
	time.sleep(4)
	PyPR2.moveArmWithJointPos(**r2)
	PyPR2.moveArmWithJointPos(**l2)


def close():
	time.sleep(10)
	PyPR2.openGripper(1)
	time.sleep(10)
	PyPR2.closeGripper(1)

def play():
	time.sleep(4)
	alt_bow_arrow()
	time.sleep(3)
	refill()
	

def check_head_proximity():
	(a,b) = PyPR2.getHeadPos()
	if a>0.3 or a<-0.3:
		return True
	else:
		return False

def adjust_to_shooting(y):
	if check_head_proximity() == True:
		PyPR2.moveBodyTo(0.0,0.0,(0.65)*PyPR2.getHeadPos()[0],1)
		PyPR2.moveHeadTo(0.0,y)

def track_human(focus_obj):
			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      			ofs_x = mid_x - 320
      			ofs_y = mid_y - 240
      			chx = chy = 0.0
			
      			if math.fabs(ofs_x) > 10:
       				chx = -ofs_x * 90.0 / 640 * 0.01745329252	
				#head_yaw_list.append(chx)
				
      			if math.fabs(ofs_y) > 10:
        			chy = ofs_y * 90.0 / 640 * 0.01745329252
      				PyPR2.updateHeadPos( chx, chy )


def isStationery():
	global track_x,track_y
	if len(track_x) >10 and len(track_y) >10:
		a = track_x[-1][0]
		for i in range(2,10):
			b = track_x[-i][0]
			if (a-b) > diff_min:
				return False

		return True


			
