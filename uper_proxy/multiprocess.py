import multiprocessing
import worker1, worker2
import uperProxy

import time

import logging

if __name__ == '__main__':
    logger = multiprocessing.log_to_stderr()
    #logger.setLevel(multiprocessing.SUBDEBUG)

    #
    #   make shared UPER and proxy to it
    #
    manager = uperProxy.UperManager()
    manager.register('SharedUper', uperProxy.setupSharedUper,
                    proxytype=uperProxy.UperProxy, exposed = ('setSecondary', 'pwm0_begin', 'pwm0_set'))

    manager.start()
    uProxy = manager.SharedUper()

    print uProxy

    #
    #   make sure we are not accesing UPER at the same time in different processes
    #
    uMutex = manager.Lock()

    #uProxy.setSecondary(22)
    #uProxy.pwm0_begin(1000)
    #uProxy.pwm0_set(2,0)

    w1 = multiprocessing.Process(target=worker1.main, args=(uProxy, uMutex,))
    w1.start()

    w2 = multiprocessing.Process(target=worker2.main, args=(uProxy, uMutex))
    w2.start()

    w1.join()
    w2.join()

