
import PyPR2
import time
import positions
import sys
import random
import math
import logging
import csv
import py_main

a=0
b=0
a2=0
b2=0
NumPeople = 0
tracking_data = [('focus_x','focus_y','avg_x','avg_y','time','NumPeople','speechCommand','actionCounter','LostConnection')]
actionCounterKey = 	[('action','key')]																		#map the actions with respective values
NEW_INTERACTION_INITIALISER = 0
csvFile = py_main.csvFile																				#the file to store the data
HumanPresence = False
csvFileCounter = 1
last_x = 0
LostConnectionCounter = 0 	
	
						#measures no.of times we loose track of the face inside an interaction
initial_left = {'l_wrist_roll_joint': -0.03343445889223928, 'l_forearm_roll_joint': -1.4370226053672253, 'l_elbow_flex_joint': -1.9698682766339202, 'l_shoulder_lift_joint': 0.9258433754370239, 'l_upper_arm_roll_joint': 0.09899174423834634, 'l_wrist_flex_joint': -0.09503205735655162, 'l_shoulder_pan_joint': 0.10351215896157584,'time_to_reach': 0.7}

def onHumanDetected(objtype, trackid, nameid, status):	
	global LostConnectionCounter
	PyPR2.say("Hi")									#change appropriately
	LostConnectionCounter += 1
	
def timerActions( id ):
  

  	global a,b,x, y , last_x, tracking_data, csvFile, csvFileCounter,LostConnectionCounter,NumPeople, msgTryTimer, NEW_INTERACTION_INITIALISER
	
  	
  
  
 	if msgTryTimer == id :
 
    		
    		 b +=1   		    		
	    	 vel_x = x - last_x
    		 last_x = x
         	 if vel_x < -0.01:
    		    	PyPR2.moveArmWithJointPos(**initial_left)
			a+=1

		 tracking_data.append((x,y,x,y,time.time(),NumPeople,"empty",1,LostConnectionCounter))
		
		#b +=1
		#updateCsv()

		 with open(csvFile, "w") as output:
   		 		writer = csv.writer(output, lineterminator='\n')
    	   			writer.writerows(tracking_data)
		




				#previous_pos = focus_obj['est_pos'][0]
				
	                #movement_tracker.append(str(CONDITION_TAG)+":"+str(focus_obj['est_pos']))


  #else:
  #  timermanager.onTimerCall( id )


def onHumanTracking(tracking_objs):
	#global busymoving
	#SHOOTING_TAG = 0
	#global start_time,last_action_counter,movement_tracker,msgTryTimer,d,x,y,track_x,track_y,track_d,elapsed_time,focus_obj,HUMAN_DETECTION_COUNTER
	global a2,b2,NEW_INTERACTION_INITIALISER, NumPeople, HumanPresence, x, y, msgTryTimer
	NumPeople = len(tracking_objs)
	a2 +=1 
	if len(tracking_objs)==0:
		NEW_INTERACTION_INITIALISER += 1
		if HumanPresence == True:
			PyPR2.removeTimer(msgTryTimer)
		
		if NEW_INTERACTION_INITIALISER > 500:
				restoreInitialState()

 		HumanPresence = False

	elif len(tracking_objs) > 0:
			if HumanPresence== False:
			
				PyPR2.onTimer = timerActions
				msgTryTimer = PyPR2.addTimer(1,-1,0.5)
				b2+=1
			#st_time = time.time()
			#no_objTracker.append(elapsed_time)
				HumanPresence = True

			object_index = closest_obj_index(tracking_objs)
			focus_obj = tracking_objs[object_index]
			x = focus_obj['est_pos'][0]
			y = focus_obj['est_pos'][1]


			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			
			mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
     			
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



def restoreInitialState():
	global LostConnectionCounter, NumPeople, tracking_data, NEW_INTERACTION_INITIALISER,csvFile,csvFileCounter,last_x

	PyPR2.tuckBothArms()												#for the time being

	#NumPeople = 0
	tracking_data = ['focus_x','focus_y','avg_x','avg_y','time','speechCommand','actionCounter']
 	NEW_INTERACTION_INITIALISER = 0
 	csvFileCounter += 1
 	csvFile = "/home/demoshare/sid_stuff/Nov26TrackData/"+str(csvFileCounter)+".csv"										#change the approprite csvFile
	LostConnectionCounter =0 
	last_x = 0
