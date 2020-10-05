#!/usr/bin/python3
#coding=utf-8

import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

kit.servo[0].angle = 15
time.sleep(1)
kit.servo[0].angle = 130
