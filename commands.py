from SIMKit import RobotScript, Event
import PyPR2



def generate():
	
	
	rs = RobotScript()
	channel_head_id = rs.addChannel("moveHeadTo")
	channel_tuck_id = rs.addChannel("tuckBothArms")
	channel_speech_id = rs.addChannel("say")
	channel_hands_id = rs.addChannel("moveArmWithJointPos")
	asset_tuck_id = rs.addAssetToChannel(channel_tuck_id, [2], ())
	asset_speech_id = rs.addAssetToChannel(channel_speech_id, [2], ("Initial lising",))
	asset_hands_id = rs.addAssetToChannel(channel_hands_id, [2], {'r_elbow_flex_joint': -0.1509690588112773, 'r_shoulder_lift_joint': -0.1, 'r_upper_arm_roll_joint': 3.955232940544562e-05, 'r_wrist_roll_joint': 0.9999717262146355, 'r_shoulder_pan_joint': 0.40000065157318243, 'r_forearm_roll_joint': 0.0, 'r_wrist_flex_joint': -0.08})
	asset_head_id = rs.addAssetToChannel(channel_head_id, [2], (2.0,0.0))
	rs.play()


