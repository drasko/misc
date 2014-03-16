#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
import logging
import time

from weioMultiApi import *

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
        self.userFunction()

        return
