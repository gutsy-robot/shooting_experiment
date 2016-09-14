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




s={'l_wrist_roll_joint': -0.0007893761161641422, 'l_forearm_roll_joint': -5.784708695053728e-05, 'l_elbow_flex_joint': -0.1483631860063741, 'l_shoulder_lift_joint': 0.356638539879416, 'l_upper_arm_roll_joint': 0.15967385473500117, 'l_wrist_flex_joint': -0.07863929718151064, 'l_shoulder_pan_joint': 0.0035887617206241673}
right_shooting = {'r_elbow_flex_joint': -1.5668266161421789, 'r_shoulder_lift_joint': -0.07156730494636866, 'r_upper_arm_roll_joint': -1.1195578453851402, 'r_wrist_roll_joint': -3.1823834614790147, 'r_shoulder_pan_joint': -0.3396092818684876, 'r_forearm_roll_joint': -1.5066273796273486, 'r_wrist_flex_joint': -1.5071675013893124}

right_pullback = {'r_elbow_flex_joint': -1.8827163083810365, 'r_shoulder_lift_joint': -0.1377205348140522, 'r_upper_arm_roll_joint': -1.1378382955913073, 'r_wrist_roll_joint': -2.8935712498579074, 'r_shoulder_pan_joint': -0.395405435349739, 'r_forearm_roll_joint': -1.3948668076388655, 'r_wrist_flex_joint': -1.6445253315659132,'time_to_reach' : 0.2}

left_shooting = {'l_wrist_roll_joint': -2.6133570702164812, 'l_forearm_roll_joint': -1.205012668267126, 'l_elbow_flex_joint': -0.4263229518627475, 'l_shoulder_lift_joint': 0.21368677576185252, 'l_upper_arm_roll_joint': 0.7678997111559798, 'l_wrist_flex_joint': -0.09263466648021362, 'l_shoulder_pan_joint': -0.17482627883160928}

right_pullback_alt = {'r_elbow_flex_joint': -2.119271650781721, 'r_shoulder_lift_joint': -0.15269383620354068, 'r_upper_arm_roll_joint': -0.9991313707813558, 'r_wrist_roll_joint': -2.479583875110267, 'r_shoulder_pan_joint': -0.33853149584284675, 'r_forearm_roll_joint': -1.2974523132141216, 'r_wrist_flex_joint': -1.6922546169151684, 'time_to_reach' : 0.5}

best_pullback = {'r_elbow_flex_joint': -2.119416421493104, 'r_shoulder_lift_joint': -0.34607783042032403, 'r_upper_arm_roll_joint': -0.4513592839018241, 'r_wrist_roll_joint': -1.6963195612773299, 'r_shoulder_pan_joint': 0.02650634037996158, 'r_forearm_roll_joint': -0.8080081105254291, 'r_wrist_flex_joint': -1.9535558036733018, 'time_to_reach' : 0.01}

right_up = {'r_elbow_flex_joint': -2.0722211695820745, 'r_shoulder_lift_joint': -0.35157650042211364, 'r_upper_arm_roll_joint': -0.7414411648049486, 'r_wrist_roll_joint': -2.2757713591637283, 'r_shoulder_pan_joint': -0.2699677232886195, 'r_forearm_roll_joint': -1.0189764366341232, 'r_wrist_flex_joint': -1.7970475243950452,'time_to_reach' : 0.2}

alt_right_shooting ={'r_elbow_flex_joint': -1.595346446284734, 'r_shoulder_lift_joint': -0.009474631387698922, 'r_upper_arm_roll_joint': -1.0682443009467766, 'r_wrist_roll_joint': -3.2004229291203083, 'r_shoulder_pan_joint': -0.3623256950243017, 'r_forearm_roll_joint': -1.5515167191009833, 'r_wrist_flex_joint': -1.5588428805297814}

alt_right_release = {'r_elbow_flex_joint': -1.2864057481922857, 'r_shoulder_lift_joint': -0.15734655697428568, 'r_upper_arm_roll_joint': -0.4683568954970323, 'r_wrist_roll_joint': -3.326642306329232, 'r_shoulder_pan_joint': -0.23547857046811338, 'r_forearm_roll_joint': -1.6584181357856194, 'r_wrist_flex_joint': -2.006767212955106}
alt_right_intermediate = {'r_elbow_flex_joint': -1.2869848310378198, 'r_shoulder_lift_joint': -0.304203343483619, 'r_upper_arm_roll_joint': -0.8610658652768834, 'r_wrist_roll_joint': -3.3490058912604237, 'r_shoulder_pan_joint': -0.4156346499848435, 'r_forearm_roll_joint': -1.3218059368203074, 'r_wrist_flex_joint': -1.811673215228525}

left_refill = 	{'l_wrist_roll_joint': -2.6438093589298246, 'l_forearm_roll_joint': -1.648931213525727, 'l_elbow_flex_joint': -0.7096392340403112, 'l_shoulder_lift_joint': 0.13805891450647004, 'l_upper_arm_roll_joint': 1.5667874561307527, 'l_wrist_flex_joint': -0.42401793925654646, 'l_shoulder_pan_joint': -0.11853268564621577}

right_refill = {'r_elbow_flex_joint': -0.6960307871702596, 'r_shoulder_lift_joint': -0.24287202423288937, 'r_upper_arm_roll_joint': -0.26262165326446807, 'r_wrist_roll_joint': -4.162579188202739, 'r_shoulder_pan_joint': -0.6893093938802535, 'r_forearm_roll_joint': -1.7945901784672387, 'r_wrist_flex_joint': -2.0064626505144085}

right_pick = {'r_elbow_flex_joint': -0.6767762825562502, 'r_shoulder_lift_joint': -0.2748489051663732, 'r_upper_arm_roll_joint': -0.12407508328088657, 'r_wrist_roll_joint': -2.4850057559226775, 'r_shoulder_pan_joint': -0.15820960309140264, 'r_forearm_roll_joint': -2.606474043818355, 'r_wrist_flex_joint': -1.727875035116706}
right_pick_further = {'r_elbow_flex_joint': -0.516515105054685, 'r_shoulder_lift_joint': -0.35132271565280027, 'r_upper_arm_roll_joint': 0.4847921924455716, 'r_wrist_roll_joint': -2.8233311186171237, 'r_shoulder_pan_joint': -0.15820960309140264, 'r_forearm_roll_joint': -3.178176804150745, 'r_wrist_flex_joint': -1.7377080510592138}
left_pick_further= {'l_wrist_roll_joint': -2.2007145166355553, 'l_forearm_roll_joint': -2.044316052832808, 'l_elbow_flex_joint': -0.9928107455064914, 'l_shoulder_lift_joint': 0.14905625451004917, 'l_upper_arm_roll_joint': 1.5773708746711654, 'l_wrist_flex_joint': -0.4879760518029503, 'l_shoulder_pan_joint': -0.03852779989672461}
left_intermediate = {'l_wrist_roll_joint': -2.9727803038028577, 'l_forearm_roll_joint': -1.614338655529292, 'l_elbow_flex_joint': -0.3585702589352563, 'l_shoulder_lift_joint': 0.21791652191707533, 'l_upper_arm_roll_joint': 1.5916424542180851, 'l_wrist_flex_joint': -0.39351818626673085, 'l_shoulder_pan_joint': -0.09880091071525321}

left_last = {'l_wrist_roll_joint': -0.0006999676759598117, 'l_forearm_roll_joint': -5.784708695053728e-05, 'l_elbow_flex_joint': -1.0000492810756678, 'l_shoulder_lift_joint': 0.5000405904704315, 'l_upper_arm_roll_joint': 0.15967385473500117, 'l_wrist_flex_joint': -0.09311103337463733, 'l_shoulder_pan_joint': 0.0035887617206241673}


l2 = {'l_wrist_roll_joint': -2.679286471527397, 'l_forearm_roll_joint': -1.0647334824120165, 'l_elbow_flex_joint': -1.6303809584395477, 'l_shoulder_lift_joint': 0.6161894198928477, 'l_upper_arm_roll_joint': 1.2972309930029742, 'l_wrist_flex_joint': -0.07532257873391857, 'l_shoulder_pan_joint': 0.278424198259032}

r2 = {'r_elbow_flex_joint': -0.7588612759107106, 'r_shoulder_lift_joint': -0.018610883082980017, 'r_upper_arm_roll_joint': 0.85072418681373554, 'r_wrist_roll_joint': -9.028506366421123, 'r_shoulder_pan_joint': -0.23149905283497807, 'r_forearm_roll_joint': -3.7593086396560755, 'r_wrist_flex_joint': -2.9993840838982049}


#a = {'r_elbow_flex_joint': -0.516515105054685, 'r_shoulder_lift_joint': -0.35132271565280027, 'r_upper_arm_roll_joint': 0.4847921924455716, 'r_wrist_roll_joint': -2.8233311186171237, 'r_shoulder_pan_joint': -0.15820960309140264, 'r_forearm_roll_joint': -3.178176804150745, 'r_wrist_flex_joint': -1.7377080510592138}
#b= {'l_wrist_roll_joint': -3.062191134607524, 'l_forearm_roll_joint': -0.8025704843520763, 'l_elbow_flex_joint': -1.6901712622409446, 'l_shoulder_lift_joint': 0.30225766025221656, 'l_upper_arm_roll_joint': 1.1533927137491862, 'l_wrist_flex_joint': -0.08264695215512896, 'l_shoulder_pan_joint': 0.42176973966926046}

#left_current = {'l_wrist_roll_joint': -2.5708187337191086, 'l_forearm_roll_joint': -1.2180861099179523, 'l_elbow_flex_joint': -1.6573083107568838, 'l_shoulder_lift_joint': 0.6408911374393484, 'l_upper_arm_roll_joint': 1.1389607793758965, 'l_wrist_flex_joint': -0.07641030173640845, 'l_shoulder_pan_joint': 0.16094552146418317}




#right_current = {'r_elbow_flex_joint': -0.5144883150953158, 'r_shoulder_lift_joint': -0.16377577113022426, 'r_upper_arm_roll_joint': 0.48463183761920137, 'r_wrist_roll_joint': -2.8072093903002204, 'r_shoulder_pan_joint': -0.4293142418487461, 'r_forearm_roll_joint': -3.3093739973546157, 'r_wrist_flex_joint': -1.7845805453665076}
left_match = {'l_wrist_roll_joint': -2.534706330036445, 'l_forearm_roll_joint': -1.2597938596093066, 'l_elbow_flex_joint': -1.663967763480526, 'l_shoulder_lift_joint': 0.5094306269350259, 'l_upper_arm_roll_joint': 1.2079133547149474, 'l_wrist_flex_joint': -0.07266853460784328, 'l_shoulder_pan_joint': 0.21964340655292902}


right_match = {'r_elbow_flex_joint': -0.6570874658080905, 'r_shoulder_lift_joint': -0.24608663131085867, 'r_upper_arm_roll_joint': 0.516382093240439, 'r_wrist_roll_joint': -2.6856889764620533, 'r_shoulder_pan_joint': -0.2559565049552889, 'r_forearm_roll_joint': -4.168171850222637, 'r_wrist_flex_joint': -2.0093041176809128}



#previous_pos = 0
CONDITION_TAG = 0 
movement_tracker = []
track_x = []
track_y = []
diff_min = 0.03

HUMAN_DETECTION_COUNTER =0


revolve_counter= 1
torso_position_counter = 0



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
	while revolve_counter==1 and PyPR2.getHeadPos()[0]<1.5:
		if HUMAN_DETECTION_COUNTER !=0:
			PyPR2.say("Tar gate found")
		else:
	
	
			revolve_cw()
		

	
	while revolve_counter==-1 and PyPR2.getHeadPos()[0]>-1.5:

		if HUMAN_DETECTION_COUNTER !=0:
			PyPR2.say("Tar gate found")
		else:
	
	
			revolve_acw()

	while PyPR2.getHeadPos()[0] >1.2:
		if HUMAN_DETECTION_COUNTER !=0:
			PyPR2.say("Tar gate Detected")

		else:
	
			revolve_counter = -1
			revolve_acw()
			find_human()

		
	while PyPR2.getHeadPos()[0] <-1.2:
		if HUMAN_DETECTION_COUNTER!=0:
			PyPR2.say("tar gate detected")
		else:

			revolve_counter = 1
			revolve_cw()
			find_human()


		

	
		
		
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
	global HUMAN_DETECTION_COUNTER,start_time
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
	global torso_pos, start_time
	#global movement_tracker
	global CONDITION_TAG	
		
	focus_obj = tracking_objs[0]
	elapsed_time = time.time() - start_time
	track_x.append((focus_obj['est_pos'][0],elapsed_time))
	track_y.append((focus_obj['est_pos'][1],elapsed_time))
	#PyPR2.moveTorsoBy(0.03,5)
	#if abs(previous_pos - focus_obj['est_pos'][0])< 0.1:	
	#	PyPR2.moveHeadTo(0.2,1.0)
	#adjust_to_shooting()
	if focus_obj['est_pos'][0]<=4 and focus_obj['est_pos'][0] >3:

			adjust_to_shooting()
			if CONDITION_TAG != 1:
				CONDITION_TAG =1

			track_human(focus_obj)
			adjust_to_shooting()
			PyPR2.moveBodyTo(0.1,0.0,0.0,1)
				#PyPR2.moveBodyTo(0.0,0.0,chx/2.0,2)
				#previous_pos = focus_obj['est_pos'][0]
			#PyPR2.moveArmWithJointPos(**left_shooting)	
			#PyPR2.moveArmWithJointPos(**alt_right_intermediate)	
			#PyPR2.moveBodyTo(0.2,0.0,0.0,1)		
	              
				

	elif focus_obj['est_pos'][0]<=3 and focus_obj['est_pos'][0] >2:
			
			
			if CONDITION_TAG != 2:
				CONDITION_TAG =2
			
			track_human(focus_obj)

			#mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			#mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      			#print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
      			#ofs_x = mid_x - 320
      			#ofs_y = mid_y - 240
      			#chx = chy = 0.0
      			#if math.fabs(ofs_x) > 10:
       			#	chx = -ofs_x * 90.0 / 640 * 0.01745329252
			#	head_yaw_list.append(chx)
				
      			#if math.fabs(ofs_y) > 10:
        		#	chy = ofs_y * 90.0 / 640 * 0.01745329252
      			#	PyPR2.updateHeadPos( chx, chy )
				#PyPR2.moveBodyTo(0.0,0.0,chx/2.0,2)
				#previous_pos = focus_obj['est_pos'][0]
			PyPR2.moveArmWithJointPos(**alt_right_shooting)
			PyPR2.openGripper(2)	
	                #movement_tracker.append(str(CONDITION_TAG)+":"+str(focus_obj['est_pos']))
	elif focus_obj['est_pos'][0] <2:
			
				
      			if CONDITION_TAG != 3:
				CONDITION_TAG =3
			track_human(focus_obj)
			'''
			mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
      			
	
	                #movement_tracker.append(str(CONDITION_TAG)+":"+str(focus_obj['est_pos']))'''
			#PyPR2.closeGripper(2)
			#time.sleep(2)
			#PyPR2.moveHeadTo(0.0,0.18)
			PyPR2.moveArmWithJointPos(**best_pullback)
	
	
			#time.sleep(3)
			#PyPR2.moveHeadTo(0.0,0.1)
			#PyPR2.openGripper(2)
			#PyPR2.moveHeadTo(0.0,0.0)
			#PyPR2.moveArmWithJointPos(**alt_right_release)

	else:
			track_human(focus_obj)
			
	   

	
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
	if a>0.5 or a<-0.5:
		return True
	else:
		return False

def adjust_to_shooting():
	if check_head_proximity() == True:
		PyPR2.moveBodyTo(0.0,0.0,(0.65)*PyPR2.getHeadPos()[0],1)
		PyPR2.moveHeadTo(0.0,0.1)

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


			
