import time
from threading import Thread

def myfunc(i):
    for j in range(3):
        print "Thread %s: %s" % (i,j)
        time.sleep(1)

for i in range(5):
    t = Thread(target=myfunc, args=(i,))
    t.start()
    time.sleep(1)
