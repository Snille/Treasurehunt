#!/usr/bin/python3
#coding=utf-8

import time
import sys
import os
import os.path
from os import path
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

# The directory where the sounds are located.
sounddir = "Sounds"

# HX711 Pinns used (GPIO number).
gpiopin1 = 20
gpiopin2 = 21

# Lid-button.
gpiopin3 = 3

# To emulate the HX711 set to True
EMULATE_HX711=False

# Coin ref = 827
# This coin is used: https://www.thingiverse.com/thing:2936980
# Printed in PLA with 20% infill.
referenceUnit = 827

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

# When control+C pressed!
def cleanAndExit():
    print("The hunt is over...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Have a nice day!")
    sys.exit()

# Pins to be used on PI.
hx = HX711(gpiopin1, gpiopin2)

# Format
hx.set_reading_format("MSB", "MSB")

# Make sure to change this at the top!
hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare()
print("Let the hunt begin!")

while True:
    try:
        # Make sure we don't get negative values.
        val = max(0, int(hx.get_weight(5)))

        # Do the logic here!
        fullpath = sounddir + "/" + str(val) + ".wav"
        # print(fullpath)
        if path.exists(fullpath):
            os.system("aplay -q " + fullpath)
        print("Collected coins so far: " + str(val))

        # Stop and reinitiate.
        hx.power_down()
        hx.power_up()

        # Wait a while.
        time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
