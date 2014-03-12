import time
import sys

from weioUserApi import *

def WeioUserSetup() :

    print attach

    # Attaches interrupt from Web client
    attach.event('testUser', buttonHandler)

    # Attaches sensor function to infinite loop
    attach.process(blinky, ("Test", 10))

    # Attaches sensor function to infinite loop
    attach.process(potentiometer)

    # Instanciate shared objects
    shared.val = 1


###
# Event Handlers
###
def buttonHandler(dataIn) :
    print "User button pressed!!!"



###
# Threads
###
def potentiometer() :
    while (1) :
        print("potentiometer") 
        shared.val = shared.val + 1

        time.sleep(1)


def blinky(s, k) :
    i = 0
    while (1) :
        print("blinky")
        i = i+1
        time.sleep(shared.val)
        print s
        print k
     
