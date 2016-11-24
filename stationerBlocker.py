import random
import math
import logging
import csv

import PyPR2
import time
import positions
import sys
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




rightHand = {'r_elbow_flex_joint': -0.39809266314295944, 'r_shoulder_lift_joint': -0.22013097517467903, 'r_upper_arm_roll_joint': 0.5810547228536669, 'r_wrist_roll_joint': -7.86682790273471, 'r_shoulder_pan_joint': 0.13506050693209304, 'r_forearm_roll_joint': -3.7613791576834474, 'r_wrist_flex_joint': -1.661172305633153}


leftHand = {'l_wrist_roll_joint': -1.5218375184201214, 'l_forearm_roll_joint': -3.7494020591289297, 'l_elbow_flex_joint': -0.44992057781826245, 'l_shoulder_lift_joint': -0.2382673614033768, 'l_upper_arm_roll_joint': 0.561455063489098, 'l_wrist_flex_joint': -1.984537439441737, 'l_shoulder_pan_joint': 0.1519296234980555}

HUMAN_COUNTER=0
no_objTracker = [(0.0,time.time())]
track_data = [('x','y','d','time')] 
msgTryTimer = -1
st_time = time.time()
csvCounter = 0
csvFile = "/home/demoshare/sid_stuff/trackdata0.csv"
csvFile2 = "/home/demoshare/sid_stuff/main.csv"
def onHumanDetected(objtype, nameid, trackid, status):
	PyPR2.moveTorsoBy(0.1,2)
	PyPR2.say("This exit is closed")


def onHumanTracking(tracking_objs):

	global HUMAN_COUNTER,track_data,msgTryTimer,x,y,d,st_time
	if len(tracking_objs) !=0:
		if HUMAN_COUNTER ==0:
			
			PyPR2.onTimer = timerActions
			msgTryTimer = PyPR2.addTimer(1,-1,2)

			elapsed_time = time.time() - st_time
			no_objTracker.append((elapsed_time,time.time()))
			HUMAN_COUNTER= len(tracking_objs)


		object_index = closest_obj_index(tracking_objs)
		focus_obj = tracking_objs[object_index]

		x = focus_obj['est_pos'][0]
		y = focus_obj['est_pos'][1]
		d = math.sqrt((math.pow(x,2))+(math.pow(y,2)))
		
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

	else:
		
		if HUMAN_COUNTER !=0:
			PyPR2.removeTimer(msgTryTimer)
			#msgTryTimer = -1
			st_time = time.time()
			HUMAN_COUNTER =0


def timerActions(id):
	global msgTryTimer,x,y,d,track_data,csvCounter,csvFile

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
		if isMovingForward == True:
			PyPR2.say("Move, Back")
		else:
			PyPR2.say("going back,,, goood")
		
		#if abs(y) >0.3:
		if abs(movementCounter)< 0.3:
				track_y.append(y)	
				movementCounter +=y
				PyPR2.moveBodyTo(0.0,y,0.0,2.0)
			
		'''
		track_data.append((x,y,d,time.time()))
		updateCsv()
		with open(csvFile, "w") as output:
   		 	writer = csv.writer(output, lineterminator='\n')
    	         	writer.writerows(track_data)
		with open(csvFile2, "w") as output:
   		 	writer = csv.writer(output, lineterminator='\n')
    	         	writer.writerows(no_objTracker)
	
def closest_obj_index(tracking_objs):
	A=[]
	for i in range(0,len(tracking_objs)):
		A.append(math.sqrt(math.pow(tracking_objs[i]['est_pos'][0],2)+math.pow(tracking_objs[i]['est_pos'][1],2)))
	index_min = min(xrange(len(A)), key=A.__getitem__)
	return index_min


def updateCsv():
	global track_data, csvFile, csvCounter
	if len(track_data) > 1000:
		csvCounter +=1
	csvFile = "/home/demoshare/sid_stuff/trackdata"+str(csvCounter)+".csv"
		
