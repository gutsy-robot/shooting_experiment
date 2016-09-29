#from magiks.specific_geometries.pr2 import skilled_pr2 as spr
from SIMKit import RobotScript, Event
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




s= positions.s
right_shooting = positions.right_shooting

right_pullback = positions.right_pullback

left_shooting = positions.left_shooting

right_pullback_alt = positions.right_pullback_alt
best_pullback_right = positions.best_pullback_right

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
shooting_down = positions.shooting_down
shooting_down_back = positions.shooting_down_back
right_high_five = positions.right_high_five




l2 = positions.l2

r2 = positions.r2


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
track_d = [('time','x','y')]

HUMAN_DETECTION_COUNTER = positions.HUMAN_DETECTION_COUNTER


revolve_counter= 1
torso_position_counter = 0
last_action_counter = 0
sub_action_flag =1 
csvfile = "/home/demoshare/shooting_experiment/test12.csv"



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
				adjust_to_shooting(PyPR2.getHeadPos()[1])


		
	
		

	
		
		



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
	if HUMAN_DETECTION_COUNTER==0:
	
		track_x.append(('x','time'))
	HUMAN_DETECTION_COUNTER+=1
	start_time = time.time()
	if torso_position_counter ==0:
		PyPR2.moveTorsoBy(0.1,3)
		torso_position_counter +=1
	#isStationery()
	
busymoving=0	

def onHumanTracking(tracking_objs):
	global busymoving
	SHOOTING_TAG = 0
	global start_time,last_action_counter,movement_tracker
	
	
	object_index = closest_obj_index(tracking_objs)
	focus_obj = tracking_objs[object_index]
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
	adjust_to_shooting(chy)
	elapsed_time = time.time() - start_time
	track_x.append(focus_obj['est_pos'][0])
	track_y.append(focus_obj['est_pos'][1])
	track_d.append((elapsed_time,focus_obj['est_pos'][0],focus_obj['est_pos'][0]))
	with open(csvfile, "w") as output:
   		 writer = csv.writer(output, lineterminator='\n')
    	         writer.writerows(track_d)

	
	#PyPR2.moveTorsoBy(0.03,5)
	#if abs(previous_pos - focus_obj['est_pos'][0])< 0.1:	
	#	PyPR2.moveHeadTo(0.2,1.0)
	#adjust_to_shooting()
        if busymoving>0: busymoving-=1

	if busymoving==0 and d>=3.5:
		if last_action_counter <4 and last_action_counter!=0:
			#obj.larm_reference = True	
			#obj.arm_down()
			
			PyPR2.moveArmWithJointPos(**right_high_five)
			PyPR.moveArmWithJointPos(**shooting_back_down)
			last_action_counter=4
			#busymoving=3
		elif last_action_counter == 4:		
			PyPR2.moveTorsoBy(0.1,2)
			
			PyPR2.say("Move Back")
			busymoving=5

			
		else:		
			PyPR2.moveArmWithJointPos(**left_shooting)
			last_action_counter=4
			#busymoving=5
	elif busymoving==0 and  d<=3.5 and d>3:
		if last_action_counter <3 and last_action_counter!=0:
				PyPR2.moveArmWithJointPos(**shooting_down)
				#obj.larm_reference = False
				#obj.arm_right()
				#PyPR2.moveBodyTo(0.01,0.0,0.0,1)
				last_action_counter=3
				
		elif last_action_counter ==3:
				PyPR2.moveBodyTo(0.07,0.0,0.0,0.51)
				busymoving=10

		elif last_action_counter ==0:
			PyPR2.moveArmWithJointPos(**left_shooting)
			PyPR2.moveArWithJointPos(**alt_right_shooting)
			busymoving=10
			PyPR2.say("Move Back")
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
	              
				

	elif busymoving==0 and d<=3 and d >2:
			
				if last_action_counter <2 and last_action_counter!=0:
					
					#obj.larm_reference = False
					#obj.arm_right()
					PyPR2.moveArmWithJointPos(**left_relax1)
					last_action_counter=2
				#elif last_action_counter==0:

				else:
					PyPR2.moveArmWithJointPos(**alt_right_shooting)
					PyPR2.moveArmWithJointPos(**left_shooting)
					PyPR2.closeGripper(2)
					#PyPR2.closeGripper(2)
					last_action_counter =2
			

				#previous_pos = focus_obj['est_pos'][0]
				
	                #movement_tracker.append(str(CONDITION_TAG)+":"+str(focus_obj['est_pos']))
	elif busymoving==0 and  d <2 and d>1 :

			if last_action_counter ==1:
					PyPR2.say("Move")
					last_action_counter=1 
					busymoving=10
			elif last_action_counter >=2:
					PyPR2.moveArmWithJointPos(**left_shooting)
					PyPR2.moveArmWithJointPos(**alt_right_shooting)
					

			#PyPR2.closeGripper(2)
			#time.sleep(2)
			#PyPR2.moveHeadTo(0.0,0.18)
			#PyPR2.moveArmWithJointPos(**best_pullback)
	
	
			#time.sleep(3)
			#PyPR2.moveHeadTo(0.0,0.1)
			#PyPR2.openGripper(2)
			#PyPR2.moveHeadTo(0.0,0.0)
			#PyPR2.moveArmWithJointPos(**alt_right_release)

	
			
	
	elif busymoving==0 :	
		busymoving=10
		#PyPR2.moveBodyTo(-0.025,0.0,0.0,0.1)
		PyPR2.moveArmWithJointPos(**alt_right_shooting)
		PyPr2.moveArmWithJointPos(**left_shooting)	

	
def reset():
	global CONDITION_TAG, movement_tracker
	movement_tracker = []
	CONDITION_TAG = 0

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
	time.sleep(3)
	PyPR2.closeGripper(2)
	time.sleep(2)
	PyPR2.moveHeadTo(0.0,0.18)
	PyPR2.moveArmWithJointPos(**best_pullback_right)
	
	
	time.sleep(5)
	PyPR2.moveHeadTo(0.0,0.1)
	PyPR2.openGripper(2)
	#PyPR2.moveHeadTo(0.0,0.0)
	PyPR2.moveArmWithJointPos(**alt_right_release)

	PyPR2.moveHeadTo(0.0,0.1)
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
	PyPR2.openGripper(3)
	time.sleep(10)
	PyPR2.closeGripper(3)

def play():
	time.sleep(4)
	alt_bow_arrow()
	time.sleep(3)
	refill()
	

def check_head_proximity():
	(a,b) = PyPR2.getHeadPos()
	if a>0.6 or a<-0.6:
		return True
	else:
		return False
last_proximity = False
def adjust_to_shooting(y):
	global last_proximity
	proximity = check_head_proximity()

	if proximity== True and last_proximity==False:
		PyPR2.moveBodyTo(0.0,0.0,(0.65)*PyPR2.getHeadPos()[0],1)
		PyPR2.moveHeadTo(0.0,y)
	last_proximity = proximity
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



def closest_obj_index(tracking_objs):
	A=[]
	for i in range(0,len(tracking_objs)):
		A.append(math.sqrt(math.pow(tracking_objs[i]['est_pos'][0],2)+math.pow(tracking_objs[i]['est_pos'][1],2)))
	index_min = min(xrange(len(A)), key=A.__getitem__)
	return index_min

def shooting_tracking(objtype,nameid,trackid,status):
	global HUMAN_DETECTION_COUNTER
	HUMAN_DETECTION_COUNTER+=1
	alt_bow_arrow()
	time.sleep(3)
	PyPR2.registerHumanDetectTracking(onHumanDetected,onHumanTracking)
	

def alt_bow_arrow2():
	PyPR2.openGripper(1)
	PyPR2.moveHeadTo(0.0,0.15)
	PyPR2.moveArmWithJointPos(**positions.right_shooting)
	PyPR2.openGripper(1)
	time.sleep(2)
	PyPR2.moveHeadTo(0.0,0.0)
	PyPR2.moveArmWithJointPos(**positions.alt_left_intermediate)
	PyPR2.moveHeadTo(0.0,0.3)
	time.sleep(3)
	PyPR2.moveArmWithJointPos(**positions.alt_left_shooting)
	time.sleep(3)
	PyPR2.closeGripper(1)
	time.sleep(2)
	PyPR2.moveHeadTo(0.0,0.18)
	PyPR2.moveArmWithJointPos(**positions.best_pullback_left)
	
	
	time.sleep(5)
	PyPR2.moveHeadTo(0.0,0.1)
	PyPR2.openGripper(2)
	#PyPR2.moveHeadTo(0.0,0.0)
	PyPR2.moveArmWithJointPos(**alt_right_release)

	PyPR2.moveHeadTo(0.0,0.1)

