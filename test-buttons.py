#!/usr/bin/python3
#coding=utf-8

import RPi.GPIO as GPIO
import time

# Pin used for the lid switch. Low when the lid is closed.
lidpin = 23

# Secret open switch Pin
secretpin = 24

# set GPIO pin mode to BCM numbering
GPIO.setmode(GPIO.BCM) 
# Setting up the input buttons.
GPIO.setup(lidpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(secretpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    # When lid opens, this happens...
    pin_status1 = GPIO.input(lidpin)
    pin_status2 = GPIO.input(secretpin)
    print(pin_status1)
    print(pin_status2)
    time.sleep(1)

GPIO.cleanup()
