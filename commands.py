from SIMKit import RobotScript, Event
import PyPR2



def generate():
	
	rs = create_obj()

	channel_torso_id = rs.addChannel("moveTorsoBy")
	asset_helloworld_id = rs.addAssetToChannel(channel_torso_id, [5], (0.06,10))
	return rs


def create_obj():
	a = RobotScript()
	return a
	
