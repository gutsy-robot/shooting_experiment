#from SIMKit import RobotScript, Event
import PyPR2
import time
import positions
import sys
import random
import math
import logging
import csv
import operator
'''import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
'''
numpy_path      = '/usr/lib/python2.7/dist-packages/'
sympy_path      = '/usr/local/lib/python2.7/dist-packages/'
pyinterval_path = '/usr/local/lib/python2.7/dist-packages/pyinterval-1.0b21-py2.7-linux-x86_64.egg/'
mtpltlib_path   = '/usr/lib/pymodules/python2.7'


sys.path.append(sympy_path)
sys.path.append(numpy_path)
sys.path.append(pyinterval_path)
sys.path.append(mtpltlib_path)
sys.path.append('/home/demoshare/shooting_experiment/Magiks/')

HUMAN_COUNTER=0
no_objTracker = []


speechCommands = ["The exit is closed, take the other exit", "The construction, Building 2 is underway, take the other exit", "Move Back"]
st_time = time.time()
a=0
b=0
msgTryTimer = -1

initial_left = {'l_wrist_roll_joint': -0.03343445889223928, 'l_forearm_roll_joint': -1.4370226053672253, 'l_elbow_flex_joint': -1.9698682766339202, 'l_shoulder_lift_joint': 0.9258433754370239, 'l_upper_arm_roll_joint': 0.09899174423834634, 'l_wrist_flex_joint': -0.09503205735655162, 'l_shoulder_pan_joint': 0.10351215896157584,'time_to_reach': 0.3}


initial_right = {'r_elbow_flex_joint': -1.9779754364713977, 'r_shoulder_lift_joint': 0.8400971960934513, 'r_upper_arm_roll_joint': 0.48404005289988583, 'r_wrist_roll_joint': -0.3022365274589296, 'r_shoulder_pan_joint': 0.2276671985198463, 'r_forearm_roll_joint': -1.224321618205765, 'r_wrist_flex_joint': -0.09133131041169806,'time_to_reach':0.3}



second_left = {'l_wrist_roll_joint': -0.031868137768653826, 'l_forearm_roll_joint': -1.4370226053672253, 'l_elbow_flex_joint': -1.7327338513877018, 'l_shoulder_lift_joint': 0.917299288203474, 'l_upper_arm_roll_joint': 0.3478624347644097, 'l_wrist_flex_joint': -0.12801181879204448, 'l_shoulder_pan_joint': 0.8335878314071925,'time_to_reach':0.3}

second_right = {'r_elbow_flex_joint': -1.9465601921011721, 'r_shoulder_lift_joint': 0.8025370502350734, 'r_upper_arm_roll_joint': 0.5132246312992053, 'r_wrist_roll_joint': -0.3050646072654031, 'r_shoulder_pan_joint': -0.42696345213091336, 'r_forearm_roll_joint': -1.2249579361622214, 'r_wrist_flex_joint': -0.10051169255271242,'time_to_reach':0.3}



full_stretch_left = {'l_wrist_roll_joint': -2.110637322287075, 'l_forearm_roll_joint': -6.319143202733678, 'l_elbow_flex_joint': -0.22147239525505558, 'l_shoulder_lift_joint': 0.11161724055664769, 'l_upper_arm_roll_joint': 0.3249316945935157, 'l_wrist_flex_joint': -0.07928182828049879, 'l_shoulder_pan_joint': 1.6414299109336616,'time_to_reach':0.3}

full_stretch_right = {'r_elbow_flex_joint': -0.2858953618207254, 'r_shoulder_lift_joint': -0.008643667413542395, 'r_upper_arm_roll_joint': 0.6464794920125809, 'r_wrist_roll_joint': -0.15134759255353547, 'r_shoulder_pan_joint': -1.3345421923378364, 'r_forearm_roll_joint': -1.8746385697039665, 'r_wrist_flex_joint': -0.09046113200970607,'time_to_reach':0.3}



movementCounter = 0.0

track_y = []
def onHumanDetected(objtype, nameid, trackid, status):
	PyPR2.moveTorsoBy(0.1,2)
	PyPR2.say("This exit is closed")



def onHumanTracking(tracking_objs):
 	global HUMAN_COUNTER, st_time,a,b, msgTryTimer,x,y
 
	#focus_obj = tracking_objs[object_inde x]
	
	
 	if len(tracking_objs) == 0:
		if HUMAN_COUNTER !=0:
			PyPR2.removeTimer(msgTryTimer)
			#msgTryTimer = -1
			st_time = time.time()
			HUMAN_COUNTER =0
			
		
			

 	elif len(tracking_objs) > 0:
		if HUMAN_COUNTER ==0:
			
			PyPR2.onTimer = timerActions
			msgTryTimer = PyPR2.addTimer(1,-1,2)
			a +=1
			elapsed_time = time.time() - st_time
			no_objTracker.append(elapsed_time)
			HUMAN_COUNTER= len(tracking_objs)
			
		object_index = closest_obj_index(tracking_objs)
		focus_obj = tracking_objs[object_index]


		x = focus_obj['est_pos'][0]
		y = focus_obj['est_pos'][1]
		
#		track_y.append(y)
	
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
		

		if x>3.5:
			PyPR2.moveArmWithJointPos(**initial_left)
			PyPR2.moveArmWithJointPos(**initial_right)

		elif 2.5<x<3.5:
			PyPR2.moveArmWithJointPos(**second_left)
			PyPR2.moveArmWithJointPos(**second_right)
		else:
			PyPR2.moveArmWithJointPos(**full_stretch_left)
			PyPR2.moveArmWithJointPos(**full_stretch_right)


previous_position =0.0
isMovingForward = False
def timerActions(id):
	global msgTryTimer,x,y,d, previous_position,movementCounter,b
	b+=1

		
	if previous_position > x:
			isMovingForward = False
			previous_position = x
	else:
			isMovingForward = True
			previous_position = True
	
	if msgTryTimer == id :
		if isMovingForward == True:
			PyPR2.say("Move, Back")
		else:
			PyPR2.say("going back,,, goood")

		#if abs(y) >0.3:
		if abs(movementCounter)< 0.3:
				track_y.append(y)	
				movementCounter +=y
				PyPR2.moveBodyTo(0.0,y,0.0,2.0)

		#adjust_to_shooting()
		

last_proximity = False
def adjust_to_shooting():
	global last_proximity
	proximity = check_head_proximity()

	if proximity== True and last_proximity==False:
		PyPR2.moveBodyTo(0.0,0.0,(0.65)*PyPR2.getHeadPos()[0],1)

def closest_obj_index(tracking_objs):
	A=[]
	for i in range(0,len(tracking_objs)):
		A.append(math.sqrt(math.pow(tracking_objs[i]['est_pos'][0],2)+math.pow(tracking_objs[i]['est_pos'][1],2)))
	index_min = min(xrange(len(A)), key=A.__getitem__)
	return index_min


def check_head_proximity():
	(a,b) = PyPR2.getHeadPos()
	if a>0.6 or a<-0.6:
		return True
	else:
		return False
	
