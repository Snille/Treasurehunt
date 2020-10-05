#!/usr/bin/env python3
#coding=utf-8

import RPi.GPIO as GPIO
from hx711 import HX711
import sys
import os
import os.path
from os import path
from adafruit_servokit import ServoKit
import random
import json
import urllib.request
import requests


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

# Servo locking chest angle.
lockangle = 15

# Servo unlocking chest angle.
unlockangle = 130

# Start number for information sample (1, 2, 3).
info = 0

# Coins to collect for the chest to open.
goal = 5

# Set to 1 if it is ok to add more coins then specified in goal (chest opens when goal or higher is reached) otherwise it must be the exact goal number.
overgoalok = 1

# Pin used for the lidswitch. Low when the lid is closed.
lidpin = 23

# Secret open switch Pin
secretpin = 24

# Coin weight number ratio in House: 855
ratio = 855
# Coin weight number ratio in Workshop: 827
#ratio = 827

# Play the sound
read = 1

# Post to the MagicMirror (1 = on or 0 = off)
mmpost = 1

# Seconds to show the message on the MagicMirror (shows until time is up or a new message is sent).
mmtime = 3600 # For each message.
mmendtime = 60 # For the last message.

# Size of the MagicMirror message (small, medium, large)
mmsize = "large"

# MagicMirror Party Profile (set to the MMM-Remote-Control module that changes profile via MMM-ProfileSwitcher)
#startprofile = "http://10.0.0.112:8080/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Treasure"
startprofile = "http://10.0.0.20:8080/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Treasure"
#endprofile = "http://10.0.0.20:8080/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Vader"
endprofile = "http://10.0.0.20:8080/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Erik"

# MagicMirror modules MMM-IFTTTs URL to use.
#url="http://10.0.0.112:8080/IFTTT"
url="http://10.0.0.20:8080/IFTTT"

# MagicMirror modules to show / hide
# Show Module: http://10.0.0.20:8080/remote?action=SHOW&module=module_2_clock
# Hide Module: http://10.0.0.20:8080/remote?action=HIDE&module=module_2_clock

# The directory where the sounds are located.
sounddir = "Sounds"

# Loking the chest
print("The hunt is on! Locking the chest!")
if mmpost == 1:
    profileresponse = urllib.request.urlopen(startprofile)
    iftttresponse = requests.post(url, json={'message': 'Leta piratmynt!', 'displaySeconds': mmtime, 'size': mmsize})

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

        # Chacks what's on the scale (returns only integers and no negative numbers).
        val = max(0, int(hx.get_weight_mean(5)))

        # When lid opens, this happens...
        if GPIO.input(lidpin) == GPIO.LOW:
            if read == 1:
                print("Collected coins so far: " + str(val))
                if mmpost == 1:
                    iftttresponse = requests.post(url, json={'message': str(val) + ' av 100 mynt hittade...', 'displaySeconds': mmtime, 'size': mmsize})
                
                if val == 0:
                    # Avoids the first message to be plyed when the program starts with the lid closed.
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

                # Setting up the count sound sample.
                fullpath = sounddir + "/" + str(val) + ".wav"

                # If the nuber sound exists, play it.
                if path.exists(fullpath):
                    os.system("aplay -q " + sounddir + "/Count-01.wav")
                    os.system("aplay -q " + fullpath)
                    os.system("aplay -q " + sounddir + "/Count-02.wav")

                    # Generates a random number between 0-8
                    rand = random.randint(1, 6)
                    # Plays a laugh if the randum namber matches.
                    if rand == 2:
                        os.system("aplay -q " + sounddir + "/Haha-01.wav")
                    elif rand == 4:
                        os.system("aplay -q " + sounddir + "/Haha-02.wav")
                    elif rand == 6:
                        os.system("aplay -q " + sounddir + "/Haha-03.wav")

                # Only play once. The lid has to be closed and opened again to play again.
                read = 0

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

        # The lid has to be opened and closed for the sounds to play again.
        if GPIO.input(lidpin) == GPIO.HIGH:
            read = 1

# At the end of everything, exit cleanly.
except (KeyboardInterrupt, SystemExit):
    kit.servo[0].angle = unlockangle
    if read == 1:
        os.system("aplay -q " + sounddir + "/Done-01.wav")

    print("Chest is now unlocked, bye...")
    if mmpost == 1:
        profileresponse = urllib.request.urlopen(endprofile)
        iftttresponse = requests.post(url, json={'message': 'Alla mynt funna! Kistan är upplåst!', 'displaySeconds': mmendtime, 'size': mmsize})

# Clean up the inputs.
finally:
    GPIO.cleanup()