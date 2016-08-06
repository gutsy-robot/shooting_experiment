from SIMKit import RobotScript, Event
import PyPR2
import time
import commands

def main():
  

  play()


def play():
	time.sleep(10.0)
	rs = RobotScript()

  channel_speech_id = rs.addChannel("say")
	
  asset_hello_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello!"))
  
  
  rs.play()
	




