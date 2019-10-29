#!/usr/bin/env python3
#coding=utf-8

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
from time import sleep
import sys
import os
import os.path
from os import path
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

# Locking chest.
kit.servo[0].angle = 15

# Coins to collect for the chest to open.
goal = 10

# Pin used for the lidswitch. Low when the lid is closed.
lidpin = 5

# Secret Open Pin
secretpin = 27

# Defines if to open using the secret button.
open = 0

# Ratio in House: 855
ratio = 855
# Ratio in Workshop: 827
#ratio = 827

# Play the sound
read = 1

# The directory where the sounds are located.
sounddir = "Sounds"


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
    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Data subtracted by offset but still not converted to units:',
              reading)
    else:
        print('invalid data', reading)
    # Setting up the input button.
    GPIO.setup(lidpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(secretpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    hx.set_scale_ratio(ratio)
    while True:
        val = max(0, int(hx.get_weight_mean(5)))

        if GPIO.input(lidpin) == GPIO.LOW:
            if read == 1:
                print("Collected coins so far: " + str(val))
                # Do the logic here!
                fullpath = sounddir + "/" + str(val) + ".wav"
                # print(fullpath)
                if path.exists(fullpath):
                    os.system("aplay -q " + sounddir + "/Count-01.wav")
                    os.system("aplay -q " + fullpath)
                    os.system("aplay -q " + sounddir + "/Count-02.wav")
                read = 0
#                time.sleep(3)
                if val == goal:
                    kit.servo[0].angle = 130

        # If secret button is pressed unlock or lock the chest.
        if GPIO.input(secretpin) == GPIO.LOW:
            
            # If open is 0 open the lock.
            if open = 0
                kit.servo[0].angle = 130

#            open = 1
 


       else:
            kit.servo[0].angle = 15

#            open = 1
 

        # The lid has to be opened and closed for the sounds to play again.
        if GPIO.input(lidpin) == GPIO.HIGH:
            read = 1

        # 
        if GPIO.input(secretpin) == GPIO.HIGH:
            open = 0


except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()
