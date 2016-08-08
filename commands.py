from SIMKit import RobotScript, Event
import PyPR2


global rs

rs = RobotScript()

def generate():
	
	

	channel_torso_id = rs.addChannel("moveTorsoBy")
	asset_helloworld_id = rs.addAssetToChannel(channel_torso_id, [5], (0.06,10))
	return rs

	
