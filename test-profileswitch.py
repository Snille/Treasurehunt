#!/usr/bin/python3
#coding=utf-8

## MagicMirror Profile switch.
# http://10.0.0.20:8080/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Treasure

import urllib.request

req = 'http://10.0.0.20:8080/remote?action=NOTIFICATION&notification=CURRENT_PROFILE&payload=Treasure'
response = urllib.request.urlopen(req)
