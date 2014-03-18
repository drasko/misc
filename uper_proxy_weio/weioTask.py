#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
import logging
import time

#uper = None
#mutex = None

#from worker1 import *

import weioMultiApi

class WeioTask(multiprocessing.Process):
    def __init__(self, userFunction, u, m):
        super(WeioTask, self).__init__()

        print 'Initializing weioTask'
        # Set globals for this process context
        global uper
        global mutex

        uper = u
        mutex = m
        self.uper = uper
        self.mutex = mutex
        self.userFunction = userFunction

    def run(self):
        p = multiprocessing.current_process()
        print 'Starting:', p.name, p.pid

        # Call the function that user provided
        #self.userFunction(self.u, self.m)
        weioMultiApi.weioTaskMain(self.userFunction, self.uper, self.mutex)

        while True:
            pass

        return
