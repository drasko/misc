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


class UserHandler(sockjs.tornado.SockJSConnection):
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weioMain.py is sent at first time"""
        print "Opened WEIO API socket"

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        self.req = json.loads(data)
        print data
        print self.req['request']

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(s)
        self.stream.connect(("localhost", 8087), self.send_request)

    def send_request(self):
        stream.write(self.req)


class TestHandler(sockjs.tornado.SockJSConnection): 
    i = 0
    def open(self):
        print 'new connection'
        self.write_message("Hello World")
      
    def on_message(self, message):
        print 'message received %s' % message

        if (message == "START"):
            print("weioMain indipendent process launching...")

            processName = "weioProcess.py"
            
            global weioPipe
            weioPipe = subprocess.Popen(['python', '-u', processName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            global ioloopObj
            ioloopObj = ioloop.IOLoop.instance()
            
            data = {}
            callback = functools.partial(self.weioMainHandler, data)
            ioloopObj.add_handler(weioPipe.stdout.fileno(), callback, ioloopObj.READ)
            stdoutHandlerIsLive = True;
        elif (message == "STOP"):
            self.stop()
        else:
            print "UNKNOWN MESSAGE"
 
    def on_close(self):
      print 'connection closed'




    def stop(self):
        """Stop running application"""
        
        global weioPipe
        global stdoutHandlerIsLive
        global stderrHandlerIsLive
        
        #print "STDOUT ", stdoutHandlerIsLive, " STDERR ", stderrHandlerIsLive
        if weioPipe != None :
            ioloopObj.remove_handler(weioPipe.stdout.fileno())

            if weioPipe.poll() is None :
                weioPipe.kill()
                    
            weioPipe = None
            
    def weioMainHandler(self, data, fd, events):
        """Stream stdout to browser"""

        global weioPipe
        line = weioPipe.stdout.readline()
        if line :
            # parse incoming data
            #stdout = line.rstrip()
            stdout = line
            print(stdout)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    tornado.options.define("port", default=8081, type=int)

    # 1. Create weio router
    TestRouter = sockjs.tornado.SockJSRouter(TestHandler, '/test')
    UserRouter = sockjs.tornado.SockJSRouter(UserHandler, '/user')

    # 2. Create Tornado application
    app = tornado.web.Application(
            list(TestRouter.urls) + list(UserRouter.urls) +
            [(r"/", IndexHandler), (r"/(.*)", tornado.web.StaticFileHandler,
	 				{"path": ".", "default_filename": "index.html"})],
            debug=True)


    # 3. Make Tornado app listen on port 8080
    logging.info(" [*] Listening on 0.0.0.0:8081")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
