from SIMKit import RobotScript, Event
import PyPR2
import time

def main():
  

  rs = RobotScript()

  channel_speech_id = rs.addChannel("say")

  asset_helloworld_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello world!",))
  asset_imchip_id = rs.addAssetToChannel(channel_speech_id, [4], ("I am Gutsy!",)
  rs.play()






