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

def weioTaskMain(userFunction, u, m):
    # Set globals for this process context
    global uper
    global mutex

    uper = u
    mutex = m

    # Call users function
    userFunction()
