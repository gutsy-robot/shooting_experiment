from SIMKit import RobotScript, Event
import PyPR2



def generate():
	
	
	rs = RobotScript()
	channel_head_id = rs.addChannel("moveHeadTo")
	asset_head_id = rs.addAssetToChannel(channel_head_id, [2], (2.0,2.0))
	rs.play()


