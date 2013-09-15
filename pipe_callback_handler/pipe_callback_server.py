# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado application. By default will listen on port 8080.
"""
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

import sockjs.tornado

import commands
import os
import subprocess

def WeioGetConfig() :
	command = "/sbin/ifconfig"
	output = "PLACEHOLDER"

	try :
		output = commands.getoutput(command)
	except :
		output = "ERR_CFG"
	
	print output
	return output

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('static/wificon/index.html')

class WeioConnection(sockjs.tornado.SockJSConnection):
    def on_message(self, msg):
        logging.info("Button pressed")
        #msg = WeioGetConfig()
        
        self.pipe = p = subprocess.Popen(['python', '-u', 'first.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        tornado.ioloop.IOLoop.instance().add_callback(self.on_subprocess_result)

    def on_subprocess_result(self):
        if self.pipe.poll() is not None :
            """ Child is terminated """
            print "Child has terminated - removing handler"
            return

        line = self.pipe.stdout.readline()
        if line :
            print line
            self.send(line)
        
        tornado.ioloop.IOLoop.instance().add_callback(self.on_subprocess_result)

    def on_open(self, info):
		 logging.info("Socket OPEN")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    tornado.options.define("port", default=8080, type=int)

    # 1. Create weio router
    WeioRouter = sockjs.tornado.SockJSRouter(WeioConnection, '/weio')

    # 2. Create Tornado application
    app = tornado.web.Application(
            list(WeioRouter.urls) + [(r"/", IndexHandler), (r"/(.*)", tornado.web.StaticFileHandler,
	 				{"path": "./static", "default_filename": "index.html"})])

	 #app = tornado.web.Application(
	 #				list(WeioRouter.urls) + [(r"/(.*)", tornado.web.StaticFileHandler,
	 #				{"path": ".", "default_filename": "index.html"})])

    # 3. Make Tornado app listen on port 8080
    #app.listen(8080)
    logging.info(" [*] Listening on 0.0.0.0:8080")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    #print "http://localhost:%d/static/" % tornado.options.options.port

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
