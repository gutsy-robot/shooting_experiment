from SIMKit import RobotScript, Event
import PyPR2


def generate():
	
	rs = RobotScript()
	channel_torso_id = rs.addChannel("moveTorsoBy")
	asset_helloworld_id = rs.addAssetToChannel(channel_torso_id, [5], (0.03,10))
	return rs
