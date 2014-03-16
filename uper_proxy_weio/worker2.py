import time

uper = None
mutex = None

def weioPwm0Set(channel, high_time):
    global mutex
    global uper

    with mutex:
        uper.pwm0_set(channel, high_time)


def main():
    """worker function"""
    print 'Worker 2'

    while True:
        print "Night"
        weioPwm0Set(2,1000)
        time.sleep(1)

    return

def weioTaskMain(u, m):
    # Set globals for this process context
    global uper
    global mutex

    uper = u
    mutex = m

    # Call users function
    main()



