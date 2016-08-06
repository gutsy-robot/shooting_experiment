from SIMKit import RobotScript, Event
import PyPR2


def generate():
	rs = RobotScript()
	channel_speech_id = rs.addChannel("say")
	channel_torso_id = rs.addChannel("moveTorsoBy")
	asset_helloworld_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello world!",))
	asset_Sid_id = rs.addAssetToChannel(channel_speech_id, [7], ("Hi Sid!",))
	rs.play()
		
