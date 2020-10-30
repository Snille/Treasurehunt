#!/usr/bin/env python3
#coding=utf-8

import RPi.GPIO as GPIO
from hx711 import HX711
import time
import sys
import os
import os.path
from os import path
from adafruit_servokit import ServoKit
import random
import json
import urllib.request
import requests
import alsaaudio

## Servo information
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
# Servo locking chest angle.
lockangle = 15
# Servo unlocking chest angle.
unlockangle = 130

## Coin stuff
# Coin weight number ratio in House: 855
ratio = 855
# Coin weight number ratio in Workshop: 827
#ratio = 827
# Coins to collect for the chest to open (100).
goal = 100
#goal = 3
# Set to 1 if it is ok to add more coins then specified in goal (chest opens when goal or higher is reached) otherwise it must be the exact goal number.
overgoalok = 1

## Button stuff
# Pin used for the lid switch. Low when the lid is closed.
lidpin = 23
# Secret open switch Pin.
secretpin = 24

## Smoke machine stuff.
# Smoke generator available (1 or 0).
usesmoke = 1
# When smoke machine is ready (warm). Set to 0 if not available on your smoke machine.
smokereadypin = 0
#smokereadypin = 24
# Smoke activation trigger When activated smoke is generated.
smokeactivatepin = 27
# Smoke machine warm up time in seconds (if the ready signal is not available).
smokewarmuptime = 150 # 2,5 minutes
#smokewarmuptime = 10 # 10 seconds
# Fill the room with smoke at start (1 or 0).
smokefill = 1
# How long (in seconds) to fill the room with smoke.
smokefilltime = 30 # 30 seconds
# Smoke "puff" time. The time in seconds the smoke machine will puff out new smoke during the "laughs".
smokepufftime = 1 # 1 second

## Sound settings
# Play the chest sounds (0 for no 1 for yes).
playsound = 1
# The directory where the sounds are located.
sounddir = "Sounds"
# Set Alsa "headphone jack" volume to "volume".
alsavolume = 100
# Start number for information sample (1, 2, 3).
info = 1

## MagicMirror stuff
# Post to the MagicMirror (1 = on or 0 = off).
mmpost = 1
# MagicMirror IP and port.
#mmip = "10.0.0.20" # Development MagicMirror.
#mmport = "8181"
mmip = "10.0.0.112" # Actual MagicMirror.
mmport = "8080"

# Time to wait before going back to the "normal" profile on the MagicMirror.
waittime = 300 # Five minutes.
#waittime = 30 # 30 seconds. 

# MagicMirror MMM-Remote-Control module commands to build on.
profilechange = "http://" + mmip + ":" + mmport + "/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload="
showmodule = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module="
hidemodule = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module="

# MagicMirror treasure hunt Profile (sent to the MMM-Remote-Control module that changes profile via MMM-ProfileSwitcher).
startprofile = profilechange + "Skattjakt"
# MagicMirror treasure hunt win profile.
endprofile = profilechange + "Grattis"
# MagicMirror "normal" profile.
normalprofile = profilechange + "Louise"

# MagicMirror modules to show / hide.
# Shows and hides the IFTTT module at the end.
showiftttmodule = showmodule + "module_54_MMM-IFTTT"
hideiftttmodule = hidemodule + "module_54_MMM-IFTTT"

# Shows and hides: http://localhost/img/magicmirror/decoration/pirate-with-flag.png
showprestartmodule = showmodule + "module_15_MMM-ImageFit"
hideprestartmodule = hidemodule + "module_15_MMM-ImageFit"

# Shows and hides: http://localhost/img/magicmirror/decoration/coin-zoom-cropped.gif
showstartmodule = showmodule + "module_16_MMM-ImageFit"
hidestartmodule = hidemodule + "module_16_MMM-ImageFit"

# Shows and hides: http://localhost/img/magicmirror/decoration/coin-fall.gif
showcoinmodule1 = showmodule + "module_17_MMM-ImageFit"
hidecoinmodule1 = hidemodule + "module_17_MMM-ImageFit"

# Shows and hides: http://localhost/img/magicmirror/decoration/chest-on-coins.png
showcoinmodule2 = showmodule + "module_18_MMM-ImageFit"
hidecoinmodule2 = hidemodule + "module_18_MMM-ImageFit"

# Shows and hides the "everyone modules" below.
# Shows and hides: MMM-Modulebar
showmodulebar = showmodule + "module_59_MMM-Modulebar"
hidemodulebar = hidemodule + "module_59_MMM-Modulebar"

# Shows and hides: MMM-Sonos
showsonos = showmodule + "module_25_MMM-Sonos"
hidesonos = hidemodule + "module_25_MMM-Sonos"

# Shows and hides: MMM-HideAll
showhideall = showmodule + "module_61_MMM-HideAll"
hidehideall = hidemodule + "module_61_MMM-HideAll"

# Shows and hides: MMM-TouchNavigation
showtouchnavigation = showmodule + "module_62_MMM-TouchNavigation"
hidetouchnavigation = hidemodule + "module_62_MMM-TouchNavigation"

# Shows and hides: currentwather
showcurrentweather = showmodule + "module_38_currentweather"
hidecurrentweather = hidemodule + "module_38_currentweather"

# Shows and hides: weaterforcast
showweatherforecast = showmodule + "module_40_weatherforecast"
hideweatherforecast = hidemodule + "module_40_weatherforecast"

# Seconds to show the IFTTT messages on the MagicMirror (shows until time is up or a new message is sent).
# MagicMirror MMM-IFTTTs modules URL to use.
ifttturl = "http://" + mmip + ":" + mmport + "/IFTTT"
# Time for each message.
mmtime = 3600
# Time for the end message.
mmendtime = 300
# Size of the MagicMirror IFTTT message (small, medium, large).
mmsize = "large"

# IFTTT messages sent to the MagicMirror.
# Pre start message, displayed when the hunt begins and the chest locks.
# English: "The hunt for the pirate coins has begun!"
iftttprestartmessage = "Jakten på piratmynten har börjat!!"
# End message, displayed when the hunt is over and the chest unlocks.
# English: "Congratulations!! You have found the 100 pirate coins, the chest is unlocked. I hope the candy is good!"
iftttendmessage = "Grattis!! Ni har hittat 100 piratmynt! Kistan är upplåst, Hoppas godiset smakar!"
# Start message, displays when the lid is opened for the first time and until the first coin is added.
# English: "To unlock the chest, you have to push at least 100 pirate coins in to the slot that opens up when trying to open the lid!"
iftttstartmessage = "För att låsa upp kistan helt måste ni peta in minst 100 piratmynt genom glipan som blir när man försöker öppna kistlocket!"
# Repeated message when coins are added (two parts). The collected number of coins is inserted in between the messages.
# English: "You have found ", " pirate coins, keep on searching..."
iftttcoinmessage = ["Ni har hittat ", " av 100 piratmynt. Fortsätt leta..."]

## Console messages.
# Pre start message, displayed when the script locks the chest.
consoleprestartmessae = "The treasure hunt has now started! Locking the chest."
# Start message in two parts when the chest is locked and waiting. The goal number is added in between the messages.
consolestartmessage = ["Chest is locked, I will now keep track of collected coins in an infinite loop. To exit press CTRL + C or collect","coins to unlock the chest."]
# Repeated message when coins are added.
consolecoinmessage = "Collected coins so far: "
# End message, when the hunt is over.
consoleendmessage = "Chest is now unlocked, I hope you had a good hunt! :)"
# Smoke machine setup message.
consolesmokesetup = "Turning on smoke machine so it can warm up."
# Smoke machine is ready.
consolesmokeready = "Smoke machine is warm, continueing..."
# Smoke filling the room message.
consolesmokefill = "Filling room with smoke..."

## SONOS control commands.
# Set to 1 if you want to use a SONOS player.
playonsonos = 1
# What player (room)
player = "kontor"
# Ip to the SONOS http API (https://github.com/jishi/node-sonos-http-api)
sonosapiip = "10.0.0.21"
# Port to the SONOS http API.
sonosapiport= "5005"
# Volume to play on.
sonosvolume = 60
# Playlist name
playlist = "Skattjakt"
# Sonos command URL
sonosaction = "http://" + sonosapiip + ":" + sonosapiport + "/" + player + "/"

## Home Assistant stuff
# Enable HA integration
haenabeld = 1

# Set your Home Assistant API key in the file .apikey
# Reads the HA key file.
with open(".apikey", "r") as file:
    hakey = file.readline()
    hakey = hakey.rstrip("\n")
    for last_line in file:
        pass

# If you don't want to use the .apikey file, you can set the key below.
#hakey = "------------------------- Your API key -------------------------"

# Switch (using the "switch" service).
haunit1 = "switch.shenzhen_neo_power_plug_08_switch"
# Dimmable light (using the "light" service).
haunit2 = "light.qubino_flush_dimmer_01_level"
# Window cover (using the "cover" service).
haunit3 = "cover.qubino_flush_shutter_dc_01_level"
# Smoke machine power socket Switch (using the "switch" service again). 
haunit4 = "switch.aeon_smart_switch_gen5_01_switch"
# Initial dim value for the dimmable light (no coins in the chest yet).
initdimval = 5
# End of dim value for the dimmable light (almost all coins are now in the chest).
meddimval = 10
# Full light on (all coins are collected and chest is unlocked).
enddimval = 150
#enddimval = 250

# Home Assistant IP.
haip = "10.0.0.249"
# Home Assistant Port.
haport = "8123"

# HA URL for manipulating switches.
haswitchurl = "http://" + haip + ":" + haport + "/api/services/switch"
# HA URL for manipulating lights.
halighturl = "http://" + haip + ":" + haport + "/api/services/light"
# HA URL for manipulating window covers.
hacoverurl = "http://" + haip + ":" + haport + "/api/services/cover"

# HA Header (with autentication).
haheader = {'Authorization': 'Bearer ' + hakey, 'Content-Type': 'application/json'}

## Config ends here!

# Reserved.
started = 0
read = 0

# Setting alsa mixer volume.
m = alsaaudio.Mixer('Headphone')
m.setvolume(alsavolume)

# Locking the chest.
print(consoleprestartmessae)
kit.servo[0].angle = lockangle

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering.
    # Create an object hx which represents your real hx711 chip.
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'.
    hx = HX711(dout_pin=21, pd_sck_pin=20)
    # measure tare and save the value as offset for current channel and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful.
    if err:
        raise ValueError('Tare is unsuccessful.')

    # Setting up the input buttons.
    GPIO.setup(lidpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(secretpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Starting to warm the smokemachine.
    if usesmoke == 1:
        print(consolesmokesetup)
        # Turns on the smoke machine on using Home Assistent.
        if haenabeld == 1:
            haresponse = requests.post(haswitchurl + "/turn_on", json={'entity_id': haunit4}, headers = haheader)
        if smokereadypin != 0:
            GPIO.setup(smokereadypin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            while GPIO.input(smokereadypin):
                time.sleep(0.5)
            # A better way? Maybe... Have to try it..
            #try:
            #    GPIO.wait_for_edge(smokereadypin, GPIO.FALLING)
        else:
            time.sleep(smokewarmuptime)
        # Smoke machine is warm.
        print(consolesmokeready)

        # Filling the room with smoke if activated.
        if smokefill == 1:
            print(consolesmokefill)
            # Setting up smoke machine trigger pin.
            GPIO.setup(smokeactivatepin, GPIO.OUT, initial = False)
            # Activating smoke.
            GPIO.output(smokeactivatepin, 0)
            #GPIO.output(smokeactivatepin, 1)
            time.sleep(smokefilltime)
            # Deactivating smoke.
            GPIO.setup(smokeactivatepin, GPIO.IN)

    print(consolestartmessage[0], goal, consolestartmessage[1])

    # Calculating the scale of one single coin.
    hx.set_scale_ratio(ratio)

    # Staring the loop.
    while True:

        # Checks what's on the scale (returns only integers and no negative numbers).
        val = max(0, int(hx.get_weight_mean(5)))

        # Make sure that the "value" (shown and spoken) of the collected coins don't overshoot the goal (if that's allowed).
        if overgoalok == 1:
            if val >= goal:
                val = goal

        # When lid opens, this happens...
        if GPIO.input(lidpin) == GPIO.LOW:
            if read == 1:
                print(consolecoinmessage + str(val))
                if mmpost == 1:
                    # Show the coin module and the message on the MagicMirror.
                    moduleresponse = urllib.request.urlopen(hidecoinmodule2)
                    time.sleep(1)
                    moduleresponse = urllib.request.urlopen(showcoinmodule1)
                    iftttresponse = requests.post(ifttturl, json={'message': iftttcoinmessage[0] + str(val) + iftttcoinmessage[1], 'displaySeconds': mmtime, 'size': mmsize})

                # This happens if the lid is opened the first time (no coins are inserted yet).
                if val == 0:
                    # Display start message on MagicMirror.
                    if mmpost == 1:
                        moduleresponse = urllib.request.urlopen(hideprestartmodule)
                        moduleresponse = urllib.request.urlopen(showstartmodule)
                        moduleresponse = urllib.request.urlopen(hidecoinmodule2)

                        iftttresponse = requests.post(ifttturl, json={'message': iftttstartmessage, 'displaySeconds': mmtime, 'size': mmsize})

                    # Only play sounds when playsound is 1.
                    if playsound == 1:
                        # Avoids the first message to be played when the program starts with the lid closed.
                        if info == 0:
                            info = 1
                        # Plays message 1 -> Next 2
                        elif info == 1:
                            os.system("aplay -q " + sounddir + "/Explain-01.wav")
                            os.system("aplay -q " + sounddir + "/Haha-01.wav")
                            info = 2
                        # Plays message 2 -> Next 3
                        elif info == 2:
                            os.system("aplay -q " + sounddir + "/Explain-02.wav")
                            os.system("aplay -q " + sounddir + "/Haha-02.wav")
                            info = 3
                        # Plays message 3 -> Next 1
                        elif info == 3:
                            os.system("aplay -q " + sounddir + "/Explain-03.wav")
                            os.system("aplay -q " + sounddir + "/Haha-03.wav")
                            info = 1

                # Playing the chest count sounds.
                if playsound == 1:
                    # Setting up the count sound sample.
                    fullpath = sounddir + "/" + str(val) + ".wav"

                    # If the number sound exists, play it.
                    if path.exists(fullpath):
                        os.system("aplay -q " + sounddir + "/Count-01.wav")
                        os.system("aplay -q " + fullpath)
                        os.system("aplay -q " + sounddir + "/Count-02.wav")

                    # Generates a random number between 1-10.
                    rand = random.randint(1, 20)
                    # Plays a laugh corresponding to the random number (if it exists).
                    fullpath = sounddir + "/Haha-" + str(rand) + ".wav"
                    if path.exists(fullpath):
                        os.system("aplay -q " + fullpath)
                        if usesmoke == 1:
                            # Setting up smoke machine trigger pin.
                            GPIO.setup(smokeactivatepin, GPIO.OUT, initial = False)
                            # Activating smoke.
                            GPIO.output(smokeactivatepin, 0)
                            #GPIO.output(smokeactivatepin, 1)
                            time.sleep(smokepufftime)
                            # Deactivating smoke.
                            GPIO.setup(smokeactivatepin, GPIO.IN)

                # Only play once. The lid has to be closed and opened again to play again.
                read = 0

                # Hide the coin module 1 and show coin module 2 on the MagicMirror.
                if mmpost == 1:
                    moduleresponse = urllib.request.urlopen(hidecoinmodule1)
                    time.sleep(2)
                    moduleresponse = urllib.request.urlopen(showcoinmodule2)

                # Turns up the lights a bit depending on the amount of coins found using Home Assistent.
                if haenabeld == 1:
                    diff = meddimval - initdimval
                    split = goal / diff
                    dimval = round(val / split) + initdimval
                    haresponse = requests.post(halighturl + "/turn_on", json={'entity_id': haunit2, 'brightness': dimval}, headers = haheader)

                # If the goal amount of coins are reached. Open the chest.
                if overgoalok == 1:
                    if val >= goal:
                        raise SystemExit
                else:
                    if val == goal:
                        raise SystemExit

        # If secret button is pressed unlock the chest as long as the button is pressed.
        if GPIO.input(secretpin) == GPIO.LOW:
            kit.servo[0].angle = unlockangle
        else:
            kit.servo[0].angle = lockangle
            if started == 0:
                # Display pre start message on the MagicMirror.
                if mmpost == 1:
                    # Hiding the "everyone modules".
                    moduleresponse = urllib.request.urlopen(hidemodulebar)
                    moduleresponse = urllib.request.urlopen(hidesonos)
                    moduleresponse = urllib.request.urlopen(hidehideall)
                    moduleresponse = urllib.request.urlopen(hidetouchnavigation)
                    moduleresponse = urllib.request.urlopen(hidecurrentweather)
                    moduleresponse = urllib.request.urlopen(hideweatherforecast)
                    
                    # Showing pre start Profile.
                    profileresponse = urllib.request.urlopen(startprofile)
                    moduleresponse = urllib.request.urlopen(showprestartmodule)
                    moduleresponse = urllib.request.urlopen(showcoinmodule2)
                    moduleresponse = urllib.request.urlopen(showiftttmodule)
                    
                    # Posting start message.
                    iftttresponse = requests.post(ifttturl, json={'message': iftttprestartmessage, 'displaySeconds': mmtime, 'size': mmsize})

                # Turns on the lights using Home Assistent.
                if haenabeld == 1:
                    haresponse = requests.post(hacoverurl + "/close_cover", json={'entity_id': haunit3}, headers = haheader)
                    haresponse = requests.post(haswitchurl + "/turn_on", json={'entity_id': haunit1}, headers = haheader)
                    haresponse = requests.post(halighturl + "/turn_on", json={'entity_id': haunit2, 'brightness': initdimval}, headers = haheader)

                # Sets the SONOS volume and start the selected playlist on the selected player.
                if playonsonos == 1:
                    sonosresponse = urllib.request.urlopen(sonosaction + "volume/" + str(sonosvolume))
                    sonosresponse = urllib.request.urlopen(sonosaction + "playlist/" + playlist)

                # The hunt is now set to started.
                started = 1

        # This plays a random laugh during the whole searching, even if no one is lifting the lid.
        # Generates a random number between 1-200.
        rand = random.randint(1, 100)
        # Plays a laugh corresponding to the random number (if it exists).
        fullpath = sounddir + "/Haha-" + str(rand) + ".wav"
        if path.exists(fullpath):
            os.system("aplay -q " + fullpath)
            if usesmoke == 1:
                # Setting up smoke machine trigger pin.
                GPIO.setup(smokeactivatepin, GPIO.OUT, initial = False)
                # Activating smoke.
                GPIO.output(smokeactivatepin, 0)
                #GPIO.output(smokeactivatepin, 1)
                time.sleep(smokepufftime)
                # Deactivating smoke.
                GPIO.setup(smokeactivatepin, GPIO.IN)
            
        # The lid has to be opened and closed for the sounds to play again.
        if GPIO.input(lidpin) == GPIO.HIGH:
            read = 1

# At the end of everything, exit cleanly.
except (KeyboardInterrupt, SystemExit):
    kit.servo[0].angle = unlockangle
    print(consoleendmessage)

    # Displays the "Win" message on the MagicMirror.
    if mmpost == 1:
        profileresponse = urllib.request.urlopen(endprofile)
        iftttresponse = requests.post(ifttturl, json={'message': iftttendmessage, 'displaySeconds': mmendtime, 'size': mmsize})

    # Plays the "win" sound from the Chest.
    if playsound == 1:
        os.system("aplay -q " + sounddir + "/Done-01.wav")

    # Decrees the SONOS volume until it's 1 and then stops playing.
    if playonsonos == 1:
        # Decrees loop.
        while (sonosvolume > 1):
            sonosvolume -= 1
            sonosresponse = urllib.request.urlopen(sonosaction+ "volume/" + str(sonosvolume))
            time.sleep(0.1)
        # Stops the playback.
        sonosresponse = urllib.request.urlopen(sonosaction + "pause")

    # Set the lights for the end.
    if haenabeld == 1:
        haresponse = requests.post(haswitchurl + "/turn_off", json={'entity_id': haunit4}, headers = haheader)
        haresponse = requests.post(hacoverurl + "/open_cover", json={'entity_id': haunit3}, headers = haheader)
        haresponse = requests.post(haswitchurl + "/turn_off", json={'entity_id': haunit1}, headers = haheader)
        haresponse = requests.post(halighturl + "/turn_on", json={'entity_id': haunit2, 'brightness': enddimval}, headers = haheader)

    
    # Setting everything on the MagicMirror back to normal.
    if mmpost == 1:
        time.sleep(waittime)

        # Showing modules and switching to the normal profile.
        profileresponse = urllib.request.urlopen(normalprofile)
        time.sleep(3)
        
        # Hiding the IFTTT module and shows the "everyone modules".
        moduleresponse = urllib.request.urlopen(hideiftttmodule)
        moduleresponse = urllib.request.urlopen(showcurrentweather)
        moduleresponse = urllib.request.urlopen(showweatherforecast)
        moduleresponse = urllib.request.urlopen(showmodulebar)
        moduleresponse = urllib.request.urlopen(showsonos)
        moduleresponse = urllib.request.urlopen(showhideall)
        moduleresponse = urllib.request.urlopen(showtouchnavigation)

# Clean up the inputs.
finally:
    GPIO.cleanup()
