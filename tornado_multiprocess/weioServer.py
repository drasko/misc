import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import web, ioloop, iostream, gen
 
import sockjs.tornado

import threading
import time
import subprocess
import functools

import json

from weioUserApi import *



import socket
import sys
import os
import multiprocessing

import multiprocessing
import weioUser




# Global variable to store SockJSConnection calss instance
# in order to call it's send() method from MainProgram thread
weioPipe = None

# Global object to store ioloop handlers that drive sterr &
# stdout from user program
ioloopObj = None


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


def weioStdoutCallback(fd, events):
    """Stream stdout to browser"""

    global weioPipe
    line = weioPipe.stdout.readline()
    if line :
        # parse incoming data
        #stdout = line.rstrip()
        stdout = line
        print "STDOUT: " + stdout


def main():
    global ioloopObj
    global weioPipe

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    tornado.options.define("port", default=8081, type=int)

    # 1. Create weio router
    

    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/", IndexHandler), (r"/(.*)", tornado.web.StaticFileHandler,
	 				{"path": ".", "default_filename": "index.html"})],
            debug=True)


    # 3. Make Tornado app listen on port 8080
    logging.info(" [*] Listening on 0.0.0.0:8081")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)

    print("weioMain indipendent process launching...")
    processName = "weioUser.py"
            
    weioPipe = subprocess.Popen(['python', '-u', processName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ioloopObj = ioloop.IOLoop.instance()

    ioloopObj.add_handler(weioPipe.stdout.fileno(), weioStdoutCallback, ioloopObj.READ)
    stdoutHandlerIsLive = True;

    # 4. Start IOLoop
    ioloopObj.start()

if __name__ == "__main__":
    main()
    os.exit(os.EX_OK)
