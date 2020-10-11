#!/usr/bin/env python3
#coding=utf-8

goal = 100
# Initial dim value for the dimmable light (no coins in the chet yet).
initdimval = 5
# End of dim value for the dimmable light (almost all coins are now in the chest).
meddimval = 14
# Full light on (all coins are collected and chest is unlocked).
enddimval = 25

value = 80

diff = meddimval - initdimval
split = goal / diff
print(split)
dimval = round(value / split) + initdimval
print(dimval)
