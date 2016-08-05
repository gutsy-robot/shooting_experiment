# Documentation of SIMKit

This is the documentation of **Smart Interactions Management Kit** (SIMKit). The present code samples are based on PyREEM version of PyRide (see https://github.com/kunle12/pyride_reem and https://github.com/uts-magic-lab/pyride_pr2). SIMKit can be used on any robot with PyRide installed.

To use SIMKit in python you just have to import the class `RobotScript` and `Event` from `SIMKit` module:

```
from SIMKit import RobotScript, Event
```

Then you can start create fancy robot scripts!


## Hello world script

A robot script is composed by **channels** and **assets**. Let's start with the small pieces of the puzzle: the assets.

An asset is simply a call to a PyRide function. For example it can be a text we want to have the robot to say, the movement of an arm, the pitch and pan of the head, or even the enrolment of a new person in the face dataset for face recognition tasks!
The asset can be played at specific times or after a certain event occurred, for example when another asset succeeded or failed, or even during more complex composed events, such as when an asset succeed after a certain time is reached.

A channel is a collection of assets. It specifies the PyRide function to use in order to run its assets and the related callback function to manage its success or failure (if available).

But putting the words into code, here is a simple example on how to design a very simple `“Hello world”` script:

```
#Creating the robot script object
rs = RobotScript()

#In this example we will have the REEM robot waving and saying hello world
#for this reason we need a channel for the speech, and another for the default motions

#to create a channel we use the method addChannel
#this method requires the PyREEM function to use in order to play the assets
#the onSuccess callback function and the onFailed callback function
#if those do not exist (or we do not want to specify them) we can use None
channel_playmotion_id = rs.addChannel("playDefaultMotion", "onPlayMotionSuccess", "onPlayMotionFailed")
channel_speech_id = rs.addChannel("say", "onSpeakSuccess", "onSpeakFailed")
 
#when creating a channel, the object RobotScript returns a string with the channelID
#we can use it to add new assets to the script

#to create an asset in a channel we use the method addAssetToChannel
#the method requires the channel_id string
#the list of starting times we want the asset to run
#and the tuple with the list of parameters for the PyREEM function specified in the channel
asset_wave_id = rs.addAssetToChannel(channel_playmotion_id, [0], ("wave",))
asset_helloworld_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello world!",))
asset_imchip_id = rs.addAssetToChannel(channel_speech_id, [4], ("I am REEM!",)

#also this time the method returns the id of the created asset
```

That's it! We just created a script with the robot waving and saying `“Hello world! I am REEM!”`. 
In this script the robot will wave right after the script is played (at 0 seconds), then say `“Hello world!”` after 2 seconds, and then `“I am REEM!”` after 2 more seconds (at 4 seconds from the beginning of the script).

Now let's run our script:

```
rs.play()
```

Easy, isn't it?! But now, here is the trick... let's say we want the script to say `“Hello”` and the name of a person that we will know only before running the script. Can we design the script in a way to be used for different names on the fly? Of course!

We can use **placeholders**. A placeholder is simply a variable inside our asset, defined as `$<name of the variable>`. The name of the variable must contains only alphanumeric characters (`[a-zA-Z0-9_]`). The current version of SIMKit can only support placeholders for parameters that are strings (_new version with more complex placeholders coming_).

```
asset_hw_placeholder_id = rs.addAssetToChannel(channel_speech_id, [2], ("Hello $NAME!",))
```

Now that we have our new asset with the placeholder we can play the script again, but before we need a dictionary in which we can specify how to translate the placeholders into proper values:

```
kb = {"NAME": "Jonathan"}
```

The dictionary can be built on the fly, just before running the script when the desired information is available. Then we can simply run the script with this new parameter:

```
rs.play(kb)
```

Obviously we can also stop a script:

```
rs.stop()
```

If so, all the channels will stop to play any further asset. However, _the assets already running would not be stopped_.


## Adding Events and Triggers

Sometimes it is preferable to synchronize assets automatically rather then using fixed times. With SIMKit it is possible to do that.
In order to do that we need to specify **events** and **triggers**. An event is a temporal situation, a change in the state of a certain asset or a composition of other events. 

But first, let's have a step back. The assets have **different states**: `off`, `on`, `succeeded`, `failed`. An asset is off when it is not playing. It is on when the asset is currently playing but not yet succeeded or failed. It is succeeded when the `onSuccess` callback function is invoked, and failed when the `onFailed` callback function is invoked. If in the channel is not specified an `onSuccess` callback function, its assets pass automatically from `“on”` to `“succeeded”`.

There are different possibilities for an action to fail in PyRide, for example when the required movement cannot reach the desired position, or when there is already a movement running for the specific required joints.

There are currently 5 types of events: `TIME_EVENT`, `SUCCEEDED_EVENT`, `FAILED_EVENT`, `AND_EVENT` and `OR_EVENT`. In the following code are shown possible examples of any event:

```
#this event occurs when 10 seconds are elapsed
#the first parameter is the type of the event
#the second parameter is the time when the event occurs
event1 = Event(Event.TIME_EVENT, 10)

#this event occurs when the helloworld asset succeeds
#the first parameter is the type of the event
#the second parameter is the asset id string we are monitoring
event2 = Event(Event.SUCCEEDED_EVENT, asset_helloworld_id)

#this event occurs when the waving fails
#the first parameter is the type of the event
#the second parameter is the asset id string we are monitoring
event3 = Event(Event.FAILED_EVENT, asset_wave_id)

#this event occurs when the helloworld asset succeeds and at least 10 seconds are elapsed
#the first parameter is the type of the event
#the second parameter is the first event to occur
#the third parameter is the second event to occur
event4 = Event(Event.AND_EVENT, event1, event2)

#this event occurs when the helloworld asset succeeds or if at least 10 seconds are elapsed, whichever first
#the first parameter is the type of the event
#the second parameter is the first event to monitor
#the third parameter is the second event to monitor
event5 = Event(Event.OR_EVENT, event1, event2)
```

Obviously, there is no limit in composing events of type `AND_EVENT` and `OR_EVENT`.

In order to play a specific asset when an event occurs we need a trigger. Let's say we want to say `“I am REEM”` 1 second after the `“Hello world”` asset fully succeeded. To create this trigger is very simple with the method `addTrigger`:

```
rs.addTrigger(asset_imchip_id, event2, 1, 1)
```

The first parameter of this method is the `assetID` string of the asset we need to run when the trigger is triggered.
The second parameter is the previously created event, in this case a `SUCCEEDED_EVENT` of the asset `helloworld`.
The third parameter is the delay time, namely how many seconds the trigger needs to wait until playing the referred asset.
The fourth parameter is the number of times the trigger needs to be triggered. If 1, the trigger is launched and then disabled, otherwise if greater than 1 and the same event occurs multiple times, the trigger is launched multiple times. If None, the trigger is launched infinite times.


## Play a default state script when the main script is committed

Another cool feature is the possibility to create a script to use as a “**default state**” of the robot to play right after the main script is fully committed. For example, coming back to the home position and setting the monitor to the Magic Lab webpage.
To avoid to duplicate this information multiple times in the scripts with the risk of possible errors, it is possible to add a default script to the main script (_not fully tested_).

In this following code we create a default state script first, and then add it to our main robot script previously created:

```
import json

#this script returns CHIP to home position and set its monitor to the CBA logo
default_rs = RobotScript()

channel_playmotion_id = default_rs.addChannel("playDefaultMotion", "onPlayMotionSuccess", "onPlayMotionFailed")
channel_monitor_id = default_rs.addChannel("directToWeb")

default_rs.addAssetToChannel(channel_playmotion_id, [0], ("home",))
default_rs.addAssetToChannel(channel_monitor_id, [0], ("http://themagiclab.org/",))

#now that we created the default state script 
#we can add it to the main script with setDefaultStateScript method
rs.setDefaultStateScript(default_rs, delay=0.5, script_KB={})

#the method takes:
#as first parameter the default state script to run after the main script is committed
#as second parameter the optional time delay to wait after the main script committed
#as third paramter the optional dictionary to use in order to translate the placeholders of the default state script
```



## How to manage the commitment of a script

If we need to know when the script is fully committed, we can also add a callback function to be invoked when the script fully commits (_not fully tested_).

```
rs.setOnCommitCallbackFunction(my_callback_function)
```

The parameter of this method is the callback function to be invoked when the script fully commits (if it has a default state script, after the default state script fully committed). The callback function needs to have one parameter, namely the notifier `RobotScript` object (at the moment the callback takes no parameters but I will change it for more convenience):

```
def my_callback_function(notifier):
  notifier.printNotificationsHystory()
```

In this example we can use the method `printNotificationsHystory` (_to be done soon_) of the notifying committed `RobotScript` object to retrieve the timeline hystory of all the assets states for each channel:

```
--------
channel_say
--------
2s: asset_1@channel_say -> ON
3.2s: asset_1@channel_say -> SUCCEEDED
4.2s: asset_2@channel_say -> ON
5.5s: asset_2@channel_say -> SUCCEEDED

--------
channel_playDefaultMotion
--------
0s: asset_1@channel_playDefaultMotion -> ON
4s: asset_1@channel_playDefaultMotion -> SUCCEEDED
```

This information can be useful to debug and test a robot script.


## Export and Import scripts with JSON

After we created and tested a script, it is convenient to save it on a file. With SIMKit it is possible to do that with just a line of code:

```
rs.exportToJSON(where_we_are_saving_the_file)
```

This method requires the URL where we desire to save the exported JSON file. The URL must include the name of the file with the extension .json.

The exportation process will include assets, channels, triggers and the default state script. It will not export the onCommit callback function, since this is independent from the script.

If we want to import the script from a previously saved json file we can do that again with a single line of code:

```
rs = RobotScript.importFromJSON(url_where_we_saved_the_file)
```

The method requires the URL where the script file in json is saved, and it returns the functioning `RobotScript` object.

To playback the script we need simply to play it again:

```
rs.play()
```


