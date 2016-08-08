from SIMKit import RobotScript, Event
import PyPR2



def generate():
	
	
	rs = RobotScript()
	channel_head_id = rs.addChannel("moveHeadTo")
	channel_tuck_id = rs.addChannel("tuckBothArms")
	asset_tuck_id = rs.addAssetToChannel(channel_tuck_id, [2], ())
	asset_head_id = rs.addAssetToChannel(channel_head_id, [2], (2.0,0.0))
	rs.play()


