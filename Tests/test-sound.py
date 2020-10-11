#!/usr/bin/env python3
#coding=utf-8

import os
import alsaaudio

# Set Alsa "headphone jack" volume to "volume".
volume = 100
m = alsaaudio.Mixer('Headphone')
m.setvolume(volume)

# The directory where the sounds are located.
sounddir = "../Sounds"
os.system("aplay -q " + sounddir + "/Haha-02.wav")
