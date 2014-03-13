import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options

import sys
import json

#import thread
import threading 

from user import *

from weioUserApi import *

from weioMain import *

class MainHandler(tornado.web.RequestHandler):
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weioMain.py is sent at first time"""
        print "8087: Opened WEIO API socket"

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        self.req = json.loads(data)
        self.serve()

    def serve(self) :
        pass
        for key in attach.events :
            if attach.events[key].event in self.req['request'] :
                attach.events[key].handler(self.req['data'])

    def initialize(self):
        print "8087: Initialize"

    def get(self):
        self.write("8087: Hello, world")


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)


    app = tornado.web.Application([
            (r'/', MainHandler)]
    )
    #app.listen(8087)
    #logging.info(" [*] Listening on 0.0.0.0:8087")

    WeioUserSetup()

    for key in attach.procs :
        print key
        t = threading.Thread(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
        t.daemon = True
        t.start()

    tornado.ioloop.IOLoop.instance().start()
