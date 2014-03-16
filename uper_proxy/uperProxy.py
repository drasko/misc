import uper
import multiprocessing.managers

#
#   Create uperProxy object
#
def setupSharedUper():
    """
    Function to setup uperProxy object shared between all processes
    The uperProxy object will be created within a separate (special) process
        run by multiprocessing.BaseManager.start()
    """

    #
    #   Log file name with logger level
    #
    print "Creating weioUper object..."
    weioUper = uper.UPER()

    return weioUper


#
#   Proxy object for UPER Access
#       Logging messages will be marshalled (forwarded) to the process where the
#       shared log lives
#
class UperProxy(multiprocessing.managers.BaseProxy):
    def setSecondary(self, pinID):
        return self._callmethod('setSecondary', (pinID,))
    def pwm0_begin(self, preiod):
        return self._callmethod('pwm0_begin', (preiod,))
    def pwm0_set(self, channel, high_time):
        return self._callmethod('pwm0_set', (channel, high_time))
    def __str__ (self):
        return "UPER proxy"


#
#   Register the setupUper function as a proxy for setup_logger
#
#   We use SyncManager as a base class so we can get a lock proxy for synchronising
#       logging later on
#
class UperManager(multiprocessing.managers.SyncManager):
    """
    Uper manager sets up its own process and will create the real UPER object there
    We refer to this (real) log via proxies
    """
    pass

UperManager.register('SharedUper', setupSharedUper, proxytype=UperProxy, exposed = ('setSecondary', 'pwm0_begin', 'pwm0_set'))
