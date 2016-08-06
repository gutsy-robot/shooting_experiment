from SIMKit import RobotScript, Event
import PyPR2
import time
import commands

def main():
  

  



	
	rs = RobotScript()  
  	channel_speech_id = rs.addChannel("say")
	asset_helloworld_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello world!",))
	time.sleep(10.0)
	rs.play()

