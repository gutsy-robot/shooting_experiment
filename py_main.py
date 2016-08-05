from SIMKit import RobotScript, Event
import PyPR2

def main():
rs = RobotScript()
channel_playmotion_id = rs.addChannel("playDefaultMotion", "onPlayMotionSuccess", "onPlayMotionFailed")
channel_speech_id = rs.addChannel("say", "onSpeakSuccess", "onSpeakFailed")
asset_wave_id = rs.addAssetToChannel(channel_playmotion_id, [0], ("wave",))
asset_helloworld_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello world!",))
asset_imchip_id = rs.addAssetToChannel(channel_speech_id, [4], ("I am REEM!",)
rs.play()






