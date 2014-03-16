import os
import time
import includeUper as u


def hello():
    print "HELLO"

def main(qin, qout, l):
    """worker function"""
    print 'Worker'

    uper = u.UPER(qin, qout, l)

    uper.setSecondary(22)
    uper.pwm0_begin(1000)

    while True:
        uper.pwm0_set(2,0)
        time.sleep(0.5)
    return

