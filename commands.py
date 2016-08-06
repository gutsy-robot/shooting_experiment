from SIMKit import RobotScript, Event
import PyPR2


def generate():
	
	rs = RobotScript()
	channel_torso_id = rs.addChannel("moveTorsoBy")
	channel_head_id = rs.addChannel("moveHeadTo")
	asset_torso_id = rs.addAssetToChannel(channel_torso_id, [3], (-0.03,10))
	asset_head_id = rs.addAssetToChannel(channel_head_id, [14], (2.0,0.2))
	return rs

 
