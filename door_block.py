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

st_time = time.time()

def onHumanDetected(objtype, nameid, trackid, status):
	PyPR2.moveTorsoBy(0.1,2)



def onHumanTracking(tracking_objs):
 global HUMAN_COUNTER, st_time
 
	#focus_obj = tracking_objs[object_index]

	
 if len(tracking_objs) == 0:
		if HUMAN_COUNTER !=0:
			st_time = time.time()
			HUMAN_COUNTER =0

		
			

 else:
		if HUMAN_DETECTION_COUNTER ==0:
			elapsed_time = time.time() - st_time
			no_objTracker.append(elapsed_time)
			HUMAN_DETECTION_COUNTER= len(tracking_objs)
			

		focus_obj = tracking_objs[object_index]


		x = focus_obj['est_pos'][0]
		y = focus_obj['est_pos'][1]

	
	
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
	
