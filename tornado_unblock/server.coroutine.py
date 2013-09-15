import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options

import sockjs.tornado

import time

import tornado.gen

import subprocess
import functools

# Global variable to store SockJSConnection calss instance
# in order to call it's send() method from MainProgram thread
weioPipe = None

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


def weioMainHandler(callback, fd, events):
    """Stream stdout to browser"""
    global weioPipe

    #print "U HANDLERU!!!"

    line = weioPipe.stdout.readline()

    if line:
        stdout = line
        print(stdout)

    if weioPipe.poll() is not None:
        """ Child is terminated STDOUT"""
        print "Child has terminated - removing handler STDOUT"
        global stdoutHandlerIsLive
        tornado.ioloop.IOLoop.instance().remove_handler(weioPipe.stdout.fileno())

        callback(888)

        print "RETURNING"
        return 777

def test():
    print "TEST!!!"

def my_function(callback):
    print 'do some work'
    # Note: this line will block!
    global weioPipe
    weioPipe = subprocess.Popen(['/bin/bash', 'waitMe.sh'], stdout=subprocess.PIPE)

    global ioloopObj
    ioloopObj = tornado.ioloop.IOLoop.instance()

    #test()

    # Callback for STDOUT
    doWork = functools.partial(weioMainHandler, callback)

    ioloopObj.add_handler(weioPipe.stdout.fileno(), doWork, ioloopObj.READ)

    print "Cao Bao"


def jaBlok():
    output = "PLACEHOLDER"


    command = "/bin/bash waitMe.sh"
    try :
        output = subprocess.check_output(command, shell=True)
    except :
        print("Comand ERROR : " + str(output) + " " + command)
        output = "ERR_CMD"

    print output
    return output

class TestHandler(sockjs.tornado.SockJSConnection):
    def on_open(self, message):
        print 'new connection'

    def on_message(self, message):
        self.handle_request(message)

    @tornado.gen.coroutine
    def handle_request(self, message):
        print 'start'
        # Call my_function and return here as soon as "callback" is called.
        # "result" is whatever argument was passed to "callback" in "my_function".
        result = yield tornado.gen.Task(my_function)
        print 'result is', result
        print 'message received %s' % message

    def on_close(self):
      print 'connection closed'

n = 0
def hello():
    global n
    print "Hello Periodic", n
    n = n + 1

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    tornado.options.define("port", default=8081, type=int)

    # 1. Create weio router
    TestRouter = sockjs.tornado.SockJSRouter(TestHandler, '/test')

    # 2. Create Tornado application
    app = tornado.web.Application(
            list(TestRouter.urls) + 
            [(r"/", IndexHandler), (r"/(.*)", tornado.web.StaticFileHandler,
	 				{"path": ".", "default_filename": "index.html"})],
            debug=True)


    # 3. Make Tornado app listen on port 8080
    logging.info(" [*] Listening on 0.0.0.0:8081")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)

    periodic = tornado.ioloop.PeriodicCallback(hello, 1000)
    periodic.start()

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
