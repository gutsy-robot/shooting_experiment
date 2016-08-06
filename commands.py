from SIMKit import RobotScript, Event
import PyPR2


def generate():
	rs = RobotScript()
	channel_speech_id = rs.addChannel("say")
	
	asset_helloworld_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello world!",))
	rs.play()
		
