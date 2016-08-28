
import PyPR2
import math
class Detection(object):
	
  LOST_OBJ = 0

  NEW_OBJ  = 1
  REC_OBJ  = 2
  
  def __init__(self):	
    PyPR2.registerHumanDetectTracking(self.onHumanDetected, self.onHumanTracking)

  def onHumanDetected( self, objtype, trackid, nameid, status ):
       PyPR2.say("Hi")
    
  def onHumanTracking(self,tracking_objs ):
    focus_obj = None
    for obj in tracking_objs:
      if obj['est_pos'][0] < 4 and obj['est_pos'][0] >= 0:
        if not focus_obj or focus_obj['est_pos'][0] > obj['est_pos'][0]:
          focus_obj = obj

        if focus_obj:
      	  mid_x = focus_obj['bound'][0] + focus_obj['bound'][2] / 2
          mid_y = focus_obj['bound'][1] + focus_obj['bound'][3] / 2
      #print "track obj {} mid pt ({}.{})".format(focus_obj['track_id'],mid_x,mid_y)
          ofs_x = mid_x - 320
          ofs_y = mid_y - 240
          chx = chy = 0.0
          if math.fabs(ofs_x) > 10:
             chx = -ofs_x * 90.0 / 640 * 0.01745329252
      	  if math.fabs(ofs_y) > 10:
             chy = ofs_y * 90.0 / 640 * 0.01745329252
     	  PyPR2.updateHeadPos( chx, chy )
  

