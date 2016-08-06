from SIMKit import RobotScript, Event
import PyPR2
import time
import commands

def main():
  

  rs = RobotScript()

  channel_speech_id = rs.addChannel("say")
	
  asset_hello_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello!"))
  
  
  a = commands(rs)
  a.play()





