from SIMKit import RobotScript, Event
import PyPR2
import time
import positions
import sys
numpy_path      = '/usr/lib/python2.7/dist-packages/'
sympy_path      = '/usr/local/lib/python2.7/dist-packages/'
pyinterval_path = '/usr/local/lib/python2.7/dist-packages/pyinterval-1.0b21-py2.7-linux-x86_64.egg/'
mtpltlib_path   = '/usr/lib/pymodules/python2.7'


sys.path.append(sympy_path)
sys.path.append(numpy_path)
sys.path.append(pyinterval_path)
sys.path.append(mtpltlib_path)
sys.path.append('/home/demoshare/shooting_experiment/Magiks/')

from magiks.specific_geometries.pr2 import skilled_pr2 as spr


def generate():
	
	
	rs = RobotScript()
	channel_head_id = rs.addChannel("moveHeadTo")
	channel_torso_id = rs.addChannel("moveTorsoBy")
	channel_speech_id = rs.addChannel("say")
	#channel_hands_id = rs.addChannel("moveArmWithJointPos")
	
	asset_torso_id = rs.addAssetToChannel(channel_torso_id, [0], (0.2,10))
	
	asset_speech_id1 = rs.addAssetToChannel(channel_speech_id, [2], ("Initial lising",))
	#asset_hands_id1 = rs.addAssetToChannel(channel_hands_id, [2.0], {'r_elbow_flex_joint': 0.0, 'r_shoulder_lift_joint': 0.0, 'r_upper_arm_roll_joint': 0.0, 'r_wrist_roll_joint': 0.0, 'r_shoulder_pan_joint': 0.0, 'r_forearm_roll_joint': 0.0, 'r_wrist_flex_joint': 0.0})
	#asset_hands_id2 = rs.addAssetToChannel(channel_hands_id, [4],({'l_wrist_roll_joint': -0.0007893761161641422, 'l_forearm_roll_joint': -5.784708695053728e-05, 'l_elbow_flex_joint': -0.1483631860063741, 'l_shoulder_lift_joint': 0.356638539879416, 'l_upper_arm_roll_joint': 0.15967385473500117, 'l_wrist_flex_joint': -0.07863929718151064, 'l_shoulder_pan_joint': 0.0035887617206241673}))
	#asset_hands_id3 = rs.addAssetToChannel(channel_hands_id, [6], ({'l_wrist_roll_joint': 3.0377253864391696, 'l_forearm_roll_joint': 3.0636974190755852, 'l_elbow_flex_joint': -2.045293817264738, 'l_shoulder_lift_joint': 0.7999295928757233, 'l_upper_arm_roll_joint': 0.11734018057335116, 'l_wrist_flex_joint': -0.6073161853116821, 'l_shoulder_pan_joint': -0.024019141859252136}))
	#asset_hands_id4 = rs.addAssetToChannel(channel_hands_id, [8], ({'r_elbow_flex_joint': -0.6838700474140432, 'r_shoulder_lift_joint': -0.2795862208602225, 'r_upper_arm_roll_joint': -0.7924339995905723, 'r_wrist_roll_joint': -0.2403805679846016, 'r_shoulder_pan_joint': -2.37771742738202e-05, 'r_forearm_roll_joint': 5.099914879735316, 'r_wrist_flex_joint': -1.7826226439620259}))
	asset_speech_id2 = rs.addAssetToChannel(channel_speech_id, [13], ("Will Kill you,   Soon",))
	asset_head_id1 = rs.addAssetToChannel(channel_head_id, [10], (2.0,0.5))
	asset_head_id2 = rs.addAssetToChannel(channel_head_id, [20], (0.0,0.0))
	rs.play()


	


def run():
	time.sleep(10)

	PyPR2.moveTorsoBy(0.2,10)
	PyPR2.say("Initial lising")
	PyPR2.moveHeadTo(0.0,-0.5)
	
	
	time.sleep(2)
	PyPR2.moveArmWithJointPos(**left_home)
	PyPR2.moveArmWithJointPos(**right_home)
	
	time.sleep(10)
	PyPR2.moveArmWithJointPos(**left_shooting)
	PyPR2.moveArmWithJointPos(**right_shooting)
	PyPR2.say("License to Kill")
	PyPR2.moveHeadTo(0.0,0.0)


def try():
	obj = spr.Skilled_PR2()
	obj.larm_reference = False
	
	time.sleep(10)
	obj.arm_back()

	

