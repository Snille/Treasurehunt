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

# Set Alsa "headphone jack" volume to "volume".
volume = 100
m = alsaaudio.Mixer('Headphone')
m.setvolume(volume)

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

# Servo locking chest angle.
lockangle = 15

# Servo unlocking chest angle.
unlockangle = 130

# Start number for information sample (1, 2, 3).
info = 1

# Coins to collect for the chest to open (100).
goal = 5

# Set to 1 if it is ok to add more coins then specified in goal (chest opens when goal or higher is reached) otherwise it must be the exact goal number.
overgoalok = 1

# Pin used for the lid switch. Low when the lid is closed.
lidpin = 23

# Secret open switch Pin
secretpin = 24

# Coin weight number ratio in House: 855
ratio = 855
# Coin weight number ratio in Workshop: 827
#ratio = 827

# Play the sound (0 for no 1 for yes)
playsound = 1

# Time to wait before going back to the "normal" profile on the mirror
#waittime = 300 # Five minutes.
waittime = 10 # 10 seconds. 

# MagicMirror IP and port.
#mmip = "10.0.0.20" # Development MagicMirror.
mmip = "10.0.0.112" # Actual MagicMirror.
mmport = "8080" 

# Post to the MagicMirror (1 = on or 0 = off)
mmpost = 1

# Seconds to show the message on the MagicMirror (shows until time is up or a new message is sent).
mmtime = 3600 # For each message.
mmendtime = 60 # For the last message.

# Size of the MagicMirror message (small, medium, large)
mmsize = "large"

# MagicMirror Party Profile (set to the MMM-Remote-Control module that changes profile via MMM-ProfileSwitcher)
startprofile = "http://" + mmip + ":" + mmport + "/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Skattjakt"
endprofile = "http://" + mmip + ":" + mmport + "/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Grattis"
normalprofile = "http://" + mmip + ":" + mmport + "/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Louise"

# MagicMirror modules MMM-IFTTTs URL to use.
url="http://" + mmip + ":" + mmport + "/IFTTT"

# MagicMirror modules to show / hide
# Module to show 
#hideallmodules = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=all"
#showiftttmodule = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_51_MMM-IFTTT"

# Shows: http://localhost/img/magicmirror/decoration/pirate-with-flag.png
showprestartmodule = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_13_MMM-ImageFit"
hideprestartmodule = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_13_MMM-ImageFit"

# Shows: http://localhost/img/magicmirror/decoration/coin-zoom-cropped.gif
showstartmodule = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_14_MMM-ImageFit"
hidestartmodule = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_14_MMM-ImageFit"

# Shows: http://localhost/img/magicmirror/decoration/coin-fall.gif
showcoinmodule1 = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_15_MMM-ImageFit"
hidecoinmodule1 = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_15_MMM-ImageFit"

# Shows: http://localhost/img/magicmirror/decoration/chest-on-coins.png
showcoinmodule2 = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_16_MMM-ImageFit"
hidecoinmodule2 = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_16_MMM-ImageFit"

# Hides the "everyone modules".
hidemodulebar = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_57_MMM-Modulebar"
hidehideall = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_59_MMM-HideAll"
hidetouchnavigation = "http://" + mmip + ":" + mmport + "/remote?action=HIDE&module=module_60_MMM-TouchNavigation"

# Shows the "everyone modules".
showmodulebar = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_57_MMM-Modulebar"
showhideall = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_59_MMM-HideAll"
showtouchnavigation = "http://" + mmip + ":" + mmport + "/remote?action=SHOW&module=module_60_MMM-TouchNavigation"


## Sonos control commands.
# Set to one if you want to use a Sonos player.
playonsonos = 1
# What player (room)
player = "kontor"
# Ip to the SONOS http API (https://github.com/jishi/node-sonos-http-api)
sonosapiip = "10.0.0.21"
# Port to the SONOS http API.
sonosapiport= "5005"
# Volume to play on.
volume = "15"
# Playlist name
playlist = "Skattjakt"


setvol = "http://" sonosapiip + ":" + sonosapiport + "/" + player + "/volume/" + volume
#
# http://10.0.0.21:5005/kontor/volume/30
# http://10.0.0.21:5005/kontor/play
# http://10.0.0.21:5005/kontor/playlist/Snilles%20List

# The directory where the sounds are located.
sounddir = "Sounds"

# Reserved.
started = 0
read = 0

# Loking the chest
print("The hunt is on! Locking the chest!")

kit.servo[0].angle = lockangle

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=21, pd_sck_pin=20)
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    # Setting up the input buttons.
    GPIO.setup(lidpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(secretpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("I will now start to keep track of collected coins in an infinite loop. To exit press 'CTRL + C' or collect", goal, "coins to unlock the chest")

    # Calculating the scale of one single coin.
    hx.set_scale_ratio(ratio)

    # Staring the loop.
    while True:

        # Checks what's on the scale (returns only integers and no negative numbers).
        val = max(0, int(hx.get_weight_mean(5)))
        # Make sure that the "value" (show and spoken) of the collected coins don't overshoot the goal (if that's allowed).
        if overgoalok == 1:
            if val >= goal:
                val = goal

        # When lid opens, this happens...
        if GPIO.input(lidpin) == GPIO.LOW:
            if read == 1:
                print("Collected coins so far: " + str(val))
                if mmpost == 1:
                    # Show the coin module and the message on the MagicMirror
                    moduleresponse = urllib.request.urlopen(hidecoinmodule2)
                    time.sleep(1)
                    moduleresponse = urllib.request.urlopen(showcoinmodule1)
                    iftttresponse = requests.post(url, json={'message': 'Ni har hittat ' + str(val) + ' av 100 piratmynt. Fortsätt leta...', 'displaySeconds': mmtime, 'size': mmsize})
                
                if val == 0:
                    # Display start message on MagicMirror
                    if mmpost == 1:
                        moduleresponse = urllib.request.urlopen(hideprestartmodule)
                        moduleresponse = urllib.request.urlopen(showstartmodule)
                        moduleresponse = urllib.request.urlopen(hidecoinmodule2)

                        iftttresponse = requests.post(url, json={'message': 'För att låsa upp kistan helt måste ni samla ihop minst 100 piratmynt och peta in dem genom glipan som blir när man försöker öppna kistlocket!', 'displaySeconds': mmtime, 'size': mmsize})
                    # Only play sounds when playsound is 1
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

                if playsound == 1:
                    # Setting up the count sound sample.
                    fullpath = sounddir + "/" + str(val) + ".wav"

                    # If the number sound exists, play it.
                    if path.exists(fullpath):
                        os.system("aplay -q " + sounddir + "/Count-01.wav")
                        os.system("aplay -q " + fullpath)
                        os.system("aplay -q " + sounddir + "/Count-02.wav")

                    # Generates a random number between 0-8
                    rand = random.randint(1, 6)
                    # Plays a laugh if the random number matches.
                    if rand == 2:
                        os.system("aplay -q " + sounddir + "/Haha-01.wav")
                    elif rand == 4:
                        os.system("aplay -q " + sounddir + "/Haha-02.wav")
                    elif rand == 6:
                        os.system("aplay -q " + sounddir + "/Haha-03.wav")

                # Only play once. The lid has to be closed and opened again to play again.
                read = 0

                # Hide the coin module 1 and show coin module 2 on the MagicMirror
                if mmpost == 1:
                    moduleresponse = urllib.request.urlopen(hidecoinmodule1)
                    time.sleep(2)
                    moduleresponse = urllib.request.urlopen(showcoinmodule2)

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
                # Display Pre start message on the MagicMirror
                if mmpost == 1:
                    # Hiding modules
                    moduleresponse = urllib.request.urlopen(hidemodulebar)
                    moduleresponse = urllib.request.urlopen(hidehideall)
                    moduleresponse = urllib.request.urlopen(hidetouchnavigation)
                    
                    # Showing Pre-Start Profile
                    profileresponse = urllib.request.urlopen(startprofile)
                    moduleresponse = urllib.request.urlopen(showprestartmodule)
                    moduleresponse = urllib.request.urlopen(showcoinmodule2)
                    
                    # Posting start message.
                    iftttresponse = requests.post(url, json={'message': 'Jakten på piratmynten har börjat!!', 'displaySeconds': mmtime, 'size': mmsize})
                # Start sonos playr
                If playonsonos == 1
                    #urllib.request.urlopen("http://" sonosapiip + ":" + sonosapiport + "/" + player + "/volume/" + volume)
                    #urllib.request.urlopen("http://" sonosapiip + ":" + sonosapiport + "/" + player + "/playlist/" + playlist)

                started = 1

        # The lid has to be opened and closed for the sounds to play again.
        if GPIO.input(lidpin) == GPIO.HIGH:
            read = 1

# At the end of everything, exit cleanly.
except (KeyboardInterrupt, SystemExit):
    kit.servo[0].angle = unlockangle
    print("Chest is now unlocked, bye...")

    if mmpost == 1:
        profileresponse = urllib.request.urlopen(endprofile)
        iftttresponse = requests.post(url, json={'message': 'Grattis!! Ni har nu hittat mer än 100 piratmynt! Kistan är upplåst, Hoppas godiset smakar!', 'displaySeconds': mmendtime, 'size': mmsize})
        
    if playsound == 1:
        os.system("aplay -q " + sounddir + "/Done-01.wav")

    if mmpost == 1:
        time.sleep(waittime)

        # Showing modules and switching to the normal profile.
        profileresponse = urllib.request.urlopen(normalprofile)
        time.sleep(3)
        moduleresponse = urllib.request.urlopen(showmodulebar)
        moduleresponse = urllib.request.urlopen(showhideall)
        moduleresponse = urllib.request.urlopen(showtouchnavigation)

# Clean up the inputs.
finally:
    GPIO.cleanup()