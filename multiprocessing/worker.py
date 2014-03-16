import os
import time

class Test():
    pera = 1
    mika = 2
    zika = "zika"

    def get(self):
        print "PERA: " + str(self.pera)
        time.sleep(1)
        print "MIKA: " + str(self.mika)
        time.sleep(1)
        print "ZIKA: " + self.zika

def hello():
    print "HELLO"

def main():
    """worker function"""
    print 'Worker'
    hello()

    t = Test()
    t.get()

    time.sleep(1)

    return

if __name__ == '__main__':
    main()

