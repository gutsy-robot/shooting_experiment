from SIMKit import RobotScript, Event
import PyPR2



def generate():
	
	
	rs = RobotScript()
	channel_head_id = rs.addChannel("moveHeadTo")
	channel_tuck_id = rs.addChannel("tuckBothArms")
	channel_speech_id = rs.addChannel("say")
	asset_tuck_id = rs.addAssetToChannel(channel_tuck_id, [2], ())
	asset_speech_id = rs.addAssetToChannel(channel_speech_id, [2], ("Initial lising",))
	asset_head_id = rs.addAssetToChannel(channel_head_id, [2], (2.0,0.0))
	rs.play()


