import time

def main(uper,lock):
    """worker function"""
    print 'Worker 1'

    with lock:
        uper.setSecondary(22)
        uper.pwm0_begin(1000)

    while True:
        with lock:
            print "Day"
            uper.pwm0_set(2,0)
        time.sleep(5)

    return

