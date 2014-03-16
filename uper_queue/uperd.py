#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
import logging
import sys
import uper
import time

class Uperd(multiprocessing.Process):
    def __init__(self, qin, qout, sem):
        super(Uperd, self).__init__()

        print 'Initializing UPER handler'
        self.uper = uper.UPER()
        self.qin = qin
        self.qout = qout
        self.sem = sem

    def run(self):
        print "Running uperd"

        with self.sem:
            while True:
                print "Try to get cmd"
                cmd = self.qin.get()
                print "Got cmd"
                result = self.uper.UPER_IO(0, cmd)
                self.qout.put(result)
        return
