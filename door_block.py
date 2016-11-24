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
import py_main
'''import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
'''

HUMAN_COUNTER=0
no_objTracker = []
maxDistance = 1.0
#c =0
avg_x = 0
avg_y = 0
#speechCommands = ["The exit is closed, take the other exit", "The construction, Building 2 is underway, take the other exit", "Move Back"]
st_time = time.time()
msgTryTimer = -1

initial_left = {'l_wrist_roll_joint': -0.03343445889223928, 'l_forearm_roll_joint': -1.4370226053672253, 'l_elbow_flex_joint': -1.9698682766339202, 'l_shoulder_lift_joint': 0.9258433754370239, 'l_upper_arm_roll_joint': 0.09899174423834634, 'l_wrist_flex_joint': -0.09503205735655162, 'l_shoulder_pan_joint': 0.10351215896157584,'time_to_reach': 0.7}


initial_right = {'r_elbow_flex_joint': -1.9779754364713977, 'r_shoulder_lift_joint': 0.8400971960934513, 'r_upper_arm_roll_joint': 0.48404005289988583, 'r_wrist_roll_joint': -0.3022365274589296, 'r_shoulder_pan_joint': 0.2276671985198463, 'r_forearm_roll_joint': -1.224321618205765, 'r_wrist_flex_joint': -0.09133131041169806,'time_to_reach':0.7}



second_left = {'l_wrist_roll_joint': -0.031868137768653826, 'l_forearm_roll_joint': -1.4370226053672253, 'l_elbow_flex_joint': -1.7327338513877018, 'l_shoulder_lift_joint': 0.917299288203474, 'l_upper_arm_roll_joint': 0.3478624347644097, 'l_wrist_flex_joint': -0.12801181879204448, 'l_shoulder_pan_joint': 0.8335878314071925,'time_to_reach':0.5}

second_right = {'r_elbow_flex_joint': -1.9465601921011721, 'r_shoulder_lift_joint': 0.8025370502350734, 'r_upper_arm_roll_joint': 0.5132246312992053, 'r_wrist_roll_joint': -0.3050646072654031, 'r_shoulder_pan_joint': -0.42696345213091336, 'r_forearm_roll_joint': -1.2249579361622214, 'r_wrist_flex_joint': -0.10051169255271242,'time_to_reach':0.5}

third_left = {'l_wrist_roll_joint': -2.1129816134346173, 'l_forearm_roll_joint': -0.22616738131809233, 'l_elbow_flex_joint': -0.22465735090549332, 'l_shoulder_lift_joint': 0.07566439823725442, 'l_upper_arm_roll_joint': 0.35058846681269795, 'l_wrist_flex_joint': -0.07849866771870584, 'l_shoulder_pan_joint': 1.1039463106083232,'time_to_reach':0.2}

third_right = {'r_elbow_flex_joint': -0.23522561283649057, 'r_shoulder_lift_joint': 0.05903227107002134, 'r_upper_arm_roll_joint': 0.64712091131806, 'r_wrist_roll_joint': -6.440593070749978, 'r_shoulder_pan_joint': -0.901935462969085, 'r_forearm_roll_joint': -1.874291487182263, 'r_wrist_flex_joint': -0.0903915177375465,'time_to_reach':0.2}


full_stretch_left = {'l_wrist_roll_joint': -2.110637322287075, 'l_forearm_roll_joint': -6.319143202733678, 'l_elbow_flex_joint': -0.22147239525505558, 'l_shoulder_lift_joint': 0.11161724055664769, 'l_upper_arm_roll_joint': 0.3249316945935157, 'l_wrist_flex_joint': -0.07928182828049879, 'l_shoulder_pan_joint': 1.6414299109336616,'time_to_reach':0.1}

full_stretch_right = {'r_elbow_flex_joint': -0.2858953618207254, 'r_shoulder_lift_joint': -0.008643667413542395, 'r_upper_arm_roll_joint': 0.6464794920125809, 'r_wrist_roll_joint': -0.15134759255353547, 'r_shoulder_pan_joint': -1.3345421923378364, 'r_forearm_roll_joint': -1.8746385697039665, 'r_wrist_flex_joint': -0.09046113200970607,'time_to_reach':0.1}

csvFile = py_main.csvFile
csvCounter = 1

movementCounter = 0.0

track_data = [('focusx','focusy','avg_x','avg_y','time','NumObjects','actionIdentifier')]
#a = 0
#b = 0
track_movementCounter = [('movementCounter','y')]
actionIdentifier = " "
isNearest = False
moveLeftCounter = 0
moveRightCounter =0


def onHumanDetected(objtype, nameid, trackid, status):
	global csvCounter,csvFile,actionIdentifier,isNearest
	PyPR2.moveTorsoBy(0.1,2)
	PyPR2.say("This exit is closed,   please use the other exit")
	csvCounter += 1
	csvFile = "/home/demoshare/sid_stuff/aggressiveBehaviourExperiment/test"+str(csvCounter)+"_"+str(time.time())+".csv"

	actionIdentifier = "Human Detected"
	isNearest = False


def onHumanTracking(tracking_objs):
 	global HUMAN_COUNTER, st_time,msgTryTimer,x,y,Numpeople,avg_y,avg_x,actionIdentifier,isNearest
 
	#focus_obj = tracking_objs[object_inde x]
	Numpeople = len(tracking_objs)
	avgPos(tracking_objs)
	
 	if len(tracking_objs) == 0:
 		#PyPR2.cancelMoveBodyAction()
		if HUMAN_COUNTER !=0:
			PyPR2.removeTimer(msgTryTimer)
			PyPR2.moveArmWithJointPos(**initial_left)
			PyPR2.moveArmWithJointPos(**initial_right)
			#msgTryTimer = -1
			#elapsed_time = time.time()-st_time

			HUMAN_COUNTER =0
			
		
			

 	elif len(tracking_objs) > 0:
		if HUMAN_COUNTER ==0:
			
			PyPR2.onTimer = timerActions
			msgTryTimer = PyPR2.addTimer(1,-1,0.5)
			#a +=1
			#st_time = time.time()
			#no_objTracker.append(elapsed_time)
			HUMAN_COUNTER= Numpeople
			
		object_index = closest_obj_index(tracking_objs)
		focus_obj = tracking_objs[object_index]


		x = focus_obj['est_pos'][0]
		y = focus_obj['est_pos'][1]
		d = math.sqrt((math.pow(x,2))+(math.pow(y,2)))

		if d<0.1:
			PyPR2.cancelMoveBodyAction()
			PyPR2.cancelMoveArmAction(True)
			PyPR2.cancelMoveArmAction(False)
			#c+=1
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
		

		if Numpeople ==1:

			if x>3.5:
				if isNearest == False:
					if y>0:
						PyPR2.moveArmWithJointPos(**initial_left)
						actionIdentifier= "initial_left"
					else:

						PyPR2.moveArmWithJointPos(**initial_right)
						actionIdentifier= "initial_right"
			elif 2.5<x<3.5:
				PyPR2.moveTorsoBy(0.1,2)
				if y>0:
					PyPR2.moveArmWithJointPos(**second_left)
					actionIdentifier = "second_left"
				else:
					PyPR2.moveArmWithJointPos(**second_right)
					actionIdentifier = "second_right"
			
			elif 1.5<x<2.5:
				PyPR2.moveTorsoBy(0.1,2)
				isNearest = True
				if y>0:
					PyPR2.moveArmWithJointPos(**third_left)
					actionIdentifier = "third_left"
				else:
					PyPR2.moveArmWithJointPos(**third_right)
					actionIdentifier = "third_right"
			else:
				isNearest = True

				PyPR2.moveArmWithJointPos(**full_stretch_left)
				PyPR2.moveArmWithJointPos(**full_stretch_right)
				actionIdentifier = "full_stretch"

		if 1<Numpeople<3:

			if x>3.5:
				if isNearest ==False:

					PyPR2.moveArmWithJointPos(**initial_left)
					PyPR2.moveArmWithJointPos(**initial_right)
					actionIdentifier = "Both_initial"

			elif 2.5<x<3.5:
				PyPR2.moveArmWithJointPos(**second_left)
				PyPR2.moveArmWithJointPos(**second_right)
				PyPR2.moveTorsoBy(0.1,2)
				actionIdentifier = "Multiple_Second"

			elif 1.5<x<2.5:
				isNearest = True
				PyPR2.moveArmWithJointPos(**third_right)
				PyPR2.moveArmWithJointPos(**third_left)
				PyPR2.moveTorsoBy(0.1,2)
				actionIdentifier = "Multiple_third"
			else:
				isNearest = True
				PyPR2.moveArmWithJointPos(**full_stretch_left)
				PyPR2.moveArmWithJointPos(**full_stretch_right)
				actionIdentifier = "Full_Multiple"
		elif Numpeople > 3:
			isNearest = True
			PyPR2.moveArmWithJointPos(**full_stretch_left)
			PyPR2.moveArmWithJointPos(**full_stretch_right)
			actionIdentifier = "TooManyPeopleBehaviour"


previous_position =0.0
isMovingForward = False
def timerActions(id):
	global msgTryTimer,x,y,d, previous_position,movementCounter,track_data,Numpeople,a,b,maxDistance,avg_y,avg_x,actionIdentifier,moveLeftCounter,moveRightCounter
	
	#a+=1
	'''	
	if previous_position > x:
			isMovingForward = False
			previous_position = x
	else:
			isMovingForward = True
			previous_position = True
	'''
	if msgTryTimer == id :
		'''
		if y>1.0:
			if moveLeftCounter <1.0:
				PyPR2.moveBodyTo(0.0,0.7,0.0,1.0)
				moveLeftCounter +=1
				moveRightCounter -= 1
			elif moveLeftCounter==1:
				PyPR2.cancelMoveBodyAction()

		elif y<-1.0:
			if moveRightCounter<1.0:
				PyPR2.moveBodyTo(0.0,-0.7,0.0,1.0)
				moveLeftCounter -=1
				moveRightCounter +=1
			elif moveRightCounter == 1:
				PyPR2.cancelMoveBodyAction()
		
		if isMovingForward == True:
			PyPR2.say("Move, Back")
		else:
			PyPR2.say("going back,,, goood")
	'''
		'''#if abs(y) >0.3:
		if PyPR2.getHeadPos()[0]>0.8:
			if (y+movementCounter)<=maxDistance:
				track_movementCounter.append((movementCounter,y))
				movementCounter += y
				PyPR2.moveBodyTo(0.0,y,0.0,0.2)

			else:
				track_movementCounter.append((movementCounter,y))
				PyPR2.moveBodyTo(0.0,(maxDistance-movementCounter),0.0,1.0)
				movementCounter = maxDistance
		elif PyPR2.getHeadPos()[0]< -0.8:
			if (y+movementCounter)>=-maxDistance:
				track_movementCounter.append((movementCounter,y))
				movementCounter += y
				PyPR2.moveBodyTo(0.0,y,0.0,0.2)

			else: 
				track_movementCounter.append((movementCounter,y))
				PyPR2.moveBodyTo(0.0,(-maxDistance-movementCounter),0.0,0.2)
				movementCounter = -maxDistance
'''
		#a += 1
		track_data.append((x,y,avg_x,avg_y,time.time(),Numpeople,actionIdentifier))
		
		#b +=1
		#updateCsv()

		with open(csvFile, "w") as output:
   		 	writer = csv.writer(output, lineterminator='\n')
    	         	writer.writerows(track_data)
		


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
	

def updateCsv():
	global track_data, csvFile, csvCounter
	if len(track_data) > 10:
		csvCounter +=1
	csvFile = "/home/demoshare/sid_stuff/aggressiveBehaviourExperiment/test"+str(csvCounter)+".csv"


def avgPos(tracking_objects):
	global avg_x,avg_y,Numpeople
	tempX = 0
	tempY = 0
	for i in range(0,Numpeople):
		tempX += tracking_objects[i]['est_pos'][0]
		tempY += tracking_objects[i]['est_pos'][1]


	avg_x = tempX/Numpeople
	avg_y = tempY/Numpeople

