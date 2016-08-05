"""SIMKit
Smart Interactions Manager Kit:

This module contains the classes for composing a robot script

ActionAsset class:
This class represents a single asset to play. It can be a sequence of joints, a default action, a speech, etc.

AssetTrigger class:
This class represents a trigger for managing the behaviour of an ActionAsset based on a certain Event

Event class:
This class represents an events tree to check whether or not a certain state happened, in order to trigger the proper triggers

TriggersDispatcher class:
This class collects a set of AssetTrigger and manage the notifications from the channels whenever an asset change its status or a timed event is elicited

AssetsChannel class
This class represents a single channel of the robot for expressing itself.

RobotScript class
This class represents a single script composed by several channels.
"""

__version__ = "0.1"
__author__ = "Jonathan Vitale"

from pyridemodule import PyRideModule
installed_module = PyRideModule.getInstalledModule()
if installed_module != None:
	PyRide = __import__(installed_module)
else:
	raise ImportError('No PyRide module detected. Please, check that the PyRide module is correctly installed.')

import functools
import threading
import time
import random
import re
import json

'''
#FOR TESTING
class PyRide:
	
	onPlayMotionSuccess = None
	onPlayMotionFailed = None
	
	@staticmethod
	def playDefaultMotion(*args):
		print("Executing: playDefaultMotion")
		threading.Timer(2, PyRide.onPlayMotionSuccess, ()).start()
	
	onSpeakSuccess = None
	onSpeakFailed = None
	
	@staticmethod
	def say(*args):
		print("Executing: say")
		threading.Timer(2, PyRide.onSpeakSuccess, ()).start()
	
	onMoveTorsoSuccess = None
	onMoveTorsoFailed = None
	
	@staticmethod
	def moveTorsoTo(*args):
		print("Executing: moveTorsoTo")
		threading.Timer(2, PyRide.onMoveTorsoSuccess, ()).start()
	
	@staticmethod
	def moveTorsoWithJointTrajectory(*args):
		print("Executing: moveTorsoWithJointTrajectory")
		threading.Timer(2, PyRide.onMoveTorsoSuccess, ()).start()
	
	onHeadActionSuccess = None
	onHeadActionFailed = None
	
	@staticmethod
	def moveHeadTo(*args):
		print("Executing: moveHeadTo")
		threading.Timer(2, PyRide.onHeadActionSuccess, ()).start()
	
	onMoveArmActionSuccess = None
	onMoveArmActionFailes = None
	
	@staticmethod
	def moveArmWithJointTrajectory(*args):
		print("Executing: moveArmWithJointTrajectory")
		threading.Timer(2, PyRide.onMoveArmActionSuccess, ()).start()
		
	@staticmethod
	def setEarLED(*args):
		print("Executing: setEarLED")
	
	@staticmethod
	def sendMessageToNode(*args):
		print("Executing: sendMessageToNode")
	
	@staticmethod
	def directToWeb(*args):
		print("Executing: directToWeb")

'''		

class ActionAsset:
	STATE_OFF = 0
	STATE_ON = 1
	STATE_SUCCEEDED = 2
	STATE_FAILED = 3
	
	def __init__(self, action_asset_id, asset_content):
		self.id = action_asset_id
		self.content = asset_content #the parameters for the PyRide function used to play the asset
		self.content_with_kb = asset_content #the parameters after replacing the placeholders with the KB variables
		self.state = ActionAsset.STATE_OFF
		
	def getActionAssetContent(self):
		return self.content_with_kb
	
	def setActionAssetContent(self, asset_content):
		self.content = asset_content
	
	def getActionAssetID(self):
		return self.id
	
	def getActionAssetState(self):
		return self.state
	
	@staticmethod
	def getStateAsString(action_state):
		if action_state == ActionAsset.STATE_OFF:
			return "off"
		if action_state == ActionAsset.STATE_ON:
			return "on"
		if action_state == ActionAsset.STATE_SUCCEEDED:
			return "succeeded"
		if action_state == ActionAsset.STATE_FAILED:
			return "failed"
	
	def setStateOff(self):
		self.state = ActionAsset.STATE_OFF
	
	def setStateOn(self):
		self.state = ActionAsset.STATE_ON
	
	def setStateSucceeded(self):
		self.state = ActionAsset.STATE_SUCCEEDED
	
	def setStateFailed(self):
		self.state = ActionAsset.STATE_FAILED
	
	def substitutePlaceholdersWithKB(self, script_KB):
		#check in the asset contents if there are placeholders ($<name placeholder>) and sobstitute them
		#at the moment the method works only with string variables
		
		#substitute the placeholders
		new_content = []
		for content in self.content:
			if isinstance(content, basestring):
				matches = re.findall("\$(\w+)",content)
				for match in matches:
					if script_KB.has_key(match):
						content = content.replace("$"+match, script_KB[match])
			new_content.append(content)
		
		self.content_with_kb = tuple(new_content)
	
	def unsetContentsWithKB(self):
		self.content_with_kb = self.content

class AssetTrigger:
	
	def __init__(self, trigger_id, ref_asset_id, trigger_event, delay=0, times=1):
		self.id = trigger_id #the id of the trigger. Must to be unique in a single dispatcher.
		self.ref_asset_id = ref_asset_id #the reference id of the asset to trigger
		self.trigger_event = trigger_event #the triggering event
		self.trigger_delay = delay
		self.times = times #number of times the trigger can be triggered (None = infinite times)
		self.times_counter = times
	
	def getAssetTriggerID(self):
		return self.id
		
	def getReferenceAssetID(self):
		return self.ref_asset_id
	
	def isTriggerActive(self):
		if self.times_counter == None or self.times_counter > 0:
			return True
		else:
			return False
	
	def disable(self):
		self.times_counter = 0
	
	def reset(self):
		self.times_counter = self.times
		self.trigger_event.reset()
	
	def run(self):
		self.times_counter -= 1
	
class Event:
	TIME_EVENT = 0 #this type of event requires 1 argument: time_to_start
	SUCCEEDED_EVENT = 1 #this type of event requires 1 argument: ref_asset_id
	FAILED_EVENT = 2 #this type of event requires 1 argument: ref_asset_id
	AND_EVENTS = 3 #this type of event requires 2 arguments: event1 and event2
	OR_EVENTS = 4 #this type of event requires 2 argument2: event1 and event2
	
	def __init__(self, event_type, *event_args):
		if event_type == Event.TIME_EVENT or event_type == Event.SUCCEEDED_EVENT or event_type == Event.FAILED_EVENT:
			self.left = None
			self.right = None
		else:
			#It is a AND or OR, event_args contains two events to compose together
			self.left = event_args[0]
			self.right = event_args[1]
		
		self.data = {"event_type":event_type, "event_args": event_args, "value":False}
	
	def assessEvent(self): #verify if the Event tree is True or False (if the event happened or not)
		if self.data["event_type"] == Event.TIME_EVENT or self.data["event_type"] == Event.SUCCEEDED_EVENT or self.data["event_type"] == Event.FAILED_EVENT:
			return self.data["value"]
		elif self.data["event_type"] == Event.AND_EVENTS:
			return self.left.assessEvent() and self.right.assessEvent()
		else:
			return self.left.assessEvent() or self.right.assessEvent()
	
	def propagateNewState(self, asset_id, asset_state): #propagates the new informed state of the asset through the Event tree
		if (((self.data["event_type"] == Event.SUCCEEDED_EVENT) and (asset_state == ActionAsset.STATE_SUCCEEDED)) or ((self.data["event_type"] == Event.FAILED_EVENT) and (asset_state == ActionAsset.STATE_FAILED))) and self.data["event_args"][0] == asset_id:
			self.data["value"] = True
		if self.left != None:
			self.left.propagateNewState(asset_id, asset_state)
		if self.right != None:
			self.right.propagateNewState(asset_id, asset_state)
	
	def getTimedEvents(self):
		event_list = []
		if self.data["event_type"] == Event.TIME_EVENT:
			event_list.append(self)
		
		if self.left != None:
			event_list.extend(self.left.getTimedEvents())
		
		if self.right != None:
			event_list.extend(self.right.getTimedEvents())
		
		return event_list
	
	def reset(self):
		self.data["value"] = False
		if self.left != None:
			self.left.reset()
		if self.right != None:
			self.right.reset()
	
	def toDictStructure(self):
		event_args = []
		for arg in self.data["event_args"]:
			if isinstance(arg, Event):
				arg = arg.toDictStructure()
			event_args.append(arg)
		data = {"event_type":self.data["event_type"], "event_args": tuple(event_args), "value":False}
		if self.left == None:
			return {"data": data, "left": None, "right": None}
		else:
			return {"data": data, "left": self.left.toDictStructure(), "right": self.right.toDictStructure()}
	
	@staticmethod
	def eventFromDict(e_dict):
		event_args = []
		for arg in e_dict["data"]["event_args"]:
			if isinstance(arg, dict):
				event_args.append(Event.eventFromDict(arg))
			else:
				event_args.append(arg)
		init_func = functools.partial(Event, e_dict["data"]["event_type"])
		for arg in event_args:
			init_func = functools.partial(init_func, arg)
		return init_func()#Event(e_dict["data"]["event_type"], event_args)
		
class TriggersDispatcher:
	
	def __init__(self, on_dispatch_callback):
		self.triggers = {}
		self.notificatons_log = {}
		self.on_dispatch_callback = on_dispatch_callback #the function called whenever it is necessary to dispatch a trigger. The function takes 1, the triggered trigger
	
	#notifiers
	
	def notifyAssetState(self, asset_id, asset_state):
		at_pos = asset_id.index('@')
		channel_id = asset_id[at_pos+1:]
		if not self.notifications_log.has_key(channel_id):
			self.notifications_log.update({channel_id: []})
		
		current_log = {"asset_id":asset_id, "asset_state": asset_state, "notification_time": time.time()}
		self.notifications_log[channel_id].append(current_log)
		
		#current_log_str = {"asset_id":asset_id, "asset_state": ActionAsset.getStateAsString(asset_state), "notification_time": time.time()}
		#print(current_log_str)
		
		if asset_state == ActionAsset.STATE_FAILED or asset_state == ActionAsset.STATE_SUCCEEDED: #In this case I need to notify the event trees and run the trigger dispatcher
			for trigger in self.triggers.values():
				#In each trigger I seek for reference of the asset_id in the trigger event tree and set the value based on the asset_state and event_type
				trigger.trigger_event.propagateNewState(asset_id,asset_state)
				self.evaluateTriggers() #something new happened, so I run the trigger dispatcher to see if there are triggers to run
			
	def notifyTimeEvent(self, event, notifier):
		#the time event is notified, so it means the event must be now true
		event.data["value"] = True
		notifier.timedEventSucceeded()
		self.evaluateTriggers() #something new happened, so I run the trigger dispatcher to see if there are triggers to run
	
	#GETs
	
	def countTriggers(self):
		return len(self.triggers)
	
	def getNextTriggerID(self, ref_asset_id):
		return "trigger_"+str(self.countTriggers()+1)+":"+ref_asset_id
	
	def getAssetTriggerOfAssetID(self, asset_id):
		asset_trigger_ids = []
		for trigger in self.triggers.values():
			if trigger.ref_asset_id == asset_id:
				asset_trigger_ids.append(trigger.id)
		
		return asset_trigger_ids
	
	def getTriggersAtChannel(self, at_channel): #returns a list of triggers referring to assets of a specific channel
		triggers_list = []
		for trigger in self.triggers.values():
			trigger_id = trigger.getAssetTriggerID()
			at_pos = trigger_id.index('@')
			channel_id = trigger_id[at_pos+1:]
			if channel_id == at_channel:
				triggers_list.append(trigger)
		
		return triggers_list
	
	def getTimedEventsAtChannel(self, at_channel):
		events_list = []
		triggers_list = self.getTriggersAtChannel(at_channel)
		for trigger in triggers_list:
			events_list.extend(trigger.trigger_event.getTimedEvents())
			
		return events_list
	
	#add / remove / disable / reset triggers
	
	def addAssetTrigger(self, asset_trigger):
		self.triggers.update({asset_trigger.getAssetTriggerID(): asset_trigger})
	
	def removeAssetTrigger(self, asset_trigger_id):
		del self.triggers[asset_trigger_id]
	
	def disableAssetTrigger(self, asset_trigger_id):
		self.triggers[asset_trigger_id].disable()
	
	def removeAssetTriggerWithAssetID(self, asset_id):
		to_remove = self.getAssetTriggerOfAssetID(asset_id)
		for key in to_remove:
			self.removeAssetTrigger(key)
	
	def disableAssetTriggerWithAssetID(self, asset_id):
		to_remove = self.getAssetTriggerOfAssetID(asset_id)
		for key in to_remove:
			self.disableAssetTrigger(key)
		
	def reset(self, at_channel): #reset the state of the triggers for assets at a specific channel to their initial states
		triggers_list = self.getTriggersAtChannel(at_channel)
		for trigger in triggers_list:
			trigger.reset()
	
	def clearNotificationsLog(self):
		self.notifications_log = {}
	
	#run triggers
	
	def evaluateTriggers(self):
		for trigger in self.triggers.values():
			if trigger.isTriggerActive() and trigger.trigger_event.assessEvent(): #the trigger is active and the Event Tree results True
				trigger.run() #decrease times
				self.on_dispatch_callback(trigger) #play the referenced asset

class AssetsChannel:
	STATE_STOP = 0
	STATE_PLAY = 1
	
	def __init__(self, channel_id, pyride_topic, triggers_dispatcher, on_channel_committed_callback, pyride_on_success_func=None, pyride_on_fail_func=None):
		self.id = channel_id #the channel id. Must be unique in a single script.
		self.pyride_topic = pyride_topic #the pyride topic used to play the assets of the channel
		self.dispatcher = triggers_dispatcher #the triggers dispatcher to manage the asset triggers
		self.callback_func_channel_committed = on_channel_committed_callback #the callback function called whenever the channel fully committed the script
		self.on_success_function = pyride_on_success_func #the pyride function name (string) for managing onSuccess callback function
		self.on_fail_function = pyride_on_fail_func #the pyride function name (string) for managing onFail callback function
		self.assets = {} #the dictionary of assets contained in the channel
		self.channel_state = AssetsChannel.STATE_STOP
		self.count_timed_threads = 0
		self.asset_playing = None
	
	#callback managers
	
	def manageAssetOnSuccess(self, argvar=()):
		succeeded_asset = self.asset_playing
		if succeeded_asset != None:
			succeeded_asset.setStateSucceeded()
			self.asset_playing = None
			self.dispatcher.notifyAssetState(succeeded_asset.getActionAssetID(),succeeded_asset.getActionAssetState())
			
			self.updateChannelState()
	
	def manageAssetOnFailed(self, argvar=()):
		failed_asset = self.asset_playing 
		if failed_asset != None:
			failed_asset.setStateFailed()
			self.asset_playing = None
			self.dispatcher.notifyAssetState(failed_asset.getActionAssetID(),failed_asset.getActionAssetState())
			
			self.updateChannelState()
	
	def timedEventSucceeded(self):
		self.count_timed_threads -= 1
	
	#GETs
	
	def getChannelID(self):
		return self.id
	
	def getNextAssetID(self):
		return "asset_"+str(self.countAssets()+1)+"@"+self.id
	
	def countAssets(self):
		return len(self.assets)
	
	def channelState(self):
		return self.channel_state
		
	#add asset, SETs
	
	def addAsset(self, action_asset, times_to_start): #times_to_start is a list of times, empty if the asset has to be triggered in non timed events
		self.assets.update({action_asset.getActionAssetID():action_asset})
		for cur_time in times_to_start:
			cur_trigger_id = self.dispatcher.getNextTriggerID(action_asset.getActionAssetID())
			e = Event(Event.TIME_EVENT, cur_time)
			t = AssetTrigger(cur_trigger_id,action_asset.getActionAssetID(), e)
			self.dispatcher.addAssetTrigger(t)
		
	def updateChannelState(self):
		any_asset_on = False
		#I check if there is still an asset in state On, waiting for the callback function
		for asset in self.assets.values():
			if asset.getActionAssetState() == ActionAsset.STATE_ON:
				any_asset_on = True
		
		if self.count_timed_threads <= 0 and  not any_asset_on:
			#no more timed events for assets on this channel
			self.channel_state = AssetsChannel.STATE_STOP
			self.callback_func_channel_committed(self)
		
	#play / stop
	
	def playAsset(self, asset_id): #TO CHECK if running two assets on the same channel makes the first being failed with the callback
		#only one asset at each time in each channel can play
		if self.asset_playing != None:
			#if this happens it means that another asset is cancelling a previously playing one
			self.asset_playing.setStateOff()
			self.dispatcher.notifyAssetState(self.asset_playing.getActionAssetID(),self.asset_playing.getActionAssetState())
			self.asset_playing = None
		
		if self.channel_state == AssetsChannel.STATE_STOP: 
			#this condition might happen if the channel committed, but another trigger based on an event involving assets 
			#from another channel triggered an asset of this channel
			self.channel_state = AssetsChannel.STATE_PLAY
		
		asset_to_play = self.assets[asset_id]
		pr_play = getattr(PyRide, self.pyride_topic)
		asset_attributes = asset_to_play.getActionAssetContent()

		for attribute in asset_attributes:
			pr_play = functools.partial(pr_play, attribute)
		
		self.asset_playing = asset_to_play
		asset_to_play.setStateOn()
		self.dispatcher.notifyAssetState(asset_to_play.getActionAssetID(),asset_to_play.getActionAssetState())
		pr_play()
		
		#if the channel does not have a callback function for success, I send the state to success immediately
		if self.on_success_function == None:
			self.manageAssetOnSuccess()
	
	def stop(self): #this method prevent ANY asset of the current channel to be played (the channel is "mute")
		for asset in self.assets.values():
			asset.setStateOff()
			self.dispatcher.disableAssetTriggerWithAssetID(asset.getActionAssetID())
		
		self.channel_state = AssetsChannel.STATE_STOP

	def play(self): #this method arms the triggers related with the assets in this channel, so that the channel can potentially play assets
		#add the callback functions
		if self.on_success_function != None:
			setattr(PyRide, self.on_success_function, self.manageAssetOnSuccess)
		
		if self.on_fail_function != None:
			setattr(PyRide, self.on_fail_function, self.manageAssetOnFailed)
			
		self.channel_state = AssetsChannel.STATE_PLAY
		self.dispatcher.reset(self.getChannelID()) #enable the triggers referring to assets of this channel
		
		#gather all the events having type TIME_EVENT and referring to asset of this channel
		timed_channel_events = self.dispatcher.getTimedEventsAtChannel(self.getChannelID())
		#create timed threads that notify the dispatcher at the given time
		for e in timed_channel_events:
			event_time_to_start = e.data["event_args"][0]
			self.count_timed_threads += 1 #increasing the counter of the active timed threads, so to know when the channel has committed and stop it
			threading.Timer(event_time_to_start, self.dispatcher.notifyTimeEvent, (e,self)).start()

class RobotScript:
	
	def __init__(self):
		self.script_channels = {}
		self.dispatcher = TriggersDispatcher(self.manageTrigger)
		self.default_state_script = None
		self.on_commit_callback_func = None
		self.obj_dict = {"channels": {}, "assets": {}, "triggers": {}, "default_state_script": None}
		self.log = []
		self.start_time = None
		
	#CALLBACK FUNCTIONS
		
	def onChannelCommitted(self, notifier): #TODO check when channel has only ON state asset without callback
		#check if there is at least some channel still playing
		for channel in self.script_channels.values():
			if channel.channelState() == AssetsChannel.STATE_PLAY:
				return False
		
		#if here it means that all the channels are in state STOP and so the script is fully committed
		self.stop()
		
		#check if there is a default state script, and run it if so
		if self.default_state_script != None:
			default_script = self.default_state_script["script"]
			delay = self.default_state_script["delay"]
			KB = self.default_state_script["KB"]
			threading.Timer(delay, default_script.play, (KB,)).start()
			
			return False
		else:
			#no more things to run, so commit back
			if self.on_commit_callback_func != None:
				self.on_commit_callback_func()
			
			return True
	
	def manageTrigger(self, trigger):
		#the asset id is composed by: asset_id@channel_id
		asset_id = trigger.getReferenceAssetID()
		at_pos = asset_id.index('@')
		channel_id = asset_id[at_pos+1:]
		self.log.append("RobotScript.manageTrigger -> trigger = {ref_asset_id: "+asset_id+", at_channel_id: "+channel_id+", trigger_delay: "+str(trigger.trigger_delay)+"}")
		threading.Timer(trigger.trigger_delay, self.script_channels[channel_id].playAsset, (asset_id,)).start()
	
	#ADD CHANNELS, ASSETS, TRIGGERS, DEFAULT STATE SCRIPT, ON COMMIT CB FUNCTION
	
	def addChannel(self, pyride_topic, pyride_on_success_func=None, pyride_on_fail_func=None):
		channel_id = "channel_"+pyride_topic
		channel = AssetsChannel(channel_id, pyride_topic, self.dispatcher, self.onChannelCommitted, pyride_on_success_func, pyride_on_fail_func)
		self.script_channels.update({channel_id: channel})
		self.obj_dict["channels"].update({channel_id: {"pyride_topic": pyride_topic, "pyride_on_success_func": pyride_on_success_func, "pyride_on_fail_func": pyride_on_fail_func}})
		return channel_id
	
	def addAssetToChannel(self, channel_id, times_to_start, asset_content):
		asset_id = self.script_channels[channel_id].getNextAssetID()
		asset = ActionAsset(asset_id, asset_content)
		self.script_channels[channel_id].addAsset(asset, times_to_start)
		self.obj_dict["assets"].update({asset_id: {"channel_id": channel_id, "times_to_start": times_to_start, "asset_content": asset_content}})
		return asset_id
	
	def addTrigger(self, ref_asset_id, trigger_event, delay=0, times=1):
		trigger_id = self.dispatcher.getNextTriggerID(ref_asset_id)
		trigger = AssetTrigger(trigger_id, ref_asset_id, trigger_event, delay, times)
		self.dispatcher.addAssetTrigger(trigger)
		self.obj_dict["triggers"].update({trigger_id: {"ref_asset_id": ref_asset_id, "trigger_event": trigger_event.toDictStructure(), "delay": delay, "times":times}})
		return trigger_id
	
	def unsetDefaultStateScript(self):
		self.default_state_script = None
		self.obj_dict["default_state_script"] = None
		
	def setDefaultStateScript(self, default_state_script, delay=0, script_KB={}):
		default_state_script.setOnCommitCallbackFunction(self.on_commit_callback_func) #when the default state script ends, it will call the on commit callback function of this object
		default_state_script.unsetDefaultStateScript() #avoid a further level, only 1 default script can follow a script
		self.default_state_script = {"script": default_state_script, "delay": delay, "KB": script_KB}
		self.obj_dict["default_state_script"] = {"script": default_state_script.toDictStructure(), "delay": delay, "KB": script_KB}
	
	def unsetOnCommitCallbackFunction(self):
		self.on_commit_callback_func = None
	
	def setOnCommitCallbackFunction(self, callback_function):
		self.on_commit_callback_func = callback_function
	
	#CHECK STATUS
	
	def isScriptPlaying(self):
		#check if there is a channel still playing
		for item in self.script_channels.values():
			if item.channelState() == AssetsChannel.STATE_PLAY:
				return True
		
		#now check if the default state script is playing
		if self.default_state_script != None:
			return self.default_state_script["script"].isScriptPlaying()
		
		#nothing is still playing
		return False
	
	def printNotificationsLog(self):
		for channel_id in self.dispatcher.notifications_log.keys():
			print(" ")
			print("------------------")
			print(channel_id+":")
			print("------------------")
			logs = self.dispatcher.notifications_log[channel_id]
			for log in logs:
				log["notification_time"] -= self.start_time
				log["asset_state"] = ActionAsset.getStateAsString(log["asset_state"])
				print(log)
	
	#PLAY / STOP
	
	def play(self, script_KB={}):
		self.start_time = time.time()
		self.dispatcher.clearNotificationsLog()
		
		#first I substitute the asset placeholders
		for channel in self.script_channels.values():
			for asset in channel.assets.values():
				asset.substitutePlaceholdersWithKB(script_KB)
		
		self.playChannels(self.script_channels.keys())
	
	def playChannels(self, channel_ids):
		for channel_key in channel_ids:
			self.script_channels[channel_key].play()
			
	def stop(self):
		self.stopChannels(self.script_channels.keys())
		
		#unset the replaced placeholders
		for channel in self.script_channels.values():
			for asset in channel.assets.values():
				asset.unsetContentsWithKB()
	
	def stopChannels(self, channel_ids):
		for channel_key in channel_ids:
			self.script_channels[channel_key].stop()
	
	#IMPORT EXPORT SCRIPTS
	
	@staticmethod
	def importFromJSON(url):
		with open(url) as fp:
			obj_dict = json.load(fp)
			
		return RobotScript.importFromDict(obj_dict)
		
	@staticmethod
	def importFromDict(obj_dict):
		rs = RobotScript()

		for channel in obj_dict["channels"].values():
			rs.addChannel(channel["pyride_topic"], channel["pyride_on_success_func"], channel["pyride_on_fail_func"])
		
		for asset in obj_dict["assets"].values():
			rs.addAssetToChannel(asset["channel_id"],asset["times_to_start"],asset["asset_content"])
		
		for trigger in obj_dict["triggers"].values():
			trigger_event = Event.eventFromDict(trigger["trigger_event"])
			rs.addTrigger(trigger["ref_asset_id"], trigger_event, trigger["delay"], trigger["times"])
		
		if obj_dict["default_state_script"] != None:
			ds = RobotScript.importFromDict(obj_dict["default_state_script"]["script"])
			rs.setDefaultStateScript(ds, obj_dict["default_state_script"]["delay"], obj_dict["default_state_script"]["KB"])
		
		return rs
		
	def exportToJSON(self, url):
		obj_dict = self.toDictStructure()
		with open(url, 'w+') as fp:
			json.dump(obj_dict, fp)
	
	def toDictStructure(self):
		return self.obj_dict
