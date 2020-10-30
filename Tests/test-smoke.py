#!/usr/bin/python3
#coding=utf-8

import RPi.GPIO as GPIO
import time

# Pin used for the lid switch. Low when the lid is closed.
smokeactivatepin = 27

# Secret open switch Pin (for testing)
smoketest = 24

# set GPIO pin mode to BCM numbering
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

# Setting up the input and outputs.
GPIO.setup(smokeactivatepin, GPIO.OUT, initial = False)
GPIO.setup(smoketest, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  
try:
    while True:
        if GPIO.input(smoketest):
            # This is the way it's suppose to work. The output is set to low (worked on other relay boards). 
            #GPIO.output(smokeactivatepin, 0)
            # But for some reason, the relay board that I got, don't turn off the relay until i set the output to an input.
            GPIO.setup(smokeactivatepin, GPIO.IN)
            print("Smoke off")
            time.sleep(0.1)
        if not GPIO.input(smoketest):
            # And because the output may be an input, I need to set it back to output before turning it on.
            GPIO.setup(smokeactivatepin, GPIO.OUT, initial = False)
            GPIO.output(smokeactivatepin, 0)
            print("Smoke on")
            time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
