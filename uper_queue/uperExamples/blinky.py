#!/usr/bin/env python
# encoding: utf-8
import uper, time 

def myCallBack(interrupt):
	print " this is my UPER1 callback working!"
	print "		interrupt No:		", interrupt[1][0]
	print "		interrupt reason:	", interrupt[1][1]

uper = uper.UPER(myCallBack) #on Windows try --> uper = UPER(myCallBack"COM5")

uper.setSecondary(30)
print "analogRead = %x" % uper.analogRead(3)

uper.attachInterrupt(2,33,4)

uper.setSecondary(22)
uper.pwm0_begin(1000)

while True:
    uper.pwm0_set(2,0)
    time.sleep(0.5)
    uper.pwm0_set(2,1000)
    time.sleep(0.5)

uper.stop()
