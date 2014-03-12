import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

import sys
import json
import sockjs.tornado
import multiprocessing

from user import *

from weioUserApi import *

from weioMain import *

userProcess = {}

class PlayHandler(sockjs.tornado.SockJSConnection): 
    i = 0
    def open(self):
        print 'new connection'
        self.write_message("Hello World")
      
    def on_message(self, message):
        print 'message received %s' % message

        if (message == "START"):
            WeioUserSetup()
            for key in attach.procs:
                print key
                userProcess[key] = multiprocessing.Process(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
                userProcess[key].daemon = True
                userProcess[key].start()
        elif (message == "STOP"):
            # Signal the stop to all processes
            for key in attach.procs:
                print key
                userProcess[key].terminate()
            # Detach all processesm events and interrupts
            attach.procs = {}
            attach.events = {}
            attach.interrupts = {}

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
        print "8082: Initialize"

    def get(self):
        self.write("8082: Hello, world")


def main():
    import logging

    global userProcess

    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create weio route
    PlayRouter = sockjs.tornado.SockJSRouter(PlayHandler, '/play')


    app = tornado.web.Application(
            list(PlayRouter.urls) +
            [(r'/', MainHandler)]
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8082)

    logging.info(" [*] Listening on 0.0.0.0:8082")

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
    os.exit(os.EX_OK)
