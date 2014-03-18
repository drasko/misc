import time

uper = None
mutex = None

def weioSetSecondary(pin):
    global mutex
    global uper

    with mutex:
        uper.setSecondary(pin)

def weioPwm0Begin(interval):
    global mutex
    global uper

    with mutex:
        uper.pwm0_begin(interval)

def weioPwm0Set(channel, high_time):
    global mutex
    global uper

    with mutex:
        uper.pwm0_set(channel, high_time)


def main():
    """worker function"""
    print 'Worker 1'

    weioSetSecondary(22)
    weioPwm0Begin(1000)

    
    while True:
        print "Day"
        weioPwm0Set(2,0)
        time.sleep(1.2)

    return

def weioTaskMain(userFunction, u, m):
    # Set globals for this process context
    global uper
    global mutex

    uper = u
    mutex = m

    # Call users function
    userFunction()



