import time

def main(uper, lock):
    """worker function"""
    print 'Worker 2'

    while True:
        with lock:
            print "Night"
            uper.pwm0_set(2,1000)
        time.sleep(2)

    return

