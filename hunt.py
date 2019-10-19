#!/usr/bin/python2
#coding=utf-8


import time
import sys
import os
import os.path
from os import path

sounddir = "Sounds"
soundfile = "1"

#os.system("aplay " + sounddir + "/" + soundfile + ".wav")

EMULATE_HX711=False


# Coin ref = 827
referenceUnit = 827

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("The hunt is over...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Have a nice day!")
    sys.exit()

# Pins to be used on PI.
hx = HX711(5, 6)

# Format
hx.set_reading_format("MSB", "MSB")

# Make sure to change this at the top!
hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare()
print("Let the hunt begin!")

while True:
    try:
        # Make sure w don't get negative values.
        val = max(0, int(hx.get_weight(5)))

        # Do the logic here!
        
        #if 
        #os.system("aplay " + sounddir + "/" + soundfile + ".wav")

        print(val)

        # Stop and reinitiate.
        hx.power_down()
        hx.power_up()

        # Wait a while.
        time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
