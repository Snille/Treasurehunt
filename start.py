#!/usr/bin/env python3
#coding=utf-8

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
#import time
#from time import sleep
import sys
import os
import os.path
from os import path
from adafruit_servokit import ServoKit

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
goal = 10

# Pin used for the lidswitch. Low when the lid is closed.
lidpin = 5

# Secret open switch Pin
secretpin = 27

# Coin weight number ratio in House: 855
ratio = 855
# Coin weight number ratio in Workshop: 827
#ratio = 827

# Play the sound
read = 1

# The directory where the sounds are located.
sounddir = "Sounds"

# Loking the chest
print("Locking the chest")
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

    reading = hx.get_raw_data_mean()
#    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
#        print('Data subtracted by offset but still not converted to units:', reading)
#    else:
#        print('invalid data', reading)

    # Setting up the input buttons.
    GPIO.setup(lidpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(secretpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("I will now start to keep track of collected coins in an infinite loop. To exit press 'CTRL + C' or collect", goal, "coins to unlock the chest")

    # Calculating the scale of one sigle coin.
    hx.set_scale_ratio(ratio)

    # Staring the loop.
    while True:

        # Chacks what's on the scale (returns only intigers and no negative numbers).
        val = max(0, int(hx.get_weight_mean(5)))

        # When lid opens, this happens...
        if GPIO.input(lidpin) == GPIO.LOW:
            if read == 1:
                print("Collected coins so far: " + str(val))
                if val == 0:
                    # Avoids the first message to be plyed when the program starts with the lid closed.
                    if info == 0:
                        info = 1
                     # Plays message 1 -> Next 2
                    elif info == 1:
                        os.system("aplay -q " + sounddir + "/Explain-01.wav")
                        info = 2
                    # Plays message 2 -> Next 3
                    elif info == 2:
                        os.system("aplay -q " + sounddir + "/Explain-02.wav")
                        info = 3
                    # Plays message 3 -> Next 1
                    elif info == 3:
                        os.system("aplay -q " + sounddir + "/Explain-03.wav")
                        info = 1

                # Set the path and filename to the number sound.
                fullpath = sounddir + "/" + str(val) + ".wav"

                # If the sound exists, play it.
                if path.exists(fullpath):
                    os.system("aplay -q " + sounddir + "/Count-01.wav")
                    os.system("aplay -q " + fullpath)
                    os.system("aplay -q " + sounddir + "/Count-02.wav")

                # Only play once. The lid has to be closed and opend again to play again.
                read = 0

                # If the goal amount of coins are reached. Open the chest.
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
    print("Chest is now unlocked, bye...")

# Clean up the inputs.
finally:
    GPIO.cleanup()
